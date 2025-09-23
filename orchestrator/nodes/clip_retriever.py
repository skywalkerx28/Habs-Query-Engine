"""
HeartBeat Engine - Video Clip Retriever Node
Montreal Canadiens Advanced Analytics Assistant

Retrieves video clips based on natural language queries.
Provides player-specific highlights, game footage, and event clips.
Supports hockey-specific terminology: "shifts" = sequences of play/clips.
"""

from typing import List, Dict, Any, Optional
import logging
from datetime import datetime
import re
from pathlib import Path

from orchestrator.utils.state import (
    AgentState,
    ToolResult,
    ToolType,
    update_state_step,
    add_tool_result,
    add_error
)
from orchestrator.config.settings import settings
from orchestrator.models.clip_models import (
    ClipIndexManager,
    ClipSearchParams,
    ClipResult,
    ClipMetadata
)

logger = logging.getLogger(__name__)

class ClipRetrieverNode:
    """
    Retrieves video clips based on natural language queries.
    
    Capabilities:
    - Player-specific clip retrieval
    - Event-based clip filtering
    - Time-based clip searches
    - Game-specific highlights
    - Team-wide clip collections
    """
    
    def __init__(self):
        # Initialize clip index manager
        clips_base_path = getattr(settings, 'clips_base_path', 'data/clips')
        self.clip_index = ClipIndexManager(clips_base_path)
        
        # Cache for recent queries
        self.query_cache = {}
        self.cache_ttl = 300  # 5 minutes
        
        # Montreal Canadiens players for name matching
        self.mtl_players = {
            # Forwards
            'nick suzuki', 'cole caufield', 'juraj slafkovsky', 'kirby dach',
            'alex newhook', 'brendan gallagher', 'josh anderson', 'jake evans',
            'joel armia', 'christian dvorak', 'emil heineman', 'oliver kapanen',
            'owen beck', 'joshua roy', 'rafael harvey-pinard',
            
            # Defensemen
            'lane hutson', 'kaiden guhle', 'mike matheson', 'david savard',
            'arber xhekaj', 'jayden struble', 'justin barron', 'logan mailloux',
            'adam engstrom',
            
            # Goalies
            'samuel montembeault', 'cayden primeau', 'jakub dobes',
            
            # Common short names and nicknames
            'suzuki', 'caufield', 'slafkovsky', 'dach', 'hutson', 'guhle',
            'matheson', 'gallagher', 'anderson', 'montembeault', 'primeau'
        }
        
        # NHL opponents for filtering
        self.nhl_teams = {
            'toronto', 'boston', 'buffalo', 'ottawa', 'detroit', 'florida',
            'tampa bay', 'washington', 'carolina', 'columbus', 'pittsburgh',
            'philadelphia', 'new jersey', 'ny rangers', 'ny islanders',
            'colorado', 'vegas', 'minnesota', 'winnipeg', 'calgary',
            'edmonton', 'vancouver', 'seattle', 'anaheim', 'los angeles',
            'san jose', 'arizona', 'utah', 'st louis', 'chicago',
            'dallas', 'nashville'
        }
        
        self._validate_clips_directory()
    
    def _validate_clips_directory(self) -> None:
        """Validate that clips directory exists"""
        
        clips_path = Path(self.clip_index.clips_base_path)
        if not clips_path.exists():
            logger.warning(f"Clips directory not found: {clips_path}")
        else:
            # Count available clips for logging
            available_clips = self.clip_index.discover_clips()
            logger.info(f"Clips directory validated - {len(available_clips)} clips found at {clips_path}")
    
    async def process(self, state: AgentState) -> AgentState:
        """Process video clip retrieval queries"""
        
        state = update_state_step(state, "clip_retrieval")
        start_time = datetime.now()
        
        try:
            # Extract analysis parameters
            query = state["original_query"]
            user_context = state["user_context"]
            intent_analysis = state["intent_analysis"]
            required_tools = state["required_tools"]
            
            logger.info(f"Processing clip retrieval for query: {query[:100]}...")
            logger.info(f"User context: {user_context.name} ({user_context.role.value})")
            
            # Parse clip query parameters
            search_params = self._parse_clip_query(query, user_context, intent_analysis)
            logger.info(f"Search params: players={search_params.player_names}, time={search_params.time_filter}")
            
            # Execute clip search
            clip_results = await self._execute_clip_search(
                search_params=search_params,
                user_context=user_context
            )
            
            logger.info(f"Clip search returned {len(clip_results)} results")
            
            # Calculate execution time
            execution_time = int((datetime.now() - start_time).total_seconds() * 1000)
            
            # Create tool result
            tool_result = ToolResult(
                tool_type=ToolType.CLIP_RETRIEVAL,
                success=len(clip_results) > 0,
                data={
                    "clips": [self._clip_result_to_dict(clip) for clip in clip_results],
                    "search_params": self._search_params_to_dict(search_params),
                    "total_found": len(clip_results)
                },
                execution_time_ms=execution_time,
                citations=self._generate_citations(clip_results)
            )
            
            # Update state (ensure analytics_data is properly initialized)
            if "analytics_data" not in state:
                state["analytics_data"] = {}
            state["analytics_data"]["clips"] = clip_results
            state = add_tool_result(state, tool_result)
            
            logger.info(f"Clip retrieval completed in {execution_time}ms - found {len(clip_results)} clips")
            
        except Exception as e:
            logger.error(f"Error in clip retrieval: {str(e)}")
            state = add_error(state, f"Clip retrieval failed: {str(e)}")
            
            # Add failed tool result
            execution_time = int((datetime.now() - start_time).total_seconds() * 1000)
            tool_result = ToolResult(
                tool_type=ToolType.CLIP_RETRIEVAL,
                success=False,
                error=str(e),
                execution_time_ms=execution_time
            )
            state = add_tool_result(state, tool_result)
        
        return state
    
    def _parse_clip_query(
        self, 
        query: str, 
        user_context, 
        intent_analysis: Dict[str, Any]
    ) -> ClipSearchParams:
        """Parse natural language query into clip search parameters"""
        
        query_lower = query.lower()
        
        # Extract player names
        player_names = self._extract_player_names(query_lower, user_context)
        
        # Extract event types
        event_types = self._extract_event_types(query_lower)
        
        # Extract opponents
        opponents = self._extract_opponents(query_lower)
        
        # Extract time filter
        time_filter = self._extract_time_filter(query_lower)
        
        # Extract limit
        limit = self._extract_limit(query_lower)
        
        return ClipSearchParams(
            player_names=player_names,
            event_types=event_types,
            opponents=opponents,
            time_filter=time_filter,
            limit=limit,
            user_context=user_context
        )
    
    def _extract_player_names(self, query: str, user_context) -> List[str]:
        """Extract player names from query"""
        
        found_players = []
        
        # Check for "my" or "me" indicating user's own clips
        if any(word in query for word in ['my', 'me', 'i ']):
            user_name = getattr(user_context, 'name', '').lower()
            if user_name:
                # Convert user name to match clip naming convention
                formatted_name = user_name.replace(' ', '_').lower()
                if formatted_name in [p.replace(' ', '_') for p in self.mtl_players]:
                    found_players.append(user_name.title())
        
        # Check for explicit player names
        for player in self.mtl_players:
            if player in query:
                found_players.append(player.title())
        
        return list(set(found_players))  # Remove duplicates
    
    def _extract_event_types(self, query: str) -> List[str]:
        """Extract event types from query with enhanced hockey terminology"""
        
        event_mapping = {
            # Primary scoring events
            'goals': ['goal', 'goals', 'scoring', 'scored', 'tally', 'tallies', 'lamp', 'net', 'finish'],
            'assists': ['assist', 'assists', 'setup', 'playmaking', 'helper', 'helpers', 'dish', 'feed'],
            
            # Goaltending events  
            'saves': ['save', 'saves', 'goaltending', 'stop', 'stops', 'denial', 'rob', 'robbed', 'glove', 'pad'],
            
            # Physical play
            'hits': ['hit', 'hits', 'check', 'checks', 'physical', 'body check', 'clean hit', 'big hit'],
            'fights': ['fight', 'fights', 'scrap', 'scraps', 'tilt', 'tilts', 'drop gloves'],
            
            # Penalties and infractions
            'penalties': ['penalty', 'penalties', 'infraction', 'infractions', 'box', 'sin bin', 'ref call'],
            
            # Special situations
            'powerplay': ['powerplay', 'power play', 'pp', 'man advantage', '5 on 4', '5v4', '4 on 3'],
            'penalty_kill': ['penalty kill', 'pk', 'short handed', 'shorthanded', '4 on 5', '4v5', '3 on 4'],
            'overtime': ['overtime', 'ot', '3 on 3', '3v3', 'extra time'],
            'shootout': ['shootout', 'so', 'penalty shot', 'breakaway'],
            
            # Game situations
            'faceoffs': ['faceoff', 'faceoffs', 'draw', 'draws', 'face-off', 'center ice', 'dot'],
            'turnovers': ['turnover', 'turnovers', 'giveaway', 'giveaways', 'takeaway', 'takeaways'],
            'blocks': ['block', 'blocks', 'blocked shot', 'blocked shots', 'shot block'],
            
            # Zone play
            'zone_entries': ['zone entry', 'zone entries', 'entry', 'entries', 'zone', 'carry in'],
            'zone_exits': ['zone exit', 'zone exits', 'exit', 'exits', 'clear', 'clearing'],
            
            # Line changes and shifts
            'shifts': ['shift', 'shifts', 'ice time', 'line change', 'change', 'bench'],
            'highlights': ['highlight', 'highlights', 'clip', 'clips', 'best', 'top play', 'sequence']
        }
        
        found_events = []
        query_lower = query.lower()
        
        for event_type, keywords in event_mapping.items():
            if any(keyword in query_lower for keyword in keywords):
                if event_type in ['highlights', 'shifts']:
                    # Generic terms - don't add as specific event filter
                    continue
                found_events.append(event_type)
        
        return found_events
    
    def _extract_opponents(self, query: str) -> List[str]:
        """Extract opponent team names from query"""
        
        found_opponents = []
        
        for team in self.nhl_teams:
            if team in query:
                found_opponents.append(team.title())
        
        # Check for "vs" or "against" patterns
        vs_patterns = [r'vs\s+(\w+)', r'against\s+(\w+)', r'versus\s+(\w+)']
        
        for pattern in vs_patterns:
            matches = re.findall(pattern, query, re.IGNORECASE)
            for match in matches:
                if match.lower() in self.nhl_teams:
                    found_opponents.append(match.title())
        
        return list(set(found_opponents))  # Remove duplicates
    
    def _extract_time_filter(self, query: str) -> str:
        """Extract time-based filters from query with enhanced hockey terminology"""
        
        time_patterns = {
            # Basic time patterns
            'last_game': r'last\s+game|previous\s+game|most\s+recent\s+game|tonight\'?s\s+game|yesterday\'?s\s+game',
            'last_2_games': r'last\s+2\s+games|past\s+2\s+games|last\s+couple\s+games',
            'last_3_games': r'last\s+3\s+games|past\s+3\s+games',
            'last_5_games': r'last\s+5\s+games|past\s+5\s+games',
            'last_10_games': r'last\s+10\s+games|past\s+10\s+games',
            
            # Hockey-specific time periods
            'this_season': r'this\s+season|current\s+season|2024-25\s+season|2024-2025\s+season',
            'last_season': r'last\s+season|previous\s+season|2023-24\s+season|2023-2024\s+season',
            'this_month': r'this\s+month|current\s+month|past\s+month',
            'this_week': r'this\s+week|past\s+week|recent\s+games',
            'recent': r'recent|lately|recently',
            
            # Game situation contexts
            'playoffs': r'playoff|playoffs|postseason|post\s+season',
            'regular_season': r'regular\s+season|season\s+games',
            'home_games': r'home\s+games?|at\s+home|bell\s+centre',
            'away_games': r'away\s+games?|on\s+the\s+road|road\s+games?',
            
            # Period-specific
            'overtime': r'overtime|OT|extra\s+time',
            'shootout': r'shootout|SO|penalty\s+shots?'
        }
        
        for time_filter, pattern in time_patterns.items():
            if re.search(pattern, query, re.IGNORECASE):
                return time_filter
        
        return ""
    
    def _extract_limit(self, query: str) -> int:
        """Extract result limit from query"""
        
        # Look for patterns like "show me 5 clips" or "first 10"
        limit_patterns = [
            r'show\s+me\s+(\d+)',
            r'first\s+(\d+)',
            r'top\s+(\d+)',
            r'(\d+)\s+clips?'
        ]
        
        for pattern in limit_patterns:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                return min(int(match.group(1)), 20)  # Cap at 20
        
        return 10  # Default limit
    
    async def _execute_clip_search(
        self, 
        search_params: ClipSearchParams,
        user_context
    ) -> List[ClipResult]:
        """Execute clip search with permission filtering"""
        
        # Apply user-based permissions
        filtered_params = self._apply_user_permissions(search_params, user_context)
        
        # Execute search
        clip_results = await self.clip_index.search_clips(filtered_params)
        
        # Sort by relevance (basic implementation)
        clip_results.sort(key=lambda x: x.relevance_score, reverse=True)
        
        return clip_results
    
    def _apply_user_permissions(
        self, 
        search_params: ClipSearchParams, 
        user_context
    ) -> ClipSearchParams:
        """Apply user permissions to search parameters"""
        
        user_role = getattr(user_context, 'role', None)
        user_name = getattr(user_context, 'name', '').title()
        
        logger.info(f"Applying permissions for {user_name} ({user_role.value if user_role else 'unknown'})")
        logger.info(f"Original search params: players={search_params.player_names}")
        
        # For now, all Montreal Canadiens personnel can see all clips
        # Players can only see their own clips unless they have broader access
        if user_role and user_role.value == 'player':
            if user_name and not search_params.player_names:
                # If no specific players requested, show user's clips
                search_params.player_names = [user_name]
                logger.info(f"Added user's name to search: {user_name}")
            elif user_name and search_params.player_names:
                # Filter to only include user's own clips
                original_names = search_params.player_names[:]
                search_params.player_names = [
                    name for name in search_params.player_names 
                    if name.lower() == user_name.lower()
                ]
                logger.info(f"Filtered player names: {original_names} → {search_params.player_names}")
        
        logger.info(f"Final search params: players={search_params.player_names}")
        return search_params
    
    def _clip_result_to_dict(self, clip_result: ClipResult) -> Dict[str, Any]:
        """Convert ClipResult to dictionary for JSON serialization"""
        
        return {
            "clip_id": clip_result.clip_id,
            "title": clip_result.title,
            "player_name": clip_result.player_name,
            "game_info": clip_result.game_info,
            "event_type": clip_result.event_type,
            "description": clip_result.description,
            "file_url": clip_result.file_url,
            "thumbnail_url": clip_result.thumbnail_url,
            "duration": clip_result.duration,
            "relevance_score": clip_result.relevance_score
        }
    
    def _search_params_to_dict(self, search_params: ClipSearchParams) -> Dict[str, Any]:
        """Convert ClipSearchParams to dictionary"""
        
        return {
            "player_names": search_params.player_names,
            "event_types": search_params.event_types,
            "opponents": search_params.opponents,
            "time_filter": search_params.time_filter,
            "limit": search_params.limit
        }
    
    def _generate_citations(self, clip_results: List[ClipResult]) -> List[str]:
        """Generate citations for clip results"""
        
        citations = []
        
        if clip_results:
            citations.append(f"[clip_database:{len(clip_results)}_clips]")
            
            # Add specific citations for unique sources
            unique_games = set()
            unique_players = set()
            
            for clip in clip_results:
                if clip.game_info:
                    unique_games.add(clip.game_info)
                unique_players.add(clip.player_name)
            
            if unique_games:
                citations.append(f"[games:{','.join(list(unique_games)[:3])}]")
            
            if unique_players:
                citations.append(f"[players:{','.join(list(unique_players)[:3])}]")
        
        return citations
