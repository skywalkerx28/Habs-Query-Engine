"""
HeartBeat Engine - Main LangGraph Orchestrator
Montreal Canadiens Advanced Analytics Assistant

Core orchestrator that coordinates between fine-tuned DeepSeek model,
Pinecone RAG, and Parquet analytics tools.
"""

from typing import Dict, Any, List, Optional
import asyncio
import logging
from datetime import datetime

from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage

from orchestrator.utils.state import (
    AgentState, 
    create_initial_state, 
    update_state_step,
    should_continue_processing,
    UserContext,
    QueryType,
    ToolType
)
from orchestrator.config.settings import settings
from orchestrator.nodes.intent_analyzer import IntentAnalyzerNode
from orchestrator.nodes.router import RouterNode
from orchestrator.nodes.pinecone_retriever import PineconeRetrieverNode
from orchestrator.nodes.parquet_analyzer import ParquetAnalyzerNode
from orchestrator.nodes.clip_retriever import ClipRetrieverNode
from orchestrator.nodes.response_synthesizer import ResponseSynthesizerNode

logger = logging.getLogger(__name__)

class HeartBeatOrchestrator:
    """
    Main orchestrator for the HeartBeat Engine.
    
    Coordinates between:
    - Fine-tuned DeepSeek model (central reasoning)
    - Pinecone vector search (hockey context/rules)
    - Parquet analytics (real-time stats/metrics)
    """
    
    def __init__(self):
        self.graph = None
        self._build_workflow()
    
    def _build_workflow(self) -> None:
        """Build the LangGraph workflow"""
        
        # Initialize workflow
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("intent_analysis", self._intent_analysis_node)
        workflow.add_node("router", self._router_node)
        workflow.add_node("pinecone_retrieval", self._pinecone_retrieval_node)
        workflow.add_node("parquet_analysis", self._parquet_analysis_node)
        workflow.add_node("clip_retrieval", self._clip_retrieval_node)
        workflow.add_node("response_synthesis", self._response_synthesis_node)
        
        # Define entry point
        workflow.set_entry_point("intent_analysis")
        
        # Add edges (workflow routing)
        workflow.add_edge("intent_analysis", "router")
        
        # Conditional routing from router
        workflow.add_conditional_edges(
            "router",
            self._route_decision,
            {
                "pinecone": "pinecone_retrieval",
                "parquet": "parquet_analysis", 
                "clips": "clip_retrieval",
                "both": "pinecone_retrieval",  # Start with pinecone, then parquet
                "clips_and_data": "clip_retrieval",  # Start with clips, then data
                "synthesis": "response_synthesis"
            }
        )
        
        # From pinecone to parquet (if both needed)
        workflow.add_conditional_edges(
            "pinecone_retrieval",
            self._after_pinecone_decision,
            {
                "parquet": "parquet_analysis",
                "synthesis": "response_synthesis"
            }
        )
        
        # From parquet to synthesis
        workflow.add_edge("parquet_analysis", "response_synthesis")
        
        # From clip retrieval - conditional routing
        workflow.add_conditional_edges(
            "clip_retrieval",
            self._after_clip_decision,
            {
                "parquet": "parquet_analysis",
                "pinecone": "pinecone_retrieval",
                "synthesis": "response_synthesis"
            }
        )
        
        # End at synthesis
        workflow.add_edge("response_synthesis", END)
        
        # Compile the graph
        self.graph = workflow.compile()
        
        logger.info("HeartBeat orchestrator workflow compiled successfully")
    
    async def process_query(
        self, 
        query: str, 
        user_context: UserContext,
        query_type: Optional[QueryType] = None
    ) -> Dict[str, Any]:
        """
        Process a user query through the complete orchestrator workflow.
        
        Args:
            query: User's hockey analytics query
            user_context: User identity and permissions
            query_type: Optional hint about query type
            
        Returns:
            Complete response with data, citations, and metadata
        """
        
        start_time = datetime.now()
        
        try:
            # Create initial state
            initial_state = create_initial_state(user_context, query, query_type)
            
            logger.info(f"Processing query for {user_context.role.value}: {query[:100]}...")
            
            # Execute the workflow
            result = await self.graph.ainvoke(initial_state)
            
            # Calculate processing time
            processing_time = (datetime.now() - start_time).total_seconds() * 1000
            result["processing_time_ms"] = int(processing_time)
            
            # Format final response
            response = {
                "response": result["final_response"],
                "query_type": result["query_type"].value,
                "evidence_chain": result["evidence_chain"],
                "tool_results": [
                    {
                        "tool": r.tool_type.value,
                        "success": r.success,
                        "data": r.data,
                        "processing_time_ms": r.execution_time_ms,
                        "citations": r.citations,
                        "error": r.error
                    } for r in result["tool_results"]
                ],
                "processing_time_ms": result["processing_time_ms"],
                "user_role": user_context.role.value,
                "errors": result["error_messages"]
            }
            
            logger.info(f"Query processed successfully in {processing_time:.0f}ms")
            return response
            
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            return {
                "response": "I apologize, but I encountered an error processing your request. Please try again or rephrase your question.",
                "error": str(e),
                "processing_time_ms": int((datetime.now() - start_time).total_seconds() * 1000),
                "success": False
            }
    
    def _intent_analysis_node(self, state: AgentState) -> AgentState:
        """Analyze user intent and classify query type"""
        node = IntentAnalyzerNode()
        return node.process(state)
    
    def _router_node(self, state: AgentState) -> AgentState:
        """Route to appropriate tools based on intent analysis"""
        node = RouterNode()
        return node.process(state)
    
    async def _pinecone_retrieval_node(self, state: AgentState) -> AgentState:
        """Retrieve relevant hockey context from Pinecone"""
        node = PineconeRetrieverNode()
        return await node.process(state)
    
    async def _parquet_analysis_node(self, state: AgentState) -> AgentState:
        """Analyze data using Parquet analytics tools"""
        node = ParquetAnalyzerNode()
        return await node.process(state)
    
    async def _clip_retrieval_node(self, state: AgentState) -> AgentState:
        """Retrieve video clips based on query parameters"""
        node = ClipRetrieverNode()
        return await node.process(state)
    
    async def _response_synthesis_node(self, state: AgentState) -> AgentState:
        """Synthesize final response using fine-tuned model"""
        node = ResponseSynthesizerNode()
        return await node.process(state)
    
    def _route_decision(self, state: AgentState) -> str:
        """Decide which tools to use based on router analysis"""
        required_tools = state["required_tools"]
        
        has_pinecone = ToolType.VECTOR_SEARCH in required_tools
        has_parquet = any(t in required_tools for t in [
            ToolType.PARQUET_QUERY, 
            ToolType.CALCULATE_METRICS,
            ToolType.MATCHUP_ANALYSIS
        ])
        has_clips = ToolType.CLIP_RETRIEVAL in required_tools
        
        # Prioritize clip retrieval if requested
        if has_clips and (has_pinecone or has_parquet):
            return "clips_and_data"
        elif has_clips:
            return "clips"
        elif has_pinecone and has_parquet:
            return "both"
        elif has_pinecone:
            return "pinecone"
        elif has_parquet:
            return "parquet"
        else:
            return "synthesis"  # Direct to response if no tools needed
    
    def _after_pinecone_decision(self, state: AgentState) -> str:
        """Decide next step after Pinecone retrieval"""
        required_tools = state["required_tools"]
        
        needs_parquet = any(t in required_tools for t in [
            ToolType.PARQUET_QUERY,
            ToolType.CALCULATE_METRICS, 
            ToolType.MATCHUP_ANALYSIS
        ])
        
        return "parquet" if needs_parquet else "synthesis"
    
    def _after_clip_decision(self, state: AgentState) -> str:
        """Decide next step after Clip retrieval"""
        required_tools = state["required_tools"]
        
        needs_parquet = any(t in required_tools for t in [
            ToolType.PARQUET_QUERY,
            ToolType.CALCULATE_METRICS, 
            ToolType.MATCHUP_ANALYSIS
        ])
        
        needs_pinecone = ToolType.VECTOR_SEARCH in required_tools
        
        if needs_parquet:
            return "parquet"
        elif needs_pinecone:
            return "pinecone"
        else:
            return "synthesis"

# Global orchestrator instance
orchestrator = HeartBeatOrchestrator()
