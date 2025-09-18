# Montreal Canadiens Power Play Line Combinations

This directory contains data and analysis for power play unit combinations and effectiveness during man-advantage situations.

## Data Types

### Power Play Unit Combinations
- **File Pattern**: `PP-Unit-[UnitNumber]-[Players]-[Season]-[AnalysisType].csv`
- **Examples**:
  - `PP-Unit-1-Suzuki-Caufield-Dach-Savard-2024-Performance.csv`
  - `PP-Unit-2-Armia-Slafkovsky-Newhook-Guhle-2024-Chemistry.csv`
  - `PP-Unit-1-Suzuki-Caufield-Dach-Matheson-2024-ShotMap.csv`

### Power Play Group Analysis
- **File Pattern**: `PowerPlay-[Season]-[AnalysisType].csv`
- **Examples**:
  - `PowerPlay-2024-UnitEffectiveness.csv`
  - `PowerPlay-2024-ShotDistribution.csv`
  - `PowerPlay-2024-ZoneEntrySuccess.csv`

### Power Play Matchups
- **File Pattern**: `PP-vs-[Opponent]-[Season]-[AnalysisType].csv`
- **Examples**:
  - `PP-vs-Boston-2024-Performance.csv`
  - `PP-vs-Toronto-2024-PenaltyKillEffectiveness.csv`

## Key Metrics for Power Play Units

### Offensive Production
- Power play goals per opportunity
- Shot attempts per minute
- Expected goals generation
- High-danger chance creation
- Conversion rate on scoring chances

### Unit Chemistry
- Time to first shot
- Shot distribution across players
- Passing accuracy and sequencing
- Zone entry success rate
- One-timer generation

### Situational Performance
- Performance by power play time remaining
- Success rates by score differential
- Performance vs different penalty kill structures
- Home vs road performance

## Usage in HabsAI

Power play data is used for:
- Unit optimization and player deployment
- Chemistry analysis for power play construction
- Strategic planning against specific penalty kills
- Performance tracking and improvement identification

## Analysis Frameworks

### Unit Effectiveness Models
- Goals per 2-minute opportunity
- Expected goals per minute
- Shot attempt rate optimization
- Conversion rate analysis

### Player Deployment Analysis
- Optimal positioning and responsibilities
- Player contribution by role (bumper, quarterback, sniper)
- Chemistry and timing optimization
- Injury contingency planning

### Strategic Matchup Analysis
- Performance vs specific penalty kill units
- Success rates by PK structure
- Optimal deployment strategies
- Risk/reward analysis

## Power Play Unit Structures

### Unit 1 (Primary Unit)
- Typically best offensive players
- Most ice time in power play situations
- Focus on high-volume shot generation
- Complex offensive schemes and sequencing

### Unit 2 (Secondary Unit)
- Complementary offensive players
- Deployment in medium-length power plays
- Focus on maintaining possession and creating space
- Simpler, more direct offensive approaches

### Specialty Units
- Faceoff unit for offensive zone draws
- Rebound/cleanup unit for loose puck situations
- Umbrella/screening unit for shot blocking and tipping

## Data Sources
- NHL play-by-play data with power play identification
- Advanced power play analytics platforms
- Shot tracking and zone entry systems
- Manual power play combination logging

## File Organization Strategy

### Primary Analysis Files
- Current season power play combinations
- Unit performance tracking
- Chemistry analysis reports

### Specialized Analytics
- Shot map analysis
- Zone entry pattern recognition
- Penalty kill matchup studies
- Machine learning optimization models

### Reporting Outputs
- Power play performance reports
- Unit optimization recommendations
- Player deployment analysis
- Strategic planning documents

## Integration with Other Data

This directory complements:
- **Forwards Stats**: Individual forward performance in PP
- **Defenseman Stats**: Individual defenseman performance in PP
- **Play-by-Play**: Granular event data for PP analysis
- **Team Stats**: Overall power play efficiency context

## Quality Assurance

### Data Validation
- Power play situation identification
- Player on-ice time accuracy
- Shot and goal attribution verification
- Cross-reference with NHL official data

### Documentation Standards
- Clear unit and player identification
- Power play time period specification
- Analysis methodology documentation
- Opponent penalty kill structure notes

## Future Enhancements

### Planned Features
- Real-time power play unit tracking
- Predictive chemistry modeling
- Automated unit optimization algorithms
- Integration with video analysis for shot maps

### Expansion Opportunities
- Historical power play combination archives
- Advanced machine learning predictions
- Player development impact on PP performance
- Cross-season power play trend analysis
