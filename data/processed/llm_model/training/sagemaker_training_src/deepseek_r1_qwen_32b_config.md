# HeartBeat Engine - DeepSeek-R1-Distill-Qwen-32B Training Configuration

## Model Details
- **Model ID**: `deepseek-ai/DeepSeek-R1-Distill-Qwen-32B`
- **Parameters**: 32.7B 
- **Architecture**: Qwen2.5-32B based, distilled from DeepSeek-R1
- **License**: MIT (more permissive than LLaMA)
- **Specialization**: Advanced reasoning, mathematical computation, code generation

## Why DeepSeek-R1-Distill-Qwen-32B is Perfect for HeartBeat Engine

### 1. **Superior Reasoning Capabilities**
- Distilled from RL-optimized DeepSeek-R1 using ~800K reasoning examples
- Exceptional mathematical computation abilities (essential for hockey analytics)
- Advanced planning and multi-step reasoning
- Better tool orchestration and decision-making

### 2. **Hockey Analytics Advantages**
- **Mathematical Excellence**: Superior at computing complex hockey metrics (xG, Corsi, RAPM)
- **Statistical Analysis**: Better understanding of statistical relationships in data
- **Pattern Recognition**: Enhanced ability to identify hockey trends and correlations
- **Tool Routing**: Intelligent decisions between Pinecone RAG and Parquet queries

### 3. **Technical Benefits**
- **MIT License**: No commercial restrictions
- **Better Architecture**: Qwen2.5 optimized for reasoning tasks
- **Model Size**: 32.7B parameters provide more capacity than 17B models
- **Training Efficiency**: Distillation process creates more efficient reasoning

## Recommended SageMaker Training Configuration

### Instance Types (in order of preference):
1. **ml.p4d.24xlarge** - RECOMMENDED - 8x A100 40GB, 96 vCPUs, 1,152 GB RAM
2. **ml.p4de.24xlarge** - Alternative - 8x A100 80GB, even more VRAM
3. **ml.p5.48xlarge** - Future option - 8x H100 80GB (if available in region)

### Memory Requirements Analysis:
**DeepSeek-R1-Distill-Qwen-32B (32.7B parameters):**
- **FP32**: ~131 GB (4 bytes × 32.7B parameters)
- **FP16**: ~65 GB (2 bytes × 32.7B parameters) 
- **4-bit Quantized**: ~16 GB (0.5 bytes × 32.7B parameters)
- **Training Memory**: ~65 GB (model + optimizer + gradients + activations)

**ml.p4d.24xlarge Capacity:**
- **8x A100 40GB**: Total 320 GB GPU memory
- **Memory per GPU**: 40 GB available
- **Total System**: 1,152 GB RAM

### Optimized Training Parameters:

```python
# SageMaker Training Job Configuration
instance_type = "ml.p4d.24xlarge"
instance_count = 1
max_runtime_in_seconds = 57600  # 16 hours

hyperparameters = {
    "MODEL_ID": "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B",
    "LEARNING_RATE": "1e-4",               # Lower LR for 32B stability
    "MAX_STEPS": "300",                    # Increased for complexity
    "PER_DEVICE_BATCH_SIZE": "1",          # Conservative for 32B
    "GRADIENT_ACCUMULATION_STEPS": "32",   # Effective batch size = 32
    "MAX_LENGTH": "4096",                  # Increased for reasoning
    "LORA_R": "16",                        # Standard LoRA rank
    "LORA_ALPHA": "32",                    # Standard LoRA alpha
    "LORA_DROPOUT": "0.05",                # Lower for large model
    "BNB_QUANT_TYPE": "nf4",              # 4-bit quantization
    "BNB_DOUBLE_QUANT": "true"            # Double quantization
}
```

### Training Analysis for 2,198 Examples:

**Effective Training:**
- **Per-device batch size**: 1
- **Gradient accumulation**: 32 steps
- **Effective batch size**: 32 examples per update
- **Total training steps**: 300
- **Total examples processed**: 300 × 32 = 9,600 examples
- **Dataset epochs**: ~4.4 epochs (optimal range for fine-tuning)

**Memory Distribution per A100 (40GB):**
- **Model (4-bit)**: ~4 GB
- **LoRA adapters**: ~200 MB
- **Optimizer states**: ~400 MB
- **Gradients**: ~200 MB
- **Activations (batch=1, seq=4096)**: ~8-12 GB
- **CUDA kernels & overhead**: ~2 GB
- **Available buffer**: ~23-27 GB (comfortable margin)

## Cost Analysis

### ml.p4d.24xlarge Pricing:
- **US East (N. Virginia)**: $32.77/hour
- **Canada (Central)**: ~$36/hour (approximate)
- **Estimated training time**: 10-14 hours
- **Estimated cost**: 14 hours × $36 = **~$525 CAD**

### Cost Comparison:
- **DeepSeek-R1-Qwen-32B**: ~$525 (superior reasoning)
- **Previous Llama-4-Scout-17B**: ~$70 (basic instruction following)
- **Original Llama3.3-70B plan**: ~$2,000+ (overkill for task)

**Cost-Performance Analysis:**
- **7.5x cost increase** vs 17B model
- **Superior mathematical reasoning** for hockey analytics
- **Better tool orchestration** and decision-making
- **MIT license** with no commercial restrictions
- **Future-proof architecture** with advanced capabilities

## Training Data Compatibility

Perfect compatibility with existing HeartBeat training data:

```json
{
  "messages": [
    {
      "role": "system",
      "content": "You are Stanley, a Montreal Canadiens analytics assistant with access to comprehensive hockey data analysis tools..."
    },
    {
      "role": "user", 
      "content": "Calculate the expected goals differential for Caufield vs league average wingers this season."
    },
    {
      "role": "assistant",
      "content": "I'll analyze Cole Caufield's expected goals performance compared to league-average wingers. Let me query the advanced statistics..."
    }
  ]
}
```

## Expected Performance Improvements vs 17B Model

### 1. **Mathematical Analytics**
- **Complex Calculations**: Better at multi-step statistical computations
- **Correlation Analysis**: Superior pattern recognition in hockey data
- **Predictive Modeling**: Enhanced ability to generate accurate predictions
- **Error Handling**: More robust mathematical reasoning with validation

### 2. **Tool Orchestration**
- **Smart Routing**: Better decisions between RAG chunks vs live Parquet queries
- **Context Management**: Superior memory of previous calculations in conversations
- **Multi-tool Workflows**: Can chain multiple data queries intelligently
- **Error Recovery**: Better handling of invalid queries or missing data

### 3. **Hockey Domain Understanding**
- **Advanced Metrics**: Better comprehension of complex hockey analytics
- **Situational Context**: Superior understanding of game situations
- **Player Comparisons**: More nuanced player performance analysis
- **Team Dynamics**: Better grasp of line combinations and systems impact

## Monitoring and Validation

### Training Metrics to Monitor:
1. **Loss Convergence**: Should decrease steadily over 300 steps
2. **GPU Memory Usage**: Monitor for OOM issues (should stay <35GB per GPU)
3. **Training Speed**: ~2-3 minutes per step expected
4. **Gradient Norms**: Watch for exploding gradients

### Post-Training Validation:
1. **Mathematical Accuracy**: Test complex hockey calculations
2. **Tool Usage**: Verify proper RAG vs Parquet routing decisions
3. **Reasoning Quality**: Evaluate multi-step analysis capabilities
4. **Response Consistency**: Check Montreal Canadiens analyst persona

## Deployment Considerations

### Inference Requirements:
- **Memory**: ~16 GB GPU memory (4-bit quantized)
- **Recommended**: ml.g5.2xlarge or ml.g4dn.2xlarge
- **Latency**: ~2-3 seconds for typical hockey analysis queries
- **Throughput**: Can handle multiple concurrent users

### Cost-Effective Inference:
- **Instance**: ml.g4dn.2xlarge (~$0.75/hour)
- **Daily cost**: 24 × $0.75 = ~$18/day
- **Monthly cost**: ~$540/month for 24/7 availability

## Next Steps

1. **Launch Training**: Use ml.p4d.24xlarge configuration
2. **Monitor Progress**: Track loss and memory usage
3. **Evaluate Results**: Test on hockey analytics benchmarks
4. **Deploy Model**: Set up inference endpoint
5. **A/B Testing**: Compare against previous 17B model performance

This configuration provides the optimal balance of advanced reasoning capabilities, cost-effectiveness, and hockey analytics performance for the HeartBeat Engine.
