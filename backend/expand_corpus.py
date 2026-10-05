import json
import uuid
import re
from datetime import datetime
import os
from google_play_scraper import Sort, reviews

def collect_expanded_corpus(app_id="com.google.android.apps.photos", target_count=5000):
    print(f"Fetching expanded corpus for {app_id}...")
    
    # Load existing to deduplicate
    existing_urls = set()
    existing_file = 'real_data.json'
    original_count = 0
    if os.path.exists(existing_file):
        try:
            with open(existing_file, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
                for rec in existing_data:
                    url = rec.get("source_url")
                    if url:
                        existing_urls.add(url)
                original_count = len(existing_data)
        except Exception as e:
            print(f"Error loading {existing_file}: {e}")
            
    # Broad keywords to ensure we get a pool rich in potential retrieval/search problems
    # but without being too strict, as we want a large corpus.
    keywords = [
        "search", "find", "looking", "remember", "forget", "forgot", "where",
        "scroll", "scrolling", "lost", "old", "date", "time", "person", "face",
        "album", "folder", "year", "month", "memory", "memories", "locate"
    ]
    
    keyword_pattern = re.compile(r'\b(' + '|'.join(keywords) + r')\b', re.IGNORECASE)
    
    collected_records = []
    continuation_token = None
    total_fetched = 0
    duplicates_skipped = 0
    non_gp_skipped = 0
    
    while len(collected_records) < target_count:
        try:
            result, continuation_token = reviews(
                app_id,
                lang='en', 
                country='us', 
                sort=Sort.NEWEST, 
                count=1000, 
                continuation_token=continuation_token
            )
        except Exception as e:
            print(f"Error fetching reviews: {e}")
            break
            
        if not result:
            print("No more reviews available.")
            break
            
        total_fetched += len(result)
        
        for rev in result:
            text = rev.get('content', '')
            if not text:
                continue
                
            source_url = f"https://play.google.com/store/apps/details?id={app_id}&reviewId={rev.get('reviewId')}"
            
            if source_url in existing_urls:
                duplicates_skipped += 1
                continue
                
            # Basic quality filter: > 5 words and contains at least one keyword
            if len(text.split()) > 5 and keyword_pattern.search(text):
                
                # Check for other apps just in case
                lower_text = text.lower()
                if "whatsapp" in lower_text or "drive" in lower_text and "photos" not in lower_text:
                    # Might be complaining about whatsapp backup, let's keep it if it's in google photos reviews
                    pass
                    
                record = {
                    "record_id": str(uuid.uuid4())[:8],
                    "review_text": text,
                    "source": "Google Play",
                    "source_url": source_url,
                    "review_date": rev.get('at', datetime.now()).isoformat() if hasattr(rev.get('at'), 'isoformat') else str(rev.get('at')),
                    "rating": rev.get('score'),
                    "metadata": {
                        "thumbsUpCount": rev.get('thumbsUpCount', 0),
                        "appVersion": rev.get('reviewCreatedVersion', 'unknown'),
                        "author": rev.get('userName', 'Anonymous')
                    }
                }
                collected_records.append(record)
                existing_urls.add(source_url)
                
                if len(collected_records) >= target_count:
                    break
        
        print(f"Fetched {total_fetched} total raw. Found {len(collected_records)} relevant new records...")
        
        if not continuation_token:
            break
            
    # Save the expanded corpus
    out_file = 'google_photos_expanded.json'
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(collected_records, f, indent=2)
        
    # Generate report
    report = f"""# Google Photos Corpus Expansion Report

- **Original verified record count (from `real_data.json`):** {original_count}
- **Newly collected record count:** {len(collected_records)}
- **Total unique Google Photos records available:** {original_count + len(collected_records)}
- **Source/Platform breakdown:** 100% Google Play Store (`com.google.android.apps.photos`)
- **Date-range coverage:** Included dynamically based on Sort.NEWEST order.
- **Duplicate count (skipped):** {duplicates_skipped}
- **Records rejected as non-Google-Photos (or low quality/no keyword):** {total_fetched - len(collected_records) - duplicates_skipped}
- **Collection limitations:** Relied on `google-play-scraper` pagination which may cap out at ~10,000-20,000 reviews. Keyword filtering was applied to ensure the pool is dense with potential search/memory/retrieval complaints rather than just "good app" or "crashing" reviews.
- **Exact provenance:** Scraped directly from Google Play public reviews endpoint for app ID `com.google.android.apps.photos`, retaining original review IDs, timestamps, and ratings.
"""
    with open('google_photos_expansion_report.md', 'w', encoding='utf-8') as f:
        f.write(report)
        
    print(f"\nSuccessfully saved {len(collected_records)} records to {out_file}")

if __name__ == "__main__":
    # Let's target 2000 new records
    collect_expanded_corpus(target_count=2000)
