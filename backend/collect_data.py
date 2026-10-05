import json
import uuid
import re
from datetime import datetime
from google_play_scraper import Sort, reviews

def collect_reviews(app_id="com.google.android.apps.photos", target_count=300):
    print(f"Fetching reviews for {app_id}...")
    
    # Keywords that might indicate a retrieval problem
    keywords = [
        "search", "find", "looking for", "can't remember", "couldn't remember",
        "where is", "trying to find", "scrolling", "lost photo", "old photo",
        "ticket", "receipt", "screenshot", "face", "person", "location", "date"
    ]
    
    keyword_pattern = re.compile(r'\b(' + '|'.join(keywords) + r')\b', re.IGNORECASE)
    
    collected_records = []
    continuation_token = None
    total_fetched = 0
    
    while len(collected_records) < target_count:
        # Fetch a chunk of 500 reviews
        result, continuation_token = reviews(
            app_id,
            lang='en', 
            country='us', 
            sort=Sort.NEWEST, 
            count=1000, 
            continuation_token=continuation_token
        )
        
        if not result:
            print("No more reviews available.")
            break
            
        total_fetched += len(result)
        
        for rev in result:
            text = rev.get('content', '')
            if not text:
                continue
                
            # Filter: must have some length and contain at least one retrieval keyword
            if len(text.split()) > 10 and keyword_pattern.search(text):
                record = {
                    "record_id": str(uuid.uuid4())[:8],
                    "source": "Google Play",
                    "source_url": f"https://play.google.com/store/apps/details?id={app_id}&reviewId={rev.get('reviewId')}",
                    "author_id": rev.get('userName', 'Anonymous'),
                    "date": rev.get('at', datetime.now()).isoformat() if hasattr(rev.get('at'), 'isoformat') else str(rev.get('at')),
                    "rating": rev.get('score'),
                    "title": "",
                    "text": text,
                    "language": "en",
                    "metadata": {
                        "thumbsUpCount": rev.get('thumbsUpCount', 0),
                        "appVersion": rev.get('reviewCreatedVersion', 'unknown')
                    }
                }
                collected_records.append(record)
                
                if len(collected_records) >= target_count:
                    break
        
        print(f"Fetched {total_fetched} total. Found {len(collected_records)} potentially relevant records...")
        
        if not continuation_token:
            break
            
    return collected_records

if __name__ == "__main__":
    records = collect_reviews(target_count=300)
    with open('real_data.json', 'w', encoding='utf-8') as f:
        json.dump(records, f, indent=2)
    print(f"\nSuccessfully saved {len(records)} records to real_data.json")
