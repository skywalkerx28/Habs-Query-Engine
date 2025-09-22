#!/usr/bin/env python3
"""
Single Record Uploader for Pinecone

Uploads records one at a time to work within MCP tool limitations.
Provides progress tracking and resume capability.
"""

import json
import os
import time
from pathlib import Path
from typing import List, Dict, Any

def load_all_records() -> List[Dict[str, Any]]:
    """Load all records from sub-batch files"""
    
    sub_batch_files = sorted([f for f in os.listdir('.') if f.startswith('sub_batch_') and f.endswith('.json')])
    
    all_records = []
    
    for batch_file in sub_batch_files:
        print(f"Loading {batch_file}...")
        
        with open(batch_file, 'r') as f:
            batch_data = json.load(f)
        
        all_records.extend(batch_data)
    
    return all_records

def generate_single_upload_commands(records: List[Dict[str, Any]], start_index: int = 0):
    """Generate individual upload commands for each record"""
    
    print(f"=== SINGLE RECORD UPLOAD COMMANDS ===")
    print(f"Total records: {len(records)}")
    print(f"Starting from index: {start_index}")
    print()
    
    for i, record in enumerate(records[start_index:], start_index + 1):
        print(f"# Record {i}/{len(records)}: {record['id']}")
        print(f"# Type: {record['type']}")
        print(f"# Content: {record['content']}")
        print(f"# Command:")
        print(f"mcp_pinecone_upsert-records(")
        print(f"  name='heartbeat-unified-index',")
        print(f"  namespace='events',")
        print(f"  records=[{record['id']}]  # Load from record {i}")
        print(f")")
        print()
        
        # Show progress milestones
        if i % 50 == 0:
            print(f"# === MILESTONE {i} RECORDS ===")
            print(f"# Check progress: mcp_pinecone_describe-index-stats(name='heartbeat-unified-index')")
            print(f"# Expected events namespace count: {i}")
            print()
        
        # Show only first 20 commands to avoid overwhelming output
        if i - start_index >= 20:
            remaining = len(records) - i
            print(f"# ... and {remaining} more records to upload")
            print(f"# Continue with systematic single-record uploads")
            break

def create_progress_tracker():
    """Create progress tracking file"""
    
    progress = {
        "total_records": 1607,
        "uploaded_records": 10,  # Current count
        "last_uploaded_id": "recap-2024-25-g20046",
        "upload_start_time": time.time(),
        "milestones": {
            "50": False,
            "100": False,
            "500": False,
            "1000": False,
            "1607": False
        },
        "errors": [],
        "notes": "Single record upload method confirmed working. MCP tool limitation requires one record per call."
    }
    
    with open('upload_progress.json', 'w') as f:
        json.dump(progress, f, indent=2)
    
    print("Created upload_progress.json for tracking")

def show_current_status():
    """Show current upload status"""
    
    print("=== CURRENT UPLOAD STATUS ===")
    print("✅ Problem identified: MCP tool only processes first record in multi-record uploads")
    print("✅ Solution confirmed: Single record uploads work perfectly")
    print("✅ Records uploaded so far: 10/1607 (0.6%)")
    print()
    print("Successfully uploaded records:")
    uploaded_ids = [
        "recap-2024-25-g20006",  # MTL 1, TOR 0
        "recap-2024-25-g20164",  # MTL 3, WSH 6  
        "recap-2024-25-g20180",  # MTL 1, PIT 3
        "recap-2024-25-g20196",  # MTL 2, CGY 3
        "recap-2024-25-g20212",  # MTL 1, NYI 2
        "recap-2024-25-g20227",  # MTL 3, BUF 1
        "recap-2024-25-g20239",  # MTL 2, EDM 3
        "recap-2024-25-g20011",  # MTL 4, BOS 6 (just added)
        "recap-2024-25-g20027",  # MTL 4, OTT 1 (just added)
        "recap-2024-25-g20046",  # MTL 3, PIT 6 (just added)
    ]
    
    for i, record_id in enumerate(uploaded_ids, 1):
        print(f"  {i:2d}. {record_id}")

def main():
    """Main execution"""
    print("=== SINGLE RECORD UPLOADER ===")
    
    # Show current status
    show_current_status()
    
    # Load all records
    print(f"\nLoading all records from sub-batch files...")
    records = load_all_records()
    print(f"Loaded {len(records)} total records")
    
    # Create progress tracker
    create_progress_tracker()
    
    # Generate upload commands (showing first 20)
    generate_single_upload_commands(records, start_index=10)  # Start after current 10
    
    print(f"\n=== NEXT STEPS ===")
    print("1. Use MCP tool to upload each record individually")
    print("2. Monitor progress with describe-index-stats every 50 uploads")
    print("3. Update upload_progress.json as you go")
    print("4. Expected completion: 1607 records in events namespace")
    print()
    print("⚠️  CRITICAL: Only upload ONE record per MCP call")
    print("✅ Single record method confirmed working")

if __name__ == "__main__":
    main()
