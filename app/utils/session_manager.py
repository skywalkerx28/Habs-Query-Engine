"""
HeartBeat Engine - Session Manager
Stanley Assistant

Session management utilities for the Streamlit application.
"""

import streamlit as st
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import json

class SessionManager:
    """
    Manages user sessions and application state.
    
    Features:
    - Session persistence and cleanup
    - Query history management
    - User preferences storage
    - Performance tracking
    """
    
    def __init__(self):
        self._initialize_session_metrics()
    
    def _initialize_session_metrics(self) -> None:
        """Initialize session metrics tracking"""
        
        if 'session_metrics' not in st.session_state:
            st.session_state.session_metrics = {
                "queries_processed": 0,
                "total_processing_time": 0,
                "successful_queries": 0,
                "failed_queries": 0,
                "session_start": datetime.now().isoformat(),
                "tools_used": {},
                "query_types": {}
            }
    
    def track_query_metrics(self, result: Dict[str, Any]) -> None:
        """Track metrics for a processed query"""
        
        metrics = st.session_state.session_metrics
        
        # Update counters
        metrics["queries_processed"] += 1
        metrics["total_processing_time"] += result.get('processing_time_ms', 0)
        
        # Track success/failure
        if result.get('success', True):
            metrics["successful_queries"] += 1
        else:
            metrics["failed_queries"] += 1
        
        # Track query types
        query_type = result.get('query_type', 'unknown')
        metrics["query_types"][query_type] = metrics["query_types"].get(query_type, 0) + 1
        
        # Track tool usage
        for tool_result in result.get('tool_results', []):
            tool_name = tool_result.get('tool', 'unknown')
            if tool_result.get('success'):
                metrics["tools_used"][tool_name] = metrics["tools_used"].get(tool_name, 0) + 1
    
    def get_session_summary(self) -> Dict[str, Any]:
        """Get session summary for display"""
        
        metrics = st.session_state.session_metrics
        
        # Calculate averages
        avg_processing_time = (
            metrics["total_processing_time"] / metrics["queries_processed"]
            if metrics["queries_processed"] > 0 else 0
        )
        
        success_rate = (
            metrics["successful_queries"] / metrics["queries_processed"] * 100
            if metrics["queries_processed"] > 0 else 0
        )
        
        return {
            "total_queries": metrics["queries_processed"],
            "avg_processing_time_ms": round(avg_processing_time, 1),
            "success_rate_percent": round(success_rate, 1),
            "session_duration_minutes": self._get_session_duration_minutes(),
            "most_used_tools": self._get_top_tools(metrics["tools_used"]),
            "query_type_distribution": metrics["query_types"]
        }
    
    def _get_session_duration_minutes(self) -> int:
        """Get session duration in minutes"""
        
        session_start = st.session_state.session_metrics.get("session_start")
        
        if session_start:
            start_time = datetime.fromisoformat(session_start)
            duration = datetime.now() - start_time
            return int(duration.total_seconds() / 60)
        
        return 0
    
    def _get_top_tools(self, tools_used: Dict[str, int], limit: int = 3) -> List[Dict[str, Any]]:
        """Get most frequently used tools"""
        
        sorted_tools = sorted(tools_used.items(), key=lambda x: x[1], reverse=True)
        
        return [
            {"tool": tool, "count": count}
            for tool, count in sorted_tools[:limit]
        ]
    
    def save_user_preferences(self, preferences: Dict[str, Any]) -> None:
        """Save user preferences to session state"""
        
        if 'user_preferences' not in st.session_state:
            st.session_state.user_preferences = {}
        
        st.session_state.user_preferences.update(preferences)
    
    def get_user_preferences(self) -> Dict[str, Any]:
        """Get user preferences from session state"""
        
        return st.session_state.get('user_preferences', {})
    
    def clear_session_data(self) -> None:
        """Clear session data (except authentication)"""
        
        # Clear query history
        if 'query_history' in st.session_state:
            st.session_state.query_history = []
        
        # Clear current results
        if 'current_result' in st.session_state:
            del st.session_state.current_result
        
        # Reset metrics
        self._initialize_session_metrics()
    
    def export_session_data(self) -> Dict[str, Any]:
        """Export session data for analysis or backup"""
        
        return {
            "session_metrics": st.session_state.get('session_metrics', {}),
            "query_history": st.session_state.get('query_history', []),
            "user_preferences": st.session_state.get('user_preferences', {}),
            "export_timestamp": datetime.now().isoformat()
        }
