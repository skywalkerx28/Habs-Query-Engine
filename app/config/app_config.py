"""
HeartBeat Engine - Streamlit Application Configuration
Stanley Assistant

Configuration settings for the Streamlit web interface.
"""

import os
from typing import Dict, List, Any
from dataclasses import dataclass, field
from pathlib import Path

@dataclass
class AppConfig:
    """Main application configuration"""
    
    # Application settings
    app_title: str = "HeartBeat Engine - Montreal Canadiens Analytics"
    app_icon: str = "Hockey"
    page_title: str = "MTL Analytics"
    layout: str = "wide"
    
    # Theme configuration
    primary_color: str = "#AF1E2D"  # Montreal Canadiens red
    background_color: str = "#FFFFFF"
    secondary_background_color: str = "#F0F2F6"
    text_color: str = "#262730"
    
    # Session configuration
    session_timeout_minutes: int = 60
    max_concurrent_sessions: int = 100
    
    # Query configuration
    max_query_length: int = 500
    query_timeout_seconds: int = 30
    max_response_length: int = 2000
    
    # Display configuration
    results_per_page: int = 10
    max_citations_display: int = 5
    enable_debug_mode: bool = os.getenv("HEARTBEAT_DEBUG", "false").lower() == "true"

@dataclass
class UIConfig:
    """User interface configuration"""
    
    # Layout settings
    sidebar_width: int = 300
    main_content_padding: str = "1rem"
    
    # Component settings
    query_input_height: int = 100
    response_container_height: int = 600
    
    # Styling
    custom_css: str = """
    <style>
    .main-header {
        color: #AF1E2D;
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .role-badge {
        background-color: #AF1E2D;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        font-size: 0.8rem;
        font-weight: bold;
    }
    
    .query-container {
        border: 2px solid #E1E5E9;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .response-container {
        background-color: #F8F9FA;
        border-radius: 0.5rem;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #AF1E2D;
    }
    
    .citation-box {
        background-color: #E8F4FD;
        border-radius: 0.25rem;
        padding: 0.5rem;
        margin: 0.5rem 0;
        font-size: 0.9rem;
        border-left: 3px solid #1E88E5;
    }
    
    .metrics-card {
        background-color: white;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border: 1px solid #E1E5E9;
    }
    
    .error-message {
        background-color: #FFEBEE;
        color: #C62828;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #C62828;
        margin: 1rem 0;
    }
    
    .success-message {
        background-color: #E8F5E8;
        color: #2E7D32;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #2E7D32;
        margin: 1rem 0;
    }
    </style>
    """

@dataclass
class AuthConfig:
    """Authentication configuration"""
    
    # Authentication settings
    enable_authentication: bool = True
    session_duration_days: int = 7
    session_timeout_minutes: int = 60
    require_password_change: bool = False
    
    # User roles and permissions
    default_role: str = "staff"
    admin_users: List[str] = field(default_factory=lambda: ["admin", "xavier.bouchard"])
    
    # Security settings
    cookie_name: str = "heartbeat_auth"
    cookie_key: str = os.getenv("HEARTBEAT_COOKIE_KEY", "heartbeat_secret_key_2024")
    cookie_expiry_days: int = 7
    
    # Default users (for development - replace with proper user management)
    default_users: Dict[str, Dict[str, Any]] = field(default_factory=lambda: {
        "coach_martin": {
            "name": "Martin St-Louis",
            "password": "coach2024",  # In production, use hashed passwords
            "role": "coach",
            "team_access": ["MTL"],
            "email": "coach@canadiens.com"
        },
        "analyst_hughes": {
            "name": "Kent Hughes", 
            "password": "analyst2024",
            "role": "analyst",
            "team_access": ["MTL"],
            "email": "analyst@canadiens.com"
        },
        "player_suzuki": {
            "name": "Nick Suzuki",
            "password": "player2024", 
            "role": "player",
            "team_access": ["MTL"],
            "email": "player@canadiens.com"
        },
        "scout_timmins": {
            "name": "Trevor Timmins",
            "password": "scout2024",
            "role": "scout", 
            "team_access": ["MTL", "ANA", "BOS", "CAR"],
            "email": "scout@canadiens.com"
        },
        "staff_molson": {
            "name": "Geoff Molson",
            "password": "staff2024",
            "role": "staff",
            "team_access": ["MTL"],
            "email": "staff@canadiens.com"
        }
    })

# Global configuration instances
app_config = AppConfig()
ui_config = UIConfig()
auth_config = AuthConfig()
