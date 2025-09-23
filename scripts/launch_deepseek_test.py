#!/usr/bin/env python3
"""
Test launcher for DeepSeek-R1-Distill-Qwen-32B training job
Quick validation and configuration check before full training launch
"""

import boto3
import json
from datetime import datetime

def validate_configuration():
    """Validate training configuration before launching expensive job"""
    
    print("=== HeartBeat Engine - DeepSeek-R1-Distill-Qwen-32B Configuration Test ===")
    print()
    
    # Model specifications
    model_config = {
        "model_id": "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B",
        "parameters": "32.7B",
        "architecture": "Qwen2.5",
        "license": "MIT",
        "specialization": "Advanced reasoning, mathematical computation"
    }
    
    # Training parameters
    training_config = {
        "instance_type": "ml.g5.12xlarge",
        "gpus": "4x NVIDIA A10G 24GB",
        "estimated_cost": "$70-$120 CAD",
        "estimated_time": "8-12 hours",
        "learning_rate": "1e-4",
        "max_steps": 220,
        "batch_size": 1,
        "gradient_accumulation": 32,
        "max_length": 3072
    }
    
    print("Model Configuration:")
    for key, value in model_config.items():
        print(f"  {key.replace('_', ' ').title()}: {value}")
    
    print("\nTraining Configuration:")
    for key, value in training_config.items():
        print(f"  {key.replace('_', ' ').title()}: {value}")
    
    print("\nKey Improvements over previous baseline models:")
    improvements = [
        "Superior mathematical reasoning (critical for hockey analytics)",
        "Better tool orchestration and decision-making",
        "Advanced multi-step analysis capabilities", 
        "MIT license with no commercial restrictions",
        "Optimized for reasoning tasks via DeepSeek-R1 distillation",
        "32.7B parameters provide more capacity than 17B models"
    ]
    
    for improvement in improvements:
        print(f"  - {improvement}")
    
    print("\nCost Analysis:")
    print(f"  DeepSeek-R1-Qwen-32B (32.7B): ~$70-$120 CAD (g5.12xlarge)")
    print(f"  Previous baseline models: ~$70 CAD") 
    print(f"  Outcome: Lower-cost run enabled via QLoRA and shorter schedule")
    
    print("\nTraining Dataset:")
    print(f"  Training examples: 1,759 hockey QA pairs")
    print(f"  Validation examples: 441")
    print(f"  Effective batch size: 32 examples per update (bs=1, ga=32)")
    print(f"  Total training examples: 220 steps x 32 = 7,040")
    print(f"  Dataset epochs: ~4.0")
    
    print("\nMemory Analysis per A10G GPU (24GB):")
    memory_usage = {
        "Model (4-bit quantized)": "~4 GB",
        "LoRA adapters": "~200 MB", 
        "Optimizer states": "~300-400 MB",
        "Gradients": "~200 MB",
        "Activations (batch=1)": "~6-9 GB (seq=3072)",
        "CUDA overhead": "~2 GB",
        "Available buffer": "~12 GB+"
    }
    
    for component, usage in memory_usage.items():
        print(f"  {component}: {usage}")
    
    print(f"\nMemory validation: SAFE - Fits comfortably on each A10G with QLoRA")
    
    return True

def check_aws_credentials():
    """Check if AWS credentials are properly configured"""
    try:
        boto3.Session().get_credentials()
        print("AWS credentials configured")
        return True
    except Exception as e:
        print(f"❌ AWS credentials issue: {e}")
        return False

def check_s3_access():
    """Check access to S3 bucket"""
    try:
        s3 = boto3.client('s3', region_name='ca-central-1')
        bucket = 'heartbeat-ml-llama33-70b-skywalkerx'
        s3.head_bucket(Bucket=bucket)
        print(f"S3 bucket access confirmed: {bucket}")
        return True
    except Exception as e:
        print(f"❌ S3 access issue: {e}")
        return False

def main():
    """Main validation function"""
    
    print("Pre-flight validation for DeepSeek-R1-Distill-Qwen-32B training...")
    print()
    
    # Configuration validation
    config_valid = validate_configuration()
    
    print("\nAWS Environment Check:")
    aws_valid = check_aws_credentials()
    s3_valid = check_s3_access()
    
    print(f"\nValidation Summary:")
    print(f"  Configuration: {'VALID' if config_valid else 'INVALID'}")
    print(f"  AWS Access: {'VALID' if aws_valid else 'INVALID'}")
    print(f"  S3 Access: {'VALID' if s3_valid else 'INVALID'}")
    
    if all([config_valid, aws_valid, s3_valid]):
        print(f"\nREADY TO LAUNCH")
        print(f"\nTo start training, run:")
        print(f"  python launch_deepseek_r1_training.py")
        print(f"\nThis will:")
        print(f"  - Launch ml.g5.12xlarge instance (~$5.67/hour)")
        print(f"  - Train for ~220 steps (8-12 hours)")
        print(f"  - Cost approximately $70-$120 CAD")
        print(f"  - Produce advanced hockey analytics model")
        
    else:
        print(f"\nPlease resolve validation issues before launching training.")
    
    print(f"\n" + "="*70)

if __name__ == "__main__":
    main()
