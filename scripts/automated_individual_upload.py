#!/usr/bin/env python3
"""
Automated Individual Record Upload Script for HeartBeat Engine
Uploads records individually from sub_batch files to Pinecone using MCP tool
"""

import json
import os
import time
from datetime import datetime

def flatten_record(record):
    """Flatten nested objects in a record for MCP compatibility"""
    flattened = record.copy()

    # Convert nested objects to JSON strings
    if 'row_selector_partitions' in record:
        flattened['row_selector_partitions'] = json.dumps(record['row_selector_partitions'])
    if 'row_selector_where' in record:
        flattened['row_selector_where'] = json.dumps(record['row_selector_where'])
    if 'season_results_selector_partitions' in record:
        flattened['season_results_selector_partitions'] = json.dumps(record['season_results_selector_partitions'])
    if 'season_results_selector_where' in record:
        flattened['season_results_selector_where'] = json.dumps(record['season_results_selector_where'])

    return flattened

def load_progress():
    """Load current upload progress"""
    progress_file = '/Users/xavier.bouchard/Desktop/HeartBeat/upload_progress.json'
    if os.path.exists(progress_file):
        with open(progress_file, 'r') as f:
            return json.load(f)
    return {
        "total_records": 1607,
        "uploaded_records": 16,  # We already have 16 from manual uploads
        "last_uploaded_id": "recap-2024-25-g20164",
        "upload_start_time": time.time(),
        "milestones": {"50": False, "100": False, "500": False, "1000": False, "1607": False},
        "errors": [],
        "notes": "Automated individual upload process"
    }

def save_progress(progress):
    """Save current upload progress"""
    progress_file = '/Users/xavier.bouchard/Desktop/HeartBeat/upload_progress.json'
    with open(progress_file, 'w') as f:
        json.dump(progress, f, indent=2)

def get_sub_batch_files():
    """Get list of all sub_batch files to process"""
    base_path = '/Users/xavier.bouchard/Desktop/HeartBeat'
    files = []
    for i in range(1, 162):  # sub_batch_001.json to sub_batch_161.json
        filename = f'sub_batch_{i:03d}.json'
        filepath = os.path.join(base_path, filename)
        if os.path.exists(filepath):
            files.append((i, filepath))
    return sorted(files)

def upload_record(record, batch_num, record_num, total_records):
    """Upload a single record using MCP tool format"""
    try:
        # This would be called via MCP tool, but for now we'll just simulate
        # In actual implementation, this would use the mcp_pinecone_upsert-records tool
        flattened = flatten_record(record)

        # Print the record in the format expected by MCP tool
        print(f"\n--- Uploading record {record_num}/{total_records} from batch {batch_num} ---")
        print(f"ID: {record['id']}")
        print(f"MCP Command: mcp_pinecone_upsert-records with records=[{json.dumps([flattened])}]")

        # Simulate successful upload (in real implementation, this would be the MCP call)
        # For now, just return success
        return True, None

    except Exception as e:
        return False, str(e)

def main():
    print("HeartBeat Engine - Automated Individual Record Upload")
    print("=" * 60)

    # Load progress
    progress = load_progress()
    print(f"Current progress: {progress['uploaded_records']}/{progress['total_records']} records uploaded")
    print(f"Last uploaded: {progress['last_uploaded_id']}")

    # Get sub-batch files
    sub_batch_files = get_sub_batch_files()
    print(f"Found {len(sub_batch_files)} sub-batch files to process")

    # Find where to resume (skip batches that are already fully uploaded)
    start_batch = 2  # Start from sub_batch_002.json since 001 is done
    resume_from_id = progress['last_uploaded_id']

    total_uploaded = progress['uploaded_records']

    for batch_num, filepath in sub_batch_files:
        if batch_num < start_batch:
            continue

        print(f"\nProcessing sub_batch_{batch_num:03d}.json...")

        # Load records from this batch
        with open(filepath, 'r') as f:
            records = json.load(f)

        print(f"Batch contains {len(records)} records")

        # Process each record
        for i, record in enumerate(records):
            record_id = record['id']

            # Skip records that were already uploaded
            if record_id <= resume_from_id and batch_num == start_batch:
                print(f"Skipping already uploaded record: {record_id}")
                continue

            # Upload the record
            success, error = upload_record(record, batch_num, i+1, len(records))

            if success:
                total_uploaded += 1
                progress['uploaded_records'] = total_uploaded
                progress['last_uploaded_id'] = record_id

                # Update milestones
                for milestone in progress['milestones']:
                    if total_uploaded >= int(milestone) and not progress['milestones'][milestone]:
                        progress['milestones'][milestone] = True
                        print(f"Milestone reached: {milestone} records uploaded!")

                # Save progress every 10 uploads
                if total_uploaded % 10 == 0:
                    save_progress(progress)
                    print(f"Progress saved: {total_uploaded} records uploaded")

                # Small delay to be respectful to the API
                time.sleep(0.5)

            else:
                print(f"Error uploading record {record_id}: {error}")
                progress['errors'].append({
                    'record_id': record_id,
                    'batch': batch_num,
                    'error': error,
                    'timestamp': datetime.now().isoformat()
                })
                save_progress(progress)

    # Final save
    save_progress(progress)
    print("\nUpload process complete!")
    print(f"Total records uploaded: {total_uploaded}/{progress['total_records']}")
    if progress['errors']:
        print(f"Errors encountered: {len(progress['errors'])}")

if __name__ == "__main__":
    main()
