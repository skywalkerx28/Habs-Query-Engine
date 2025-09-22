"""
HeartBeat Engine - Response Synthesizer Node
Montreal Canadiens Advanced Analytics Assistant

Synthesizes final responses using the fine-tuned Llama 3.3 70B model,
integrating RAG context and analytics data into coherent, evidence-based responses.
"""

from typing import Dict, List, Any, Optional
import logging
from datetime import datetime
import asyncio
import json

try:
    import openai
except ImportError:
    openai = None

from orchestrator.utils.state import (
    AgentState,
    ToolResult,
    ToolType,
    update_state_step,
    add_tool_result,
    add_error,
    has_required_data
)
from orchestrator.config.settings import settings, UserRole

logger = logging.getLogger(__name__)

class ResponseSynthesizerNode:
    """
    Synthesizes final responses using the fine-tuned Llama 3.3 70B model.
    
    Capabilities:
    - Integration of RAG context and analytics data
    - Role-appropriate response formatting
    - Evidence-based reasoning chains
    - Citation and source attribution
    - Montreal Canadiens specific terminology
    """
    
    def __init__(self):
        self.model_config = settings.model
        self.orchestration_config = settings.orchestration
        
        # Response templates by user role
        self.role_templates = {
            UserRole.COACH: {
                "system_prompt": "You are responding to a Montreal Canadiens coach. Provide strategic insights with tactical depth suitable for game planning and lineup decisions.",
                "style": "tactical_strategic",
                "focus": ["strategy", "matchups", "deployment", "adjustments"]
            },
            UserRole.PLAYER: {
                "system_prompt": "You are responding to a Montreal Canadiens player. Provide performance insights and actionable feedback for skill development.",
                "style": "performance_focused",
                "focus": ["individual_performance", "improvement", "comparisons", "goals"]
            },
            UserRole.ANALYST: {
                "system_prompt": "You are responding to a hockey analyst. Provide comprehensive data-driven insights with statistical depth and context.",
                "style": "analytical_comprehensive",
                "focus": ["statistics", "trends", "correlations", "predictions"]
            },
            UserRole.STAFF: {
                "system_prompt": "You are responding to Montreal Canadiens staff. Provide clear, accessible insights focused on team operations and player welfare.",
                "style": "operational_clear",
                "focus": ["team_operations", "player_welfare", "logistics", "communication"]
            },
            UserRole.SCOUT: {
                "system_prompt": "You are responding to a scout. Provide detailed player evaluation insights and comparative analysis for recruitment decisions.",
                "style": "evaluative_detailed",
                "focus": ["player_evaluation", "comparisons", "potential", "fit_assessment"]
            }
        }
    
    async def process(self, state: AgentState) -> AgentState:
        """Process response synthesis using fine-tuned model"""
        
        state = update_state_step(state, "response_synthesis")
        start_time = datetime.now()
        
        try:
            # Validate we have sufficient data for response
            if not has_required_data(state):
                return self._handle_insufficient_data(state, start_time)
            
            # Extract synthesis parameters
            user_context = state["user_context"]
            query = state["original_query"]
            retrieved_context = state.get("retrieved_context", [])
            analytics_data = state.get("analytics_data", {})
            tool_results = state.get("tool_results", [])
            
            logger.info(f"Synthesizing response for {user_context.role.value}: {query[:100]}...")
            
            # Build comprehensive prompt
            synthesis_prompt = self._build_synthesis_prompt(
                user_context=user_context,
                query=query,
                retrieved_context=retrieved_context,
                analytics_data=analytics_data,
                tool_results=tool_results
            )
            
            # Generate response using model
            response = await self._generate_response(synthesis_prompt, user_context)
            
            # Post-process and validate response
            final_response = self._post_process_response(
                response, state, user_context
            )
            
            # Calculate execution time
            execution_time = int((datetime.now() - start_time).total_seconds() * 1000)
            
            # Create tool result
            tool_result = ToolResult(
                tool_type=ToolType.PARQUET_QUERY,  # Represents synthesis
                success=len(final_response.strip()) > 0,
                data={"response": final_response, "word_count": len(final_response.split())},
                execution_time_ms=execution_time,
                citations=state.get("evidence_chain", [])
            )
            
            # Update state
            state["final_response"] = final_response
            state = add_tool_result(state, tool_result)
            
            logger.info(f"Response synthesis completed in {execution_time}ms ({len(final_response.split())} words)")
            
        except Exception as e:
            logger.error(f"Error in response synthesis: {str(e)}")
            state = add_error(state, f"Response synthesis failed: {str(e)}")
            
            # Provide fallback response
            state["final_response"] = self._generate_fallback_response(state)
            
            # Add failed tool result
            execution_time = int((datetime.now() - start_time).total_seconds() * 1000)
            tool_result = ToolResult(
                tool_type=ToolType.PARQUET_QUERY,
                success=False,
                error=str(e),
                execution_time_ms=execution_time
            )
            state = add_tool_result(state, tool_result)
        
        return state
    
    def _build_synthesis_prompt(
        self,
        user_context,
        query: str,
        retrieved_context: List[Dict[str, Any]],
        analytics_data: Dict[str, Any],
        tool_results: List[ToolResult]
    ) -> str:
        """Build comprehensive prompt for response synthesis"""
        
        role_config = self.role_templates.get(
            user_context.role, 
            self.role_templates[UserRole.STAFF]
        )
        
        # Build context sections
        context_section = self._format_retrieved_context(retrieved_context)
        analytics_section = self._format_analytics_data(analytics_data)
        evidence_section = self._format_evidence_chain(tool_results)
        
        # Construct synthesis prompt
        synthesis_prompt = f"""
{role_config['system_prompt']}

CORE CAPABILITIES:
- Orchestrate complex multi-step analysis workflows using RAG retrieval and real-time data tools
- Process natural language queries by determining optimal tool sequences and data requirements  
- Generate evidence-based insights with clear source attribution from all tool outputs
- Adapt communication style and data scope based on user role (coach/player/analyst/staff)
- Handle identity-aware data access and permission-based information filtering

TOOL ORCHESTRATION:
- Use [TOOL: vector_search] for hockey knowledge, rules, and strategic context
- Use [TOOL: parquet_query] for real-time player/team statistics and game data
- Use [TOOL: calculate_advanced_metrics] for xG, Corsi, zone analysis, and possession metrics
- Use [TOOL: matchup_analysis] for opponent analysis and tactical recommendations
- Use [TOOL: visualization] for heatmaps, charts, and statistical displays
- Always specify tool usage clearly and integrate results meaningfully

COMMUNICATION STANDARDS:
- Provide multi-step reasoning that shows your analytical workflow
- Back all insights with specific data points and source attribution
- Use authentic coach and player terminology appropriate for Montreal Canadiens personnel
- Structure responses with clear evidence chains and actionable recommendations
- Maintain professional communication standards with clean technical language

USER QUERY: {query}

RETRIEVED CONTEXT:
{context_section}

ANALYTICS DATA:
{analytics_section}

EVIDENCE CHAIN:
{evidence_section}

INSTRUCTIONS:
1. Analyze the user's query in the context of their role ({user_context.role.value})
2. Integrate the retrieved context and analytics data meaningfully
3. Provide a comprehensive response that demonstrates tool orchestration
4. Include clear source attribution for all claims and data points
5. Structure the response with evidence-based reasoning
6. Use appropriate Montreal Canadiens terminology and context
7. Ensure the response is actionable and role-appropriate

Generate a professional, evidence-based response that demonstrates sophisticated analytical orchestration:
"""
        
        return synthesis_prompt
    
    async def _generate_response(
        self, 
        synthesis_prompt: str, 
        user_context
    ) -> str:
        """Generate response using the fine-tuned model or fallback"""
        
        # Try primary model (SageMaker endpoint) first
        if self.model_config.primary_model_endpoint:
            try:
                return await self._call_sagemaker_endpoint(synthesis_prompt)
            except Exception as e:
                logger.warning(f"SageMaker endpoint failed, falling back: {str(e)}")
        
        # Fallback to OpenAI for development/testing
        if self.model_config.fallback_api_key and openai:
            try:
                return await self._call_openai_fallback(synthesis_prompt)
            except Exception as e:
                logger.warning(f"OpenAI fallback failed: {str(e)}")
        
        # Final fallback to template-based response
        return self._generate_template_response(synthesis_prompt, user_context)
    
    async def _call_sagemaker_endpoint(self, prompt: str) -> str:
        """Call the SageMaker endpoint for the fine-tuned model"""
        
        # This would implement actual SageMaker endpoint calling
        # For now, return a placeholder indicating the integration point
        
        logger.info("Calling SageMaker endpoint (placeholder)")
        
        # Simulate processing time
        await asyncio.sleep(0.1)
        
        return "SageMaker endpoint response placeholder - integrate with actual fine-tuned Llama 3.3 70B model"
    
    async def _call_openai_fallback(self, prompt: str) -> str:
        """Call OpenAI API as fallback during development"""
        
        if not openai:
            raise Exception("OpenAI library not available")
        
        try:
            client = openai.AsyncOpenAI(api_key=self.model_config.fallback_api_key)
            
            response = await client.chat.completions.create(
                model=self.model_config.fallback_model,
                messages=[
                    {"role": "system", "content": "You are an elite hockey analytics assistant for the Montreal Canadiens."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.model_config.temperature,
                max_tokens=self.model_config.max_tokens,
                top_p=self.model_config.top_p
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"OpenAI API call failed: {str(e)}")
            raise
    
    def _generate_template_response(
        self, 
        synthesis_prompt: str, 
        user_context
    ) -> str:
        """Generate template-based response as final fallback"""
        
        role_config = self.role_templates.get(
            user_context.role,
            self.role_templates[UserRole.STAFF]
        )
        
        template_response = f"""
I understand you're asking about hockey analytics from a {user_context.role.value} perspective. 

Based on the available data and context, I can provide insights focused on {', '.join(role_config['focus'])}.

However, I'm currently operating in fallback mode. For the most comprehensive analysis with our fine-tuned Montreal Canadiens analytics model, please ensure:

1. The SageMaker endpoint is properly configured
2. All data sources are available
3. Network connectivity is established

I'm designed to provide sophisticated analysis combining:
- Hockey domain knowledge from our RAG system
- Real-time statistics from Parquet data files  
- Advanced metrics calculations
- Role-specific insights for Montreal Canadiens personnel

Please try your query again once the full system is available.
"""
        
        return template_response
    
    def _format_retrieved_context(
        self, 
        retrieved_context: List[Dict[str, Any]]
    ) -> str:
        """Format retrieved context for prompt integration"""
        
        if not retrieved_context:
            return "No specific hockey context retrieved."
        
        formatted_context = []
        
        for i, context in enumerate(retrieved_context[:3], 1):  # Limit to top 3
            content = context.get("content", "")
            source = context.get("source", "unknown")
            category = context.get("category", "general")
            
            formatted_context.append(
                f"{i}. [{source}:{category}] {content[:200]}..."
            )
        
        return "\n".join(formatted_context)
    
    def _format_analytics_data(self, analytics_data: Dict[str, Any]) -> str:
        """Format analytics data for prompt integration"""
        
        if not analytics_data:
            return "No analytics data available."
        
        analysis_type = analytics_data.get("analysis_type", "unknown")
        
        if "error" in analytics_data:
            return f"Analytics error: {analytics_data['error']}"
        
        # Format based on analysis type
        if analysis_type == "player_performance":
            return self._format_player_analytics(analytics_data)
        elif analysis_type == "team_performance":
            return self._format_team_analytics(analytics_data)
        else:
            return f"Analytics type: {analysis_type}\nData: {str(analytics_data)[:300]}..."
    
    def _format_player_analytics(self, data: Dict[str, Any]) -> str:
        """Format player analytics data"""
        
        players = data.get("players", [])
        metrics = data.get("metrics", {})
        
        formatted = f"Player Analysis: {', '.join(players)}\n"
        
        for player, stats in metrics.items():
            formatted += f"- {player}: {stats.get('points', 0)} points in {stats.get('games_played', 0)} games\n"
        
        return formatted
    
    def _format_team_analytics(self, data: Dict[str, Any]) -> str:
        """Format team analytics data"""
        
        team = data.get("team", "MTL")
        metrics = data.get("metrics", {})
        
        record = metrics.get("record", {})
        formatted = f"Team Analysis: {team}\n"
        formatted += f"- Record: {record.get('wins', 0)}-{record.get('losses', 0)}-{record.get('overtime', 0)}\n"
        formatted += f"- Goals For/Against: {metrics.get('goals_for', 0)}/{metrics.get('goals_against', 0)}\n"
        
        return formatted
    
    def _format_evidence_chain(self, tool_results: List[ToolResult]) -> str:
        """Format evidence chain from tool results"""
        
        if not tool_results:
            return "No evidence chain available."
        
        evidence_items = []
        
        for result in tool_results:
            if result.success and result.citations:
                evidence_items.extend(result.citations)
        
        if evidence_items:
            return "Evidence sources: " + ", ".join(set(evidence_items))
        else:
            return "Evidence chain in development."
    
    def _post_process_response(
        self, 
        response: str, 
        state: AgentState, 
        user_context
    ) -> str:
        """Post-process and validate the generated response"""
        
        # Ensure response length is appropriate
        if len(response) > self.orchestration_config.max_response_length:
            response = response[:self.orchestration_config.max_response_length] + "..."
        
        # Add citations if required and available
        if self.orchestration_config.require_citations:
            citations = state.get("evidence_chain", [])
            if citations and not any(cite in response for cite in citations):
                response += f"\n\nSources: {', '.join(set(citations))}"
        
        return response.strip()
    
    def _handle_insufficient_data(
        self, 
        state: AgentState, 
        start_time: datetime
    ) -> AgentState:
        """Handle case when insufficient data is available"""
        
        logger.warning("Insufficient data for response synthesis")
        
        fallback_response = """
I apologize, but I don't have sufficient data to provide a comprehensive analysis for your query. 

This could be due to:
- Data sources being temporarily unavailable
- Query requiring data outside my current scope
- Network connectivity issues

Please try rephrasing your question or check back shortly. I'm designed to provide detailed hockey analytics combining contextual knowledge with real-time statistics.
"""
        
        execution_time = int((datetime.now() - start_time).total_seconds() * 1000)
        
        tool_result = ToolResult(
            tool_type=ToolType.PARQUET_QUERY,
            success=False,
            error="Insufficient data for synthesis",
            execution_time_ms=execution_time
        )
        
        state["final_response"] = fallback_response
        state = add_tool_result(state, tool_result)
        
        return state
    
    def _generate_fallback_response(self, state: AgentState) -> str:
        """Generate a fallback response when synthesis fails"""
        
        query = state.get("original_query", "your query")
        
        return f"""
I encountered an issue processing your request about "{query[:100]}...". 

I'm designed to provide comprehensive hockey analytics by combining:
- Domain expertise from hockey knowledge base
- Real-time statistics and performance data
- Advanced metrics and comparative analysis

Please try your question again, or contact support if the issue persists.
"""
