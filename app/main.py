#!/usr/bin/env python3
"""
HeartBeat Engine - Main Streamlit Application
Stanley Assistant

Main web interface for the HeartBeat hockey analytics platform.
"""

import streamlit as st
import asyncio
import json
from datetime import datetime
from typing import Dict, Any, List
import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from app.config.app_config import app_config, ui_config
from app.auth.authentication import auth_manager
from app.components.query_interface import QueryInterface
from app.components.response_display import ResponseDisplay
from app.utils.session_manager import SessionManager
from orchestrator.config.settings import UserRole

# Configure Streamlit page
st.set_page_config(
    page_title=app_config.page_title,
    page_icon=app_config.app_icon,
    layout=app_config.layout,
    initial_sidebar_state="expanded"
)

# Apply custom CSS
st.markdown(ui_config.custom_css, unsafe_allow_html=True)

class HeartBeatApp:
    """
    Main HeartBeat application class.
    
    Manages the complete Streamlit interface including:
    - User authentication and session management
    - Query processing and response display
    - Real-time analytics and visualizations
    - Role-based access control
    """
    
    def __init__(self):
        self.session_manager = SessionManager()
        self.query_interface = QueryInterface()
        self.response_display = ResponseDisplay()
    
    def run(self) -> None:
        """Main application entry point"""
        
        # Handle authentication
        if not auth_manager.render_login_form():
            return
        
        # Render main application
        self._render_main_interface()
    
    def _render_main_interface(self) -> None:
        """Render the main application interface"""
        
        # Render sidebar with user info and navigation
        self._render_sidebar()
        
        # Main content area
        self._render_header()
        
        # Query interface
        self._render_query_section()
        
        # Response and analytics section
        self._render_response_section()
        
        # Footer with system status
        self._render_footer()
    
    def _render_sidebar(self) -> None:
        """Render sidebar with user info and navigation"""
        
        # User information
        auth_manager.render_user_info_sidebar()
        
        st.sidebar.markdown("---")
        
        # Navigation menu
        st.sidebar.markdown("### Analytics")
        
        # Quick actions based on user role
        user_context = auth_manager.get_user_context()
        
        if user_context:
            role_actions = self._get_role_specific_actions(user_context.role)
            
            for action in role_actions:
                if st.sidebar.button(action["label"], key=action["key"]):
                    st.session_state.quick_query = action["query"]
                    st.rerun()
        
        st.sidebar.markdown("---")
        
        # System status
        st.sidebar.markdown("### System Status")
        
        # Training status
        training_status = self._get_training_status()
        st.sidebar.markdown(f"**Model Training:** {training_status}")
        
        # Data sources status
        st.sidebar.markdown("**Data Sources:**")
        st.sidebar.markdown("- Online: Pinecone RAG (100 records)")
        st.sidebar.markdown("- Online: NHL Player Stats (30 teams)")
        st.sidebar.markdown("- Online: MTL Analytics (176+ files)")
        
        # Performance metrics
        if 'last_query_time' in st.session_state:
            st.sidebar.markdown(f"**Last Query:** {st.session_state.last_query_time}ms")
    
    def _render_header(self) -> None:
        """Render main header"""
        
        user_info = auth_manager.get_user_info()
        
        st.markdown(f"""
        <div class="main-header">
            HeartBeat Engine
        </div>
        <div style="text-align: center; margin-bottom: 1rem;">
            <h4>Welcome, {user_info['name'] if user_info else 'User'}</h4>
            <p>Stanley - Your Montreal Canadiens Analytics Assistant</p>
        </div>
        """, unsafe_allow_html=True)
    
    def _render_query_section(self) -> None:
        """Render query input and processing section"""
        
        st.markdown("### Ask Your Hockey Analytics Question")
        
        # Check for quick query from sidebar
        default_query = st.session_state.get('quick_query', '')
        if default_query:
            st.session_state.quick_query = ''  # Clear after use
        
        # Render query interface
        query_result = self.query_interface.render(default_query=default_query)
        
        if query_result:
            # Store result in session state for response display
            st.session_state.current_result = query_result
            st.session_state.last_query_time = query_result.get('processing_time_ms', 0)
    
    def _render_response_section(self) -> None:
        """Render response and analytics section"""
        
        if 'current_result' in st.session_state:
            result = st.session_state.current_result
            
            # Display response
            self.response_display.render(result)
            
            # Display analytics and citations
            self._render_analytics_details(result)
    
    def _render_analytics_details(self, result: Dict[str, Any]) -> None:
        """Render detailed analytics and tool results"""
        
        if not result.get('tool_results'):
            return
        
        st.markdown("### Analytics Details")
        
        # Create tabs for different result types
        tab_names = ["Tool Results", "Data Sources", "Performance"]
        tabs = st.tabs(tab_names)
        
        with tabs[0]:  # Tool Results
            for i, tool_result in enumerate(result['tool_results'], 1):
                with st.expander(f"Tool {i}: {tool_result.get('tool', 'Unknown')}", expanded=False):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"**Status:** {'Success' if tool_result.get('success') else 'Failed'}")
                        st.markdown(f"**Citations:** {len(tool_result.get('citations', []))}")
                    
                    with col2:
                        if tool_result.get('citations'):
                            st.markdown("**Sources:**")
                            for citation in tool_result['citations']:
                                st.markdown(f"- {citation}")
        
        with tabs[1]:  # Data Sources
            st.markdown("**Evidence Chain:**")
            evidence = result.get('evidence_chain', [])
            
            if evidence:
                for source in evidence:
                    st.markdown(f"- {source}")
            else:
                st.markdown("*No evidence chain available*")
        
        with tabs[2]:  # Performance
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Processing Time", f"{result.get('processing_time_ms', 0)}ms")
            
            with col2:
                st.metric("Tools Used", len(result.get('tool_results', [])))
            
            with col3:
                st.metric("Query Type", result.get('query_type', 'Unknown'))
    
    def _render_footer(self) -> None:
        """Render footer with system information"""
        
        st.markdown("---")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**HeartBeat Engine v1.0**")
            st.markdown("Montreal Canadiens Analytics")
        
        with col2:
            st.markdown("**Powered By:**")
            st.markdown("deepseek-ai/DeepSeek-R1-Distill-Qwen-32B + RAG + Real-time Analytics")
        
        with col3:
            st.markdown("**Status:**")
            st.markdown(f"Online - {datetime.now().strftime('%H:%M:%S')}")
    
    def _get_role_specific_actions(self, role: UserRole) -> List[Dict[str, str]]:
        """Get quick action buttons based on user role"""
        
        base_actions = [
            {
                "label": "Team Overview",
                "query": "Give me an overview of Montreal Canadiens performance this season",
                "key": "team_overview"
            },
            {
                "label": "Top Players",
                "query": "Who are our top performing players this season?",
                "key": "top_players"
            }
        ]
        
        role_specific = {
            UserRole.COACH: [
                {
                    "label": "Line Combinations",
                    "query": "Analyze our current line combinations effectiveness",
                    "key": "line_combos"
                },
                {
                    "label": "Tactical Analysis",
                    "query": "What are our tactical strengths and weaknesses?",
                    "key": "tactical"
                }
            ],
            UserRole.PLAYER: [
                {
                    "label": "My Performance",
                    "query": "How am I performing compared to my teammates?",
                    "key": "my_performance"
                },
                {
                    "label": "Improvement Areas",
                    "query": "What areas should I focus on for improvement?",
                    "key": "improvement"
                }
            ],
            UserRole.ANALYST: [
                {
                    "label": "Advanced Metrics",
                    "query": "Show me advanced analytics and xG metrics for the team",
                    "key": "advanced_metrics"
                },
                {
                    "label": "Deep Dive Analysis",
                    "query": "Provide comprehensive statistical analysis of recent performance",
                    "key": "deep_dive"
                }
            ],
            UserRole.SCOUT: [
                {
                    "label": "Player Evaluation",
                    "query": "Evaluate our prospects and their development progress",
                    "key": "player_eval"
                },
                {
                    "label": "Opponent Analysis",
                    "query": "Analyze upcoming opponent strengths and weaknesses",
                    "key": "opponent_analysis"
                }
            ],
            UserRole.STAFF: [
                {
                    "label": "Team Summary",
                    "query": "Provide a high-level team performance summary",
                    "key": "team_summary"
                }
            ]
        }
        
        return base_actions + role_specific.get(role, [])
    
    def _get_training_status(self) -> str:
        """Get current model training status"""
        
        # This would check actual SageMaker job status
        # For now, return static status
        return "In Progress"

def main():
    """Main application entry point"""
    
    try:
        app = HeartBeatApp()
        app.run()
        
    except Exception as e:
        st.error(f"Application error: {str(e)}")
        
        if app_config.enable_debug_mode:
            st.exception(e)

if __name__ == "__main__":
    main()
