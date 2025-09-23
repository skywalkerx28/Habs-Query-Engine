# Launch HeartBeat Training on ml.g5.12xlarge

## Quick Launch Guide for $70 Overnight Training

### 1. **Pre-Launch Checklist**
- ✅ Training data uploaded to S3
- ✅ Validation data uploaded to S3  
- ✅ HuggingFace token stored in AWS Secrets Manager (`heartbeat-hf-token`)
- ✅ SageMaker execution role configured
- ✅ Training script (`train.py`) uploaded to S3 or ECR

### 2. **SageMaker Training Job Configuration**

```python
import boto3
from sagemaker.pytorch import PyTorch
from sagemaker import get_execution_role

# Initialize SageMaker session
sagemaker_session = boto3.Session().region_name
role = get_execution_role()  # Or specify your SageMaker execution role ARN

# Training job configuration
estimator = PyTorch(
    entry_point='train.py',
    source_dir='sagemaker_training_src/',
    role=role,
    instance_type='ml.g5.12xlarge',
    instance_count=1,
    framework_version='2.1.0',
    py_version='py310',
    max_runtime_in_seconds=43200,  # 12 hours
    
    # Optimized hyperparameters for A10G GPUs
    hyperparameters={
        'MODEL_ID': 'meta-llama/Llama-4-Scout-17B-16E-Instruct',
        'LEARNING_RATE': '2e-4',
        'MAX_STEPS': '200',
        'PER_DEVICE_BATCH_SIZE': '1',
        'GRADIENT_ACCUMULATION_STEPS': '64',
        'MAX_LENGTH': '3072',
        'LORA_R': '16',
        'LORA_ALPHA': '32',
        'LORA_DROPOUT': '0.1',
        'BNB_QUANT_TYPE': 'nf4',
        'BNB_DOUBLE_QUANT': 'true'
    },
    
    # Enable checkpointing for safety
    checkpoint_s3_uri='s3://your-bucket/heartbeat-checkpoints/',
    use_spot_instances=False,  # Use On-Demand for reliability
    
    # Resource configuration
    volume_size=100,  # GB - enough for model and data
)

# Launch training
estimator.fit({
    'training': 's3://your-bucket/training-data/',
    'validation': 's3://your-bucket/validation-data/'
})
```

### 3. **Expected Timeline**

**🌙 Perfect for Overnight Training:**
- **Start**: 10:00 PM
- **Expected Completion**: 6:00-10:00 AM  
- **Total Cost**: ~$68-70
- **You wake up**: Fine-tuned model ready! ☕

### 4. **Monitoring Your Training**

```bash
# Check training job status
aws sagemaker describe-training-job --training-job-name your-job-name

# View CloudWatch logs
aws logs tail /aws/sagemaker/TrainingJobs --follow
```

### 5. **What Happens During Training**

**Hours 1-2**: Model loading and setup
- Downloads Llama-4-Scout-17B-16E-Instruct
- Applies 4-bit quantization  
- Sets up LoRA adapters

**Hours 3-10**: Training loop (200 steps)
- Processes your 2,198 hockey analytics examples
- Saves checkpoints every 100 steps
- Evaluates on validation set every 50 steps

**Hours 10-12**: Final model saving
- Saves LoRA adapters
- Uploads to S3
- Training metrics export

### 6. **Cost Breakdown**
- **Compute**: 12 hours × $5.67/hour = $68.04
- **Storage**: <$1 (small dataset)
- **Total**: **~$70** 🎯

### 7. **After Training Completes**

Your fine-tuned model will be saved to:
```
s3://your-bucket/model-artifacts/
├── final/
│   ├── adapter_config.json
│   ├── adapter_model.safetensors  # LoRA weights (~32MB)
│   └── tokenizer files
└── training_metrics.json
```

### 8. **Next Steps**
1. **Test the model** with sample hockey queries
2. **Deploy to SageMaker Endpoint** for production use
3. **Integrate with your HeartBeat web app**

## 🚀 Ready to Launch?

This configuration is optimized for your dataset size and budget. The ml.g5.12xlarge will efficiently train your hockey analytics assistant overnight for just $70!

**Launch Command:**
```bash
python launch_training.py --instance-type ml.g5.12xlarge --max-runtime 43200
```
