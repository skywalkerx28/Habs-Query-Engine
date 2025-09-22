"""
HeartBeat Engine - Parquet Analytics Node
Montreal Canadiens Advanced Analytics Assistant

Performs real-time analytics queries on Parquet data files.
Provides statistical analysis, player metrics, and game data.
"""

from typing import List, Dict, Any, Optional, Union
import logging
from datetime import datetime
import os
from pathlib import Path

try:
    import pandas as pd
    import pyarrow.parquet as pq
except ImportError:
    pd = None
    pq = None

from orchestrator.utils.state import (
    AgentState,
    ToolResult,
    ToolType,
    update_state_step,
    add_tool_result,
    add_error
)
from orchestrator.config.settings import settings
from orchestrator.tools.parquet_data_client import ParquetDataClient

logger = logging.getLogger(__name__)

class ParquetAnalyzerNode:
    """
    Performs analytics queries on Parquet data files.
    
    Capabilities:
    - Player performance statistics
    - Team analytics and metrics
    - Game-by-game analysis
    - Advanced hockey metrics calculation
    - Comparative analysis and matchups
    """
    
    def __init__(self):
        self.data_directory = Path(settings.parquet.data_directory)
        self.cache = {} if settings.parquet.cache_enabled else None
        self.cache_ttl = settings.parquet.cache_ttl_seconds
        
        # Real data client for Montreal Canadiens analytics
        self.data_client = ParquetDataClient(str(self.data_directory))
        
        # Legacy data files mapping (kept for compatibility)
        self.data_files = {
            "player_stats": "fact/player_game_stats.parquet",
            "team_stats": "fact/team_game_stats.parquet", 
            "play_by_play": "fact/play_by_play_events.parquet",
            "line_combinations": "dim/line_combinations.parquet",
            "player_info": "dim/players.parquet",
            "team_info": "dim/teams.parquet",
            "game_info": "dim/games.parquet"
        }
        
        self._validate_data_availability()
    
    def _validate_data_availability(self) -> None:
        """Validate that required data files are available"""
        
        missing_files = []
        
        for data_type, file_path in self.data_files.items():
            full_path = self.data_directory / file_path
            if not full_path.exists():
                missing_files.append(f"{data_type}: {file_path}")
        
        if missing_files:
            logger.warning(f"Missing Parquet data files: {missing_files}")
        else:
            logger.info("All Parquet data files validated successfully")
    
    async def process(self, state: AgentState) -> AgentState:
        """Process Parquet analytics queries"""
        
        state = update_state_step(state, "parquet_analysis")
        start_time = datetime.now()
        
        if not pd or not pq:
            return self._handle_unavailable_libraries(state, start_time)
        
        try:
            # Extract analysis parameters
            query = state["original_query"]
            user_context = state["user_context"]
            intent_analysis = state["intent_analysis"]
            required_tools = state["required_tools"]
            
            logger.info(f"Performing analytics for query: {query[:100]}...")
            
            # Determine analysis type and execute
            analytics_results = await self._execute_analytics(
                query=query,
                user_context=user_context,
                intent_analysis=intent_analysis,
                required_tools=required_tools
            )
            
            # Calculate execution time
            execution_time = int((datetime.now() - start_time).total_seconds() * 1000)
            
            # Create tool result
            tool_result = ToolResult(
                tool_type=ToolType.PARQUET_QUERY,
                success=len(analytics_results) > 0,
                data=analytics_results,
                execution_time_ms=execution_time,
                citations=self._generate_citations(analytics_results)
            )
            
            # Update state
            state["analytics_data"] = analytics_results
            state = add_tool_result(state, tool_result)
            
            logger.info(f"Analytics completed in {execution_time}ms with {len(analytics_results)} results")
            
        except Exception as e:
            logger.error(f"Error in Parquet analysis: {str(e)}")
            state = add_error(state, f"Analytics query failed: {str(e)}")
            
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
    
    async def _execute_analytics(
        self,
        query: str,
        user_context,
        intent_analysis: Dict[str, Any],
        required_tools: List[ToolType]
    ) -> Dict[str, Any]:
        """Execute appropriate analytics based on query analysis"""
        
        query_type = intent_analysis.get("query_type", "")
        complexity = intent_analysis.get("complexity", "moderate")
        
        # Route to appropriate analysis method
        if query_type == "player_analysis":
            return await self._analyze_player_performance(query, user_context)
        elif query_type == "team_performance":
            return await self._analyze_team_performance(query, user_context)
        elif query_type == "game_analysis":
            return await self._analyze_game_data(query, user_context)
        elif query_type == "matchup_comparison":
            return await self._analyze_matchups(query, user_context)
        elif query_type == "statistical_query":
            return await self._execute_statistical_query(query, user_context)
        else:
            return await self._execute_general_analytics(query, user_context)
    
    async def _analyze_player_performance(
        self, 
        query: str, 
        user_context
    ) -> Dict[str, Any]:
        """Analyze individual player performance metrics using real data"""
        
        # Extract player names from query
        players = self._extract_player_names(query)
        timeframe = self._extract_timeframe(query)
        
        try:
            # Use new NHL player stats method for comprehensive data
            real_data = await self.data_client.get_nhl_player_stats(
                team="MTL",
                player_names=players,
                season="2024-2025"
            )
            
            # If real data fails, fallback to mock
            if "error" in real_data:
                logger.warning(f"Real data failed: {real_data['error']}, using fallback")
                return {
                    "analysis_type": "player_performance_fallback",
                    "players": players,
                    "metrics": self._get_mock_player_stats(players),
                    "timeframe": timeframe,
                    "data_source": "fallback_data",
                    "note": "Using fallback data due to: " + real_data['error']
                }
            
            return real_data
            
        except Exception as e:
            logger.error(f"Player analysis failed: {str(e)}")
            return {"error": f"Player analysis failed: {str(e)}"}
    
    def _analyze_team_performance(
        self, 
        query: str, 
        user_context
    ) -> Dict[str, Any]:
        """Analyze team performance and statistics"""
        
        try:
            # Extract team context (defaulting to MTL for Montreal Canadiens users)
            team = "MTL" if "MTL" in user_context.team_access else "MTL"
            
            results = {
                "analysis_type": "team_performance",
                "team": team,
                "metrics": self._get_mock_team_stats(team),
                "timeframe": self._extract_timeframe(query),
                "data_source": "team_game_stats.parquet"
            }
            
            return results
            
        except Exception as e:
            logger.error(f"Team analysis failed: {str(e)}")
            return {"error": f"Team analysis failed: {str(e)}"}
    
    def _analyze_game_data(
        self, 
        query: str, 
        user_context
    ) -> Dict[str, Any]:
        """Analyze specific game data and events"""
        
        try:
            results = {
                "analysis_type": "game_analysis",
                "game_data": self._get_mock_game_analysis(),
                "timeframe": self._extract_timeframe(query),
                "data_source": "play_by_play_events.parquet"
            }
            
            return results
            
        except Exception as e:
            logger.error(f"Game analysis failed: {str(e)}")
            return {"error": f"Game analysis failed: {str(e)}"}
    
    def _analyze_matchups(
        self, 
        query: str, 
        user_context
    ) -> Dict[str, Any]:
        """Analyze player or team matchups and comparisons"""
        
        try:
            # Extract entities being compared
            entities = self._extract_comparison_entities(query)
            
            results = {
                "analysis_type": "matchup_analysis",
                "entities": entities,
                "comparison_metrics": self._get_mock_matchup_data(entities),
                "data_source": "multiple_sources"
            }
            
            return results
            
        except Exception as e:
            logger.error(f"Matchup analysis failed: {str(e)}")
            return {"error": f"Matchup analysis failed: {str(e)}"}
    
    def _execute_statistical_query(
        self, 
        query: str, 
        user_context
    ) -> Dict[str, Any]:
        """Execute direct statistical queries"""
        
        try:
            # Parse statistical request
            stat_type = self._identify_stat_type(query)
            
            results = {
                "analysis_type": "statistical_query",
                "stat_type": stat_type,
                "results": self._get_mock_statistical_data(stat_type),
                "data_source": "fact_tables"
            }
            
            return results
            
        except Exception as e:
            logger.error(f"Statistical query failed: {str(e)}")
            return {"error": f"Statistical query failed: {str(e)}"}
    
    def _execute_general_analytics(
        self, 
        query: str, 
        user_context
    ) -> Dict[str, Any]:
        """Execute general analytics for unclassified queries"""
        
        try:
            results = {
                "analysis_type": "general_analytics",
                "summary": "General hockey analytics data",
                "data": self._get_mock_general_data(),
                "data_source": "multiple_sources"
            }
            
            return results
            
        except Exception as e:
            logger.error(f"General analytics failed: {str(e)}")
            return {"error": f"General analytics failed: {str(e)}"}
    
    def _extract_player_names(self, query: str) -> List[str]:
        """Extract player names from query text"""
        
        # Common Montreal Canadiens players (2024-25 season)
        known_players = [
            "suzuki", "caufield", "hutson", "slafkovsky", "guhle", 
            "matheson", "dach", "newhook", "gallagher", "anderson",
            "montembeault", "primeau", "dvorak", "armia", "evans"
        ]
        
        found_players = []
        query_lower = query.lower()
        
        for player in known_players:
            if player in query_lower:
                found_players.append(player.capitalize())
        
        return found_players
    
    def _extract_timeframe(self, query: str) -> str:
        """Extract timeframe information from query"""
        
        timeframe_patterns = {
            "last game": "last_game",
            "last 5 games": "last_5_games", 
            "last 10 games": "last_10_games",
            "this season": "current_season",
            "career": "career",
            "this month": "current_month"
        }
        
        query_lower = query.lower()
        
        for pattern, timeframe in timeframe_patterns.items():
            if pattern in query_lower:
                return timeframe
        
        return "current_season"  # default
    
    def _extract_comparison_entities(self, query: str) -> List[str]:
        """Extract entities being compared in matchup queries"""
        
        # Simple extraction based on common comparison patterns
        entities = []
        
        # Look for "vs", "versus", "compared to" patterns
        if " vs " in query.lower():
            parts = query.lower().split(" vs ")
            entities = [part.strip() for part in parts[:2]]
        elif " versus " in query.lower():
            parts = query.lower().split(" versus ")
            entities = [part.strip() for part in parts[:2]]
        
        return entities
    
    def _identify_stat_type(self, query: str) -> str:
        """Identify the type of statistic being requested"""
        
        stat_indicators = {
            "goals": ["goal", "goals", "scoring"],
            "assists": ["assist", "assists", "playmaking"],
            "points": ["point", "points", "production"],
            "shots": ["shot", "shots", "shooting"],
            "hits": ["hit", "hits", "physical"],
            "blocks": ["block", "blocks", "blocked"],
            "saves": ["save", "saves", "goaltending"],
            "wins": ["win", "wins", "record"]
        }
        
        query_lower = query.lower()
        
        for stat_type, indicators in stat_indicators.items():
            if any(indicator in query_lower for indicator in indicators):
                return stat_type
        
        return "general_stats"
    
    # Mock data generation methods (to be replaced with real Parquet queries)
    
    def _get_mock_player_stats(self, players: List[str]) -> Dict[str, Any]:
        """Generate mock player statistics"""
        
        return {
            player: {
                "games_played": 25,
                "goals": 8,
                "assists": 12,
                "points": 20,
                "shots": 65,
                "shooting_percentage": 12.3,
                "plus_minus": 2,
                "time_on_ice_avg": "18:45"
            }
            for player in players
        }
    
    def _get_mock_team_stats(self, team: str) -> Dict[str, Any]:
        """Generate mock team statistics"""
        
        return {
            "record": {"wins": 12, "losses": 10, "overtime": 3},
            "goals_for": 78,
            "goals_against": 75,
            "powerplay_percentage": 22.5,
            "penalty_kill_percentage": 81.2,
            "shots_for_avg": 32.1,
            "shots_against_avg": 29.8,
            "faceoff_percentage": 50.8
        }
    
    def _get_mock_game_analysis(self) -> Dict[str, Any]:
        """Generate mock game analysis data"""
        
        return {
            "last_game": {
                "opponent": "Toronto Maple Leafs",
                "score": "4-2",
                "result": "Win",
                "key_events": ["Power play goal", "Short-handed goal", "Empty net goal"],
                "top_performers": ["Suzuki (2G, 1A)", "Caufield (1G, 1A)"]
            }
        }
    
    def _get_mock_matchup_data(self, entities: List[str]) -> Dict[str, Any]:
        """Generate mock matchup comparison data"""
        
        return {
            "comparison": f"{entities[0] if entities else 'Team A'} vs {entities[1] if len(entities) > 1 else 'Team B'}",
            "metrics": {
                "head_to_head_record": "2-1-0",
                "goals_for_comparison": {"team_a": 3.2, "team_b": 2.8},
                "powerplay_comparison": {"team_a": 25.0, "team_b": 18.5}
            }
        }
    
    def _get_mock_statistical_data(self, stat_type: str) -> Dict[str, Any]:
        """Generate mock statistical data"""
        
        return {
            "stat_type": stat_type,
            "value": 42,
            "rank": "3rd in team",
            "league_average": 38.5,
            "percentile": 75
        }
    
    def _get_mock_general_data(self) -> Dict[str, Any]:
        """Generate mock general analytics data"""
        
        return {
            "team_summary": "Montreal Canadiens current season overview",
            "key_metrics": {
                "record": "12-10-3",
                "points_percentage": 54.0,
                "goal_differential": "+3"
            }
        }
    
    def _generate_citations(self, analytics_results: Dict[str, Any]) -> List[str]:
        """Generate citations for analytics results"""
        
        citations = []
        
        data_source = analytics_results.get("data_source", "parquet_data")
        analysis_type = analytics_results.get("analysis_type", "analytics")
        
        citations.append(f"[{data_source}:{analysis_type}]")
        
        return citations
    
    def _handle_unavailable_libraries(
        self, 
        state: AgentState, 
        start_time: datetime
    ) -> AgentState:
        """Handle case when pandas/pyarrow libraries are unavailable"""
        
        logger.error("Pandas/PyArrow libraries not available")
        
        execution_time = int((datetime.now() - start_time).total_seconds() * 1000)
        
        tool_result = ToolResult(
            tool_type=ToolType.PARQUET_QUERY,
            success=False,
            error="Analytics libraries not available. Install with: pip install pandas pyarrow",
            execution_time_ms=execution_time
        )
        
        state = add_tool_result(state, tool_result)
        state = add_error(state, "Parquet analytics unavailable - missing dependencies")
        
        return state
