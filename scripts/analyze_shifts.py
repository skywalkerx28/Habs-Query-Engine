#!/usr/bin/env python3
"""
Analyze player shifts from unified play-by-play data.

This script calculates how many shifts a player made in a specific game
by analyzing their appearance in the on-ice player lists.
"""

import pandas as pd
import numpy as np
from pathlib import Path

def analyze_player_shifts(pbp_file: str, game_id: int, player_id: str):
    """
    Analyze shifts for a specific player in a specific game.

    Args:
        pbp_file: Path to the unified PBP parquet file
        game_id: Game ID to analyze
        player_id: Player ID to track shifts for
    """
    print(f"=== ANALYZING SHIFTS FOR PLAYER {player_id} IN GAME {game_id} ===")

    # Load the PBP data
    print(f"Loading PBP data from: {pbp_file}")
    df = pd.read_parquet(pbp_file)

    # Filter to specific game
    game_data = df[df['game_id'] == game_id].copy()
    print(f"Found {len(game_data)} total events in game {game_id}")

    if game_data.empty:
        print(f"No data found for game {game_id}")
        return

    # Sort by period and period_seconds to ensure chronological order
    game_data = game_data.sort_values(['period', 'period_seconds']).reset_index(drop=True)

    # Create a clean player ID for matching (remove .0 if present)
    clean_player_id = player_id.replace('.0', '')

    # Count every off-ice to on-ice transition as a shift
    # Also calculate total ice time by tracking continuous on-ice periods
    print(f"\nAnalyzing shifts and ice time for player {clean_player_id}...")
    print(f"Counting every off-ice to on-ice transition as a shift...")

    shift_count = 0
    total_ice_time = 0
    was_on_ice = False
    current_shift_start_time = None

    for idx, row in game_data.iterrows():
        on_ice_ids = row.get('on_ice_ids', [])

        # Convert numpy array to list if needed
        if isinstance(on_ice_ids, np.ndarray):
            on_ice_ids = on_ice_ids.tolist()

        # Clean the on_ice_ids (remove any .0 suffixes)
        if isinstance(on_ice_ids, list):
            on_ice_ids = [str(pid).replace('.0', '') for pid in on_ice_ids]

        current_time = row['period'] * 1200 + row['period_seconds']
        is_on_ice = clean_player_id in on_ice_ids

        # Track ice time
        if is_on_ice and not was_on_ice:
            # Player coming on ice - start tracking time
            current_shift_start_time = current_time
            shift_count += 1
            print(f"Shift {shift_count} START: Period {row['period']}, {row['period_seconds']:.1f}s ({row.get('event_type', 'unknown')})")

        elif not is_on_ice and was_on_ice and current_shift_start_time is not None:
            # Player going off ice - add time to total
            shift_duration = current_time - current_shift_start_time
            total_ice_time += shift_duration
            print(f"Shift {shift_count} END: Period {row['period']}, {row['period_seconds']:.1f}s - Duration: {shift_duration:.1f}s")
            current_shift_start_time = None

        was_on_ice = is_on_ice

    # Handle case where player is still on ice at end of game
    if current_shift_start_time is not None:
        # Use the last event time as end time
        last_time = game_data.iloc[-1]['period'] * 1200 + game_data.iloc[-1]['period_seconds']
        final_shift_duration = last_time - current_shift_start_time
        total_ice_time += final_shift_duration
        print(f"Shift {shift_count} END: Game end - Duration: {final_shift_duration:.1f}s")

    print(f"\nDetected {shift_count} shifts")
    print(f"Total ice time: {total_ice_time:.1f} seconds ({total_ice_time/60:.1f} minutes)")
    shifts = []

    print()

    print("=== SHIFT ANALYSIS SUMMARY ===")
    print(f"Player: {clean_player_id}")
    print(f"Game: {game_id}")
    print(f"Total shifts identified: {shift_count}")
    print(f"Total ice time: {total_ice_time:.1f} seconds ({total_ice_time/60:.1f} minutes)")

    if shift_count > 0:
        avg_shift_duration = total_ice_time / shift_count
        print(f"Average shift duration: {avg_shift_duration:.1f} seconds")

    return shift_count

def main():
    """Main function to run the shift analysis."""

    # File paths
    pbp_file = "/Users/xavier.bouchard/Desktop/HeartBeat/data/processed/fact/pbp/unified_pbp_2024-25.parquet"
    game_id = 20726
    player_id = "nhl_8479318.0"  # Auston Matthews

    # Run analysis
    shifts = analyze_player_shifts(pbp_file, game_id, player_id)

    print("\n=== FINAL RESULT ===")
    print(f"Auston Matthews made {shifts} shifts in game {game_id}")

if __name__ == "__main__":
    main()
