#!/usr/bin/env python3
"""
Convert season reports and team stats CSV files to Parquet format for efficient storage and querying.

This script processes:
- Season reports (comprehensive Montreal season analytics)
- Team statistics (league-wide team performance metrics)
- Strengths/weaknesses analysis (team comparison data)
- XG benchmarks (expected goals benchmarking data)

All data is converted to Parquet format and organized in the processed analytics directory.
"""

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from pathlib import Path
import time
import logging
from typing import Optional, Tuple

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SeasonTeamStatsConverter:
    """Convert season reports and team statistics CSV files to Parquet format."""

    def __init__(self, base_dir: str = "/Users/xavier.bouchard/Desktop/HeartBeat"):
        self.base_dir = Path(base_dir)
        self.data_dir = self.base_dir / "data"
        self.processed_dir = self.data_dir / "processed" / "analytics"
        self.season_reports_dir = self.data_dir / "season_reports"
        self.team_stats_dir = self.data_dir / "team_stats"

        # Ensure processed directories exist
        self.processed_season_dir = self.processed_dir / "season_reports"
        self.processed_team_dir = self.processed_dir / "team_stats"

        self.processed_season_dir.mkdir(parents=True, exist_ok=True)
        self.processed_team_dir.mkdir(parents=True, exist_ok=True)

        logger.info(f"Initialized converter with base directory: {self.base_dir}")

    def find_csv_header_line(self, csv_path: Path) -> int:
        """
        Find the actual header line in CSV file, skipping comment lines that start with #.

        Args:
            csv_path: Path to the CSV file

        Returns:
            Line number (0-indexed) where the header starts
        """
        with open(csv_path, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                # Skip empty lines and comment lines
                if line.strip() and not line.strip().startswith('#'):
                    return i
        return 0

    def convert_csv_to_parquet(self, csv_path: Path, output_path: Path) -> Tuple[bool, str]:
        """
        Convert a single CSV file to Parquet format.

        Args:
            csv_path: Path to input CSV file
            output_path: Path for output Parquet file

        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            start_time = time.time()

            # Find the header line (skip comment lines)
            header_line = self.find_csv_header_line(csv_path)

            # Read CSV file starting from header line
            df = pd.read_csv(csv_path, header=header_line, encoding='utf-8')

            # Clean column names (remove extra whitespace, handle special characters)
            df.columns = df.columns.str.strip()

            # Basic data cleaning
            df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

            read_time = time.time() - start_time
            logger.info(f"Read CSV file in {read_time:.2f} seconds")

            # Convert to PyArrow table and save as Parquet
            table = pa.Table.from_pandas(df)
            pq.write_table(table, output_path, compression='snappy')

            total_time = time.time() - start_time
            logger.info(f"Converted and saved Parquet file in {total_time:.2f} seconds")
            return True, f"Successfully converted {csv_path.name} ({len(df)} rows, {len(df.columns)} columns)"

        except Exception as e:
            error_msg = f"Failed to convert {csv_path.name}: {str(e)}"
            logger.error(error_msg)
            return False, error_msg

    def process_season_reports(self) -> Tuple[int, int]:
        """Process all season report CSV files."""
        logger.info("Processing season reports...")

        csv_files = list(self.season_reports_dir.glob("*.csv"))
        success_count = 0
        total_count = len(csv_files)

        for csv_file in csv_files:
            # Output filename: same name but .parquet extension
            output_file = self.processed_season_dir / f"{csv_file.stem}.parquet"

            success, message = self.convert_csv_to_parquet(csv_file, output_file)
            if success:
                success_count += 1
                logger.info(message)
            else:
                logger.error(message)

        return success_count, total_count

    def process_team_stats(self) -> Tuple[int, int]:
        """Process all team statistics CSV files."""
        logger.info("Processing team statistics...")

        csv_files = list(self.team_stats_dir.glob("*.csv"))
        success_count = 0
        total_count = len(csv_files)

        for csv_file in csv_files:
            # Output filename: same name but .parquet extension
            output_file = self.processed_team_dir / f"{csv_file.stem}.parquet"

            success, message = self.convert_csv_to_parquet(csv_file, output_file)
            if success:
                success_count += 1
                logger.info(message)
            else:
                logger.error(message)

        return success_count, total_count

    def run_conversion(self) -> None:
        """Run the complete conversion process for all season and team statistics files."""
        logger.info("Starting conversion of season reports and team statistics to Parquet format")

        total_success = 0
        total_files = 0

        # Process season reports
        season_success, season_total = self.process_season_reports()
        total_success += season_success
        total_files += season_total

        # Process team statistics
        team_success, team_total = self.process_team_stats()
        total_success += team_success
        total_files += team_total

        logger.info(f"Conversion complete: {total_success}/{total_files} files successfully converted")

        if total_success < total_files:
            logger.warning(f"Failed to convert {total_files - total_success} files")
        else:
            logger.info("All files converted successfully!")

def main():
    """Main entry point for the conversion script."""
    converter = SeasonTeamStatsConverter()
    converter.run_conversion()

if __name__ == "__main__":
    main()
