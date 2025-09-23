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
    "MAX_STEPS": "400",             # Reduced steps
    "PER_DEVICE_BATCH_SIZE": "2",   # Larger batch size
    "GRADIENT_ACCUMULATION_STEPS": "32",  # Reduced accumulation
    "MAX_LENGTH": "4096",           # Longer sequences for better context
    "LORA_R": "16",                 # Standard LoRA rank
    "LORA_ALPHA": "32",             # Standard LoRA alpha
    "LORA_DROPOUT": "0.05",         # Low dropout
}
```

### Training Time & Cost Estimates:
- **Training Time**: 4-8 hours (vs 24-72 for 70B)
- **Cost**: ~$200-400 (vs $1000-3000 for 70B)
- **Max Runtime**: 28,800 seconds (8 hours) - much safer margin

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
