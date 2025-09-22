#!/usr/bin/env python3
"""
Production Chunk Generator V2

Creates production-ready chunks with sophisticated row_selector metadata
for seamless Pinecone integration and deterministic rehydration.
"""

import pandas as pd
import numpy as np
import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
import time

class ProductionChunkGenerator:
    """Generates production chunks with advanced row_selector metadata"""
    
    def __init__(self, base_path: str = "/Users/xavier.bouchard/Desktop/HeartBeat"):
        self.base_path = Path(base_path)
        self.data_path = self.base_path / "data"
        self.processed_path = self.data_path / "processed"
        
        self.season = "2024-25"
        self.version = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        self.ingest_ts = int(time.time())

    def load_dimension_tables(self) -> Dict[str, pd.DataFrame]:
        """Load dimension tables for canonical IDs and names"""
        dims = {}
        
        dim_path = self.processed_path / "dim"
        
        # Load players dimension
        players_file = dim_path / "players.parquet"
        if players_file.exists():
            dims['players'] = pd.read_parquet(players_file)
            print(f"Loaded {len(dims['players'])} players")
        
        # Load teams dimension
        teams_file = dim_path / "teams.parquet"
        if teams_file.exists():
            dims['teams'] = pd.read_parquet(teams_file)
            print(f"Loaded {len(dims['teams'])} teams")
        
        return dims

    def create_game_recap_chunks(self, pbp_file: str, season_results_file: str, dims: Dict[str, pd.DataFrame]) -> List[Dict[str, Any]]:
        """Create game recap chunks with comprehensive metadata"""
        print("Creating game recap chunks...")
        
        # Load data
        df_pbp = pd.read_parquet(pbp_file)
        df_results = pd.read_parquet(season_results_file)
        
        chunks = []
        
        # Group by game
        for game_id in df_pbp['game_id'].unique():
            game_data = df_pbp[df_pbp['game_id'] == game_id]
            
            # Find corresponding season result by game number
            # The season results use simple game numbers (1, 2, 3...)
            # while PBP uses NHL game IDs (20006, 20011, etc.)
            # We need to map based on order or find another way
            
            # For now, use game index mapping (game_id order should match Game order)
            game_ids = sorted(df_pbp['game_id'].unique())
            if game_id in game_ids:
                game_index = game_ids.index(game_id) + 1  # Game column is 1-indexed
                season_row = df_results[df_results['Game'] == game_index]
            else:
                game_index = None
                season_row = pd.DataFrame()  # Empty dataframe
            
            if len(season_row) == 0:
                print(f"No season result found for game {game_id}")
                continue
                
            season_info = season_row.iloc[0]
            
            # Extract game metadata from authoritative season results
            opponent = self._extract_opponent(season_info)
            home_away = self._determine_home_away(season_info)
            final_score = self._extract_score(season_info)
            result = self._extract_result(season_info)  # Use authoritative result from season results
            ot_so = self._determine_overtime(season_info)
            
            # Use authoritative data from season results (source of truth)
            mtl_sog = int(season_info.get('MTL_SOG', 0))
            opp_sog = int(season_info.get('Opp_SOG', 0))
            
            # Calculate PBP-derived statistics for context
            mtl_attempts = len(game_data[game_data['team_abbr'] == 'MTL'])
            total_plays = len(game_data)
            
            mtl_possessions = len(game_data[
                (game_data['team_abbr'] == 'MTL') & 
                (game_data['is_possession_event'] == True)
            ])
            
            # Extract key players (most events)
            key_players = self._extract_key_players(game_data, dims.get('players'))
            
            # Create readable text summary using authoritative season results data
            date_str = self._format_game_date(season_info)
            result_str = result  # W/L/OTL from season results
            
            # Add overtime/shootout context if applicable
            if ot_so:
                result_str += f" ({ot_so})"
            
            text_summary = f"{date_str} — MTL {final_score['mtl']}, {opponent} {final_score['opp']} ({home_away}). Result: {result_str}. MTL SOG: {mtl_sog}, {opponent} SOG: {opp_sog}. Key players: {', '.join(key_players[:3]) if key_players else 'N/A'}."
            
            # Create chunk
            chunk = {
                "id": f"recap-{self.season}-g{str(game_id).zfill(4)}",
                "text": text_summary,
                "metadata": {
                    "type": "game_recap",
                    "season": self.season,
                    "game_id": int(game_id),
                    "date_ts": self._extract_date_timestamp(season_info),
                    "opponent_abbr": opponent,
                    "home_away": home_away,
                    "result": result,
                    "ot_so": ot_so,
                    "final_score": final_score,
                    "mtl_sog": mtl_sog,
                    "opp_sog": opp_sog,
                    "mtl_attempts": mtl_attempts,
                    "opp_attempts": total_plays - mtl_attempts,
                    "mtl_possessions": mtl_possessions,
                    "total_plays": total_plays,
                    "players_ids": self._get_canonical_player_ids(key_players, dims.get('players')),
                    "players": key_players,
                    "source_uri": [
                        "parquet://data/processed/fact/pbp/",
                        "parquet://data/processed/analytics/mtl_season_results/2024-2025/mtl_season_game_results_2024-2025.parquet"
                    ],
                    "parquet_ref": {
                        "season": self.season,
                        "game_id": int(game_id)
                    },
                    "row_selector": {
                        "table": "pbp",
                        "partitions": {"season": self.season, "game_id": int(game_id)},
                        "where": {"period": {"$in": [1, 2, 3]}},
                        "columns": [
                            "row_id", "period", "period_seconds", "event_type", 
                            "team_abbr", "x_coord", "y_coord", "player_id", 
                            "on_ice_ids", "xg", "strength", "zone"
                        ]
                    },
                    "season_results_selector": {
                        "table": "season_results",
                        "partitions": {"season": self.season},
                        "where": {"Game": {"$eq": game_index}} if game_index else {},
                        "columns": ["Game", "Date", "Home/Away", "Opponent", "MTL_G", "OPP_G", "Result", "OT_SO", "MTL_SOG", "Opp_SOG"]
                    },
                    "ingest_ts": self.ingest_ts,
                    "version": self.version
                }
            }
            
            chunks.append(chunk)
        
        print(f"Created {len(chunks)} game recap chunks")
        return chunks

    def create_event_excerpt_chunks(self, pbp_file: str, dims: Dict[str, pd.DataFrame]) -> List[Dict[str, Any]]:
        """Create event excerpt chunks for notable sequences"""
        print("Creating event excerpt chunks...")
        
        df_pbp = pd.read_parquet(pbp_file)
        chunks = []
        
        # Define notable event types for excerpts
        notable_events = ['GOAL', 'SHOT', 'PENALTY']
        
        # Group by game and create excerpts for notable sequences
        for game_id in df_pbp['game_id'].unique()[:10]:  # Limit for testing
            game_data = df_pbp[df_pbp['game_id'] == game_id]
            
            # Find notable event sequences
            notable_mask = game_data['event_type'].isin(notable_events)
            notable_events_df = game_data[notable_mask]
            
            if len(notable_events_df) == 0:
                continue
            
            # Group by period and time windows (30 second windows around notable events)
            for _, event_row in notable_events_df.iterrows():
                if pd.isna(event_row['period_seconds']):
                    continue
                    
                event_time = event_row['period_seconds']
                period = event_row['period']
                
                # Create time window around event
                window_start = max(0, event_time - 15)
                window_end = event_time + 15
                
                # Get events in window
                window_events = game_data[
                    (game_data['period'] == period) &
                    (game_data['period_seconds'] >= window_start) &
                    (game_data['period_seconds'] <= window_end)
                ]
                
                if len(window_events) < 3:  # Skip small sequences
                    continue
                
                # Extract involved players
                involved_players = self._extract_sequence_players(window_events, dims.get('players'))
                
                # Create text summary
                time_str = f"{int(event_time//60):02d}:{int(event_time%60):02d}"
                event_desc = self._describe_event_sequence(window_events)
                
                text_summary = f"G{game_id} P{period} {time_str} — {event_desc}"
                
                # Determine opponent from game context
                opponent = self._get_opponent_for_game(game_data)
                
                chunk = {
                    "id": f"ev-{self.season}-g{game_id}-p{period}-{time_str.replace(':', '')}",
                    "text": text_summary,
                    "metadata": {
                        "type": "event_excerpt",
                        "season": self.season,
                        "game_id": int(game_id),
                        "period": int(period),
                        "period_seconds": int(event_time),
                        "strength": event_row.get('strength', 'EV'),
                        "opponent_abbr": opponent,
                        "players_ids": self._get_canonical_player_ids(involved_players, dims.get('players')),
                        "players": involved_players,
                        "source_uri": "parquet://data/processed/fact/pbp/",
                        "parquet_ref": {
                            "season": self.season,
                            "game_id": int(game_id)
                        },
                        "row_selector": {
                            "table": "pbp",
                            "partitions": {"season": self.season, "game_id": int(game_id)},
                            "where": {
                                "period": {"$eq": int(period)},
                                "period_seconds": {"$between": [window_start, window_end]}
                            },
                            "columns": [
                                "row_id", "event_type", "period", "period_seconds", 
                                "xg", "player_id", "team_abbr", "x_coord", "y_coord"
                            ]
                        },
                        "date_ts": self.ingest_ts  # Simplified for event excerpts
                    }
                }
                
                chunks.append(chunk)
        
        print(f"Created {len(chunks)} event excerpt chunks")
        return chunks

    def _extract_opponent(self, season_info: pd.Series) -> str:
        """Extract opponent abbreviation from season info"""
        if 'Opponent' in season_info and pd.notna(season_info['Opponent']):
            opponent_name = str(season_info['Opponent']).strip()  # Strip trailing spaces
            # Map common team names to abbreviations
            team_mapping = {
                'Toronto': 'TOR', 'Boston': 'BOS', 'Tampa Bay': 'TBL',
                'Florida': 'FLA', 'Ottawa': 'OTT', 'Buffalo': 'BUF',
                'Detroit': 'DET', 'New York Rangers': 'NYR', 'New York Islanders': 'NYI',
                'New York': 'NYR', 'NY Rangers': 'NYR', 'NY Islanders': 'NYI',  # Handle NY variations
                'New Jersey': 'NJD', 'Philadelphia': 'PHI', 'Pittsburgh': 'PIT',
                'Washington': 'WSH', 'Carolina': 'CAR', 'Columbus': 'CBJ',
                'Chicago': 'CHI', 'Colorado': 'COL', 'Dallas': 'DAL',
                'Minnesota': 'MIN', 'Nashville': 'NSH', 'St. Louis': 'STL',
                'Winnipeg': 'WPG', 'Calgary': 'CGY', 'Edmonton': 'EDM',
                'Vancouver': 'VAN', 'Seattle': 'SEA', 'Los Angeles': 'LAK',
                'San Jose': 'SJS', 'Anaheim': 'ANA', 'Vegas': 'VGK',
                'Utah': 'UTA'
            }
            return team_mapping.get(opponent_name, opponent_name[:3].upper())

        return 'UNK'

    def _determine_home_away(self, season_info: pd.Series) -> str:
        """Determine if Montreal was home or away"""
        if 'Home/Away' in season_info and pd.notna(season_info['Home/Away']):
            value = str(season_info['Home/Away']).upper()
            return 'H' if value.startswith('H') else 'A'
        
        return 'H'  # Default

    def _extract_score(self, season_info: pd.Series) -> Dict[str, int]:
        """Extract final score from season info"""
        mtl_score = 0
        opp_score = 0
        
        if 'MTL_G' in season_info and pd.notna(season_info['MTL_G']):
            try:
                mtl_score = int(season_info['MTL_G'])
            except ValueError:
                pass
        
        if 'OPP_G' in season_info and pd.notna(season_info['OPP_G']):
            try:
                opp_score = int(season_info['OPP_G'])
            except ValueError:
                pass
        
        return {"mtl": mtl_score, "opp": opp_score}

    def _extract_result(self, season_info: pd.Series) -> str:
        """Extract authoritative game result from season results"""
        if 'Result' in season_info and pd.notna(season_info['Result']):
            result = str(season_info['Result']).upper()
            # Map to standard format
            if result in ['W', 'WIN']:
                return 'W'
            elif result in ['L', 'LOSS']:
                return 'L' 
            elif result in ['OTL', 'SOL', 'OVERTIME LOSS', 'SHOOTOUT LOSS']:
                return 'OTL'
            else:
                return result
        
        # Fallback to score-based determination
        return self._determine_result_from_score(season_info)

    def _determine_result_from_score(self, season_info: pd.Series) -> str:
        """Fallback: determine game result from score"""
        final_score = self._extract_score(season_info)
        if final_score['mtl'] > final_score['opp']:
            return 'W'
        elif final_score['mtl'] < final_score['opp']:
            return 'L'
        else:
            return 'OTL'  # Assume overtime/shootout loss for ties

    def _determine_overtime(self, season_info: pd.Series) -> Optional[str]:
        """Determine if game went to overtime/shootout"""
        if 'OT_SO' in season_info and pd.notna(season_info['OT_SO']):
            value = str(season_info['OT_SO']).upper()
            if 'OT' in value:
                return 'OT'
            elif 'SO' in value:
                return 'SO'
        return None

    def _extract_key_players(self, game_data: pd.DataFrame, players_dim: Optional[pd.DataFrame]) -> List[str]:
        """Extract key players from game data"""
        if game_data.empty:
            return []

        # Count events by player
        player_counts = game_data[game_data['team_abbr'] == 'MTL']['player_id'].value_counts()

        if len(player_counts) == 0:
            return []

        # Get top players
        top_player_ids = player_counts.head(5).index.tolist()

        # Convert to names if possible
        if players_dim is not None:
            player_names = []
            for player_id in top_player_ids:
                # Clean the player_id from PBP data (remove .0 suffix)
                clean_player_id = str(player_id)
                if clean_player_id.endswith('.0'):
                    clean_player_id = clean_player_id[:-2]

                match = players_dim[players_dim['player_id'] == clean_player_id]
                if len(match) > 0:
                    name = match.iloc[0]['last_name']
                    player_names.append(name)
                else:
                    player_names.append(clean_player_id.replace('nhl_', ''))
            return player_names

        return [str(pid).replace('.0', '').replace('nhl_', '') for pid in top_player_ids]

    def _get_canonical_player_ids(self, player_names: List[str], players_dim: Optional[pd.DataFrame]) -> List[str]:
        """Convert player names to canonical IDs"""
        if not players_dim is not None:
            return player_names

        canonical_ids = []
        for name in player_names:
            # Try to find matching player
            matches = players_dim[
                players_dim['last_name'].str.contains(name, na=False, case=False) |
                players_dim['full_name'].str.contains(name, na=False, case=False)
            ]
            if len(matches) > 0:
                player_id = str(matches.iloc[0]['player_id'])
                # Strip trailing .0 from player IDs
                if player_id.endswith('.0'):
                    player_id = player_id[:-2]
                canonical_ids.append(player_id)
            else:
                canonical_ids.append(f"name_{name.lower()}")

        return canonical_ids

    def _format_game_date(self, season_info: pd.Series) -> str:
        """Format game date for display"""
        if 'Date' in season_info and pd.notna(season_info['Date']):
            try:
                date_val = pd.to_datetime(season_info['Date'])
                return date_val.strftime("%m-%d")
            except:
                pass
        return "XX-XX"

    def _extract_date_timestamp(self, season_info: pd.Series) -> int:
        """Extract Unix timestamp from season info"""
        if 'Date' in season_info and pd.notna(season_info['Date']):
            try:
                date_val = pd.to_datetime(season_info['Date'])
                return int(date_val.timestamp())
            except:
                pass
        return self.ingest_ts

    def _extract_sequence_players(self, sequence_data: pd.DataFrame, players_dim: Optional[pd.DataFrame]) -> List[str]:
        """Extract involved players from event sequence"""
        if sequence_data.empty:
            return []

        # Get unique players in sequence
        mtl_players = sequence_data[sequence_data['team_abbr'] == 'MTL']['player_id'].unique()

        # Convert to names
        player_names = []
        for player_id in mtl_players[:3]:  # Top 3
            if players_dim is not None:
                # Clean the player_id from PBP data (remove .0 suffix)
                clean_player_id = str(player_id)
                if clean_player_id.endswith('.0'):
                    clean_player_id = clean_player_id[:-2]

                match = players_dim[players_dim['player_id'] == clean_player_id]
                if len(match) > 0:
                    player_names.append(match.iloc[0]['last_name'])
                else:
                    player_names.append(clean_player_id.replace('nhl_', ''))
            else:
                player_names.append(str(player_id).replace('.0', '').replace('nhl_', ''))

        return player_names

    def _describe_event_sequence(self, sequence_data: pd.DataFrame) -> str:
        """Create descriptive text for event sequence"""
        if sequence_data.empty:
            return "No events"
        
        # Summarize key events
        events = sequence_data['event_type'].tolist()
        
        # Look for common patterns
        if 'GOAL' in events:
            return "Goal sequence with build-up"
        elif 'SHOT' in events:
            return "Scoring chance opportunity"
        elif 'ENTRY' in events:
            return "Zone entry and possession"
        else:
            return f"{len(events)} events sequence"

    def _get_opponent_for_game(self, game_data: pd.DataFrame) -> str:
        """Extract opponent from game data"""
        non_mtl_teams = game_data[game_data['team_abbr'] != 'MTL']['team_abbr'].unique()
        if len(non_mtl_teams) > 0:
            return non_mtl_teams[0]
        return 'UNK'

    def generate_all_production_chunks(self) -> List[Dict[str, Any]]:
        """Generate all production chunks"""
        print("Generating all production chunks...")
        
        # Load dimensions
        dims = self.load_dimension_tables()
        
        # Define file paths
        pbp_file = self.processed_path / "fact" / "pbp" / f"unified_pbp_{self.season}.parquet"
        season_results_file = self.processed_path / "analytics" / "mtl_season_results" / "2024-2025" / "mtl_season_game_results_2024-2025.parquet"
        
        # Fallback to original locations if new structure doesn't exist
        if not pbp_file.exists():
            pbp_file = self.processed_path / "analytics" / "mtl_play_by_play" / "unified_play_by_play_2024_2025.parquet"
        
        all_chunks = []
        
        # Generate game recap chunks
        if pbp_file.exists() and season_results_file.exists():
            game_chunks = self.create_game_recap_chunks(str(pbp_file), str(season_results_file), dims)
            all_chunks.extend(game_chunks)
        else:
            print(f"Warning: Missing files - PBP: {pbp_file.exists()}, Results: {season_results_file.exists()}")
        
        # Generate event excerpt chunks
        if pbp_file.exists():
            event_chunks = self.create_event_excerpt_chunks(str(pbp_file), dims)
            all_chunks.extend(event_chunks)
        
        print(f"\n=== CHUNK GENERATION SUMMARY ===")
        print(f"Total chunks generated: {len(all_chunks)}")
        print(f"Game recaps: {len([c for c in all_chunks if c['metadata']['type'] == 'game_recap'])}")
        print(f"Event excerpts: {len([c for c in all_chunks if c['metadata']['type'] == 'event_excerpt'])}")
        
        return all_chunks

    def save_production_chunks(self, chunks: List[Dict[str, Any]], output_file: str = None) -> str:
        """Save production chunks to JSON file"""
        if output_file is None:
            output_file = self.base_path / f"production_game_chunks_{self.season.replace('-', '_')}_v2.json"
        
        print(f"Saving {len(chunks)} chunks to: {output_file}")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(chunks, f, indent=2, ensure_ascii=False)
        
        file_size = Path(output_file).stat().st_size / (1024 * 1024)
        print(f"Saved {file_size:.2f} MB to {output_file}")
        
        return str(output_file)

def main():
    """Main execution function"""
    generator = ProductionChunkGenerator()
    
    # Generate all chunks
    chunks = generator.generate_all_production_chunks()
    
    # Save to file
    output_file = generator.save_production_chunks(chunks)
    
    print(f"\nProduction chunks generated successfully!")
    print(f"Output: {output_file}")
    
    return chunks

if __name__ == "__main__":
    main()
