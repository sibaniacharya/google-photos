import csv
import json
import uuid
import argparse
from datetime import datetime

def import_csv(csv_file: str, json_file: str):
    """
    Imports records from a CSV file (e.g., from Reddit, App Store) into the main real_data.json.
    Expected CSV columns: source, source_url, author_id, date, rating, title, text, language
    """
    with open(json_file, 'r', encoding='utf-8') as f:
        try:
            existing_data = json.load(f)
        except json.JSONDecodeError:
            existing_data = []
            
    new_records = []
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            record = {
                "record_id": str(uuid.uuid4())[:8],
                "source": row.get('source', 'Unknown CSV Import'),
                "source_url": row.get('source_url', ''),
                "author_id": row.get('author_id', 'Anonymous'),
                "date": row.get('date', datetime.now().isoformat()),
                "rating": int(row['rating']) if row.get('rating') and row['rating'].isdigit() else None,
                "title": row.get('title', ''),
                "text": row.get('text', ''),
                "language": row.get('language', 'en'),
                "metadata": {"imported": True}
            }
            if record["text"]:
                new_records.append(record)
                
    existing_data.extend(new_records)
    
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, indent=2)
        
    print(f"Successfully imported {len(new_records)} records from {csv_file} to {json_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Import CSV records to real_data.json")
    parser.add_argument("--csv", required=True, help="Input CSV file")
    parser.add_argument("--json", default="real_data.json", help="Output JSON file")
    
    args = parser.parse_args()
    import_csv(args.csv, args.json)
