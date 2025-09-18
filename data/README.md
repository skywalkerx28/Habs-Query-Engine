# HabsAI Data Organization

This directory contains all data sources for the Montreal Canadiens AI Query Engine. Data is organized by type and source for efficient processing and analysis.

## Directory Structure

```
data/
├── season_reports/           # High-level season summaries and team stats
│   ├── Season-Report-Montreal.csv
│   └── [additional season reports]
├── line_combinations/        # Line chemistry and pairing data
│   ├── forwards_combinations/    # Forward line combinations
│   │   ├── ForwardLine-[P1]-[P2]-[P3]-[Season]-[Analysis].csv
│   │   └── ForwardLines-[Season]-[Analysis].csv
│   ├── defenseman_combinations/  # Defense pair combinations
│   │   ├── DefensePair-[P1]-[P2]-[Season]-[Analysis].csv
│   │   └── DefensePairs-[Season]-[Analysis].csv
│   ├── power_play/              # Power play unit combinations
│   │   ├── PP-Unit-[Num]-[Players]-[Season]-[Analysis].csv
│   │   └── PowerPlay-[Season]-[Analysis].csv
│   ├── short_handed/           # Penalty kill combinations
│   │   ├── PK-Unit-[Num]-[Players]-[Season]-[Analysis].csv
│   │   └── PenaltyKill-[Season]-[Analysis].csv
│   └── [additional combination CSVs]
├── player_stats/            # Individual player performance data
│   └── [player-specific CSVs]
├── team_stats/              # Advanced team analytics and metrics
│   └── [team performance CSVs]
├── play_by_play/            # Raw event-level data (symlink to mtl_games_2024-2025)
└── processed/               # Derived datasets and processed files
    ├── embeddings/          # Generated vector embeddings
    ├── chunks/             # Text chunks for RAG
    └── aggregated/         # Pre-computed aggregations
```

## Data Types & Usage

### **Season Reports** (`season_reports/`)
- **Purpose**: High-level team performance summaries
- **Usage**: Strategic analysis, comparative insights, executive summaries
- **Example**: `Season-Report-Montreal.csv` - Advanced metrics (xG, Corsi, zone entries, etc.)
- **Processing**: Direct loading for dashboard displays and high-level queries

### **Line Combinations** (`line_combinations/`)
- **Purpose**: Player pairing data and chemistry metrics organized by situation
- **Usage**: Line effectiveness analysis, strategic recommendations, situational optimization
- **Processing**: Correlation with play-by-play data for combination analysis by game state

#### Situation-Specific Subdirectories:
```
line_combinations/
├── forwards_combinations/    # Even-strength forward line combinations
│   ├── ForwardLine-[P1]-[P2]-[P3]-[Season]-[Analysis].csv
│   └── ForwardLines-[Season]-[Analysis].csv
├── defenseman_combinations/  # Even-strength defense pair combinations
│   ├── DefensePair-[P1]-[P2]-[Season]-[Analysis].csv
│   └── DefensePairs-[Season]-[Analysis].csv
├── power_play/              # Man-advantage power play unit combinations
│   ├── PP-Unit-[Num]-[Players]-[Season]-[Analysis].csv
│   └── PowerPlay-[Season]-[Analysis].csv
├── short_handed/           # Man-down penalty kill combinations
│   ├── PK-Unit-[Num]-[Players]-[Season]-[Analysis].csv
│   └── PenaltyKill-[Season]-[Analysis].csv
├── 5_unit/                 # Full 5-player unit chemistry analysis
│   ├── Unit5-[F1]-[F2]-[F3]-[D1]-[D2]-[Season]-[Analysis].csv
│   └── Units5-[Season]-[Analysis].csv
└── [additional combination CSVs]
```

### **Player Stats** (`player_stats/`)
- **Purpose**: Individual and aggregate player performance data organized by position
- **Usage**: Player-specific queries, position comparisons, team performance analysis
- **Processing**: Player ID mapping and performance aggregation by position groups

#### Position-Specific Subdirectories:
```
player_stats/
├── forwards_stats/          # Forward player performance data
│   ├── Forward-[Player]-[Season]-[Metric].csv
│   ├── Forwards-[Season]-[Analysis].csv
│   └── README.md
├── defenseman_stats/        # Defenseman player performance data
│   ├── Defenseman-[Player]-[Season]-[Metric].csv
│   ├── DefensePair-[P1]-[P2]-[Season]-[Analysis].csv
│   └── README.md
└── all_skaters_stats/       # Team-wide skater performance analysis
    ├── AllSkaters-[Season]-[Analysis].csv
    ├── PositionComparison-[Season]-[Metric].csv
    └── README.md
```

### **Team Stats** (`team_stats/`)
- **Purpose**: Advanced team analytics and situational data
- **Usage**: Team performance analysis, opponent analysis
- **Processing**: Integration with play-by-play for comprehensive insights

### **Play-by-Play** (`play_by_play/`)
- **Purpose**: Granular event-level data
- **Usage**: Core RAG system, detailed event analysis
- **Source**: `../mtl_games_2024-2025/` (symlinked for consistency)

## Data Processing Pipeline

1. **Raw Data** → `data/[type]/` directories
2. **Cleaning** → `data/processed/aggregated/`
3. **Chunking** → `data/processed/chunks/` (for RAG)
4. **Embeddings** → `data/processed/embeddings/` (for vector search)

## File Naming Convention

```
[DataType]-[Team]-[Season]-[Description].csv
```

**Examples:**
- `Season-Report-Montreal-2024.csv`
- `Line-Chemistry-Montreal-2024.csv`
- `Player-Stats-Montreal-2024.csv`
- `PowerPlay-Analytics-Montreal-2024.csv`

## Data Quality Standards

- **Schema Consistency**: All files in a directory follow same structure
- **Naming Convention**: Descriptive, consistent file names
- **Documentation**: Each major file has header comments explaining fields
- **Compression**: Large files use `.parquet` or `.csv.gz` format
- **Metadata**: Include collection date, source, and version info

## Integration Points

- **Vector Database**: All data types feed into FAISS/Pinecone
- **LLM Context**: Rich metadata enables better query understanding
- **Analytics Engine**: Combined datasets for comprehensive insights

---

**Note**: This structure supports the phased development approach while maintaining scalability for future seasons and data types.
