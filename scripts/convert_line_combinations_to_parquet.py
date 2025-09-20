#!/usr/bin/env python3
"""
Convert line combination CSV files to Parquet format for efficient storage and querying.

This script processes:
- Defenseman combinations (pair analysis)
- Forwards combinations (line chemistry)
- Power play units (special teams offensive combinations)
- Short-handed units (penalty kill combinations)
- 5-unit combinations (full team chemistry analysis)

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

class LineCombinationsConverter:
    """Convert line combination CSV files to Parquet format."""

    def __init__(self, base_dir: str = "/Users/xavier.bouchard/Desktop/HeartBeat"):
        self.base_dir = Path(base_dir)
        self.data_dir = self.base_dir / "data"
        self.processed_dir = self.data_dir / "processed" / "analytics"
        self.line_combinations_dir = self.data_dir / "line_combinations"

        # Ensure processed directories exist
        self.processed_line_combinations_dir = self.processed_dir / "line_combinations"
        self.processed_line_combinations_dir.mkdir(parents=True, exist_ok=True)

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

    def process_line_combinations(self) -> Tuple[int, int]:
        """Process all line combination CSV files."""
        logger.info("Processing line combination CSV files...")

        csv_files = []
        # Find all CSV files in subdirectories, excluding example_files.txt
        for subdir in ['defenseman_combinations', 'forwards_combinations', 'power_play', 'short_handed', 'unit_5']:
            subdir_path = self.line_combinations_dir / subdir
            if subdir_path.exists():
                for csv_file in subdir_path.glob("*.csv"):
                    csv_files.append(csv_file)

        success_count = 0
        total_count = len(csv_files)

        logger.info(f"Found {total_count} line combination CSV files to process")

        for csv_file in csv_files:
            # Create subdirectory structure in processed folder
            relative_path = csv_file.relative_to(self.line_combinations_dir)
            output_file = self.processed_line_combinations_dir / f"{relative_path.stem}.parquet"

            success, message = self.convert_csv_to_parquet(csv_file, output_file)
            if success:
                success_count += 1
                logger.info(message)
            else:
                logger.error(message)

        return success_count, total_count

    def run_conversion(self) -> None:
        """Run the complete conversion process for all line combination files."""
        logger.info("Starting conversion of line combination CSV files to Parquet format")

        total_success, total_files = self.process_line_combinations()

        logger.info(f"Conversion complete: {total_success}/{total_files} files successfully converted")

        if total_success < total_files:
            logger.warning(f"Failed to convert {total_files - total_success} files")
        else:
            logger.info("All line combination files converted successfully!")

def main():
    """Main entry point for the conversion script."""
    converter = LineCombinationsConverter()
    converter.run_conversion()

if __name__ == "__main__":
    main()
