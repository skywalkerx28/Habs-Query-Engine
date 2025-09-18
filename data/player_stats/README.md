# Montreal Canadiens Player Statistics

This directory contains comprehensive player performance data for the Montreal Canadiens, organized by position for targeted analysis and insights.

## Directory Structure

```
player_stats/
├── forwards_stats/          # Forward player performance data
├── defenseman_stats/        # Defenseman player performance data
├── all_skaters_stats/       # Team-wide skater performance analysis
└── README.md               # This file
```

## Position-Based Organization

### Forwards Stats (`forwards_stats/`)
**Focus**: Offensive production, playmaking, and scoring efficiency
- Individual forward performance metrics
- Line chemistry and combination analysis
- Power play and penalty kill contributions
- Shooting and scoring opportunity creation

### Defenseman Stats (`defenseman_stats/`)
**Focus**: Defensive impact, puck movement, and transition play
- Individual defenseman performance metrics
- Defense pair chemistry and effectiveness
- Zone exit and entry prevention
- Power play quarterbacking and offensive contribution

### All Skaters Stats (`all_skaters_stats/`)
**Focus**: Team-wide player performance synthesis and comparisons
- Position-specific performance comparisons
- Team-wide contribution analysis
- Player rankings and percentiles
- Cross-position performance benchmarking

## Key Performance Categories

### Offensive Metrics
- Goals, assists, points per 60 minutes
- Shooting percentage and expected goals
- Scoring chance creation and conversion
- Power play efficiency

### Defensive Metrics
- Shot suppression and expected goals against
- Puck possession and zone control
- Transition play effectiveness
- Penalty killing performance

### Physical Metrics
- Hits, blocked shots, takeaways
- Physical engagement rate
- Board battle win percentage
- Forechecking effectiveness

### Advanced Analytics
- Corsi, Fenwick, PDO
- High-danger scoring chances
- Zone start quality
- Quality of competition faced

## Integration with HabsAI System

### Position-Specific Analysis
- **Forwards**: Individual scoring and playmaking evaluation
- **Defensemen**: Defensive pairing and transition analysis
- **All Skaters**: Team balance and deployment optimization

### Query Types Supported
- Individual player performance analysis
- Position-specific comparisons
- Line combination optimization
- Injury impact assessment
- Player development tracking

## Data Processing Pipeline

### Input Sources
- NHL play-by-play data
- Advanced analytics platforms
- Team performance tracking systems
- Manual performance logging

### Processing Steps
1. **Data Collection**: Gather raw player performance data
2. **Position Classification**: Organize by forwards/defensemen
3. **Metric Calculation**: Compute advanced analytics metrics
4. **Quality Validation**: Ensure data accuracy and completeness
5. **Analysis Generation**: Create position-specific insights

### Output Formats
- CSV files with standardized naming conventions
- Position-specific performance reports
- Comparative analysis across positions
- Individual player evaluation reports

## Usage Guidelines

### For Coaches & Analysts
- Use position-specific folders for targeted analysis
- Reference all_skaters_stats for team-wide insights
- Compare across positions for balanced evaluation

### For Player Development
- Individual player files in position folders
- Track progress against position benchmarks
- Identify development opportunities by position

### For Strategic Planning
- Line combination analysis in forwards folder
- Defense pairing evaluation in defenseman folder
- Team balance assessment in all_skaters folder

## File Naming Conventions

### Individual Players
- `Position-[PlayerName]-[Season]-[MetricType].csv`
- Examples: `Forward-Suzuki-2024-Shooting.csv`, `Defenseman-Guhle-2024-Defensive.csv`

### Group Analysis
- `Positions-[Season]-[AnalysisType].csv`
- Examples: `Forwards-2024-LineChemistry.csv`, `Defensemen-2024-ZoneExits.csv`

### Comparative Analysis
- `PositionComparison-[Season]-[MetricType].csv`
- `PlayerRankings-[Season]-[Category]-[PositionFilter].csv`

## Quality Assurance

### Data Validation
- Metric range checking
- Statistical outlier detection
- Cross-reference validation with NHL data
- Position-specific benchmark verification

### Documentation Standards
- Each file includes header documentation
- Metric definitions and calculations explained
- Data source and collection date recorded
- Quality score and validation status noted

## Future Enhancements

### Planned Features
- Real-time player performance monitoring
- Predictive analytics for player development
- Automated report generation
- Integration with video analysis systems

### Expansion Opportunities
- Goalie statistics integration
- Historical performance trend analysis
- Player health and injury correlation analysis
- Advanced machine learning performance predictions
