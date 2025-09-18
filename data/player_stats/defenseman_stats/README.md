# Montreal Canadiens Defenseman Statistics

This directory contains performance data and analytics specifically for defenseman players on the Montreal Canadiens.

## Data Types

### Individual Defenseman Performance
- **File Pattern**: `Defenseman-[PlayerName]-[Season]-[MetricType].csv`
- **Examples**:
  - `Defenseman-Guhle-2024-Defensive.csv`
  - `Defenseman-Savard-2024-Playmaking.csv`
  - `Defenseman-Edmundson-2024-Physical.csv`

### Defense Pair Analytics
- **File Pattern**: `DefensePair-[Player1]-[Player2]-[Season]-[AnalysisType].csv`
- **Examples**:
  - `DefensePair-Guhle-Savard-2024-ZoneExits.csv`
  - `DefensePair-Matheson-Xhekaj-2024-ShotSuppression.csv`

### Defensive Group Analytics
- **File Pattern**: `Defensemen-[Season]-[AnalysisType].csv`
- **Examples**:
  - `Defensemen-2024-ZoneExitEfficiency.csv`
  - `Defensemen-2024-ShotSuppression.csv`
  - `Defensemen-2024-PuckMoving.csv`

## Key Metrics for Defensemen

### Defensive Metrics
- Shot suppression (shots allowed per 60)
- Expected goals against per 60
- High-danger chance prevention
- Defensive zone coverage

### Puck Movement Metrics
- Zone exit success rate
- Controlled exit percentage
- First pass success rate
- Transition play involvement

### Physical Metrics
- Hits, blocked shots, takeaways
- Physical engagement in defensive zone
- Board battle win percentage
- Gap control effectiveness

### Offensive Contribution
- Power play points/assists
- Rush participation
- Offensive zone time percentage
- Playmaking from blue line

## Usage in HabsAI

Defenseman data is used for:
- Defense pair optimization
- Zone exit strategy analysis
- Defensive structure evaluation
- Transition game assessment

## Position-Specific Context

### Offensive Defensemen (e.g., Savard, Matheson)
- Higher focus on playmaking and power play contribution
- Rush participation and offensive zone time
- Point production and play drive

### Defensive Defensemen (e.g., Edmundson, Guhle)
- Emphasis on shot suppression and gap control
- Physical play and board battles
- Defensive zone coverage and exit prevention

### Two-Way Defensemen (e.g., Barron, Xhekaj)
- Balance of offensive and defensive metrics
- Transition play effectiveness
- Overall puck management

## Data Sources
- NHL play-by-play data
- Advanced defensive analytics
- Zone exit tracking systems
- Physical engagement monitoring
