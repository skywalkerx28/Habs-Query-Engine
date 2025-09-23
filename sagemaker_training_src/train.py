#!/usr/bin/env python3
"""
HeartBeat Engine - Llama 4 Scout 17B Instruct QLoRA Fine-Tuning Script
Stanley - Montreal Canadiens Advanced Analytics Assistant Training 

Fine-tunes Llama-4-Scout-17B-16E-Instruct for hockey analytics with tool orchestration,
role-based responses, and evidence-based analysis capabilities.
"""

import json
import os
import logging
import torch
import datasets
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling,
    set_seed,
)
from transformers import BitsAndBytesConfig
from peft import (
    LoraConfig,
    get_peft_model,
    prepare_model_for_kbit_training,
)
from transformers.trainer_utils import IntervalStrategy
import boto3

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_hf_token():
    """Retrieve Hugging Face access token from AWS Secrets Manager"""
    secret_name = "heartbeat-hf-token"
    region_name = "ca-central-1"
    
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
        secret = get_secret_value_response['SecretString']
        return json.loads(secret)['HF_API_TOKEN']
    except Exception as e:
        logger.error(f"Error retrieving HF token: {e}")
        raise e

def setup_model_and_tokenizer(model_id: str):
    """Initialize tokenizer and QLoRA-wrapped model (4-bit quantization + LoRA).

    The model is loaded in 4-bit and sharded across available local GPUs using
    device_map="auto". This avoids DDP and instead relies on Accelerate's model
    dispatch to split layers across devices within a single process.
    """
    logger.info(f"Loading tokenizer and model (QLoRA): {model_id}")

    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(
        model_id,
        use_fast=True,
        padding_side="right",
        trust_remote_code=True,
    )

    # Ensure a valid pad token is present
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
        tokenizer.pad_token_id = tokenizer.eos_token_id

    # BitsAndBytes 4-bit config (QLoRA)
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type=os.environ.get("BNB_QUANT_TYPE", "nf4"),
        bnb_4bit_use_double_quant=os.environ.get("BNB_DOUBLE_QUANT", "true").lower() == "true",
        bnb_4bit_compute_dtype=torch.bfloat16,
    )

    # Load base model quantized in 4-bit and shard across local GPUs
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        quantization_config=bnb_config,
        device_map="auto",
        torch_dtype=torch.bfloat16,
        trust_remote_code=True,
    )

    # Prepare for k-bit training and wrap with LoRA
    model = prepare_model_for_kbit_training(model)

    lora_targets_env = os.environ.get(
        "LORA_TARGETS",
        "q_proj,k_proj,v_proj,o_proj,gate_proj,up_proj,down_proj",
    )
    lora_targets = [t.strip() for t in lora_targets_env.split(",") if t.strip()]

    lora_config = LoraConfig(
        r=int(os.environ.get("LORA_R", "16")),
        lora_alpha=int(os.environ.get("LORA_ALPHA", "32")),
        lora_dropout=float(os.environ.get("LORA_DROPOUT", "0.05")),
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=lora_targets,
    )

    model = get_peft_model(model, lora_config)

    # Enable gradient checkpointing for memory efficiency
    model.gradient_checkpointing_enable()

    try:
        model.print_trainable_parameters()  # Helpful summary in logs
    except Exception:
        pass

    return model, tokenizer

def load_and_process_data(
    train_path: str, val_path: str, tokenizer, max_length: int = 8192
):
    """Load and tokenize the training data"""
    logger.info(f"Loading training data from: {train_path}")
    logger.info(f"Loading validation data from: {val_path}")
    
    # Load datasets
    train_dataset = datasets.load_dataset("json", data_files=train_path, split="train")
    val_dataset = datasets.load_dataset("json", data_files=val_path, split="train")
    
    logger.info(f"Training examples: {len(train_dataset)}")
    logger.info(f"Validation examples: {len(val_dataset)}")
    
    def format_messages(example):
        """Convert messages to chat format"""
        messages = example["messages"]
        text = tokenizer.apply_chat_template(
            messages, 
            tokenize=False, 
            add_generation_prompt=False
        )
        return {"text": text}
    
    def tokenize_function(examples):
        """Tokenize the formatted text"""
        return tokenizer(
            examples["text"],
            truncation=True,
            max_length=max_length,
            padding=False,
            return_tensors=None
        )
    
    # Process datasets
    train_dataset = train_dataset.map(format_messages, remove_columns=["messages"])
    val_dataset = val_dataset.map(format_messages, remove_columns=["messages"])
    
    # Tokenize
    train_dataset = train_dataset.map(
        tokenize_function,
        batched=True,
        remove_columns=["text"],
        desc="Tokenizing training data"
    )
    
    val_dataset = val_dataset.map(
        tokenize_function,
        batched=True,
        remove_columns=["text"],
        desc="Tokenizing validation data"
    )
    
    return train_dataset, val_dataset

def main():
    # Set up Hugging Face authentication
    try:
        hf_token = get_hf_token()
        os.environ['HF_TOKEN'] = hf_token
        logger.info("Successfully retrieved and set HF token")
    except Exception as e:
        logger.error(f"Failed to set up HF authentication: {e}")
        raise e
    
    # Set seed for reproducibility
    set_seed(42)
    
    # Get environment variables
    model_id = os.environ.get("MODEL_ID", "meta-llama/Llama-4-Scout-17B-16E-Instruct")
    
    # SageMaker data paths - check multiple possible locations
    train_base = os.environ.get("SM_CHANNEL_TRAINING", "/opt/ml/input/data/training")
    val_base = os.environ.get("SM_CHANNEL_VALIDATION", "/opt/ml/input/data/validation")
    
    # Find the actual training file
    if os.path.isfile(os.path.join(train_base, "train.jsonl")):
        train_path = os.path.join(train_base, "train.jsonl")
    elif os.path.isfile(train_base) and train_base.endswith('.jsonl'):
        train_path = train_base
    else:
        # Look for any .jsonl file in the training directory
        train_files = [f for f in os.listdir(train_base) if f.endswith('.jsonl')]
        if train_files:
            train_path = os.path.join(train_base, train_files[0])
        else:
            raise FileNotFoundError(f"No training data found in {train_base}")
    
    # Find the actual validation file
    if os.path.isfile(os.path.join(val_base, "val.jsonl")):
        val_path = os.path.join(val_base, "val.jsonl")
    elif os.path.isfile(val_base) and val_base.endswith('.jsonl'):
        val_path = val_base
    else:
        # Look for any .jsonl file in the validation directory
        val_files = [f for f in os.listdir(val_base) if f.endswith('.jsonl')]
        if val_files:
            val_path = os.path.join(val_base, val_files[0])
        else:
            raise FileNotFoundError(f"No validation data found in {val_base}")
    
    output_dir = os.environ.get("SM_MODEL_DIR", "/opt/ml/model")
    
    logger.info(f"Training data path: {train_path}")
    logger.info(f"Validation data path: {val_path}")
    
    # Training hyperparameters optimized for 17B model (QLoRA-friendly defaults)
    learning_rate = float(os.environ.get("LEARNING_RATE", "2e-4"))
    max_steps = int(os.environ.get("MAX_STEPS", "400"))
    per_device_batch_size = int(os.environ.get("PER_DEVICE_BATCH_SIZE", "2"))
    gradient_accumulation_steps = int(os.environ.get("GRADIENT_ACCUMULATION_STEPS", "32"))
    max_length = int(os.environ.get("MAX_LENGTH", "4096"))  # Increased for 17B model
    
    logger.info("=== HeartBeat Engine - Llama 4 Scout 17B Fine-Tuning ===")
    logger.info(f"Model ID: {model_id}")
    logger.info(f"Learning Rate: {learning_rate}")
    logger.info(f"Max Steps: {max_steps}")
    logger.info(f"Batch Size: {per_device_batch_size}")
    logger.info(f"Gradient Accumulation: {gradient_accumulation_steps}")
    logger.info(f"Max Length: {max_length}")
    
    # Setup model and tokenizer (QLoRA)
    model, tokenizer = setup_model_and_tokenizer(model_id)
    
    # Load and process data
    train_dataset, val_dataset = load_and_process_data(
        train_path, val_path, tokenizer, max_length
    )
    
    # Data collator for language modeling
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False,
        pad_to_multiple_of=8
    )
    
    # Training arguments optimized for QLoRA on Llama 4 Scout 17B
    training_args = TrainingArguments(
        output_dir=output_dir,
        
        # Model and precision settings
        bf16=True,
        tf32=True,
        
        # Learning rate and optimization
        learning_rate=learning_rate,
        weight_decay=0.1,
        warmup_ratio=0.1,
        lr_scheduler_type="cosine",
        optim="paged_adamw_8bit",
        
        # Training steps and batching
        num_train_epochs=1,
        max_steps=max_steps,
        per_device_train_batch_size=per_device_batch_size,
        per_device_eval_batch_size=per_device_batch_size,
        gradient_accumulation_steps=gradient_accumulation_steps,
        gradient_checkpointing=True,
        
        # Evaluation and saving
        evaluation_strategy=IntervalStrategy.STEPS,
        eval_steps=50,
        save_strategy=IntervalStrategy.STEPS,
        save_steps=100,
        save_total_limit=3,
        
        # Logging
        logging_steps=10,
        logging_strategy=IntervalStrategy.STEPS,
        
        # Performance optimizations
        dataloader_num_workers=4,
        dataloader_pin_memory=True,
        remove_unused_columns=False,
        
        # Distributed training settings (we run single process; avoid DDP)
        ddp_find_unused_parameters=False,
        
        # Memory and stability
        max_grad_norm=1.0,
        
        # Disable wandb and other integrations
        report_to=[],
        
        # Avoid DP; rely on Accelerate device_map sharding across local GPUs
        warmup_steps=int(max_steps * 0.1),
    )
    
    # Initialize trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        tokenizer=tokenizer,
        data_collator=data_collator,
    )
    
    # Start training
    logger.info("Starting fine-tuning...")
    trainer.train()
    
    # Save LoRA adapters (not full 17B weights)
    logger.info("Saving LoRA adapters and tokenizer...")
    final_dir = os.path.join(output_dir, "final")
    os.makedirs(final_dir, exist_ok=True)
    trainer.model.save_pretrained(final_dir)
    tokenizer.save_pretrained(final_dir)
    
    # Save training metrics
    metrics = trainer.state.log_history
    with open(os.path.join(output_dir, "training_metrics.json"), "w") as f:
        json.dump(metrics, f, indent=2)
    
    logger.info("=== Fine-tuning completed successfully! ===")

if __name__ == "__main__":
    main()
