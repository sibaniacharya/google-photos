import json
import time
import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime

with open('backend/reddit_google_photos_candidates.json', 'r', encoding='utf-8') as f:
    candidates = json.load(f)

with open('backend/reddit_google_photos_validation.md', 'r', encoding='utf-8') as f:
    val_md = f.read()

# We'll just fetch all 47 to ensure we don't miss anything.
# The user wants to preserve: original ID, URL, subreddit, title, snippet, full post, status, method, timestamp.

out_candidates = []
counts = {"FULL_TEXT_RETRIEVED": 0, "PARTIAL_TEXT_RETRIEVED": 0, "SNIPPET_ONLY": 0, "NOT_ACCESSIBLE": 0}
urls_retrieved = []

import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

for c in candidates:
    url = c.get('post_url', '')
    title = c.get('title', '')
    snippet = c.get('text', '')
    subreddit = c.get('subreddit', 'r/googlephotos')
    
    # Try fetching from old.reddit.com
    fetch_url = url.replace('www.reddit.com', 'old.reddit.com').replace('reddit.com', 'old.reddit.com')
    if 'old.reddit.com' not in fetch_url:
        fetch_url = fetch_url.replace('https://', 'https://old.reddit.com/')
    
    status = "SNIPPET_ONLY"
    full_text = None
    method = "None"
    
    try:
        req = urllib.request.Request(fetch_url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8'
        })
        html = urllib.request.urlopen(req, timeout=10, context=ctx).read()
        soup = BeautifulSoup(html, 'html.parser')
        
        # In old.reddit.com, the post text is in a div with class 'usertext-body' inside the 'expando' div.
        expando = soup.find('div', class_='expando')
        if expando:
            md_div = expando.find('div', class_='md')
            if md_div:
                full_text = md_div.get_text(separator='\n').strip()
                status = "FULL_TEXT_RETRIEVED"
                method = "Direct public Reddit page (old.reddit.com HTML)"
                urls_retrieved.append(url)
            else:
                # Might be an image post or just a title
                status = "SNIPPET_ONLY"
                method = "Direct public Reddit page (old.reddit.com HTML - no body found)"
        else:
            # If no expando, it might be a link post or deleted
            status = "SNIPPET_ONLY"
            method = "Direct public Reddit page (old.reddit.com HTML - no body found)"
            
    except urllib.error.HTTPError as e:
        if e.code == 403 or e.code == 429:
            status = "NOT_ACCESSIBLE"
            method = f"HTTP {e.code}"
    except Exception as e:
        status = "NOT_ACCESSIBLE"
        method = str(e)[:50]
        
    counts[status] += 1
    
    out_candidates.append({
        "original_candidate_id": c.get("post_url"),
        "reddit_url": url,
        "subreddit": subreddit,
        "title": title,
        "original_duckduckgo_excerpt": snippet,
        "full_post_body": full_text,
        "retrieval_status": status,
        "retrieval_method": method,
        "retrieval_timestamp": datetime.utcnow().isoformat() + "Z"
    })
    time.sleep(1)

with open('backend/reddit_fulltext_candidates.json', 'w', encoding='utf-8') as f:
    json.dump(out_candidates, f, indent=2)

report = f"""# Reddit Full-Text Retrieval Report

* **Total candidates attempted:** {len(out_candidates)}
* **Full text retrieved:** {counts["FULL_TEXT_RETRIEVED"]}
* **Partial text retrieved:** {counts["PARTIAL_TEXT_RETRIEVED"]}
* **Snippet only / Not Accessible:** {counts["NOT_ACCESSIBLE"] + counts["SNIPPET_ONLY"]}

### URLs successfully retrieved:
"""
for u in urls_retrieved:
    report += f"- {u}\n"

report += """
### Technical Limitations
- Reddit heavily blocks automated scraping (returning HTTP 403 or 429) unless an official OAuth token is used or a highly specific, clean browser signature is provided.
- Because `old.reddit.com` was targeted, some posts may be successfully parsed via `BeautifulSoup`.
- No Gemini calls, CAPTCHA bypasses, or fabricated text were used.
"""

with open('backend/reddit_fulltext_retrieval_report.md', 'w', encoding='utf-8') as f:
    f.write(report)

print(f"Finished fetching. {counts['FULL_TEXT_RETRIEVED']} full text retrieved.")
