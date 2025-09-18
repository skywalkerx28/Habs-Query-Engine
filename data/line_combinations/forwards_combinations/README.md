# Montreal Canadiens Forwards Line Combinations

This directory contains data and analysis for forward line combinations and chemistry during even-strength play.

## Data Types

### Individual Line Combinations
- **File Pattern**: `ForwardLine-[Player1]-[Player2]-[Player3]-[Season]-[AnalysisType].csv`
- **Examples**:
  - `ForwardLine-Suzuki-Caufield-Dach-2024-Chemistry.csv`
  - `ForwardLine-Armia-Slafkovsky-Newhook-2024-Performance.csv`
  - `ForwardLine-Evans-Pitlick-Pezzetta-2024-IceTime.csv`

### Line Group Analysis
- **File Pattern**: `ForwardLines-[Season]-[AnalysisType].csv`
- **Examples**:
  - `ForwardLines-2024-ChemistryMatrix.csv`
  - `ForwardLines-2024-UsagePatterns.csv`
  - `ForwardLines-2024-ScoringRates.csv`

### Line Matchups
- **File Pattern**: `ForwardLine-vs-[Opponent]-[Season]-[AnalysisType].csv`
- **Examples**:
  - `ForwardLine-vs-Boston-2024-Performance.csv`
  - `ForwardLine-vs-Toronto-2024-Chemistry.csv`

## Key Metrics for Forward Lines

### Chemistry & Performance
- Goals/assists per 60 minutes together
- Corsi/Fenwick when playing together
- Shot attempt differential
- Expected goals for/against
- Faceoff win percentage

### Usage Patterns
- Ice time distribution
- Zone start quality
- Quality of competition faced
- Shift length and recovery time

### Matchup Performance
- Performance vs specific opponent lines
- Zone entry success rates
- Defensive zone coverage
- Transition play effectiveness

## Usage in HabsAI

Forward line data is used for:
- Line optimization and player deployment
- Chemistry analysis for line construction
- Performance tracking across different situations
- Strategic planning for line matching

## Analysis Frameworks

### Line Chemistry Models
- Player compatibility scoring
- Performance correlation analysis
- Ice time optimization algorithms
- Line balance assessment

### Performance Tracking
- Goals/assists per minute together
- Shot attempt differentials
- Expected goals contribution
- Faceoff battle success

### Strategic Deployment
- Zone start quality assessment
- Opponent line matching
- Game state performance analysis
- Injury contingency planning

## Data Sources
- NHL play-by-play data with line identification
- Advanced analytics platforms
- Team performance tracking systems
- Manual line combination logging

## File Organization Strategy

### Primary Analysis Files
- Current season line combinations
- Historical line performance data
- Chemistry analysis reports

### Specialized Analytics
- Machine learning line optimization
- Predictive performance modeling
- Advanced statistical correlations

### Reporting Outputs
- Line performance reports
- Chemistry analysis summaries
- Optimization recommendations

## Integration with Other Data

This directory complements:
- **Forwards Stats**: Individual player performance data
- **Play-by-Play**: Granular event data for line analysis
- **Team Stats**: Overall team performance context

## Quality Assurance

### Data Validation
- Line combination accuracy verification
- Time-on-ice calculation validation
- Performance metric consistency checks
- Cross-reference with NHL official data

### Documentation Standards
- Clear player identification
- Time period specification
- Analysis methodology documentation
- Data source attribution

## Future Enhancements

### Planned Features
- Real-time line combination tracking
- Predictive chemistry modeling
- Automated line optimization algorithms
- Integration with video analysis systems

### Expansion Opportunities
- Historical line combination archives
- Advanced machine learning predictions
- Player development impact analysis
- Cross-season trend analysis
