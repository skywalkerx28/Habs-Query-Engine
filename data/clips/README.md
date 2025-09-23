# HeartBeat Engine - Video Clips Directory

## Directory Structure

### Season Organization
- `2024-2025/` - Current season clips
- `2025-2026/` - Next season clips

### Player Organization (Primary Structure)
Under each season folder:
```
[season]/
  players/
    [player_name]/
      [game_folder]/
```

Each player directory contains 82 game folders representing all regular season games:
- Game folders are named by opponent and **actual game date**: `vs_[team_name]_[date]`
- Dates are taken from the official Montreal Canadiens schedule
- Example: `vs_toronto_2024-10-09`, `vs_boston_2024-10-10`, `vs_ottawa_2024-10-12`
- All players have identical game folder structures for consistency
- 2025-2026 season uses the same opponent schedule but with 2025 dates

### Supporting Folders (Per Season)
- `metadata/` - Clip metadata and indexing files
- `thumbnails/` - Auto-generated video thumbnails

## Naming Conventions

### Clip Files
Format: `[player]_[event]_[time].mp4`
Example: `suzuki_goal_12-34.mp4`, `caufield_assist_08-15.mp4`

### Game Folders
Format: `vs_[team_name]_[date]`
Example: `vs_toronto_2024-11-13`, `vs_boston_2024-12-01`

## Integration with HeartBeat System

These clips will be automatically indexed by the HeartBeat orchestrator system and made available through natural language queries like:
- "Show me Suzuki's goals from last game"
- "Display our power play clips vs Toronto"  
- "Get Caufield's assists from the past 5 games"
