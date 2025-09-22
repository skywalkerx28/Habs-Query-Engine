"""
HeartBeat Engine - Authentication System
Stanley Assistant

Role-based authentication and session management for the Streamlit interface.
"""

import streamlit as st
import hashlib
import hmac
from typing import Dict, Optional, Any
from datetime import datetime, timedelta
import json

from app.config.app_config import auth_config
from orchestrator.config.settings import UserRole
from orchestrator.utils.state import UserContext

class AuthenticationManager:
    """
    Manages user authentication and session state for the HeartBeat application.
    
    Features:
    - Role-based access control
    - Session management
    - User context creation
    - Security validation
    """
    
    def __init__(self):
        self.config = auth_config
        self._initialize_session_state()
    
    def _initialize_session_state(self) -> None:
        """Initialize Streamlit session state for authentication"""
        
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False
        
        if 'user_context' not in st.session_state:
            st.session_state.user_context = None
        
        if 'login_attempts' not in st.session_state:
            st.session_state.login_attempts = 0
        
        if 'session_start' not in st.session_state:
            st.session_state.session_start = None
    
    def render_login_form(self) -> bool:
        """
        Render login form and handle authentication.
        
        Returns:
            bool: True if user is authenticated, False otherwise
        """
        
        if self.is_authenticated():
            return True
        
        st.markdown("""
        <div class="main-header">
            HeartBeat Engine
        </div>
        <div style="text-align: center; margin-bottom: 2rem;">
            <h3>Montreal Canadiens Advanced Analytics</h3>
            <p>Stanley - Professional hockey analytics platform for coaches, players, analysts, and staff</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Create login form
        with st.container():
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col2:
                st.markdown("### Login")
                
                with st.form("login_form"):
                    username = st.text_input("Username", placeholder="Enter your username")
                    password = st.text_input("Password", type="password", placeholder="Enter your password")
                    
                    col_login, col_demo = st.columns(2)
                    
                    with col_login:
                        login_clicked = st.form_submit_button("Login", use_container_width=True)
                    
                    with col_demo:
                        demo_clicked = st.form_submit_button("Demo Mode", use_container_width=True)
                
                # Handle login attempt
                if login_clicked and username and password:
                    if self._validate_credentials(username, password):
                        self._create_user_session(username)
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
                        st.session_state.login_attempts += 1
                        
                        if st.session_state.login_attempts >= 3:
                            st.error("Too many failed attempts. Please contact administrator.")
                
                # Handle demo mode
                if demo_clicked:
                    self._create_demo_session()
                    st.rerun()
                
                # Display demo users for development
                if self.config.enable_authentication:
                    with st.expander("🧪 Demo Users (Development Only)", expanded=False):
                        st.markdown("**Available demo accounts:**")
                        
                        demo_users = [
                            ("coach_martin", "Martin St-Louis", "Coach"),
                            ("analyst_hughes", "Kent Hughes", "Analyst"), 
                            ("player_suzuki", "Nick Suzuki", "Player"),
                            ("scout_lapointe", "Martin Lapointe", "Scout"),
                            ("staff_molson", "Geoff Molson", "Staff")
                        ]
                        
                        for username, name, role in demo_users:
                            st.markdown(f"- **{username}** ({name}) - {role}")
                        
                        st.markdown("*Password for all demo accounts: [role]2024 (e.g., coach2024)*")
        
        return False
    
    def _validate_credentials(self, username: str, password: str) -> bool:
        """Validate user credentials"""
        
        if not self.config.enable_authentication:
            return True
        
        # Check against default users (in production, use proper user database)
        user_data = self.config.default_users.get(username)
        
        if not user_data:
            return False
        
        # Simple password check (in production, use proper password hashing)
        return user_data["password"] == password
    
    def _create_user_session(self, username: str) -> None:
        """Create authenticated user session"""
        
        user_data = self.config.default_users.get(username)
        
        if user_data:
            # Create user context for orchestrator
            user_context = UserContext(
                user_id=username,
                role=UserRole(user_data["role"]),
                name=user_data["name"],
                team_access=user_data["team_access"],
                session_id=self._generate_session_id()
            )
            
            # Update session state
            st.session_state.authenticated = True
            st.session_state.user_context = user_context
            st.session_state.session_start = datetime.now()
            st.session_state.login_attempts = 0
            
            # Store session info for display
            st.session_state.user_info = {
                "username": username,
                "name": user_data["name"],
                "role": user_data["role"],
                "email": user_data["email"],
                "team_access": user_data["team_access"]
            }
    
    def _create_demo_session(self) -> None:
        """Create demo session for testing"""
        
        # Create demo analyst user
        demo_context = UserContext(
            user_id="demo_user",
            role=UserRole.ANALYST,
            name="Demo User",
            team_access=["MTL"],
            session_id=self._generate_session_id()
        )
        
        st.session_state.authenticated = True
        st.session_state.user_context = demo_context
        st.session_state.session_start = datetime.now()
        st.session_state.user_info = {
            "username": "demo_user",
            "name": "Demo User",
            "role": "analyst",
            "email": "demo@heartbeat.com",
            "team_access": ["MTL"]
        }
    
    def _generate_session_id(self) -> str:
        """Generate unique session ID"""
        timestamp = datetime.now().isoformat()
        return hashlib.md5(timestamp.encode()).hexdigest()[:16]
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated and session is valid"""
        
        if not st.session_state.authenticated:
            return False
        
        # Check session timeout
        if st.session_state.session_start:
            session_duration = datetime.now() - st.session_state.session_start
            if session_duration > timedelta(minutes=self.config.session_timeout_minutes):
                self.logout()
                return False
        
        return True
    
    def get_user_context(self) -> Optional[UserContext]:
        """Get current user context for orchestrator"""
        return st.session_state.user_context
    
    def get_user_info(self) -> Optional[Dict[str, Any]]:
        """Get current user information for display"""
        return st.session_state.get('user_info')
    
    def logout(self) -> None:
        """Logout current user and clear session"""
        
        st.session_state.authenticated = False
        st.session_state.user_context = None
        st.session_state.user_info = None
        st.session_state.session_start = None
        st.session_state.login_attempts = 0
        
        # Clear any cached data
        if 'query_history' in st.session_state:
            st.session_state.query_history = []
        
        st.rerun()
    
    def render_user_info_sidebar(self) -> None:
        """Render user information in sidebar"""
        
        if not self.is_authenticated():
            return
        
        user_info = self.get_user_info()
        user_context = self.get_user_context()
        
        if user_info and user_context:
            st.sidebar.markdown("### User Profile")
            
            # User details
            st.sidebar.markdown(f"**Name:** {user_info['name']}")
            st.sidebar.markdown(f"**Role:** <span class='role-badge'>{user_info['role'].upper()}</span>", unsafe_allow_html=True)
            st.sidebar.markdown(f"**Teams:** {', '.join(user_info['team_access'])}")
            
            # Session info
            if st.session_state.session_start:
                session_duration = datetime.now() - st.session_state.session_start
                minutes = int(session_duration.total_seconds() / 60)
                st.sidebar.markdown(f"**Session:** {minutes} minutes")
            
            # Permissions
            with st.sidebar.expander("Permissions", expanded=False):
                from orchestrator.config.settings import settings
                permissions = settings.get_user_permissions(user_context.role)
                
                st.markdown(f"**Data Scope:** {', '.join(permissions['data_scope'])}")
                st.markdown(f"**Advanced Metrics:** {'Yes' if permissions['advanced_metrics'] else 'No'}")
                st.markdown(f"**Opponent Data:** {'Yes' if permissions['opponent_data'] else 'No'}")
                st.markdown(f"**Tactical Analysis:** {'Yes' if permissions['tactical_analysis'] else 'No'}")
            
            # Logout button
            if st.sidebar.button("Logout", use_container_width=True):
                self.logout()

# Global authentication manager
auth_manager = AuthenticationManager()
