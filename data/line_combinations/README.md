# Montreal Canadiens Line Combinations

This directory contains comprehensive player combination data and analysis for different game situations, enabling strategic optimization and performance evaluation.

## Directory Structure

```
line_combinations/
├── forwards_combinations/    # Even-strength forward line combinations
├── defenseman_combinations/  # Even-strength defense pair combinations
├── power_play/              # Man-advantage power play unit combinations
├── short_handed/           # Man-down penalty kill combinations
├── 5_unit/                 # Full 5-player unit chemistry analysis
└── README.md               # This file
```

## Situation-Based Organization

### Forwards Combinations (`forwards_combinations/`)
**Focus**: Offensive line chemistry during even-strength play
- Forward line performance metrics
- Chemistry analysis between wingers and centers
- Ice time distribution and usage patterns
- Scoring and playmaking effectiveness

### Defenseman Combinations (`defenseman_combinations/`)
**Focus**: Defensive pair chemistry during even-strength play
- Defense pair performance metrics
- Chemistry analysis between defensemen
- Zone exit and transition effectiveness
- Shot suppression and gap control

### Power Play (`power_play/`)
**Focus**: Man-advantage unit combinations and effectiveness
- Power play unit performance metrics
- Chemistry analysis for PP formations
- Zone entry and shot generation
- Conversion rates and efficiency

### Short Handed (`short_handed/`)
**Focus**: Man-down penalty kill combinations and effectiveness
- Penalty kill unit performance metrics
- Chemistry analysis for PK formations
- Shot suppression and clear effectiveness
- Kill rate and defensive structure

### 5-Unit Chemistry (`5_unit/`)
**Focus**: Full team chemistry and performance across all 5 positions
- Complete unit combination analysis
- Team-wide chemistry metrics
- Multi-positional compatibility
- Full roster synergy evaluation

## Key Performance Categories

### Chemistry & Performance
- Goals/assists per 60 minutes together
- Corsi/Fenwick differential when playing together
- Expected goals for/against
- Faceoff win percentage (for forwards)

### Usage Patterns
- Ice time distribution across situations
- Quality of competition faced
- Zone start quality and deployment
- Game state performance (leading/trailing)

### Situational Effectiveness
- Performance vs specific opponent units
- Success rates by score differential
- Home vs road performance splits
- Time of game effectiveness

## Usage in HabsAI

Line combination data is used for:
- Unit optimization and player deployment
- Chemistry analysis and compatibility scoring
- Strategic planning against specific opponents
- Performance tracking and improvement identification

## Analysis Frameworks

### Chemistry Models
- Player compatibility scoring algorithms
- Performance correlation analysis
- Chemistry matrix development
- Optimal combination identification

### Performance Tracking
- Goals/assists per minute together
- Shot attempt differentials
- Expected goals contribution
- Faceoff battle success rates

### Strategic Deployment
- Opponent-specific line matching
- Game state optimal deployments
- Injury contingency planning
- Line balance optimization

## Data Processing Pipeline

### Input Sources
- NHL play-by-play data with combination identification
- Advanced analytics platforms
- Team performance tracking systems
- Manual combination logging

### Processing Steps
1. **Combination Identification**: Extract player groupings from game data
2. **Performance Calculation**: Compute metrics for each combination
3. **Chemistry Analysis**: Analyze compatibility and effectiveness
4. **Optimization Modeling**: Develop combination optimization algorithms
5. **Reporting Generation**: Create combination analysis reports

### Output Formats
- CSV files with standardized naming conventions
- Combination performance reports
- Chemistry analysis summaries
- Optimization recommendations

## Integration with Other Data

This directory complements:
- **Player Stats**: Individual player performance within combinations
- **Play-by-Play**: Granular event data for combination analysis
- **Team Stats**: Overall team performance context
- **Season Reports**: Long-term combination trends

## File Naming Conventions

### Forward Lines
- `ForwardLine-[P1]-[P2]-[P3]-[Season]-[Analysis].csv`
- `ForwardLines-[Season]-[Analysis].csv`

### Defense Pairs
- `DefensePair-[P1]-[P2]-[Season]-[Analysis].csv`
- `DefensePairs-[Season]-[Analysis].csv`

### Power Play Units
- `PP-Unit-[Num]-[Players]-[Season]-[Analysis].csv`
- `PowerPlay-[Season]-[Analysis].csv`

### Penalty Kill Units
- `PK-Unit-[Num]-[Players]-[Season]-[Analysis].csv`
- `PenaltyKill-[Season]-[Analysis].csv`

## Quality Assurance

### Data Validation
- Combination accuracy verification
- Time-on-ice calculation validation
- Performance metric consistency checks
- Cross-reference with NHL official data

### Documentation Standards
- Clear player identification and positioning
- Time period and situation specification
- Analysis methodology documentation
- Performance context description

## Advanced Analytics

### Chemistry Algorithms
- Player compatibility matrix development
- Performance prediction modeling
- Combination optimization algorithms
- Machine learning-based recommendations

### Predictive Modeling
- Future combination performance forecasting
- Injury impact scenario planning
- Opponent-specific strategy development
- Seasonal trend analysis

## Future Enhancements

### Planned Features
- Real-time combination tracking and analysis
- Predictive chemistry modeling
- Automated combination optimization
- Integration with video analysis systems

### Expansion Opportunities
- Historical combination archives
- Advanced machine learning predictions
- Player development impact analysis
- Cross-season combination trend analysis

## Strategic Applications

### Coaching Applications
- Optimal line construction for different game situations
- Player deployment strategy development
- Opponent-specific combination planning
- Performance improvement identification

### Management Applications
- Player acquisition and trade analysis
- Contract and salary cap optimization
- Long-term team building strategy
- Performance benchmarking and evaluation

### Player Development Applications
- Individual skill development within combinations
- Chemistry building exercises and drills
- Performance feedback and improvement tracking
- Career progression planning and analysis
