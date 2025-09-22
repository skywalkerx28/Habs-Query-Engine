"""
HeartBeat Engine - LangGraph State Management
Montreal Canadiens Advanced Analytics Assistant

State management for the LangGraph orchestrator workflow.
"""

from typing import Dict, List, Any, Optional, TypedDict, Annotated
from dataclasses import dataclass, field
from datetime import datetime
import operator
from enum import Enum

from orchestrator.config.settings import UserRole

class QueryType(Enum):
    """Types of queries the orchestrator can handle"""
    PLAYER_ANALYSIS = "player_analysis"
    TEAM_PERFORMANCE = "team_performance"
    GAME_ANALYSIS = "game_analysis"
    MATCHUP_COMPARISON = "matchup_comparison"
    TACTICAL_ANALYSIS = "tactical_analysis"
    STATISTICAL_QUERY = "statistical_query"
    GENERAL_HOCKEY = "general_hockey"

class ToolType(Enum):
    """Available tools in the orchestrator"""
    VECTOR_SEARCH = "vector_search"
    PARQUET_QUERY = "parquet_query"
    CALCULATE_METRICS = "calculate_metrics"
    MATCHUP_ANALYSIS = "matchup_analysis"
    VISUALIZATION = "visualization"

@dataclass
class UserContext:
    """User context for identity-aware processing"""
    user_id: str
    role: UserRole
    name: str = ""
    team_access: List[str] = field(default_factory=lambda: ["MTL"])
    session_id: str = ""
    preferences: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ToolResult:
    """Result from a tool execution"""
    tool_type: ToolType
    success: bool
    data: Any = None
    error: Optional[str] = None
    execution_time_ms: int = 0
    citations: List[str] = field(default_factory=list)

class AgentState(TypedDict):
    """
    State structure for the LangGraph orchestrator.
    
    This represents the complete state that flows through all nodes
    in the orchestrator workflow.
    """
    # User context and query
    user_context: UserContext
    original_query: str
    query_type: QueryType
    
    # Processing state
    current_step: str
    iteration_count: int
    
    # Analysis and routing
    intent_analysis: Dict[str, Any]
    required_tools: List[ToolType]
    tool_sequence: List[str]
    
    # Tool execution results
    tool_results: Annotated[List[ToolResult], operator.add]
    
    # Data and context
    retrieved_context: List[Dict[str, Any]]
    analytics_data: Dict[str, Any]
    
    # Response generation
    evidence_chain: List[str]
    response_draft: str
    final_response: str
    
    # Metadata
    processing_time_ms: int
    error_messages: Annotated[List[str], operator.add]
    debug_info: Dict[str, Any]

def create_initial_state(
    user_context: UserContext,
    query: str,
    query_type: Optional[QueryType] = None
) -> AgentState:
    """Create initial state for a new orchestrator workflow"""
    
    return AgentState(
        # User and query
        user_context=user_context,
        original_query=query,
        query_type=query_type or QueryType.GENERAL_HOCKEY,
        
        # Processing
        current_step="intent_analysis",
        iteration_count=0,
        
        # Analysis
        intent_analysis={},
        required_tools=[],
        tool_sequence=[],
        
        # Results
        tool_results=[],
        
        # Data
        retrieved_context=[],
        analytics_data={},
        
        # Response
        evidence_chain=[],
        response_draft="",
        final_response="",
        
        # Metadata
        processing_time_ms=0,
        error_messages=[],
        debug_info={
            "start_time": datetime.now().isoformat(),
            "workflow_version": "1.0"
        }
    )

def update_state_step(state: AgentState, step_name: str) -> AgentState:
    """Update the current processing step"""
    state["current_step"] = step_name
    state["iteration_count"] += 1
    return state

def add_tool_result(state: AgentState, result: ToolResult) -> AgentState:
    """Add a tool execution result to the state"""
    state["tool_results"].append(result)
    
    # Update evidence chain if citations are available
    if result.citations:
        state["evidence_chain"].extend(result.citations)
    
    return state

def add_error(state: AgentState, error: str) -> AgentState:
    """Add an error message to the state"""
    state["error_messages"].append(f"[{datetime.now().isoformat()}] {error}")
    return state

def get_latest_tool_result(state: AgentState, tool_type: ToolType) -> Optional[ToolResult]:
    """Get the most recent result for a specific tool type"""
    for result in reversed(state["tool_results"]):
        if result.tool_type == tool_type:
            return result
    return None

def has_required_data(state: AgentState) -> bool:
    """Check if we have sufficient data to generate a response"""
    return (
        len(state["retrieved_context"]) > 0 or 
        len(state["analytics_data"]) > 0 or 
        any(result.success for result in state["tool_results"])
    )

def should_continue_processing(state: AgentState, max_iterations: int = 10) -> bool:
    """Determine if processing should continue"""
    return (
        state["iteration_count"] < max_iterations and
        len(state["error_messages"]) < 3 and
        state["final_response"] == ""
    )
