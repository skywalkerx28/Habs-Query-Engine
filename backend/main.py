"""
HeartBeat Engine - FastAPI Backend
Montreal Canadiens Advanced Analytics Assistant

FastAPI wrapper around the existing LangGraph orchestrator.
Provides HTTP API endpoints for the Next.js frontend.
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from contextlib import asynccontextmanager
import logging
import os
import sys
from typing import Dict, Any

# Add orchestrator to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Add backend directory to path for api imports
sys.path.append(os.path.dirname(__file__))

from orchestrator.agents.heartbeat_orchestrator import HeartBeatOrchestrator
from orchestrator.config.settings import UserRole, settings
from orchestrator.utils.state import UserContext

# Import API routes
from api.routes.auth import router as auth_router
from api.routes.query import router as query_router
from api.routes.analytics import router as analytics_router
from api.routes.clips import router as clips_router
from api.dependencies import set_orchestrator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global orchestrator instance
orchestrator: HeartBeatOrchestrator = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    global orchestrator
    
    # Startup
    logger.info("Starting HeartBeat Engine API...")
    
    # Initialize orchestrator
    try:
        orchestrator = HeartBeatOrchestrator()
        logger.info("Orchestrator initialized successfully")
        
        # Set orchestrator for dependency injection
        set_orchestrator(orchestrator)
        
        # Validate configuration
        if settings.validate_config():
            logger.info("Configuration validation passed")
        else:
            logger.warning("Configuration validation failed - some features may not work")
            
    except Exception as e:
        logger.error(f"Failed to initialize orchestrator: {str(e)}")
        orchestrator = None
    
    yield
    
    # Shutdown
    logger.info("Shutting down HeartBeat Engine API...")

# Create FastAPI application
app = FastAPI(
    title="HeartBeat Engine API",
    description="Montreal Canadiens Advanced Analytics Assistant",
    version="2.1.0",
    lifespan=lifespan
)

# Configure CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001", 
        "http://localhost:3008",
        "http://localhost:3009",
        "http://192.168.0.118:3000",
        "http://192.168.0.118:3008",
        "http://192.168.0.118:3009",
        "http://10.121.114.200:3000",  # Current network IP
        "http://10.121.114.200:3001",
        "http://10.121.114.200:3008",
        "http://10.121.114.200:3009"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(auth_router)
app.include_router(query_router)
app.include_router(analytics_router)
app.include_router(clips_router)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "HeartBeat Engine API",
        "version": "2.1.0",
        "status": "online",
        "orchestrator_available": orchestrator is not None,
        "description": "Montreal Canadiens Advanced Analytics Assistant"
    }

@app.get("/api/v1/health")
async def health_check():
    """Detailed health check"""
    health_status = {
        "status": "healthy",
        "orchestrator": orchestrator is not None,
        "pinecone_configured": bool(settings.pinecone.api_key),
        "data_directory_exists": os.path.exists(settings.parquet.data_directory),
        "configuration_valid": settings.validate_config()
    }
    
    return health_status

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        log_level="info"
    )
