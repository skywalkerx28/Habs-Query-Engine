"""
HeartBeat Engine - FastAPI Dependencies
Montreal Canadiens Advanced Analytics Assistant

Dependency injection for FastAPI routes.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import base64
import logging

from orchestrator.agents.heartbeat_orchestrator import HeartBeatOrchestrator
from orchestrator.config.settings import UserRole
from orchestrator.utils.state import UserContext

logger = logging.getLogger(__name__)

# Security scheme
security = HTTPBearer()

# Global orchestrator instance (will be initialized in main.py)
_orchestrator: HeartBeatOrchestrator = None

def set_orchestrator(orchestrator: HeartBeatOrchestrator) -> None:
    """Set the global orchestrator instance"""
    global _orchestrator
    _orchestrator = orchestrator

def get_orchestrator() -> HeartBeatOrchestrator:
    """Get the orchestrator instance"""
    if _orchestrator is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Orchestrator not available"
        )
    return _orchestrator

# User database (same as auth.py for consistency)
USERS_DB = {
    "coach_martin": {
        "password": "coach2024",
        "name": "Martin St-Louis",
        "role": UserRole.COACH,
        "email": "martin@canadiens.com",
        "team_access": ["MTL"]
    },
    "analyst_hughes": {
        "password": "analyst2024", 
        "name": "Kent Hughes",
        "role": UserRole.ANALYST,
        "email": "kent@canadiens.com",
        "team_access": ["MTL"]
    },
    "player_suzuki": {
        "password": "player2024",
        "name": "Nick Suzuki", 
        "role": UserRole.PLAYER,
        "email": "nick@canadiens.com",
        "team_access": ["MTL"]
    },
    "scout_lapointe": {
        "password": "scout2024",
        "name": "Martin Lapointe",
        "role": UserRole.SCOUT, 
        "email": "martin.lapointe@canadiens.com",
        "team_access": ["MTL"]
    },
    "staff_molson": {
        "password": "staff2024",
        "name": "Geoff Molson",
        "role": UserRole.STAFF,
        "email": "geoff@canadiens.com", 
        "team_access": ["MTL"]
    }
}

def get_current_user_context(credentials: HTTPAuthorizationCredentials = Depends(security)) -> UserContext:
    """
    Extract user context from authentication token.
    
    For development, using simple token format: base64(username:password)
    In production, use proper JWT tokens with signing and expiration.
    """
    
    try:
        # Decode simple token format
        decoded = base64.b64decode(credentials.credentials).decode()
        username, password = decoded.split(":", 1)
        
        # Validate credentials
        user_data = USERS_DB.get(username)
        if not user_data or user_data["password"] != password:
            logger.warning(f"Invalid credentials for user: {username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Create user context for orchestrator
        user_context = UserContext(
            user_id=username,
            role=user_data["role"],
            name=user_data["name"],
            team_access=user_data["team_access"],
            session_id=f"api-session-{username}"
        )
        
        logger.debug(f"User context created for: {username} ({user_data['role'].value})")
        return user_context
        
    except ValueError as e:
        logger.error(f"Token format error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token format",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        logger.error(f"Authentication error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed",
            headers={"WWW-Authenticate": "Bearer"},
        )
