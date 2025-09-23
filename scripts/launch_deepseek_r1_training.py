#!/usr/bin/env python3
"""
Launch HeartBeat Engine - DeepSeek-R1-Distill-Qwen-32B Training Job
Optimized for ml.g5.12xlarge cost-effective training
"""

import boto3
from sagemaker import image_uris
import time
import os
import tarfile
import tempfile
from datetime import datetime

def _make_code_tarball(source_dir: str, output_tar_path: str):
    """Create sourcedir.tar.gz for SageMaker script mode."""
    with tarfile.open(output_tar_path, mode="w:gz") as tar:
        tar.add(source_dir, arcname=".")


def launch_training_job():
    """Launch SageMaker training job for DeepSeek-R1-Distill-Qwen-32B"""
    
    # Initialize SageMaker client
    region = 'ca-central-1'
    sagemaker = boto3.client('sagemaker', region_name=region)
    
    # Generate unique job name with timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    job_name = f"heartbeat-deepseek-r1-qwen-32b-{timestamp}"
    
    # Resolve a valid SageMaker DLC for this region/instance automatically
    training_image_uri = image_uris.retrieve(
        framework="pytorch",
        region=region,
        version="2.3.0",          # lets SageMaker map to a valid regional tag (cu121)
        py_version="py311",
        instance_type="ml.g5.12xlarge",
        image_scope="training",
    )

    # Package training code and upload to S3
    s3 = boto3.client('s3', region_name=region)
    code_dir = os.path.join(os.path.dirname(__file__), 'sagemaker_training_src')
    if not os.path.isdir(code_dir):
        raise FileNotFoundError(f"Code directory not found: {code_dir}")

    bucket = 'heartbeat-ml-llama33-70b-skywalkerx'
    code_key_prefix = f"llm/deepseek-r1-qwen-32b/source/{job_name}"
    s3_tar_key = f"{code_key_prefix}/sourcedir.tar.gz"

    with tempfile.TemporaryDirectory() as tmpdir:
        tar_path = os.path.join(tmpdir, 'sourcedir.tar.gz')
        _make_code_tarball(code_dir, tar_path)
        s3.upload_file(tar_path, bucket, s3_tar_key)

    submit_dir_s3_uri = f"s3://{bucket}/{s3_tar_key}"

    # Upload local datasets to S3 for this job
    # Local dataset paths provided by user
    local_train = os.path.join(
        os.path.dirname(__file__),
        'data/processed/llm_model/training/fine_tuning/heartbeat_llama33_70b_training_dataset_session_2.jsonl'
    )
    local_val = os.path.join(
        os.path.dirname(__file__),
        'data/processed/llm_model/training/fine_tuning/heartbeat_llama33_70b_validation_dataset_session_2.jsonl'
    )

    dataset_prefix = f"llm/deepseek-r1-qwen-32b/datasets/session2"
    train_prefix = f"{dataset_prefix}/train"
    val_prefix = f"{dataset_prefix}/val"
    train_key = f"{train_prefix}/train.jsonl"
    val_key = f"{val_prefix}/val.jsonl"

    try:
        if os.path.isfile(local_train):
            s3.upload_file(local_train, bucket, train_key)
        else:
            print(f"Warning: training file not found at {local_train}")
        if os.path.isfile(local_val):
            s3.upload_file(local_val, bucket, val_key)
        else:
            print(f"Warning: validation file not found at {local_val}")
    except Exception as e:
        print(f"Error uploading datasets to S3: {e}")

    # Training job configuration
    training_job_config = {
        'TrainingJobName': job_name,
        'RoleArn': 'arn:aws:iam::803243354066:role/HeartBeatSageMakerExecutionRole',
        
        # Algorithm specification
        'AlgorithmSpecification': {
            'TrainingImage': training_image_uri,
            'TrainingInputMode': 'File'
        },
        
        # Input data configuration
        'InputDataConfig': [
            {
                'ChannelName': 'training',
                'DataSource': {
                    'S3DataSource': {
                        'S3DataType': 'S3Prefix',
                        'S3Uri': f's3://{bucket}/{train_prefix}/',
                        'S3DataDistributionType': 'FullyReplicated'
                    }
                },
                'ContentType': 'application/jsonlines',
                'CompressionType': 'None'
            },
            {
                'ChannelName': 'validation', 
                'DataSource': {
                    'S3DataSource': {
                        'S3DataType': 'S3Prefix',
                        'S3Uri': f's3://{bucket}/{val_prefix}/',
                        'S3DataDistributionType': 'FullyReplicated'
                    }
                },
                'ContentType': 'application/jsonlines',
                'CompressionType': 'None'
            }
        ],
        
        # Output configuration
        'OutputDataConfig': {
            'S3OutputPath': f's3://{bucket}/llm/deepseek-r1-qwen-32b/models/{job_name}/'
        },
        
        # Resource configuration - ml.g5.12xlarge for cost-effective QLoRA training
        'ResourceConfig': {
            'InstanceType': 'ml.g5.12xlarge',  # 4x A10G 24GB GPUs
            'InstanceCount': 1,
            'VolumeSizeInGB': 100
        },
        
        # Stopping condition - 12 hours max runtime for cost control
        'StoppingCondition': {
            'MaxRuntimeInSeconds': 43200  # 12 hours
        },
        
        # Hyperparameters optimized for DeepSeek-R1-Distill-Qwen-32B
        'HyperParameters': {
            'MODEL_ID': 'deepseek-ai/DeepSeek-R1-Distill-Qwen-32B',
            'LEARNING_RATE': '1e-4',
            'MAX_STEPS': '220',                    # ~4 epochs at eff. batch size 32
            'PER_DEVICE_BATCH_SIZE': '1',
            'GRADIENT_ACCUMULATION_STEPS': '32',   # Effective batch size 32
            'MAX_LENGTH': '3072',                  # Memory-optimized for A10G
            'LORA_R': '16',                        # Standard LoRA rank
            'LORA_ALPHA': '32',                    # Standard LoRA alpha
            'LORA_DROPOUT': '0.05',                # Lower dropout for large model
            'BNB_QUANT_TYPE': 'nf4',
            'BNB_DOUBLE_QUANT': 'true',

            # Script Mode parameters must be passed as hyperparameters (not env)
            'sagemaker_program': 'train.py',
            'sagemaker_submit_directory': submit_dir_s3_uri,
            'sagemaker_requirements': 'requirements.txt',
            'sagemaker_container_log_level': '20',
            'sagemaker_job_name': job_name,
            'sagemaker_region': region
        },
        
        # Environment configuration (empty; script-mode config provided via HyperParameters)
        'Environment': {},
        
        # Checkpointing for safety
        'CheckpointConfig': {
            'S3Uri': f's3://heartbeat-ml-llama33-70b-skywalkerx/llm/deepseek-r1-qwen-32b/checkpoints/{job_name}/',
            'LocalPath': '/opt/ml/checkpoints'
        },
        
        # Profiler configuration
        'ProfilerConfig': {
            'S3OutputPath': f's3://heartbeat-ml-llama33-70b-skywalkerx/llm/deepseek-r1-qwen-32b/profiler/{job_name}/',
            'ProfilingIntervalInMilliseconds': 500
        },
        
        # Tags for organization
        'Tags': [
            {'Key': 'Project', 'Value': 'HeartBeat-Engine'},
            {'Key': 'Model', 'Value': 'DeepSeek-R1-Distill-Qwen-32B'},
            {'Key': 'Purpose', 'Value': 'Advanced-Hockey-Analytics'},
            {'Key': 'CostCenter', 'Value': 'ML-Research'},
            {'Key': 'Owner', 'Value': 'Skywalkerx'}
        ]
    }
    
    try:
        print("Launching HeartBeat Engine Training Job...")
        print(f"Job Name: {job_name}")
        print(f"Instance: ml.g5.12xlarge (4x NVIDIA A10G 24GB)")
        print(f"Max Runtime: 12 hours")
        print(f"Estimated Cost: ~$70-$120")
        print(f"Model: DeepSeek-R1-Distill-Qwen-32B")
        print(f"Training Steps: 220 (~4 epochs with effective batch size 32)")
        print(f"Using Training Image: {training_image_uri}")
        print(f"Training data S3: s3://{bucket}/{train_prefix}/train.jsonl")
        print(f"Validation data S3: s3://{bucket}/{val_prefix}/val.jsonl")
        print()
        
        # Launch the training job
        response = sagemaker.create_training_job(**training_job_config)
        
        print("Training job launched successfully!")
        print(f"Training Job ARN: {response['TrainingJobArn']}")
        print()
        print("Monitoring Commands:")
        print(f"aws sagemaker describe-training-job --training-job-name {job_name}")
        print(f"aws logs tail /aws/sagemaker/TrainingJobs --follow")
        print()
        print("Cost-optimized training - check back in 8-12 hours")
        print("Expected completion: Next morning")
        
        return response
        
    except Exception as e:
        print(f"Error launching training job: {str(e)}")
        return None

def check_training_status(job_name):
    """Check the status of a training job"""
    sagemaker = boto3.client('sagemaker', region_name='ca-central-1')
    
    try:
        response = sagemaker.describe_training_job(TrainingJobName=job_name)
        status = response['TrainingJobStatus']
        
        print(f"Training Job Status: {status}")
        
        if status == 'InProgress':
            print(f"Training started: {response['TrainingStartTime']}")
            if 'BillableTimeInSeconds' in response:
                print(f"Billable time so far: {response['BillableTimeInSeconds']} seconds")
        elif status == 'Completed':
            print(f"Training completed: {response['TrainingEndTime']}")
            print(f"Total billable time: {response['BillableTimeInSeconds']} seconds")
            print(f"Model artifacts: {response['ModelArtifacts']['S3ModelArtifacts']}")
        elif status == 'Failed':
            print(f"Training failed: {response['FailureReason']}")
        
        return response
        
    except Exception as e:
        print(f"Error checking training status: {str(e)}")
        return None

if __name__ == "__main__":
    print("HeartBeat Engine - DeepSeek-R1-Distill-Qwen-32B Training Launcher")
    print("=" * 70)
    
    # Launch training job
    result = launch_training_job()
    
    if result:
        print("\nTraining job launched successfully!")
        print("Check AWS Console or use the monitoring commands above to track progress.")
    else:
        print("\nFailed to launch training job. Check your AWS credentials and permissions.")
