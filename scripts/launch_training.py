#!/usr/bin/env python3
"""
HeartBeat Engine - SageMaker Training Job Launcher
Launches Llama 3.3 70B QLoRA fine-tuning job on AWS SageMaker (single node)
"""

import boto3
import sagemaker
from sagemaker.huggingface import HuggingFace
from datetime import datetime
import os

def main():
    # Configuration
    BUCKET_NAME = "heartbeat-ml-llama33-70b-skywalkerx"
    ROLE_ARN = "arn:aws:iam::803243354066:role/HeartBeatSageMakerExecutionRole"
    REGION = "ca-central-1"
    
    # Training data paths
    TRAIN_DATA = f"s3://{BUCKET_NAME}/llm/llama33-70b/session2/train.jsonl"
    VAL_DATA = f"s3://{BUCKET_NAME}/llm/llama33-70b/session2/val.jsonl"
    
    # Output path
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    OUTPUT_PATH = f"s3://{BUCKET_NAME}/llm/llama33-70b/session2/models/heartbeat-llama33-70b-{timestamp}"
    
    print("=== HeartBeat Engine - Llama 3.3 70B Training Job ===")
    print(f"Training Data: {TRAIN_DATA}")
    print(f"Validation Data: {VAL_DATA}")
    print(f"Output Path: {OUTPUT_PATH}")
    print(f"Role ARN: {ROLE_ARN}")
    
    # Initialize SageMaker session
    session = sagemaker.Session(boto3.Session(region_name=REGION))
    
    # Hyperparameters for QLoRA fine-tuning
    hyperparameters = {
        "MODEL_ID": "meta-llama/Llama-3.3-70B-Instruct",
        "LEARNING_RATE": "1e-4",
        "MAX_STEPS": "150",
        "PER_DEVICE_BATCH_SIZE": "1",
        "GRADIENT_ACCUMULATION_STEPS": "128",
        "MAX_LENGTH": "2048",  # Reduced for memory optimization
        # QLoRA specific
        "LORA_R": "16",
        "LORA_ALPHA": "32",
        "LORA_DROPOUT": "0.05",
        "LORA_TARGETS": "q_proj,k_proj,v_proj,o_proj,gate_proj,up_proj,down_proj",
        "BNB_QUANT_TYPE": "nf4",
        "BNB_DOUBLE_QUANT": "true",
    }
    
    # Create HuggingFace estimator
    estimator = HuggingFace(
        entry_point="train.py",
        source_dir="./sagemaker_training_src",
        role=ROLE_ARN,
        
        # Container configuration
        transformers_version="4.49.0",
        pytorch_version="2.5.1",
        py_version="py311",
        
        # Single-node instance (device_map sharding across local GPUs)
        instance_type="ml.g5.12xlarge",  # 4x A10G 24GB GPUs per instance
        instance_count=1,
        
        # Training configuration
        hyperparameters=hyperparameters,
        
        # Resource limits
        max_run=4 * 60 * 60,  # 4 hours max
        volume_size=1000,     # 1TB EBS volume
        
        # Output configuration
        output_path=OUTPUT_PATH,
        
        # Environment variables
        environment={
            "NCCL_DEBUG": "INFO",
            "TRANSFORMERS_CACHE": "/tmp/transformers_cache",
            "HF_HOME": "/tmp/hf_cache",
            # Prevent multi-process DDP so device_map can shard within one process
            "SM_NUM_GPUS": "4",
            # bitsandbytes / CUDA allocator stability
            "PYTORCH_CUDA_ALLOC_CONF": "expandable_segments:True",
        },
        
        # Checkpointing
        checkpoint_s3_uri=f"s3://{BUCKET_NAME}/llm/llama33-70b/session2/checkpoints/",
        
        # Session
        sagemaker_session=session,
        
        # Job name
        base_job_name="heartbeat-llama33-70b-qlora",

        # Disable Torch Distributed so we run a single process that uses device_map
        distribution={
            "torch_distributed": {"enabled": False}
        }
    )
    
    # Data channels
    data_channels = {
        "training": TRAIN_DATA,
        "validation": VAL_DATA
    }
    
    print("\n=== Starting Training Job ===")
    print("This will take approximately 2-4 hours...")
    print("Monitor progress in SageMaker Console or check CloudWatch logs")
    
    # Launch training job
    estimator.fit(data_channels, wait=False)
    
    print(f"\n=== Training Job Submitted ===")
    print(f"Job Name: {estimator.latest_training_job.name}")
    print(f"Status: {estimator.latest_training_job.describe()['TrainingJobStatus']}")
    print(f"Console: https://console.aws.amazon.com/sagemaker/home?region={REGION}#/jobs/{estimator.latest_training_job.name}")
    
    # Save job details
    job_details = {
        "job_name": estimator.latest_training_job.name,
        "model_id": "meta-llama/Llama-3.3-70B-Instruct",
        "training_data": TRAIN_DATA,
        "validation_data": VAL_DATA,
        "output_path": OUTPUT_PATH,
        "instance_type": "ml.g5.12xlarge",
        "hyperparameters": hyperparameters,
        "timestamp": timestamp
    }
    
    with open(f"training_job_{timestamp}.json", "w") as f:
        import json
        json.dump(job_details, f, indent=2)
    
    print(f"Job details saved to: training_job_{timestamp}.json")
    
    return estimator

if __name__ == "__main__":
    estimator = main()
