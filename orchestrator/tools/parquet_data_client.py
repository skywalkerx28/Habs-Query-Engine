"""
HeartBeat Engine - Real Parquet Data Client
Montreal Canadiens Advanced Analytics Assistant

Parquet data integration for Montreal Canadiens analytics.
Connects to actual processed hockey data files.
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

logger = logging.getLogger(__name__)

class ParquetDataClient:
    """
    Real Parquet data client for Montreal Canadiens analytics.
    
    Provides access to:
    - Player statistics by team (MTL focus)
    - Team performance metrics and analytics
    - Game-by-game data and play-by-play events
    - Advanced hockey metrics and line combinations
    """
    
    def __init__(self, data_directory: str = "data/processed"):
        self.data_directory = Path(data_directory)
        self.cache = {}
        
        # Real data file mapping based on your structure
        self.data_files = {
            # Core data
            "players": "dim/players.parquet",
            "teams": "dim/teams.parquet", 
            "pbp_unified": "fact/pbp/unified_pbp_2024-25.parquet",
            
            # MTL specific analytics
            "mtl_season_results": "analytics/mtl_season_results/2024-2025/mtl_season_game_results_2024-2025.parquet",
            "mtl_season_report": "analytics/mtl_season_reports/Season-Report-Montreal.parquet",
            "mtl_matchup_reports": "analytics/mtl_matchup_reports/unified_matchup_reports_2024_2025.parquet",
            
            # Line combinations
            "line_combinations_forwards": "analytics/mtl_line_combinations_2024-2025/Line_Combinations_Metrics_for_Forwards (1).parquet",
            "line_combinations_defense": "analytics/mtl_line_combinations_2024-2025/Line_Combinations_Metrics_for_Defencemen.parquet",
            "line_combinations_pp": "analytics/mtl_line_combinations_2024-2025/Line_Combinations_Metrics_for_PPUnits.parquet",
            "line_combinations_pk": "analytics/mtl_line_combinations_2024-2025/Line_Combinations_Metrics_for_SHUnits.parquet",
            
            # Advanced metrics
            "strengths_weaknesses": "analytics/mtl_team_stats/Strengths-Weaknesses-Montreal-2024.parquet",
            "xg_benchmarks": "analytics/mtl_team_stats/XG-Benchmarks-Montreal-2024.parquet",
            "team_stats_2024": "analytics/mtl_team_stats/Teams_Statistics_For_2024-2025_Regular_-_9_18_25,_6_15_PM.parquet",
            
            # NHL player stats (all teams)
            "nhl_player_stats_base": "analytics/nhl_player_stats",
            
            # Specific analytics categories
            "mtl_defensive": "analytics/mtl_team_stats/mtl_defensive",
            "mtl_shooting": "analytics/mtl_team_stats/mtl_shooting", 
            "mtl_passing": "analytics/mtl_team_stats/mtl_passing",
            "mtl_faceoffs": "analytics/mtl_team_stats/mtl_faceoffs",
            "mtl_possession": "analytics/mtl_team_stats/mtl_possession",
            "mtl_goalie": "analytics/mtl_team_stats/mtl_goalie"
        }
        
        self._validate_data_availability()
    
    def _validate_data_availability(self) -> None:
        """Validate that data files are available"""
        
        available_files = []
        missing_files = []
        
        for data_type, file_path in self.data_files.items():
            full_path = self.data_directory / file_path
            
            if full_path.exists():
                if full_path.is_file():
                    available_files.append(data_type)
                elif full_path.is_dir():
                    # Check if directory has parquet files
                    parquet_files = list(full_path.glob("*.parquet"))
                    if parquet_files:
                        available_files.append(f"{data_type} ({len(parquet_files)} files)")
                    else:
                        missing_files.append(f"{data_type}: no parquet files in directory")
            else:
                missing_files.append(f"{data_type}: {file_path}")
        
        logger.info(f"Available data sources: {len(available_files)}")
        for source in available_files[:10]:  # Show first 10
            logger.info(f"{source}")
        
        if missing_files:
            logger.warning(f"Missing data sources: {len(missing_files)}")
            for missing in missing_files[:5]:  # Show first 5
                logger.warning(f"{missing}")
    
    async def get_player_performance(
        self,
        player_names: List[str],
        timeframe: str = "current_season",
        team: str = "MTL"
    ) -> Dict[str, Any]:
        """Get real player performance data from NHL player stats"""
        
        try:
            # Use new NHL player stats structure  
            nhl_stats_base = self.data_directory / self.data_files["nhl_player_stats_base"]
            team_stats_dir = nhl_stats_base / team.upper() / "2024-2025"
            
            if not team_stats_dir.exists():
                return {"error": f"Player stats directory not found for team {team}: {team_stats_dir}"}
            
            # Get all parquet files for the team (including subdirectories)
            stat_files = list(team_stats_dir.glob("**/*.parquet"))
            
            if not stat_files:
                return {"error": f"No player stat files found for team {team} in 2024-2025 season"}
            
            logger.info(f"Loading {team} player stats from: {len(stat_files)} files")
            
            if not pd:
                return {"error": "Pandas not available for data processing"}
            
            # Load and combine all stat files for the team
            combined_data = []
            file_info = []
            
            for stats_file in stat_files:
                try:
                    df = pd.read_parquet(stats_file)
                    
                    # Filter for requested players if specified
                    if player_names:
                        # Try different possible column names for player identification
                        player_cols = [col for col in df.columns if any(term in col.lower() for term in ['player', 'name', 'first', 'last'])]
                        
                        if player_cols:
                            player_col = player_cols[0]
                            # Case-insensitive matching for player names
                            mask = df[player_col].str.lower().str.contains('|'.join([p.lower() for p in player_names]), na=False)
                            filtered_df = df[mask]
                        else:
                            # If no clear player column, take first few rows
                            filtered_df = df.head(5)
                    else:
                        # If no specific players requested, take sample
                        filtered_df = df.head(10)
                    
                    if not filtered_df.empty:
                        # Add file source information
                        filtered_df = filtered_df.copy()
                        filtered_df['data_source_file'] = stats_file.name
                        combined_data.append(filtered_df)
                        
                        file_info.append({
                            "file": stats_file.name,
                            "records": len(df),
                            "columns": len(df.columns),
                            "players_found": len(filtered_df)
                        })
                
                except Exception as e:
                    logger.warning(f"Failed to load {stats_file.name}: {str(e)}")
                    continue
            
            if not combined_data:
                return {"error": f"No valid player data found for {team} players: {player_names}"}
            
            # Combine all data
            final_df = pd.concat(combined_data, ignore_index=True)
            
            results = {
                "analysis_type": "real_nhl_player_performance",
                "team": team,
                "season": "2024-2025",
                "players_requested": player_names,
                "players_found": len(final_df),
                "timeframe": timeframe,
                "data_sources": file_info,
                "total_files_processed": len(stat_files),
                "columns": list(final_df.columns) if not final_df.empty else [],
                "sample_data": final_df.head(5).to_dict('records') if not final_df.empty else [],
                "summary": {
                    "total_records": len(final_df),
                    "unique_players": len(final_df.drop_duplicates(subset=[col for col in final_df.columns if 'player' in col.lower() or 'name' in col.lower()][:1])) if not final_df.empty else 0
                }
            }
            
            return results
                
        except Exception as e:
            logger.error(f"Error loading NHL player performance data: {str(e)}")
            return {"error": f"Failed to load NHL player data: {str(e)}"}
    
    async def get_nhl_player_stats(
        self,
        team: str,
        player_names: Optional[List[str]] = None,
        season: str = "2024-2025"
    ) -> Dict[str, Any]:
        """Get NHL player stats for any team"""
        
        try:
            # Navigate to team-specific directory
            nhl_stats_base = self.data_directory / self.data_files["nhl_player_stats_base"]
            team_stats_dir = nhl_stats_base / team.upper() / season
            
            if not team_stats_dir.exists():
                return {"error": f"Player stats not available for team {team} in {season}"}
            
            # Get all parquet files for the team (including subdirectories)
            stat_files = list(team_stats_dir.glob("**/*.parquet"))
            
            if not stat_files:
                return {"error": f"No player stat files found for {team} in {season}"}
            
            logger.info(f"Loading {team} player stats: {len(stat_files)} files")
            
            if not pd:
                return {"error": "Pandas not available for data processing"}
            
            # Load all stat files and combine
            all_data = []
            file_details = []
            
            for stats_file in stat_files:
                try:
                    df = pd.read_parquet(stats_file)
                    
                    # Add metadata
                    df = df.copy()
                    df['source_file'] = stats_file.name
                    df['team'] = team.upper()
                    df['season'] = season
                    
                    all_data.append(df)
                    file_details.append({
                        "file": stats_file.name,
                        "records": len(df),
                        "columns": list(df.columns)
                    })
                    
                except Exception as e:
                    logger.warning(f"Failed to load {stats_file.name}: {str(e)}")
                    continue
            
            if not all_data:
                return {"error": f"No valid data loaded for {team}"}
            
            # Combine all dataframes
            combined_df = pd.concat(all_data, ignore_index=True)
            
            # Filter for specific players if requested
            if player_names:
                player_cols = [col for col in combined_df.columns if any(term in col.lower() for term in ['player', 'name', 'first', 'last'])]
                
                if player_cols:
                    player_col = player_cols[0]
                    mask = combined_df[player_col].str.lower().str.contains('|'.join([p.lower() for p in player_names]), na=False)
                    combined_df = combined_df[mask]
            
            results = {
                "analysis_type": "real_nhl_player_stats",
                "team": team.upper(),
                "season": season,
                "players_requested": player_names,
                "players_found": len(combined_df),
                "data_files": file_details,
                "total_files": len(stat_files),
                "columns": list(combined_df.columns),
                "sample_data": combined_df.head(10).to_dict('records') if not combined_df.empty else [],
                "summary": {
                    "total_records": len(combined_df),
                    "data_coverage": f"{len(stat_files)} stat categories for {team}"
                }
            }
            
            return results
                
        except Exception as e:
            logger.error(f"Error loading NHL player stats for {team}: {str(e)}")
            return {"error": f"Failed to load NHL player stats: {str(e)}"}
    
    async def get_team_analytics(
        self,
        team: str = "MTL",
        analysis_type: str = "general"
    ) -> Dict[str, Any]:
        """Get real team analytics data"""
        
        try:
            # Load MTL season results
            season_results_file = self.data_directory / self.data_files["mtl_season_results"]
            
            if not season_results_file.exists():
                return {"error": "MTL season results file not found"}
            
            logger.info(f"Loading team analytics from: {season_results_file.name}")
            
            if pd:
                df = pd.read_parquet(season_results_file)
                
                # Basic team statistics
                results = {
                    "analysis_type": "real_team_analytics",
                    "data_source": season_results_file.name,
                    "team": team,
                    "season": "2024-2025",
                    "total_games": len(df),
                    "columns": list(df.columns),
                    "sample_data": df.head(5).to_dict('records') if not df.empty else [],
                }
                
                # Calculate basic metrics if possible
                if 'MTL_G' in df.columns and 'OPP_G' in df.columns:
                    results["goals_for"] = int(df['MTL_G'].sum()) if 'MTL_G' in df.columns else 0
                    results["goals_against"] = int(df['OPP_G'].sum()) if 'OPP_G' in df.columns else 0
                    results["goal_differential"] = results["goals_for"] - results["goals_against"]
                
                if 'Result' in df.columns:
                    wins = len(df[df['Result'] == 'W'])
                    losses = len(df[df['Result'] == 'L'])
                    ot_losses = len(df[df['Result'] == 'OTL']) if 'OTL' in df['Result'].values else 0
                    results["record"] = {"wins": wins, "losses": losses, "ot_losses": ot_losses}
                
                return results
            else:
                return {"error": "Pandas not available for data processing"}
                
        except Exception as e:
            logger.error(f"Error loading team analytics: {str(e)}")
            return {"error": f"Failed to load team data: {str(e)}"}
    
    async def get_advanced_metrics(
        self,
        metric_type: str = "xg",
        team: str = "MTL"
    ) -> Dict[str, Any]:
        """Get real advanced hockey metrics"""
        
        try:
            if metric_type.lower() in ["xg", "expected_goals"]:
                # Load xG benchmarks
                xg_file = self.data_directory / self.data_files["xg_benchmarks"]
                
                if xg_file.exists() and pd:
                    df = pd.read_parquet(xg_file)
                    
                    results = {
                        "analysis_type": "real_xg_metrics",
                        "data_source": xg_file.name,
                        "metric_type": "expected_goals",
                        "team": team,
                        "columns": list(df.columns),
                        "sample_data": df.head(3).to_dict('records') if not df.empty else [],
                        "total_records": len(df)
                    }
                    
                    return results
            
            # Load strengths/weaknesses analysis
            strengths_file = self.data_directory / self.data_files["strengths_weaknesses"]
            
            if strengths_file.exists() and pd:
                df = pd.read_parquet(strengths_file)
                
                results = {
                    "analysis_type": "real_strengths_weaknesses",
                    "data_source": strengths_file.name,
                    "metric_type": metric_type,
                    "team": team,
                    "columns": list(df.columns),
                    "sample_data": df.head(3).to_dict('records') if not df.empty else [],
                    "total_records": len(df)
                }
                
                return results
            
            return {"error": f"Advanced metrics file not found for {metric_type}"}
                
        except Exception as e:
            logger.error(f"Error loading advanced metrics: {str(e)}")
            return {"error": f"Failed to load advanced metrics: {str(e)}"}
    
    async def get_line_combinations(
        self,
        unit_type: str = "forwards"
    ) -> Dict[str, Any]:
        """Get real line combination analytics"""
        
        try:
            # Map unit types to files
            file_mapping = {
                "forwards": "line_combinations_forwards",
                "defense": "line_combinations_defense", 
                "defensemen": "line_combinations_defense",
                "powerplay": "line_combinations_pp",
                "pp": "line_combinations_pp",
                "penalty_kill": "line_combinations_pk",
                "pk": "line_combinations_pk"
            }
            
            file_key = file_mapping.get(unit_type.lower(), "line_combinations_forwards")
            line_file = self.data_directory / self.data_files[file_key]
            
            if not line_file.exists():
                return {"error": f"Line combinations file not found for {unit_type}"}
            
            logger.info(f"Loading line combinations from: {line_file.name}")
            
            if pd:
                df = pd.read_parquet(line_file)
                
                results = {
                    "analysis_type": "real_line_combinations",
                    "data_source": line_file.name,
                    "unit_type": unit_type,
                    "total_combinations": len(df),
                    "columns": list(df.columns),
                    "sample_data": df.head(5).to_dict('records') if not df.empty else []
                }
                
                return results
            else:
                return {"error": "Pandas not available for data processing"}
                
        except Exception as e:
            logger.error(f"Error loading line combinations: {str(e)}")
            return {"error": f"Failed to load line combinations: {str(e)}"}
    
    async def get_game_data(
        self,
        game_id: Optional[int] = None,
        opponent: Optional[str] = None,
        limit: int = 10
    ) -> Dict[str, Any]:
        """Get real game data and play-by-play events"""
        
        try:
            # Load unified play-by-play data
            pbp_file = self.data_directory / self.data_files["pbp_unified"]
            
            if not pbp_file.exists():
                return {"error": "Play-by-play data file not found"}
            
            logger.info(f"Loading game data from: {pbp_file.name}")
            
            if pd:
                # Load with chunking for large files
                df = pd.read_parquet(pbp_file)
                
                # Filter by game_id if specified
                if game_id:
                    df = df[df['game_id'] == game_id] if 'game_id' in df.columns else df
                
                # Filter by opponent if specified
                if opponent:
                    # Look for opponent columns
                    opp_cols = [col for col in df.columns if 'opp' in col.lower() or 'opponent' in col.lower()]
                    if opp_cols:
                        df = df[df[opp_cols[0]].str.contains(opponent, case=False, na=False)]
                
                # Limit results
                df_sample = df.head(limit)
                
                results = {
                    "analysis_type": "real_game_data",
                    "data_source": pbp_file.name,
                    "game_id": game_id,
                    "opponent": opponent,
                    "total_events": len(df),
                    "sample_events": len(df_sample),
                    "columns": list(df.columns),
                    "sample_data": df_sample.to_dict('records') if not df_sample.empty else []
                }
                
                return results
            else:
                return {"error": "Pandas not available for data processing"}
                
        except Exception as e:
            logger.error(f"Error loading game data: {str(e)}")
            return {"error": f"Failed to load game data: {str(e)}"}
    
    async def get_specialized_analytics(
        self,
        category: str,
        subcategory: str = "all"
    ) -> Dict[str, Any]:
        """Get specialized analytics from category directories"""
        
        try:
            # Map categories to directory paths
            category_mapping = {
                "defensive": "mtl_defensive",
                "shooting": "mtl_shooting",
                "passing": "mtl_passing", 
                "faceoffs": "mtl_faceoffs",
                "possession": "mtl_possession",
                "goalie": "mtl_goalie"
            }
            
            if category not in category_mapping:
                return {"error": f"Unknown analytics category: {category}"}
            
            category_dir = self.data_directory / "analytics/mtl_team_stats" / category_mapping[category]
            
            if not category_dir.exists():
                return {"error": f"Analytics directory not found: {category}"}
            
            # Get all parquet files in the category
            parquet_files = list(category_dir.glob("*.parquet"))
            
            if not parquet_files:
                return {"error": f"No parquet files found in {category} analytics"}
            
            logger.info(f"Loading {category} analytics: {len(parquet_files)} files")
            
            # Load first relevant file (you can enhance selection logic)
            selected_file = parquet_files[0]
            
            # Filter by subcategory if specified
            if subcategory != "all":
                matching_files = [f for f in parquet_files if subcategory.lower() in f.name.lower()]
                if matching_files:
                    selected_file = matching_files[0]
            
            if pd:
                df = pd.read_parquet(selected_file)
                
                results = {
                    "analysis_type": f"real_{category}_analytics",
                    "data_source": selected_file.name,
                    "category": category,
                    "subcategory": subcategory,
                    "available_files": [f.name for f in parquet_files],
                    "selected_file": selected_file.name,
                    "total_records": len(df),
                    "columns": list(df.columns),
                    "sample_data": df.head(5).to_dict('records') if not df.empty else []
                }
                
                return results
            else:
                return {"error": "Pandas not available for data processing"}
                
        except Exception as e:
            logger.error(f"Error loading {category} analytics: {str(e)}")
            return {"error": f"Failed to load {category} analytics: {str(e)}"}
    
    def get_available_data_sources(self) -> Dict[str, Any]:
        """Get information about available data sources"""
        
        available_sources = {}
        
        for data_type, file_path in self.data_files.items():
            full_path = self.data_directory / file_path
            
            if full_path.exists():
                if full_path.is_file():
                    try:
                        if pd:
                            df = pd.read_parquet(full_path)
                            available_sources[data_type] = {
                                "path": str(file_path),
                                "type": "file",
                                "records": len(df),
                                "columns": list(df.columns)
                            }
                    except Exception as e:
                        available_sources[data_type] = {
                            "path": str(file_path),
                            "type": "file",
                            "error": str(e)
                        }
                elif full_path.is_dir():
                    parquet_files = list(full_path.glob("*.parquet"))
                    available_sources[data_type] = {
                        "path": str(file_path),
                        "type": "directory", 
                        "files": len(parquet_files),
                        "file_names": [f.name for f in parquet_files[:5]]  # First 5
                    }
        
        return {
            "total_sources": len(available_sources),
            "sources": available_sources,
            "data_directory": str(self.data_directory)
        }
