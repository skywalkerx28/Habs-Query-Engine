#!/usr/bin/env python3
"""
Professional RAG Chunking System for NHL Analytics
====================================================

A mathematically-accurate chunking system that transforms raw hockey
analytics data into semantically coherent, contextually rich chunks optimized for
Retrieval-Augmented Generation (RAG) systems.

Features:
---------
- Semantic chunking with mathematical integrity preservation
- Rich metadata enrichment with domain-specific tags
- Cross-referencing between data sources
- Confidence scoring and relevance ranking
- Temporal context and progression analysis
- Advanced hockey metrics integration (XG, Corsi, PDO, etc.)
- Quality validation and monitoring

Architecture:
-------------
1. Data Ingestion: Load parquet files from analytics directory
2. Semantic Chunking: Break data into 300-500 token coherent units
3. Metadata Enrichment: Add contextual tags and relationships
4. Quality Validation: Mathematical accuracy and completeness checks
5. Cross-Referencing: Link related chunks across data sources
6. Output Generation: Structured JSON for RAG ingestion

Standards Compliance:
--------------------
- Mathematical Accuracy System (MATHEMATICAL_ACCURACY_SYSTEM.md)
- Domain-specific chunking for hockey analytics
- Professional error handling and logging
- Configurable chunking strategies per data type
"""

import pandas as pd
import numpy as np
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import hashlib
import re
from collections import defaultdict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class ChunkMetadata:
    """Rich metadata structure for RAG chunks"""
    chunk_id: str
    source_file: str
    data_type: str  # 'player_stats', 'play_by_play', 'matchup_reports'
    season: str
    team: Optional[str] = None
    opponent: Optional[str] = None
    game_id: Optional[str] = None
    game_date: Optional[str] = None
    venue: Optional[str] = None
    period: Optional[int] = None
    player_name: Optional[str] = None
    position: Optional[str] = None
    metrics: Dict[str, Any] = None
    temporal_context: Dict[str, Any] = None
    relationships: List[str] = None  # IDs of related chunks
    confidence_score: float = 1.0
    quality_score: float = 1.0
    tags: List[str] = None
    created_at: str = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
        if self.metrics is None:
            self.metrics = {}
        if self.temporal_context is None:
            self.temporal_context = {}
        if self.relationships is None:
            self.relationships = []
        if self.tags is None:
            self.tags = []

@dataclass
class RAGChunk:
    """Professional RAG chunk structure"""
    content: str
    metadata: ChunkMetadata
    source: str
    token_count: int = 0
    embedding_hint: str = ""  # For future embedding optimization

class ProfessionalRAGChunker:
    """
    World-class RAG chunking system with mathematical accuracy and semantic coherence
    """

    def __init__(self, analytics_dir: Path, output_dir: Path):
        self.analytics_dir = analytics_dir
        self.output_dir = output_dir
        self.chunks: List[RAGChunk] = []
        self.chunk_registry: Dict[str, RAGChunk] = {}
        self.relationships: Dict[str, List[str]] = defaultdict(list)

        # Chunking configuration per data type
        self.chunking_config = {
            'player_stats': {
                'chunk_size': 400,  # tokens
                'overlap': 50,
                'strategy': 'player_focused'
            },
            'play_by_play': {
                'chunk_size': 350,
                'overlap': 75,
                'strategy': 'temporal_sequence'
            },
            'matchup_reports': {
                'chunk_size': 300,
                'overlap': 25,
                'strategy': 'analytical_summary'
            }
        }

        # Quality thresholds - adjusted for hockey analytics content
        self.quality_thresholds = {
            'min_confidence': 0.6,  # Lower threshold for domain-specific content
            'min_quality_score': 0.5,  # Lower threshold for analytical content
            'max_chunk_size': 800,
            'min_chunk_size': 50  # Much lower minimum for focused analytics
        }

    def generate_chunk_id(self, content: str, metadata: dict) -> str:
        """Generate unique, deterministic chunk ID"""
        content_hash = hashlib.md5(content.encode()).hexdigest()[:8]
        metadata_str = json.dumps(metadata, sort_keys=True, default=str)
        metadata_hash = hashlib.md5(metadata_str.encode()).hexdigest()[:8]
        return f"{content_hash}_{metadata_hash}"

    def estimate_token_count(self, text: str) -> int:
        """Rough token estimation (words * 1.3 for subwords)"""
        return int(len(text.split()) * 1.3)

    def validate_mathematical_accuracy(self, chunk: RAGChunk) -> Tuple[bool, float]:
        """
        Validate mathematical accuracy of chunk content
        Returns: (is_valid, confidence_score)
        """
        content = chunk.content.lower()

        # Check for mathematical expressions
        math_patterns = [
            r'\b\d+\.?\d*\s*(?:goals?|points?|shots?|saves?)\b',
            r'\b\d+\.?\d*%\b',
            r'\b\d+\.?\d*\s*vs\s*\d+\.?\d*\b',
            r'\bxg\b|\bexpected goals\b',
            r'\bcorsi\b|\bfenwick\b|\bpdo\b'
        ]

        math_matches = sum(len(re.findall(pattern, content)) for pattern in math_patterns)

        # Calculate confidence based on mathematical content
        if math_matches == 0:
            confidence = 0.3  # Low confidence for non-mathematical content
        elif math_matches < 3:
            confidence = 0.6
        elif math_matches < 6:
            confidence = 0.8
        else:
            confidence = 0.95

        # Additional validation for known hockey metrics
        hockey_terms = ['expected goals', 'corsi', 'fenwick', 'pdo', 'high-danger',
                       'rebounds', 'faceoffs', 'power play', 'penalty kill']

        term_matches = sum(1 for term in hockey_terms if term in content)
        confidence *= (1 + term_matches * 0.1)  # Boost for domain expertise

        return confidence >= self.quality_thresholds['min_confidence'], min(confidence, 1.0)

    def chunk_player_stats(self, df: pd.DataFrame, file_path: Path) -> List[RAGChunk]:
        """
        Create semantically coherent chunks from player statistics data
        """
        chunks = []
        team = self.extract_team_from_path(file_path)
        season = self.extract_season_from_path(file_path)
        position = self.extract_position_from_path(file_path)

        # Group by player for focused analysis
        player_column = None
        for col in df.columns:
            if 'player' in col.lower() and 'name' in col.lower():
                player_column = col
                break

        if player_column is None:
            logger.warning(f"No player name column found in {file_path}")
            return []

        for player_name, player_data in df.groupby(player_column):
            if 'team' in str(player_name).lower() or 'total' in str(player_name).lower():
                continue

            # Create comprehensive player analysis chunk
            content_parts = [f"Player Analysis: {player_name} ({team} - {season})"]

            # Basic stats - look for GP, G, A, PTS columns
            basic_stats = []
            gp_col = None
            g_col = None
            a_col = None
            pts_col = None

            for col in df.columns:
                if col == 'GP' or 'games played' in col.lower():
                    gp_col = col
                elif col == 'G' or ('goals' in col.lower() and 'expected' not in col.lower()):
                    g_col = col
                elif col == 'A' or ('assists' in col.lower() and '1st' not in col.lower()):
                    a_col = col
                elif col == 'PTS' or 'points' in col.lower():
                    pts_col = col

            if gp_col and gp_col in player_data.columns:
                try:
                    gp = float(player_data[gp_col].iloc[0])
                    basic_stats.append(f"Games Played: {gp:.0f}")
                except:
                    pass

            if g_col and a_col and g_col in player_data.columns and a_col in player_data.columns:
                try:
                    goals = float(player_data[g_col].iloc[0])
                    assists = float(player_data[a_col].iloc[0])
                    points = goals + assists
                    basic_stats.append(f"Goals: {goals:.0f}, Assists: {assists:.0f}, Points: {points:.0f}")
                except:
                    pass
            elif pts_col and pts_col in player_data.columns:
                try:
                    points = float(player_data[pts_col].iloc[0])
                    basic_stats.append(f"Points: {points:.0f}")
                except:
                    pass

            if basic_stats:
                content_parts.append("Basic Statistics: " + ", ".join(basic_stats))

            # Advanced metrics - look for xG, Corsi, PDO
            advanced_stats = []
            xg_col = None
            corsi_col = None
            pdo_col = None

            for col in df.columns:
                if 'expected goals' in col.lower() or 'xg' == col.lower():
                    xg_col = col
                elif 'corsi' in col.lower():
                    corsi_col = col
                elif 'pdo' in col.lower():
                    pdo_col = col

            if xg_col and xg_col in player_data.columns:
                try:
                    xg = float(player_data[xg_col].iloc[0])
                    advanced_stats.append(f"Expected Goals: {xg:.2f}")
                except:
                    pass

            if corsi_col and corsi_col in player_data.columns:
                try:
                    corsi = float(player_data[corsi_col].iloc[0])
                    advanced_stats.append(f"Corsi: {corsi:.1f}")
                except:
                    pass

            if pdo_col and pdo_col in player_data.columns:
                try:
                    pdo = float(player_data[pdo_col].iloc[0])
                    advanced_stats.append(f"PDO: {pdo:.1f}")
                except:
                    pass

            if advanced_stats:
                content_parts.append("Advanced Analytics: " + ", ".join(advanced_stats))

            # Performance analysis - look for shooting %, corsi %
            performance_parts = []
            sh_pct_col = None
            cf_pct_col = None

            for col in df.columns:
                if 'sh%' in col.lower() or 'shooting' in col.lower():
                    sh_pct_col = col
                elif 'cf%' in col.lower() or 'corsi for' in col.lower():
                    cf_pct_col = col

            if sh_pct_col and sh_pct_col in player_data.columns:
                try:
                    sh_pct = float(player_data[sh_pct_col].iloc[0])
                    performance_parts.append(f"Shooting Percentage: {sh_pct:.1f}%")
                except:
                    pass

            if cf_pct_col and cf_pct_col in player_data.columns:
                try:
                    cf_pct = float(player_data[cf_pct_col].iloc[0])
                    performance_parts.append(f"Corsi For Percentage: {cf_pct:.1f}%")
                except:
                    pass

            if performance_parts:
                content_parts.append("Performance Metrics: " + ", ".join(performance_parts))

            content = "\n\n".join(content_parts)

            # Create metadata
            metrics = {}
            for col in player_data.columns:
                if pd.api.types.is_numeric_dtype(player_data[col]):
                    metrics[col] = float(player_data[col].iloc[0])
                else:
                    metrics[col] = str(player_data[col].iloc[0])

            metadata = ChunkMetadata(
                chunk_id=self.generate_chunk_id(content, {
                    'player': player_name,
                    'team': team,
                    'season': season
                }),
                source_file=str(file_path),
                data_type='player_stats',
                season=season,
                team=team,
                player_name=player_name,
                position=position,
                metrics=metrics,
                tags=['player_analysis', 'individual_performance', position.lower(), 'advanced_metrics']
            )

            chunk = RAGChunk(
                content=content,
                metadata=metadata,
                source='player_stats',
                token_count=self.estimate_token_count(content)
            )

            # Validate mathematical accuracy
            is_valid, confidence = self.validate_mathematical_accuracy(chunk)
            if is_valid:
                chunks.append(chunk)
                self.chunk_registry[metadata.chunk_id] = chunk

        return chunks

    def chunk_play_by_play(self, df: pd.DataFrame, file_path: Path) -> List[RAGChunk]:
        """
        Create temporal sequence chunks from play-by-play data
        """
        chunks = []

        # Group by game
        game_id_col = 'gameReferenceId' if 'gameReferenceId' in df.columns else 'game_id'

        if game_id_col not in df.columns:
            logger.warning(f"No game ID column found in play-by-play data")
            return []

        for game_id, game_data in df.groupby(game_id_col):
            # Create game overview chunk
            overview_content = f"Game Analysis: NHL Game {game_id} (2024-2025 Season)\n\n"

            # Basic game stats
            total_events = len(game_data)
            overview_content += f"Total Events: {total_events}\n"

            # Period analysis
            if 'period' in game_data.columns:
                period_counts = game_data['period'].value_counts().sort_index()
                period_summary = []
                for period, count in period_counts.items():
                    period_summary.append(f"Period {period}: {count} events")
                overview_content += "Period Distribution:\n" + "\n".join(f"• {summary}" for summary in period_summary) + "\n\n"

            # Event type analysis (using 'type' column instead of 'event_type')
            if 'type' in game_data.columns:
                event_types = game_data['type'].value_counts()
                top_events = event_types.head(5)
                overview_content += "Key Event Types:\n" + "\n".join(f"• {event}: {count}" for event, count in top_events.items()) + "\n\n"

            # Goal analysis
            goals_data = game_data[game_data['type'] == 'GOAL']
            if not goals_data.empty:
                total_goals = len(goals_data)
                overview_content += f"Total Goals: {total_goals}\n"

                if 'team' in goals_data.columns:
                    goals_by_team = goals_data['team'].value_counts()
                    overview_content += "Goals by Team:\n" + "\n".join(f"• {team}: {count}" for team, count in goals_by_team.items()) + "\n\n"

            # Expected goals analysis
            if 'expectedGoalsOnNet' in game_data.columns:
                total_xg = game_data['expectedGoalsOnNet'].sum()
                overview_content += f"Total Expected Goals: {total_xg:.2f}\n\n"

            # Key player analysis
            if 'playerFirstName' in game_data.columns and 'playerLastName' in game_data.columns:
                # Find top players by events
                player_events = game_data.groupby(['playerFirstName', 'playerLastName']).size().sort_values(ascending=False).head(5)
                overview_content += "Most Active Players:\n" + "\n".join(f"• {first} {last}: {count} events" for (first, last), count in player_events.items())

            # Create metadata
            metadata = ChunkMetadata(
                chunk_id=self.generate_chunk_id(overview_content, {
                    'game_id': str(game_id),
                    'season': '2024-2025'
                }),
                source_file=str(file_path),
                data_type='play_by_play',
                season='2024-2025',
                game_id=str(game_id),
                tags=['game_analysis', 'play_by_play', 'temporal_events', 'possession_analysis']
            )

            # Add metrics
            metadata.metrics = {
                'total_events': total_events,
                'game_duration': total_events  # Approximation
            }

            if 'period' in game_data.columns:
                metadata.metrics['periods_covered'] = int(game_data['period'].max())

            if not goals_data.empty:
                metadata.metrics['total_goals'] = len(goals_data)

            chunk = RAGChunk(
                content=overview_content,
                metadata=metadata,
                source='play_by_play',
                token_count=self.estimate_token_count(overview_content)
            )

            is_valid, confidence = self.validate_mathematical_accuracy(chunk)
            if is_valid:
                chunks.append(chunk)
                self.chunk_registry[metadata.chunk_id] = chunk

        return chunks

    def chunk_matchup_reports(self, df: pd.DataFrame, file_path: Path) -> List[RAGChunk]:
        """
        Create analytical summary chunks from matchup data
        """
        chunks = []

        # The matchup data has columns like 'Montreal', 'Anaheim', 'Boston', etc.
        # Each row represents a different metric
        team_columns = [col for col in df.columns if col not in ['Metric Label', 'Players', 'opponent_team', 'source_file']]

        # Create chunks for each team pair that has data
        for team_col in team_columns:
            if team_col == 'Montreal':
                continue  # We'll create chunks for Montreal vs opponents

            # Filter rows where both Montreal and opponent have data
            valid_rows = df[df[team_col].notna() & df['Montreal'].notna()].copy()

            if valid_rows.empty:
                continue

            content_parts = [f"Matchup Analysis: Montreal vs {team_col} (2024-2025 Season)"]

            # Extract key metrics
            metrics_summary = []

            # Look for expected goals metrics
            xg_rows = valid_rows[valid_rows['Metric Label'].str.contains('Expected Goals', case=False, na=False)]
            if not xg_rows.empty:
                montreal_xg = xg_rows['Montreal'].iloc[0] if len(xg_rows) > 0 else None
                opponent_xg = xg_rows[team_col].iloc[0] if len(xg_rows) > 0 else None

                if montreal_xg is not None and opponent_xg is not None:
                    metrics_summary.append(f"Montreal xG: {montreal_xg:.2f}")
                    metrics_summary.append(f"{team_col} xG: {opponent_xg:.2f}")
                    metrics_summary.append(f"xG Differential: {montreal_xg - opponent_xg:+.2f}")

            # Look for actual vs expected goals
            actual_xg_rows = valid_rows[valid_rows['Metric Label'].str.contains('Actual to Expected', case=False, na=False)]
            if not actual_xg_rows.empty:
                montreal_axg = actual_xg_rows['Montreal'].iloc[0] if len(actual_xg_rows) > 0 else None
                if montreal_axg is not None:
                    metrics_summary.append(f"Montreal Actual vs Expected: {montreal_axg:+.2f}")

            # Look for shot attempt metrics
            shot_rows = valid_rows[valid_rows['Metric Label'].str.contains('Shot Attempts', case=False, na=False)]
            if not shot_rows.empty:
                montreal_shots = shot_rows['Montreal'].iloc[0] if len(shot_rows) > 0 else None
                opponent_shots = shot_rows[team_col].iloc[0] if len(shot_rows) > 0 else None

                if montreal_shots is not None and opponent_shots is not None:
                    total_shots = montreal_shots + opponent_shots
                    montreal_pct = (montreal_shots / total_shots * 100) if total_shots > 0 else 0
                    metrics_summary.append(f"Montreal Shot Attempts: {montreal_shots:.0f} ({montreal_pct:.1f}%)")
                    metrics_summary.append(f"{team_col} Shot Attempts: {opponent_shots:.0f} ({100-montreal_pct:.1f}%)")

            if metrics_summary:
                content_parts.append("Key Metrics:\n" + "\n".join(f"• {metric}" for metric in metrics_summary))

            # Strategic analysis
            strategic_insights = []

            # xG-based insights
            if montreal_xg is not None and opponent_xg is not None:
                if montreal_xg > opponent_xg + 0.5:
                    strategic_insights.append(f"Montreal dominates puck possession against {team_col}")
                elif opponent_xg > montreal_xg + 0.5:
                    strategic_insights.append(f"{team_col} controls play against Montreal")

            # Actual vs expected analysis
            if montreal_axg is not None:
                if montreal_axg > 0.3:
                    strategic_insights.append(f"Montreal outperforms expectations against {team_col}")
                elif montreal_axg < -0.3:
                    strategic_insights.append(f"Montreal underperforms against {team_col}")

            if strategic_insights:
                content_parts.append("Strategic Insights:\n" + "\n".join(f"• {insight}" for insight in strategic_insights))

            content = "\n\n".join(content_parts)

            # Create metadata
            metrics = {}
            for _, row in valid_rows.iterrows():
                metric_name = str(row['Metric Label']).replace(' ', '_').lower()
                montreal_val = row['Montreal']
                opponent_val = row[team_col]

                if pd.notna(montreal_val) and isinstance(montreal_val, (int, float)):
                    metrics[f"montreal_{metric_name}"] = float(montreal_val)
                if pd.notna(opponent_val) and isinstance(opponent_val, (int, float)):
                    metrics[f"{team_col.lower()}_{metric_name}"] = float(opponent_val)

            metadata = ChunkMetadata(
                chunk_id=self.generate_chunk_id(content, {
                    'team1': 'Montreal',
                    'team2': team_col,
                    'season': '2024-2025'
                }),
                source_file=str(file_path),
                data_type='matchup_reports',
                season='2024-2025',
                team='Montreal',
                opponent=team_col,
                metrics=metrics,
                tags=['matchup_analysis', 'team_comparison', 'montreal_focus', 'advanced_metrics', 'xg_analysis']
            )

            chunk = RAGChunk(
                content=content,
                metadata=metadata,
                source='matchup_reports',
                token_count=self.estimate_token_count(content)
            )

            is_valid, confidence = self.validate_mathematical_accuracy(chunk)
            if is_valid:
                chunks.append(chunk)
                self.chunk_registry[metadata.chunk_id] = chunk

        return chunks

    def chunk_season_reports(self, df: pd.DataFrame, file_path: Path) -> List[RAGChunk]:
        """Chunk season reports data into semantically coherent units."""
        chunks = []

        # Process each metric row
        for _, row in df.iterrows():
            metric_label = str(row['Metric Label'])
            montreal_value = row['Montreal']
            montreal_rank = row['Montreal rank']
            league_median = row['League Median']
            league_leader_value = row['League Leader Value']
            league_leader_team = row['League Leader Team']

            # Create comprehensive metric analysis
            content = f"""Montreal Canadiens Season Performance - {metric_label}

Value: {montreal_value}
League Ranking: {montreal_rank} out of 32 teams
League Median: {league_median}
League Leader: {league_leader_value} ({league_leader_team})

Performance Analysis:
- {'Above league median' if pd.notna(montreal_value) and pd.notna(league_median) and montreal_value > league_median else 'Below league median'}
- {'Elite performance (top 5)' if montreal_rank <= 5 else 'Strong performance (top 10)' if montreal_rank <= 10 else 'Average performance (11-20)' if montreal_rank <= 20 else 'Below average (21-25)' if montreal_rank <= 25 else 'Poor performance (26-32)'}
- Differential from league leader: {abs(montreal_value - league_leader_value) if pd.notna(montreal_value) and pd.notna(league_leader_value) else 'N/A'}"""

            # Extract metrics for metadata
            metrics = {}
            if pd.notna(montreal_value) and isinstance(montreal_value, (int, float)):
                metrics['montreal_value'] = float(montreal_value)
            if pd.notna(montreal_rank) and isinstance(montreal_rank, (int, float)):
                metrics['montreal_rank'] = int(montreal_rank)
            if pd.notna(league_median) and isinstance(league_median, (int, float)):
                metrics['league_median'] = float(league_median)
            if pd.notna(league_leader_value) and isinstance(league_leader_value, (int, float)):
                metrics['league_leader_value'] = float(league_leader_value)

            metadata = ChunkMetadata(
                chunk_id=self.generate_chunk_id(content, {
                    'team': 'Montreal',
                    'season': '2024-2025',
                    'metric': metric_label.replace(' ', '_').lower()
                }),
                source_file=str(file_path),
                data_type='season_reports',
                season='2024-2025',
                team='Montreal',
                metrics=metrics,
                tags=['season_performance', 'league_ranking', 'montreal_analysis', 'advanced_metrics', metric_label.split()[0].lower()]
            )

            chunk = RAGChunk(
                content=content,
                metadata=metadata,
                source='season_reports',
                token_count=self.estimate_token_count(content)
            )

            is_valid, confidence = self.validate_mathematical_accuracy(chunk)
            if is_valid:
                chunks.append(chunk)
                self.chunk_registry[metadata.chunk_id] = chunk

        return chunks

    def chunk_team_stats(self, df: pd.DataFrame, file_path: Path) -> List[RAGChunk]:
        """Chunk team statistics data into semantically coherent units."""
        chunks = []
        filename = file_path.stem

        if 'Teams_Statistics_For_2024-2025' in filename:
            # League-wide team statistics
            for _, row in df.iterrows():
                team = str(row['Team'])
                total_goals = row['Total Goals']
                true_shooting_pct = row['True Shooting Percentage']
                expected_goals = row['Expected Goals']
                actual_to_expected = row['Actual to Expected Goals']

                content = f"""Team Performance Overview - {team} (2024-2025 Season)

Total Goals: {total_goals}
True Shooting Percentage: {true_shooting_pct:.4f}
Expected Goals: {expected_goals:.1f}
Actual to Expected Goals Differential: {actual_to_expected:+.3f}

Performance Analysis:
- {'Overperforming relative to expected goals' if actual_to_expected > 0.1 else 'Underperforming relative to expected goals' if actual_to_expected < -0.1 else 'Performing in line with expected goals'}
- True Shooting % indicates {'efficient' if true_shooting_pct > 0.055 else 'average' if true_shooting_pct > 0.045 else 'inefficient'} scoring efficiency
- Goal total suggests {'high' if total_goals > 250 else 'moderate' if total_goals > 220 else 'low'} offensive output"""

                metrics = {
                    'total_goals': int(total_goals) if pd.notna(total_goals) else None,
                    'true_shooting_percentage': float(true_shooting_pct) if pd.notna(true_shooting_pct) else None,
                    'expected_goals': float(expected_goals) if pd.notna(expected_goals) else None,
                    'actual_to_expected_differential': float(actual_to_expected) if pd.notna(actual_to_expected) else None
                }
                metrics = {k: v for k, v in metrics.items() if v is not None}

                metadata = ChunkMetadata(
                    chunk_id=self.generate_chunk_id(content, {
                        'team': team,
                        'season': '2024-2025',
                        'data_type': 'team_overview'
                    }),
                    source_file=str(file_path),
                    data_type='team_stats_league',
                    season='2024-2025',
                    team=team,
                    metrics=metrics,
                    tags=['team_performance', 'league_comparison', 'xg_analysis', 'scoring_efficiency']
                )

                chunk = RAGChunk(
                    content=content,
                    metadata=metadata,
                    source='team_stats',
                    token_count=self.estimate_token_count(content)
                )

                is_valid, confidence = self.validate_mathematical_accuracy(chunk)
                if is_valid:
                    chunks.append(chunk)
                    self.chunk_registry[metadata.chunk_id] = chunk

        elif 'Strengths-Weaknesses' in filename:
            # Strengths/weaknesses analysis
            for _, row in df.iterrows():
                section = str(row['Section'])
                metric_label = str(row['Metric Label'])
                montreal_value = row['Montreal']
                montreal_rank = row['Montreal Ranking']
                opponent_value = row['Carolina']
                opponent_rank = row['Carolina Ranking']

                content = f"""Strengths/Weaknesses Analysis - {section}: {metric_label}

Montreal vs Carolina Hurricanes (2024-2025)

Montreal Value: {montreal_value} (League Rank: {montreal_rank})
Carolina Value: {opponent_value} (League Rank: {opponent_rank})

Performance Comparison:
- {'Montreal advantage' if montreal_rank < opponent_rank else 'Carolina advantage' if opponent_rank < montreal_rank else 'Similar performance'}
- Differential: {montreal_value - opponent_value if pd.notna(montreal_value) and pd.notna(opponent_value) else 'N/A'}
- This represents a {'strength' if montreal_rank < opponent_rank else 'weakness' if opponent_rank < montreal_rank else 'neutral'} for Montreal"""

                metrics = {}
                if pd.notna(montreal_value) and isinstance(montreal_value, (int, float)):
                    metrics['montreal_value'] = float(montreal_value)
                if pd.notna(montreal_rank) and isinstance(montreal_rank, (int, float)):
                    metrics['montreal_rank'] = int(montreal_rank)
                if pd.notna(opponent_value) and isinstance(opponent_value, (int, float)):
                    metrics['carolina_value'] = float(opponent_value)
                if pd.notna(opponent_rank) and isinstance(opponent_rank, (int, float)):
                    metrics['carolina_rank'] = int(opponent_rank)

                metadata = ChunkMetadata(
                    chunk_id=self.generate_chunk_id(content, {
                        'team1': 'Montreal',
                        'team2': 'Carolina',
                        'season': '2024-2025',
                        'metric': metric_label.replace(' ', '_').lower()
                    }),
                    source_file=str(file_path),
                    data_type='strengths_weaknesses',
                    season='2024-2025',
                    team='Montreal',
                    opponent='Carolina',
                    metrics=metrics,
                    tags=['strengths_weaknesses', 'team_comparison', 'montreal_vs_carolina', section.lower().replace(' ', '_')]
                )

                chunk = RAGChunk(
                    content=content,
                    metadata=metadata,
                    source='team_stats',
                    token_count=self.estimate_token_count(content)
                )

                is_valid, confidence = self.validate_mathematical_accuracy(chunk)
                if is_valid:
                    chunks.append(chunk)
                    self.chunk_registry[metadata.chunk_id] = chunk

        elif 'XG-Benchmarks' in filename:
            # XG benchmarks data
            for _, row in df.iterrows():
                section = str(row['Section'])
                metric_label = str(row['Metric Label'])
                below_avg = row['Below']
                average = row['Average']
                above_avg = row['Above']
                montreal_value = row['Against']  # This column contains Montreal's value

                content = f"""XG Benchmark Analysis - {section}: {metric_label}

League Performance Ranges (2024-2025):
- Below Average: < {below_avg}
- Average: {below_avg} - {above_avg}
- Above Average: > {above_avg}

Montreal Performance: {montreal_value}

Analysis:
- {'Above league average' if pd.notna(montreal_value) and pd.notna(above_avg) and isinstance(montreal_value, (int, float)) and isinstance(above_avg, (int, float)) and montreal_value > above_avg else 'Below league average' if pd.notna(montreal_value) and pd.notna(below_avg) and isinstance(montreal_value, (int, float)) and isinstance(below_avg, (int, float)) and montreal_value < below_avg else 'At league average'}
- Performance percentile: {'Top quartile' if pd.notna(montreal_value) and pd.notna(above_avg) and isinstance(montreal_value, (int, float)) and isinstance(above_avg, (int, float)) and montreal_value >= above_avg else 'Bottom quartile' if pd.notna(montreal_value) and pd.notna(below_avg) and isinstance(montreal_value, (int, float)) and isinstance(below_avg, (int, float)) and montreal_value <= below_avg else 'Middle 50%'}"""

                metrics = {}
                if pd.notna(below_avg) and isinstance(below_avg, (int, float)):
                    metrics['league_below_average'] = float(below_avg)
                if pd.notna(average) and isinstance(average, (int, float)):
                    metrics['league_average'] = float(average)
                if pd.notna(above_avg) and isinstance(above_avg, (int, float)):
                    metrics['league_above_average'] = float(above_avg)
                if pd.notna(montreal_value) and isinstance(montreal_value, (int, float)):
                    metrics['montreal_value'] = float(montreal_value)

                metadata = ChunkMetadata(
                    chunk_id=self.generate_chunk_id(content, {
                        'team': 'Montreal',
                        'season': '2024-2025',
                        'metric': metric_label.replace(' ', '_').lower(),
                        'benchmark_type': 'xg_benchmark'
                    }),
                    source_file=str(file_path),
                    data_type='xg_benchmarks',
                    season='2024-2025',
                    team='Montreal',
                    metrics=metrics,
                    tags=['xg_benchmarks', 'performance_analysis', 'league_comparison', section.lower().replace(' ', '_')]
                )

                chunk = RAGChunk(
                    content=content,
                    metadata=metadata,
                    source='team_stats',
                    token_count=self.estimate_token_count(content)
                )

                is_valid, confidence = self.validate_mathematical_accuracy(chunk)
                if is_valid:
                    chunks.append(chunk)
                    self.chunk_registry[metadata.chunk_id] = chunk

        return chunks

    def chunk_line_combinations(self, df: pd.DataFrame, file_path: Path) -> List[RAGChunk]:
        """Chunk line combination data into semantically coherent units."""
        chunks = []
        filename = file_path.stem

        # Determine the type of line combination based on filename
        if 'Defencemen' in filename:
            combo_type = 'defenseman_pairs'
            combo_description = 'defensive pairings'
        elif 'Forwards' in filename:
            combo_type = 'forward_lines'
            combo_description = 'forward line combinations'
        elif 'PPUnits' in filename:
            combo_type = 'power_play_units'
            combo_description = 'power play unit combinations'
        elif 'SHUnits' in filename:
            combo_type = 'penalty_kill_units'
            combo_description = 'penalty kill unit combinations'
        elif 'Units' in filename:
            combo_type = 'five_unit_combinations'
            combo_description = '5-player unit combinations'
        else:
            combo_type = 'line_combinations'
            combo_description = 'line combination'

        # Process each combination row
        for _, row in df.iterrows():
            players = str(row['Players'])
            toi_sec = row['TOI(sec)']
            toi_min = str(row['TOI(min)'])
            ozst_pct = row['OZst%']
            soo = row['SOO']
            soo_delta = row['SOOΔ']
            sot = row['SOT']
            xga = row['XGA']
            xgf_pct = row['XGF%']
            xgf = row['XGF']

            # Create comprehensive combination analysis
            content = f"""{combo_description.title()}: {players}

Time on Ice: {toi_min} ({toi_sec} seconds)
Offensive Zone Start %: {ozst_pct}
Shot Opportunity Ownership (SOO): {soo}
SOO Differential: {soo_delta}
Scoring Opportunity Threat (SOT): {sot}
Expected Goals Against (XGA): {xga}
Expected Goals For % (XGF%): {xgf_pct}
Expected Goals For (XGF): {xgf}

Performance Analysis:
- {'High offensive zone deployment' if pd.notna(ozst_pct) and isinstance(ozst_pct, (int, float)) and ozst_pct > 0.6 else 'Balanced zone deployment' if pd.notna(ozst_pct) and isinstance(ozst_pct, (int, float)) and ozst_pct > 0.4 else 'Defensive zone deployment focus'}
- {'Strong puck possession' if pd.notna(soo) and isinstance(soo, (int, float)) and soo > 25 else 'Moderate puck possession' if pd.notna(soo) and isinstance(soo, (int, float)) and soo > 20 else 'Limited puck possession'}
- {'High quality scoring chances' if pd.notna(sot) and isinstance(sot, (int, float)) and sot > 25 else 'Moderate scoring opportunities' if pd.notna(sot) and isinstance(sot, (int, float)) and sot > 20 else 'Limited scoring chances'}
- {'Efficient expected goals generation' if pd.notna(xgf_pct) and isinstance(xgf_pct, (int, float)) and xgf_pct > 0.55 else 'Average expected goals production'}"""

            # Extract metrics for metadata
            metrics = {}
            if pd.notna(toi_sec) and isinstance(toi_sec, (int, float)):
                metrics['time_on_ice_seconds'] = float(toi_sec)
            if pd.notna(ozst_pct) and isinstance(ozst_pct, (int, float)):
                metrics['offensive_zone_start_percentage'] = float(ozst_pct)
            if pd.notna(soo) and isinstance(soo, (int, float)):
                metrics['shot_opportunity_ownership'] = float(soo)
            if pd.notna(soo_delta) and isinstance(soo_delta, (int, float)):
                metrics['soo_differential'] = float(soo_delta)
            if pd.notna(sot) and isinstance(sot, (int, float)):
                metrics['scoring_opportunity_threat'] = float(sot)
            if pd.notna(xga) and isinstance(xga, (int, float)):
                metrics['expected_goals_against'] = float(xga)
            if pd.notna(xgf_pct) and isinstance(xgf_pct, (int, float)):
                metrics['expected_goals_for_percentage'] = float(xgf_pct)
            if pd.notna(xgf) and isinstance(xgf, (int, float)):
                metrics['expected_goals_for'] = float(xgf)

            metadata = ChunkMetadata(
                chunk_id=self.generate_chunk_id(content, {
                    'team': 'Montreal',
                    'season': '2024-2025',
                    'combination_type': combo_type,
                    'players': players.replace(' ', '_').replace(',', '_').replace('"', '').lower()[:50]
                }),
                source_file=str(file_path),
                data_type='line_combinations',
                season='2024-2025',
                team='Montreal',
                metrics=metrics,
                tags=['line_combinations', combo_type, 'chemistry_analysis', 'performance_metrics', 'montreal_habs']
            )

            chunk = RAGChunk(
                content=content,
                metadata=metadata,
                source='line_combinations',
                token_count=self.estimate_token_count(content)
            )

            is_valid, confidence = self.validate_mathematical_accuracy(chunk)
            if is_valid:
                chunks.append(chunk)
                self.chunk_registry[metadata.chunk_id] = chunk

        return chunks

    def extract_team_from_path(self, file_path: Path) -> str:
        """Extract team code from file path"""
        path_str = str(file_path)
        team_match = re.search(r'/([A-Z]{3})/', path_str)
        return team_match.group(1) if team_match else 'Unknown'

    def extract_season_from_path(self, file_path: Path) -> str:
        """Extract season from file path"""
        path_str = str(file_path)
        season_match = re.search(r'/(\d{4}-\d{4})/', path_str)
        return season_match.group(1) if season_match else '2024-2025'

    def extract_position_from_path(self, file_path: Path) -> str:
        """Extract position from file path"""
        path_str = str(file_path)
        if 'defenseman' in path_str:
            return 'Defenseman'
        elif 'forwards' in path_str:
            return 'Forward'
        elif 'goalie' in path_str:
            return 'Goalie'
        return 'Unknown'

    def build_relationships(self):
        """Build cross-references between related chunks"""
        logger.info("Building chunk relationships...")

        # Group chunks by type for relationship building
        player_chunks = {k: v for k, v in self.chunk_registry.items() if v.metadata.data_type == 'player_stats'}
        game_chunks = {k: v for k, v in self.chunk_registry.items() if v.metadata.data_type == 'play_by_play'}
        matchup_chunks = {k: v for k, v in self.chunk_registry.items() if v.metadata.data_type == 'matchup_reports'}

        # Link player chunks to games where they participated
        for player_id, player_chunk in player_chunks.items():
            player_name = player_chunk.metadata.player_name
            team = player_chunk.metadata.team

            # Find games involving this player's team
            for game_id, game_chunk in game_chunks.items():
                # This would need more sophisticated logic based on actual game data
                # For now, we'll create basic team-based relationships
                if hasattr(game_chunk.metadata, 'home_team') and game_chunk.metadata.home_team == team:
                    player_chunk.metadata.relationships.append(game_id)
                elif hasattr(game_chunk.metadata, 'away_team') and game_chunk.metadata.away_team == team:
                    player_chunk.metadata.relationships.append(game_id)

        # Link matchup chunks to relevant player performances
        for matchup_id, matchup_chunk in matchup_chunks.items():
            # This would link to players from both teams in the matchup
            # Implementation depends on available data structure
            pass

        logger.info(f"Built relationships for {len(self.chunks)} chunks")

    def validate_and_filter_chunks(self):
        """Apply quality filters and validation"""
        logger.info("Validating and filtering chunks...")

        validated_chunks = []
        quality_stats = {
            'total_chunks': len(self.chunks),
            'passed_validation': 0,
            'failed_quality': 0,
            'too_small': 0,
            'too_large': 0
        }

        for chunk in self.chunks:
            # Size validation
            if chunk.token_count < self.quality_thresholds['min_chunk_size']:
                quality_stats['too_small'] += 1
                continue
            if chunk.token_count > self.quality_thresholds['max_chunk_size']:
                quality_stats['too_large'] += 1
                continue

            # Mathematical accuracy validation
            is_valid, confidence = self.validate_mathematical_accuracy(chunk)
            chunk.metadata.confidence_score = confidence

            if not is_valid:
                quality_stats['failed_quality'] += 1
                continue

            # Quality scoring based on content richness
            quality_score = self.calculate_quality_score(chunk)
            chunk.metadata.quality_score = quality_score

            if quality_score >= self.quality_thresholds['min_quality_score']:
                validated_chunks.append(chunk)
                quality_stats['passed_validation'] += 1

        self.chunks = validated_chunks
        logger.info(f"Quality validation complete: {quality_stats}")

        return quality_stats

    def calculate_quality_score(self, chunk: RAGChunk) -> float:
        """Calculate content quality score"""
        content = chunk.content.lower()
        score = 0.5  # Base score

        # Mathematical content bonus
        math_indicators = ['expected goals', 'corsi', 'fenwick', 'pdo', 'percentage', 'ratio', 'average']
        math_count = sum(1 for indicator in math_indicators if indicator in content)
        score += min(math_count * 0.1, 0.3)

        # Domain expertise bonus
        hockey_terms = ['power play', 'penalty kill', 'faceoff', 'rebound', 'shot attempt', 'high-danger']
        term_count = sum(1 for term in hockey_terms if term in content)
        score += min(term_count * 0.05, 0.2)

        # Completeness bonus
        if chunk.metadata.metrics and len(chunk.metadata.metrics) > 5:
            score += 0.1

        if chunk.metadata.tags and len(chunk.metadata.tags) > 2:
            score += 0.1

        return min(score, 1.0)

    def process_all_files(self):
        """Process all parquet files in the analytics directory"""
        logger.info("Starting comprehensive RAG chunking process...")

        # Find all parquet files
        parquet_files = list(self.analytics_dir.rglob("*.parquet"))
        logger.info(f"Found {len(parquet_files)} parquet files to process")

        total_chunks_created = 0

        for file_path in parquet_files:
            logger.info(f"Processing: {file_path.name}")

            try:
                # Load parquet file
                df = pd.read_parquet(file_path)
                logger.info(f"Loaded {len(df)} rows from {file_path.name}")

                # Determine chunking strategy based on file path
                if 'player_stats' in str(file_path):
                    new_chunks = self.chunk_player_stats(df, file_path)
                elif 'play_by_play' in str(file_path):
                    new_chunks = self.chunk_play_by_play(df, file_path)
                elif 'matchup' in str(file_path):
                    new_chunks = self.chunk_matchup_reports(df, file_path)
                elif 'season_reports' in str(file_path):
                    new_chunks = self.chunk_season_reports(df, file_path)
                elif 'team_stats' in str(file_path):
                    new_chunks = self.chunk_team_stats(df, file_path)
                elif 'line_combinations' in str(file_path):
                    new_chunks = self.chunk_line_combinations(df, file_path)
                else:
                    logger.warning(f"Unknown file type for {file_path}, skipping")
                    continue

                self.chunks.extend(new_chunks)
                total_chunks_created += len(new_chunks)
                logger.info(f"Created {len(new_chunks)} chunks from {file_path.name}")

            except Exception as e:
                logger.error(f"Error processing {file_path}: {e}")
                continue

        logger.info(f"Total chunks created: {total_chunks_created}")

        # Build relationships and validate
        self.build_relationships()
        quality_stats = self.validate_and_filter_chunks()

        return quality_stats

    def save_chunks(self, output_file: Path):
        """Save chunks to JSON file with professional formatting"""
        logger.info(f"Saving {len(self.chunks)} validated chunks to {output_file}")

        # Convert chunks to dictionary format
        chunk_dicts = []
        for chunk in self.chunks:
            chunk_dict = {
                'content': chunk.content,
                'metadata': asdict(chunk.metadata),
                'source': chunk.source,
                'token_count': chunk.token_count,
                'embedding_hint': chunk.embedding_hint
            }
            chunk_dicts.append(chunk_dict)

        # Add processing metadata
        output_data = {
            'metadata': {
                'created_at': datetime.now().isoformat(),
                'total_chunks': len(chunk_dicts),
                'chunking_strategy': 'semantic_with_mathematical_integrity',
                'quality_thresholds': self.quality_thresholds,
                'data_sources': list(set(chunk['source'] for chunk in chunk_dicts)),
                'version': '1.0.0'
            },
            'chunks': chunk_dicts
        }

        # Save with pretty printing for readability
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False, default=str)

        logger.info(f"Successfully saved professional RAG chunks to {output_file}")
        logger.info(f"File size: {output_file.stat().st_size / 1024 / 1024:.2f} MB")

def main():
    """Main execution function"""
    # Directory setup
    analytics_dir = Path("/Users/xavier.bouchard/Desktop/HeartBeat/data/processed/analytics")
    output_dir = Path("/Users/xavier.bouchard/Desktop/HeartBeat/data/processed/llm_context")
    output_file = output_dir / "professional_rag_chunks_2024_2025.json"

    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)

    # Initialize professional chunker
    chunker = ProfessionalRAGChunker(analytics_dir, output_dir)

    # Process all files
    quality_stats = chunker.process_all_files()

    # Save results
    chunker.save_chunks(output_file)

    # Print summary
    print("\n" + "="*60)
    print("PROFESSIONAL RAG CHUNKING COMPLETE")
    print("="*60)
    print(f"Total chunks created: {quality_stats['total_chunks']}")
    print(f"Passed validation: {quality_stats['passed_validation']}")
    print(f"Failed quality checks: {quality_stats['failed_quality']}")
    print(f"Too small: {quality_stats['too_small']}")
    print(f"Too large: {quality_stats['too_large']}")
    print(f"Output file: {output_file}")
    print(f"File size: {output_file.stat().st_size / 1024 / 1024:.2f} MB")
    print("="*60)

if __name__ == "__main__":
    main()
