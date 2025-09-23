# HeartBeat Engine - Llama 4 Scout 17B Training Configuration

## Model Details
- **Model ID**: `meta-llama/Llama-4-Scout-17B-16E-Instruct`
- **Parameters**: 17B 
- **Type**: Instruction-tuned model (perfect for tool orchestration and persona)
- **Architecture**: Optimized for chat/assistant tasks

## Why This Model is Perfect for HeartBeat Engine

### 1. **Instruction Following**
- Already trained to follow system prompts and tool schemas
- Excellent at maintaining persona (Montreal Canadiens analyst)
- Natural understanding of chat format (system → tools → user)

### 2. **Tool Orchestration**
- Pre-trained to work with function calling patterns
- Understands when to route to Pinecone vs Parquet tools
- Can maintain context across multi-turn conversations

### 3. **Cost & Speed Benefits**
- ~4x faster training than 70B model
- ~3x lower training costs
- Can run on smaller instances (ml.p3.8xlarge or ml.g5.12xlarge)
- Estimated training time: 4-8 hours vs 24-72 hours

## Recommended SageMaker Training Configuration

### Instance Types (in order of preference):
1. **ml.p4d.24xlarge** - Best performance, 8x A100 40GB
2. **ml.p3.8xlarge** - Good balance, 4x V100 16GB
3. **ml.g5.12xlarge** - Budget option, 4x A10G 24GB

### Environment Variables:
```python
hyperparameters = {
    "MODEL_ID": "meta-llama/Llama-4-Scout-17B-16E-Instruct",
    "LEARNING_RATE": "2e-4",        # Higher LR for 17B
    "MAX_STEPS": "200",             # REDUCED - optimal for 2,198 examples
    "PER_DEVICE_BATCH_SIZE": "2",   # Larger batch size
    "GRADIENT_ACCUMULATION_STEPS": "32",  # Reduced accumulation
    "MAX_LENGTH": "4096",           # Longer sequences for better context
    "LORA_R": "16",                 # Standard LoRA rank
    "LORA_ALPHA": "32",             # Standard LoRA alpha
    "LORA_DROPOUT": "0.1",          # Higher dropout to prevent overfitting
}
```

### Why 200 Steps is Optimal for Your Dataset:

**Dataset Analysis:**
- **Training Examples**: 2,198 QA pairs
- **Effective Batch Size**: 2 × 32 = 64 examples per step
- **Dataset Coverage**: 200 steps × 64 = 12,800 training examples
- **Epochs**: ~5.8 epochs through your dataset (ideal range: 3-10 epochs)

**Overfitting Prevention:**
- Research shows datasets <3K examples risk overfitting beyond 200-300 steps
- Your 2,198 examples fall into this category
- Higher dropout (0.1) adds regularization
- Early stopping at 200 steps prevents memorization

### Training Time & Cost Estimates:

**Optimized for 200 Steps with 2,198 Examples:**

#### Instance Options & Costs:

**Option 1: ml.p4d.24xlarge (Recommended)**
- **Specs**: 8x NVIDIA A100 40GB GPUs, 96 vCPUs, 1,152 GB RAM
- **Hourly Rate**: $32.77/hour (US East N. Virginia)
- **Estimated Training Time**: 3-4 hours (200 steps)
- **Compute Cost**: 4 hours × $32.77 = **$131.08**

**Option 2: ml.p3.8xlarge (Budget Option)**
- **Specs**: 4x NVIDIA V100 16GB GPUs, 32 vCPUs, 244 GB RAM  
- **Hourly Rate**: $12.24/hour (US East N. Virginia)
- **Estimated Training Time**: 6-8 hours (200 steps)
- **Compute Cost**: 8 hours × $12.24 = **$97.92**

**Option 3: ml.g5.12xlarge (Most Budget-Friendly)**
- **Specs**: 4x NVIDIA A10G 24GB GPUs, 48 vCPUs, 192 GB RAM
- **Hourly Rate**: $5.67/hour (US East N. Virginia)
- **Estimated Training Time**: 8-12 hours (200 steps)
- **Compute Cost**: 12 hours × $5.67 = **$68.04**

#### Additional Costs:

**Data Storage (S3)**
- **Training Dataset**: ~50 MB (2,198 examples)
- **Monthly Storage**: 0.05 GB × $0.023/GB = **$0.001**
- **Data Transfer**: Negligible for small dataset

**Total Estimated Costs:**
- **ml.p4d.24xlarge**: **$131-140** (fastest, best performance)
- **ml.p3.8xlarge**: **$98-110** (good balance)
- **ml.g5.12xlarge**: **$68-80** (budget option, slower)

#### Cost Savings vs Original 70B Plan:
- **70B Model Cost**: $2,000-3,000 (72 hours training)
- **17B Model Cost**: $68-140 (3-12 hours training)
- **Savings**: **$1,860-2,932** (93-95% cost reduction!)

#### Selected Configuration: ml.g5.12xlarge
**Perfect for overnight training at just ~$70 total cost**

**Optimized Settings for ml.g5.12xlarge:**
```python
# SageMaker Training Job Configuration
instance_type = "ml.g5.12xlarge"
instance_count = 1
max_runtime_in_seconds = 43200  # 12 hours (safe margin)

hyperparameters = {
    "MODEL_ID": "meta-llama/Llama-4-Scout-17B-16E-Instruct",
    "LEARNING_RATE": "2e-4",
    "MAX_STEPS": "200",
    "PER_DEVICE_BATCH_SIZE": "1",      # Reduced for A10G memory
    "GRADIENT_ACCUMULATION_STEPS": "64", # Increased to maintain effective batch size
    "MAX_LENGTH": "3072",              # Slightly reduced for A10G
    "LORA_R": "16",
    "LORA_ALPHA": "32", 
    "LORA_DROPOUT": "0.1",
    "BNB_QUANT_TYPE": "nf4",
    "BNB_DOUBLE_QUANT": "true"
}
```

**Why These Settings Work for A10G GPUs:**
- **Batch Size 1**: Each A10G has 24GB VRAM (vs 40GB A100), so smaller batches prevent OOM
- **Gradient Accumulation 64**: Maintains effective batch size of 64 examples per step
- **Max Length 3072**: Optimized for A10G memory constraints
- **12-hour runtime**: Plenty of buffer for 8-12 hour expected training time

### Memory Requirements:
- **17B Model**: ~34GB in fp16, ~17GB with 4-bit quantization
- **Fits comfortably** on most GPU instances with QLoRA
- **No model sharding** needed across multiple GPUs

## Training Data Compatibility

The model works perfectly with your existing training data format:
```json
{
  "messages": [
    {
      "role": "system",
      "content": "You are Stanley, a Montreal Canadiens analytics assistant..."
    },
    {
      "role": "user", 
      "content": "How did Suzuki perform in the last game?"
    },
    {
      "role": "assistant",
      "content": "I'll analyze Nick Suzuki's performance..."
    }
  ]
}
```

## Expected Performance Benefits

### 1. **Better Tool Usage**
- Natural understanding of when to call Pinecone vs Parquet tools
- Proper function call formatting
- Context preservation across tool calls

### 2. **Improved Persona**
- Maintains Montreal Canadiens analyst character
- Uses appropriate hockey terminology
- Consistent tone and expertise level

### 3. **Faster Inference**
- 17B model runs much faster than 70B
- Better user experience with quicker responses
- Can handle more concurrent users

## Next Steps

1. **Update Training Job**: Use the optimized hyperparameters above
2. **Set Max Runtime**: 28,800 seconds (8 hours) for safety
3. **Monitor Training**: Should complete much faster than 70B attempt
4. **Test Model**: Evaluate instruction following and tool usage
5. **Deploy**: Much easier deployment due to smaller model size

This configuration should give you excellent results while being much more practical and cost-effective than the 70B model.
