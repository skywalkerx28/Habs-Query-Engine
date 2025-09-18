# Montreal Canadiens Defenseman Pair Combinations

This directory contains data and analysis for defenseman pair combinations and chemistry during even-strength play.

## Data Types

### Defense Pair Combinations
- **File Pattern**: `DefensePair-[Player1]-[Player2]-[Season]-[AnalysisType].csv`
- **Examples**:
  - `DefensePair-Guhle-Savard-2024-Chemistry.csv`
  - `DefensePair-Hudson-Xhekaj-2024-Performance.csv`
  - `DefensePair-Matheson-Barron-2024-ZoneExits.csv`

### Pair Group Analysis
- **File Pattern**: `DefensePairs-[Season]-[AnalysisType].csv`
- **Examples**:
  - `DefensePairs-2024-ChemistryMatrix.csv`
  - `DefensePairs-2024-UsagePatterns.csv`
  - `DefensePairs-2024-ShotSuppression.csv`

### Pair Matchups
- **File Pattern**: `DefensePair-vs-[Opponent]-[Season]-[AnalysisType].csv`
- **Examples**:
  - `DefensePair-vs-Boston-2024-Performance.csv`
  - `DefensePair-vs-Toronto-2024-Chemistry.csv`

## Key Metrics for Defense Pairs

### Chemistry & Performance
- Goals/assists per 60 minutes together
- Shot attempt differential (Corsi/Fenwick)
- Expected goals for/against
- Puck possession time
- Zone exit success rate

### Defensive Impact
- Shot suppression effectiveness
- High-danger chance prevention
- Puck retrieval success
- Gap control and positioning

### Transition Play
- Zone entry denial success
- Breakout pass completion
- Neutral zone control
- Rush prevention effectiveness

## Usage in HabsAI

Defense pair data is used for:
- Pair optimization and player matching
- Defensive structure analysis
- Transition play evaluation
- Strategic deployment planning

## Analysis Frameworks

### Pair Chemistry Models
- Player compatibility scoring for defensive pairs
- Performance correlation analysis
- Ice time optimization for pair balance
- Defensive responsibility alignment

### Defensive Performance Tracking
- Shot attempt suppression metrics
- High-danger chance prevention
- Zone exit success rates
- Puck possession in defensive zone

### Strategic Deployment
- Opponent line matching for defense pairs
- Game state performance analysis
- Injury contingency pair planning
- Quality of competition assessment

## Position-Specific Considerations

### Offensive Defensemen Pairs (e.g., Savard-Guhle)
- Higher emphasis on offensive contribution
- Power play participation
- Rush joining and offensive zone time
- Playmaking and point production

### Defensive Defensemen Pairs (e.g., Edmundson-Xhekaj)
- Focus on shot suppression and gap control
- Physical play and board battles
- Defensive zone coverage
- Transition prevention

### Balanced Pairs (e.g., Matheson-Barron)
- Combination of offensive and defensive skills
- Versatile deployment across situations
- Consistent performance across game states
- All-around pair reliability

## Data Sources
- NHL play-by-play data with pair identification
- Advanced defensive analytics platforms
- Zone exit and transition tracking systems
- Manual pair combination logging

## File Organization Strategy

### Primary Analysis Files
- Current season pair combinations
- Historical pair performance data
- Chemistry analysis reports

### Specialized Analytics
- Machine learning pair optimization
- Predictive performance modeling
- Advanced defensive correlations

### Reporting Outputs
- Pair performance reports
- Chemistry analysis summaries
- Optimization recommendations

## Integration with Other Data

This directory complements:
- **Defenseman Stats**: Individual defenseman performance data
- **Play-by-Play**: Granular event data for pair analysis
- **Team Stats**: Overall defensive structure context

## Quality Assurance

### Data Validation
- Pair combination accuracy verification
- Time-on-ice calculation validation
- Defensive metric consistency checks
- Cross-reference with NHL official data

### Documentation Standards
- Clear player pair identification
- Time period specification
- Analysis methodology documentation
- Defensive focus specification

## Future Enhancements

### Planned Features
- Real-time pair combination tracking
- Predictive chemistry modeling
- Automated pair optimization algorithms
- Integration with defensive video analysis

### Expansion Opportunities
- Historical pair combination archives
- Advanced machine learning predictions
- Player development impact analysis
- Cross-season defensive trend analysis
