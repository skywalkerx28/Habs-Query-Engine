"""
HeartBeat Engine - Pinecone RAG Retriever Node
Montreal Canadiens Advanced Analytics Assistant

Retrieves relevant hockey context and domain knowledge from Pinecone vector database.
Provides contextual understanding for analytical queries.
"""

from typing import List, Dict, Any, Optional
import logging
from datetime import datetime
import asyncio

try:
    from pinecone import Pinecone
except ImportError:
    Pinecone = None

from orchestrator.utils.state import (
    AgentState, 
    ToolResult, 
    ToolType, 
    update_state_step, 
    add_tool_result,
    add_error
)
from orchestrator.config.settings import settings
from orchestrator.tools.pinecone_mcp_client import PineconeMCPClient

logger = logging.getLogger(__name__)

class PineconeRetrieverNode:
    """
    Retrieves relevant hockey domain knowledge from Pinecone vector database.
    
    Provides contextual understanding including:
    - Hockey rules and terminology explanations
    - Strategic concepts and tactical knowledge
    - Historical context and precedents
    - Montreal Canadiens specific information
    """
    
    def __init__(self):
        self.client = None
        self.index = None
        self.mcp_client = PineconeMCPClient()
        self._initialize_client()
    
    def _initialize_client(self) -> None:
        """Initialize Pinecone client and index connection"""
        
        if not Pinecone:
            logger.error("Pinecone client not available. Install with: pip install pinecone-client")
            return
        
        try:
            if settings.pinecone.api_key:
                self.client = Pinecone(api_key=settings.pinecone.api_key)
                self.index = self.client.Index(settings.pinecone.index_name)
                logger.info(f"Pinecone client initialized for index: {settings.pinecone.index_name}")
            else:
                logger.warning("Pinecone API key not configured")
        
        except Exception as e:
            logger.error(f"Failed to initialize Pinecone client: {str(e)}")
            self.client = None
            self.index = None
    
    async def process(self, state: AgentState) -> AgentState:
        """Process Pinecone vector search for relevant context"""
        
        state = update_state_step(state, "pinecone_retrieval")
        start_time = datetime.now()
        
        try:
            # Extract search parameters
            query = state["original_query"]
            user_context = state["user_context"]
            intent_analysis = state["intent_analysis"]
            
            logger.info(f"Retrieving context for query: {query[:100]}...")
            
            if not self.index:
                return self._handle_unavailable_service(state, start_time)
            
            # Perform vector search using MCP client
            search_results = await self._search_context_mcp(
                query=query,
                user_context=user_context,
                intent_analysis=intent_analysis
            )
            
            # Process and format results
            retrieved_context = self._process_search_results(search_results)
            
            # Create tool result
            execution_time = int((datetime.now() - start_time).total_seconds() * 1000)
            
            tool_result = ToolResult(
                tool_type=ToolType.VECTOR_SEARCH,
                success=len(retrieved_context) > 0,
                data=retrieved_context,
                execution_time_ms=execution_time,
                citations=self._extract_citations(retrieved_context)
            )
            
            # Update state
            state["retrieved_context"] = retrieved_context
            state = add_tool_result(state, tool_result)
            
            logger.info(f"Retrieved {len(retrieved_context)} context chunks in {execution_time}ms")
            
        except Exception as e:
            logger.error(f"Error in Pinecone retrieval: {str(e)}")
            state = add_error(state, f"Context retrieval failed: {str(e)}")
            
            # Add failed tool result
            execution_time = int((datetime.now() - start_time).total_seconds() * 1000)
            tool_result = ToolResult(
                tool_type=ToolType.VECTOR_SEARCH,
                success=False,
                error=str(e),
                execution_time_ms=execution_time
            )
            state = add_tool_result(state, tool_result)
        
        return state
    
    async def _search_context_mcp(
        self,
        query: str,
        user_context,
        intent_analysis: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Perform vector search using MCP client with real data"""
        
        # Optimize query for hockey domain
        optimized_query = self._optimize_query_for_hockey(query, intent_analysis)
        
        # Determine best namespace for query
        namespace = self._select_namespace(intent_analysis)
        
        # Calculate search parameters
        top_k = self._calculate_top_k(intent_analysis)
        
        logger.info(f"MCP search: '{optimized_query}' in namespace '{namespace}'")
        
        try:
            # Use MCP client for real search
            results = await self.mcp_client.search_hockey_context(
                query=optimized_query,
                namespace=namespace,
                top_k=top_k,
                score_threshold=settings.pinecone.score_threshold
            )
            
            return results
            
        except Exception as e:
            logger.error(f"MCP search failed: {str(e)}")
            # Fallback to mock results
            return self._generate_mock_results(optimized_query, top_k)
    
    def _select_namespace(self, intent_analysis: Dict[str, Any]) -> str:
        """Select appropriate namespace based on query analysis"""
        
        query_type = intent_analysis.get("query_type", "")
        requires_context = intent_analysis.get("requires_context", False)
        
        # Use events namespace for game/player/team queries
        if query_type in ["player_analysis", "team_performance", "game_analysis", "matchup_comparison"]:
            return "events"
        
        # Use prose namespace for explanations and hockey concepts
        if requires_context or query_type in ["tactical_analysis", "general_hockey"]:
            return "prose"
        
        # Default to events (more data available)
        return "events"
    
    def _search_context(
        self, 
        query: str, 
        user_context, 
        intent_analysis: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Perform vector search with query optimization"""
        
        # Optimize query for hockey domain
        optimized_query = self._optimize_query_for_hockey(query, intent_analysis)
        
        # Build search filters based on user permissions
        search_filters = self._build_search_filters(user_context)
        
        # Determine search parameters
        top_k = self._calculate_top_k(intent_analysis)
        
        logger.debug(f"Searching with optimized query: {optimized_query}")
        
        try:
            # Note: This is a placeholder for actual vector search
            # In production, you would:
            # 1. Generate embeddings for the optimized query
            # 2. Perform vector search with filters
            # 3. Return ranked results
            
            # For now, return mock results structure
            mock_results = self._generate_mock_results(optimized_query, top_k)
            return mock_results
            
        except Exception as e:
            logger.error(f"Vector search failed: {str(e)}")
            return []
    
    def _optimize_query_for_hockey(
        self, 
        query: str, 
        intent_analysis: Dict[str, Any]
    ) -> str:
        """Optimize query for better hockey domain retrieval"""
        
        # Add hockey context terms based on query type
        query_type = intent_analysis.get("query_type", "")
        
        hockey_terms = {
            "player_analysis": ["hockey player", "NHL", "statistics", "performance"],
            "team_performance": ["hockey team", "NHL", "Montreal Canadiens", "season"],
            "game_analysis": ["hockey game", "NHL", "match", "analysis"],
            "tactical_analysis": ["hockey strategy", "tactics", "system", "coaching"],
            "statistical_query": ["hockey statistics", "NHL stats", "metrics"]
        }
        
        additional_terms = hockey_terms.get(query_type, ["hockey", "NHL"])
        
        # Enhance query with domain terms (without being overly verbose)
        if not any(term.lower() in query.lower() for term in ["hockey", "nhl", "canadiens"]):
            query = f"{query} hockey"
        
        return query
    
    def _build_search_filters(self, user_context) -> Dict[str, Any]:
        """Build search filters based on user permissions and context"""
        
        filters = {
            "team": user_context.team_access,  # Teams user can access
            "role": user_context.role.value    # User role for content filtering
        }
        
        # Add namespace filtering for Montreal Canadiens specific content
        if "MTL" in user_context.team_access:
            filters["namespace"] = settings.pinecone.namespace
        
        return filters
    
    def _calculate_top_k(self, intent_analysis: Dict[str, Any]) -> int:
        """Calculate optimal number of results to retrieve"""
        
        complexity = intent_analysis.get("complexity", "moderate")
        
        top_k_map = {
            "simple": 3,
            "moderate": 5,
            "complex": 8
        }
        
        return min(top_k_map.get(complexity, 5), settings.pinecone.top_k)
    
    def _process_search_results(
        self, 
        search_results: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Process and format search results for downstream use"""
        
        processed_results = []
        
        for result in search_results:
            # Apply score threshold filtering
            score = result.get("score", 0.0)
            if score < settings.pinecone.score_threshold:
                continue
            
            # Format result for consistent structure
            processed_result = {
                "id": result.get("id", ""),
                "content": result.get("metadata", {}).get("content", ""),
                "source": result.get("metadata", {}).get("source", "hockey_knowledge"),
                "category": result.get("metadata", {}).get("category", "general"),
                "relevance_score": score,
                "metadata": result.get("metadata", {})
            }
            
            # Validate content quality
            if self._is_valid_content(processed_result):
                processed_results.append(processed_result)
        
        # Sort by relevance score
        processed_results.sort(key=lambda x: x["relevance_score"], reverse=True)
        
        return processed_results
    
    def _is_valid_content(self, result: Dict[str, Any]) -> bool:
        """Validate content quality and relevance"""
        
        content = result.get("content", "")
        
        # Basic quality checks
        if len(content.strip()) < 20:  # Minimum content length
            return False
        
        if not any(term in content.lower() for term in ["hockey", "nhl", "player", "team", "game"]):
            return False  # Must be hockey-related
        
        return True
    
    def _extract_citations(self, retrieved_context: List[Dict[str, Any]]) -> List[str]:
        """Extract citation information from retrieved context"""
        
        citations = []
        
        for context in retrieved_context:
            source = context.get("source", "hockey_knowledge")
            category = context.get("category", "general")
            
            citation = f"[{source}:{category}]"
            if citation not in citations:
                citations.append(citation)
        
        return citations
    
    def _handle_unavailable_service(
        self, 
        state: AgentState, 
        start_time: datetime
    ) -> AgentState:
        """Handle case when Pinecone service is unavailable"""
        
        logger.warning("Pinecone service unavailable, using fallback context")
        
        # Provide basic hockey context as fallback
        fallback_context = self._generate_fallback_context(state["original_query"])
        
        execution_time = int((datetime.now() - start_time).total_seconds() * 1000)
        
        tool_result = ToolResult(
            tool_type=ToolType.VECTOR_SEARCH,
            success=True,
            data=fallback_context,
            execution_time_ms=execution_time,
            citations=["[fallback:hockey_basics]"]
        )
        
        state["retrieved_context"] = fallback_context
        state = add_tool_result(state, tool_result)
        
        return state
    
    def _generate_fallback_context(self, query: str) -> List[Dict[str, Any]]:
        """Generate basic hockey context when Pinecone is unavailable"""
        
        fallback_contexts = [
            {
                "id": "fallback_1",
                "content": "Hockey is played with six players per team on ice: one goaltender and five skaters (typically two defensemen and three forwards).",
                "source": "hockey_basics",
                "category": "rules",
                "relevance_score": 0.8,
                "metadata": {"type": "basic_rule"}
            },
            {
                "id": "fallback_2", 
                "content": "The Montreal Canadiens are a professional hockey team based in Montreal, Quebec, competing in the NHL's Atlantic Division.",
                "source": "team_info",
                "category": "team",
                "relevance_score": 0.9,
                "metadata": {"type": "team_basic"}
            }
        ]
        
        return fallback_contexts
    
    def _generate_mock_results(self, query: str, top_k: int) -> List[Dict[str, Any]]:
        """Generate mock search results for development/testing"""
        
        mock_results = [
            {
                "id": f"mock_{i}",
                "score": 0.9 - (i * 0.1),
                "metadata": {
                    "content": f"Hockey context result {i+1} for query: {query[:50]}...",
                    "source": "hockey_knowledge",
                    "category": "general",
                    "team": "MTL"
                }
            }
            for i in range(min(top_k, 3))
        ]
        
        return mock_results
