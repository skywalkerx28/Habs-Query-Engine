"""
HeartBeat Engine - Query Interface Component
Stanley

Query input and processing interface for the Streamlit application.
"""

import streamlit as st
import asyncio
from datetime import datetime
from typing import Dict, Any, Optional, List
import json

from app.auth.authentication import auth_manager
from orchestrator import orchestrator

class QueryInterface:
    """
    Query interface component for hockey analytics queries.
    
    Features:
    - Natural language query input
    - Query suggestions based on user role
    - Real-time processing with progress indicators
    - Query history and favorites
    """
    
    def __init__(self):
        self._initialize_session_state()
    
    def _initialize_session_state(self) -> None:
        """Initialize session state for query interface"""
        
        if 'query_history' not in st.session_state:
            st.session_state.query_history = []
        
        if 'favorite_queries' not in st.session_state:
            st.session_state.favorite_queries = []
        
        if 'current_query' not in st.session_state:
            st.session_state.current_query = ""
    
    def render(self, default_query: str = "") -> Optional[Dict[str, Any]]:
        """
        Render query interface and handle query processing.
        
        Args:
            default_query: Default query text to populate
            
        Returns:
            Query result if processing completed, None otherwise
        """
        
        user_context = auth_manager.get_user_context()
        
        if not user_context:
            st.error("User context not available")
            return None
        
        # Query input section
        with st.container():
            # Query input with suggestions
            query_text = self._render_query_input(default_query)
            
            # Query action buttons
            col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
            
            with col1:
                process_clicked = st.button(
                    "Analyze", 
                    use_container_width=True,
                    type="primary",
                    disabled=not query_text.strip()
                )
            
            with col2:
                clear_clicked = st.button("Clear", use_container_width=True)
            
            with col3:
                example_clicked = st.button("Example", use_container_width=True)
            
            with col4:
                history_clicked = st.button("History", use_container_width=True)
        
        # Handle button clicks
        if clear_clicked:
            st.session_state.current_query = ""
            st.rerun()
        
        if example_clicked:
            example_query = self._get_example_query(user_context.role)
            st.session_state.current_query = example_query
            st.rerun()
        
        if history_clicked:
            self._show_query_history()
        
        # Process query if requested
        if process_clicked and query_text.strip():
            return self._process_query(query_text, user_context)
        
        return None
    
    def _render_query_input(self, default_query: str = "") -> str:
        """Render query input with suggestions"""
        
        # Use default query or session state
        initial_value = default_query or st.session_state.get('current_query', '')
        
        # Query input
        query_text = st.text_area(
            "Enter your hockey analytics question:",
            value=initial_value,
            height=100,
            placeholder="e.g., How is Suzuki performing this season? What are our powerplay statistics?",
            help="Ask natural language questions about player performance, team analytics, game analysis, or tactical insights."
        )
        
        # Update session state
        st.session_state.current_query = query_text
        
        # Query suggestions based on user role
        if not query_text.strip():
            self._render_query_suggestions()
        
        return query_text
    
    def _render_query_suggestions(self) -> None:
        """Render query suggestions based on user role"""
        
        user_context = auth_manager.get_user_context()
        
        if not user_context:
            return
        
        suggestions = self._get_query_suggestions(user_context.role)
        
        if suggestions:
            st.markdown("**Suggested Questions:**")
            
            cols = st.columns(min(len(suggestions), 3))
            
            for i, suggestion in enumerate(suggestions[:3]):
                with cols[i]:
                    if st.button(suggestion["label"], key=f"suggestion_{i}", use_container_width=True):
                        st.session_state.current_query = suggestion["query"]
                        st.rerun()
    
    def _process_query(self, query: str, user_context) -> Dict[str, Any]:
        """Process hockey analytics query"""
        
        # Show processing indicator
        with st.spinner("Processing your query..."):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Update progress
                progress_bar.progress(25)
                status_text.text("Analyzing query intent...")
                
                # Process query using orchestrator
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                progress_bar.progress(50)
                status_text.text("Retrieving hockey context...")
                
                result = loop.run_until_complete(
                    orchestrator.process_query(
                        query=query,
                        user_context=user_context
                    )
                )
                
                progress_bar.progress(75)
                status_text.text("Generating response...")
                
                # Add query to history
                self._add_to_history(query, result)
                
                progress_bar.progress(100)
                status_text.text("Complete!")
                
                # Clear progress indicators
                progress_bar.empty()
                status_text.empty()
                
                return result
                
            except Exception as e:
                progress_bar.empty()
                status_text.empty()
                
                st.error(f"Error processing query: {str(e)}")
                
                return {
                    "response": "I apologize, but I encountered an error processing your request. Please try again or rephrase your question.",
                    "error": str(e),
                    "success": False,
                    "processing_time_ms": 0
                }
    
    def _add_to_history(self, query: str, result: Dict[str, Any]) -> None:
        """Add query and result to history"""
        
        history_entry = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "query_type": result.get('query_type', 'unknown'),
            "success": result.get('success', True),
            "processing_time_ms": result.get('processing_time_ms', 0),
            "response_preview": result.get('response', '')[:100] + "..." if result.get('response') else ""
        }
        
        # Add to beginning of history
        st.session_state.query_history.insert(0, history_entry)
        
        # Keep only last 20 queries
        st.session_state.query_history = st.session_state.query_history[:20]
    
    def _show_query_history(self) -> None:
        """Display query history in sidebar or modal"""
        
        history = st.session_state.query_history
        
        if not history:
            st.info("No query history available")
            return
        
        with st.expander("Query History", expanded=True):
            for i, entry in enumerate(history[:10]):  # Show last 10
                timestamp = datetime.fromisoformat(entry['timestamp']).strftime('%H:%M:%S')
                status_icon = "Success" if entry['success'] else "Failed"
                
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    if st.button(
                        f"{status_icon} {entry['query'][:50]}...", 
                        key=f"history_{i}",
                        help=f"Query type: {entry['query_type']}, Time: {entry['processing_time_ms']}ms"
                    ):
                        st.session_state.current_query = entry['query']
                        st.rerun()
                
                with col2:
                    st.markdown(f"*{timestamp}*")
    
    def _get_query_suggestions(self, role) -> List[Dict[str, str]]:
        """Get query suggestions based on user role"""
        
        from orchestrator.config.settings import UserRole
        
        suggestions = {
            UserRole.COACH: [
                {
                    "label": "Line Analysis",
                    "query": "Analyze the effectiveness of our current line combinations"
                },
                {
                    "label": "Special Teams",
                    "query": "How are our powerplay and penalty kill units performing?"
                },
                {
                    "label": "Matchup Strategy",
                    "query": "What should our strategy be against Boston's top line?"
                }
            ],
            UserRole.PLAYER: [
                {
                    "label": "Personal Stats",
                    "query": "How am I performing compared to my position average?"
                },
                {
                    "label": "Improvement Focus",
                    "query": "What skills should I focus on improving?"
                },
                {
                    "label": "Team Role",
                    "query": "How does my performance impact the team's success?"
                }
            ],
            UserRole.ANALYST: [
                {
                    "label": "Advanced Metrics",
                    "query": "Show me xG and Corsi metrics for our top line"
                },
                {
                    "label": "Trend Analysis",
                    "query": "Analyze performance trends over the last 10 games"
                },
                {
                    "label": "League Comparison",
                    "query": "How do we compare to other Atlantic Division teams?"
                }
            ],
            UserRole.SCOUT: [
                {
                    "label": "Player Evaluation",
                    "query": "Evaluate prospects in our system for NHL readiness"
                },
                {
                    "label": "Opponent Scouting",
                    "query": "Scout the next opponent's key players and tendencies"
                },
                {
                    "label": "Draft Analysis",
                    "query": "Analyze potential draft targets and their fit with our system"
                }
            ],
            UserRole.STAFF: [
                {
                    "label": "Team Summary",
                    "query": "Provide a summary of team performance this month"
                },
                {
                    "label": "Player Health",
                    "query": "How are our players managing their workload and health?"
                },
                {
                    "label": "Fan Engagement",
                    "query": "What positive stories can we share with fans?"
                }
            ]
        }
        
        return suggestions.get(role, [])
    
    def _get_example_query(self, role) -> str:
        """Get example query based on user role"""
        
        suggestions = self._get_query_suggestions(role)
        
        if suggestions:
            return suggestions[0]["query"]
        else:
            return "How is the team performing this season?"
