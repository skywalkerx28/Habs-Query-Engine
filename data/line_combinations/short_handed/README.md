# Montreal Canadiens Short-Handed/Penalty Kill Combinations

This directory contains data and analysis for penalty kill/short-handed unit combinations and effectiveness during man-down situations.

## Data Types

### Penalty Kill Unit Combinations
- **File Pattern**: `PK-Unit-[UnitNumber]-[Players]-[Season]-[AnalysisType].csv`
- **Examples**:
  - `PK-Unit-1-Suzuki-Armia-Evans-Guhle-2024-Performance.csv`
  - `PK-Unit-2-Dach-Newhook-Pezzetta-Xhekaj-2024-Chemistry.csv`
  - `PK-Unit-1-Slafkovsky-Pitlick-Matheson-Edmundson-2024-ShotSuppression.csv`

### Penalty Kill Group Analysis
- **File Pattern**: `PenaltyKill-[Season]-[AnalysisType].csv`
- **Examples**:
  - `PenaltyKill-2024-UnitEffectiveness.csv`
  - `PenaltyKill-2024-ShotSuppression.csv`
  - `PenaltyKill-2024-ZoneExitPrevention.csv`

### Penalty Kill Matchups
- **File Pattern**: `PK-vs-[Opponent]-[Season]-[AnalysisType].csv`
- **Examples**:
  - `PK-vs-Boston-2024-Performance.csv`
  - `PK-vs-Toronto-2024-PowerPlayEffectiveness.csv`

## Key Metrics for Short-Handed Units

### Defensive Effectiveness
- Goals allowed per penalty kill opportunity
- Shot attempt suppression (Corsi/Fenwick against)
- High-danger chance prevention
- Zone exit denial success rate

### Puck Management
- Clear attempts and success rate
- Neutral zone pressure application
- Offensive zone time prevention
- Transition game control

### Situational Performance
- Performance by shorthanded time remaining
- Success rates by power play structure faced
- Home vs road performance
- Kill rate by infraction type

## Usage in HabsAI

Short-handed data is used for:
- Penalty kill unit optimization
- Defensive structure analysis during PK
- Strategic planning against specific power plays
- Performance tracking and improvement identification

## Analysis Frameworks

### Kill Rate Optimization
- Goals allowed per 2-minute penalty
- Kill percentage by situation
- Shot suppression effectiveness
- Clear success rate analysis

### Unit Chemistry Models
- Player positioning and responsibility alignment
- Chemistry scoring for PK units
- Communication and timing optimization
- Injury contingency planning

### Strategic Matchup Analysis
- Performance vs specific power play units
- Success rates by PP formation
- Optimal deployment strategies
- Risk assessment and management

## Penalty Kill Unit Structures

### Primary Kill Unit (PK1)
- Best defensive players and shot suppressors
- Most ice time in penalty kill situations
- Focus on preventing shots and maintaining possession
- Aggressive forechecking and pressure application

### Secondary Kill Unit (PK2)
- Complementary defensive players
- Deployment in medium-length penalties
- Focus on conservative gap control
- Emphasis on preventing transition opportunities

### Specialty Situations
- 5-on-3 emergency kill unit
- Double minor kill strategies
- Late-game penalty kill tactics
- High-danger zone protection units

## Data Sources
- NHL play-by-play data with penalty kill identification
- Advanced defensive analytics platforms
- Shot suppression and clear tracking systems
- Manual penalty kill combination logging

## File Organization Strategy

### Primary Analysis Files
- Current season penalty kill combinations
- Unit performance tracking
- Defensive analysis reports

### Specialized Analytics
- Shot suppression analysis
- Clear pattern recognition
- Power play matchup studies
- Machine learning optimization models

### Reporting Outputs
- Penalty kill performance reports
- Unit optimization recommendations
- Defensive deployment analysis
- Strategic planning documents

## Integration with Other Data

This directory complements:
- **Forwards Stats**: Individual forward performance in PK
- **Defenseman Stats**: Individual defenseman performance in PK
- **Play-by-Play**: Granular event data for PK analysis
- **Team Stats**: Overall penalty kill efficiency context

## Quality Assurance

### Data Validation
- Penalty kill situation identification
- Player on-ice time accuracy during PK
- Shot and goal attribution verification
- Cross-reference with NHL official data

### Documentation Standards
- Clear unit and player identification
- Penalty duration and type specification
- Analysis methodology documentation
- Opponent power play structure notes

## Future Enhancements

### Planned Features
- Real-time penalty kill unit tracking
- Predictive kill rate modeling
- Automated unit optimization algorithms
- Integration with defensive video analysis

### Expansion Opportunities
- Historical penalty kill combination archives
- Advanced machine learning predictions
- Player development impact on PK performance
- Cross-season penalty kill trend analysis
