"""
HeartBeat Engine - SageMaker Endpoint Management
Stanley Assistant

SageMaker inference endpoint configuration and management.
"""

import boto3
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional
import asyncio
import aiohttp

logger = logging.getLogger(__name__)

class SageMakerEndpointManager:
    """
    Manages SageMaker inference endpoints for the fine-tuned DeepSeek-R1-Distill-Qwen-32B model.
    
    Features:
    - Endpoint deployment and configuration
    - Real-time inference calls
    - Auto-scaling and performance monitoring
    - Fallback and error handling
    """
    
    def __init__(self, region: str = "ca-central-1"):
        self.region = region
        self.sagemaker_client = boto3.client('sagemaker', region_name=region)
        self.runtime_client = boto3.client('sagemaker-runtime', region_name=region)
        
        # Endpoint configuration
        self.endpoint_config = {
            "model_name": "heartbeat-deepseek-r1-qwen-32b",
            "endpoint_name": "heartbeat-deepseek-r1-qwen-32b-endpoint",
            "endpoint_config_name": "heartbeat-deepseek-r1-qwen-32b-config",
            "instance_type": "ml.g5.2xlarge",  # Start with smaller instance for inference
            "initial_instance_count": 1,
            "max_instance_count": 3,
            "target_model_name": "model.tar.gz"
        }
    
    async def deploy_model_endpoint(self, model_s3_path: str) -> Dict[str, Any]:
        """
        Deploy the fine-tuned model to a SageMaker endpoint.
        
        Args:
            model_s3_path: S3 path to the trained model artifacts
            
        Returns:
            Deployment status and endpoint information
        """
        
        try:
            logger.info(f"Deploying model from {model_s3_path}")
            
            # Step 1: Create model
            model_response = await self._create_model(model_s3_path)
            
            # Step 2: Create endpoint configuration
            config_response = await self._create_endpoint_config()
            
            # Step 3: Create endpoint
            endpoint_response = await self._create_endpoint()
            
            # Step 4: Wait for endpoint to be in service
            endpoint_status = await self._wait_for_endpoint()
            
            return {
                "success": True,
                "endpoint_name": self.endpoint_config["endpoint_name"],
                "endpoint_status": endpoint_status,
                "model_created": model_response["success"],
                "config_created": config_response["success"],
                "endpoint_created": endpoint_response["success"],
                "deployment_time": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Model deployment failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "deployment_time": datetime.now().isoformat()
            }
    
    async def _create_model(self, model_s3_path: str) -> Dict[str, Any]:
        """Create SageMaker model"""
        
        try:
            # Prepare model creation request
            model_name = f"{self.endpoint_config['model_name']}-{int(datetime.now().timestamp())}"
            
            # Get execution role ARN
            execution_role = "arn:aws:iam::803243354066:role/HeartBeatSageMakerExecutionRole"
            
            # Create model
            response = self.sagemaker_client.create_model(
                ModelName=model_name,
                PrimaryContainer={
                    'Image': '763104351884.dkr.ecr.ca-central-1.amazonaws.com/huggingface-pytorch-inference:2.5.1-transformers4.49.0-gpu-py311-cu124-ubuntu22.04',
                    'ModelDataUrl': model_s3_path,
                    'Environment': {
                        'HF_MODEL_ID': 'deepseek-ai/DeepSeek-R1-Distill-Qwen-32B',
                        'HF_TASK': 'text-generation',
                        'SAGEMAKER_CONTAINER_LOG_LEVEL': '20',
                        'SAGEMAKER_REGION': self.region
                    }
                },
                ExecutionRoleArn=execution_role
            )
            
            # Update endpoint config with actual model name
            self.endpoint_config["actual_model_name"] = model_name
            
            logger.info(f"Model created: {model_name}")
            
            return {
                "success": True,
                "model_name": model_name,
                "model_arn": response["ModelArn"]
            }
            
        except Exception as e:
            logger.error(f"Model creation failed: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _create_endpoint_config(self) -> Dict[str, Any]:
        """Create endpoint configuration"""
        
        try:
            config_name = f"{self.endpoint_config['endpoint_config_name']}-{int(datetime.now().timestamp())}"
            model_name = self.endpoint_config["actual_model_name"]
            
            response = self.sagemaker_client.create_endpoint_config(
                EndpointConfigName=config_name,
                ProductionVariants=[
                    {
                        'VariantName': 'primary',
                        'ModelName': model_name,
                        'InitialInstanceCount': self.endpoint_config["initial_instance_count"],
                        'InstanceType': self.endpoint_config["instance_type"],
                        'InitialVariantWeight': 1
                    }
                ]
            )
            
            # Update endpoint config with actual config name
            self.endpoint_config["actual_config_name"] = config_name
            
            logger.info(f"Endpoint config created: {config_name}")
            
            return {
                "success": True,
                "config_name": config_name,
                "config_arn": response["EndpointConfigArn"]
            }
            
        except Exception as e:
            logger.error(f"Endpoint config creation failed: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _create_endpoint(self) -> Dict[str, Any]:
        """Create inference endpoint"""
        
        try:
            endpoint_name = f"{self.endpoint_config['endpoint_name']}-{int(datetime.now().timestamp())}"
            config_name = self.endpoint_config["actual_config_name"]
            
            response = self.sagemaker_client.create_endpoint(
                EndpointName=endpoint_name,
                EndpointConfigName=config_name
            )
            
            # Update endpoint config with actual endpoint name
            self.endpoint_config["actual_endpoint_name"] = endpoint_name
            
            logger.info(f"Endpoint creation started: {endpoint_name}")
            
            return {
                "success": True,
                "endpoint_name": endpoint_name,
                "endpoint_arn": response["EndpointArn"]
            }
            
        except Exception as e:
            logger.error(f"Endpoint creation failed: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _wait_for_endpoint(self, timeout_minutes: int = 15) -> str:
        """Wait for endpoint to be in service"""
        
        endpoint_name = self.endpoint_config["actual_endpoint_name"]
        timeout_time = datetime.now() + timedelta(minutes=timeout_minutes)
        
        while datetime.now() < timeout_time:
            try:
                response = self.sagemaker_client.describe_endpoint(
                    EndpointName=endpoint_name
                )
                
                status = response['EndpointStatus']
                
                if status == 'InService':
                    logger.info(f"Endpoint {endpoint_name} is now in service")
                    return status
                elif status == 'Failed':
                    logger.error(f"Endpoint {endpoint_name} failed to deploy")
                    return status
                
                # Wait before checking again
                await asyncio.sleep(30)
                
            except Exception as e:
                logger.error(f"Error checking endpoint status: {str(e)}")
                await asyncio.sleep(30)
        
        logger.warning(f"Endpoint {endpoint_name} deployment timed out")
        return "Timeout"
    
    async def invoke_endpoint(
        self, 
        prompt: str, 
        max_tokens: int = 2048,
        temperature: float = 0.1
    ) -> Dict[str, Any]:
        """
        Invoke the SageMaker endpoint for inference.
        
        Args:
            prompt: Input prompt for the model
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            
        Returns:
            Model response and metadata
        """
        
        endpoint_name = self.endpoint_config.get("actual_endpoint_name")
        
        if not endpoint_name:
            return {
                "success": False,
                "error": "No endpoint deployed"
            }
        
        try:
            # Prepare inference request
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": max_tokens,
                    "temperature": temperature,
                    "top_p": 0.95,
                    "do_sample": True,
                    "return_full_text": False
                }
            }
            
            # Invoke endpoint
            start_time = datetime.now()
            
            response = self.runtime_client.invoke_endpoint(
                EndpointName=endpoint_name,
                ContentType='application/json',
                Body=json.dumps(payload)
            )
            
            # Parse response
            result = json.loads(response['Body'].read().decode())
            
            inference_time = int((datetime.now() - start_time).total_seconds() * 1000)
            
            return {
                "success": True,
                "response": result,
                "inference_time_ms": inference_time,
                "endpoint_name": endpoint_name
            }
            
        except Exception as e:
            logger.error(f"Endpoint invocation failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "endpoint_name": endpoint_name
            }
    
    def get_endpoint_status(self) -> Dict[str, Any]:
        """Get current endpoint status"""
        
        endpoint_name = self.endpoint_config.get("actual_endpoint_name")
        
        if not endpoint_name:
            return {
                "status": "NotDeployed",
                "message": "No endpoint deployed"
            }
        
        try:
            response = self.sagemaker_client.describe_endpoint(
                EndpointName=endpoint_name
            )
            
            return {
                "status": response['EndpointStatus'],
                "endpoint_name": endpoint_name,
                "creation_time": response.get('CreationTime'),
                "last_modified_time": response.get('LastModifiedTime'),
                "instance_type": self.endpoint_config["instance_type"]
            }
            
        except Exception as e:
            logger.error(f"Error getting endpoint status: {str(e)}")
            return {
                "status": "Error",
                "error": str(e)
            }
    
    def delete_endpoint(self) -> Dict[str, Any]:
        """Delete the inference endpoint"""
        
        endpoint_name = self.endpoint_config.get("actual_endpoint_name")
        
        if not endpoint_name:
            return {
                "success": False,
                "error": "No endpoint to delete"
            }
        
        try:
            # Delete endpoint
            self.sagemaker_client.delete_endpoint(
                EndpointName=endpoint_name
            )
            
            logger.info(f"Endpoint deletion initiated: {endpoint_name}")
            
            return {
                "success": True,
                "message": f"Endpoint {endpoint_name} deletion initiated"
            }
            
        except Exception as e:
            logger.error(f"Endpoint deletion failed: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

# Global endpoint manager
endpoint_manager = SageMakerEndpointManager()
