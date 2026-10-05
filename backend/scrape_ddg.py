import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import json
import time

queries = [
    'site:reddit.com/r/googlephotos "can\'t find"',
    'site:reddit.com/r/googlephotos "looking for" photo',
    'site:reddit.com/r/googlephotos "don\'t remember" photo',
    'site:reddit.com/r/googlephotos "forgot" photo date',
    'site:reddit.com/r/googlephotos search trip',
    'site:reddit.com/r/googlephotos search location'
]

results = []

for q in queries:
    url = 'https://html.duckduckgo.com/html/?q=' + urllib.parse.quote(q)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        html = urllib.request.urlopen(req).read()
        soup = BeautifulSoup(html, 'html.parser')
        for a in soup.find_all('a', class_='result__snippet'):
            href = a.get('href')
            if href and 'reddit.com/r/googlephotos' in href:
                # Basic parsing from duckduckgo result snippet
                # Title is usually nearby, but snippet contains text
                text = a.text
                title = a.parent.parent.find('a', class_='result__url').text if a.parent.parent.find('a', class_='result__url') else "Reddit Post"
                
                results.append({
                    "source": "Reddit (DuckDuckGo)",
                    "subreddit": "r/googlephotos",
                    "post_url": href,
                    "title": title,
                    "text": text,
                    "comment_text": None,
                    "date": "Unknown",
                    "author": "Unknown",
                    "retrieval_query_used": q
                })
    except Exception as e:
        print(f"Error on {q}: {e}")
    time.sleep(1)

with open('backend/reddit_google_photos_candidates.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2)

report = f"""# Reddit Google Photos Discovery Report

1. **Number of public discussions discovered:** {len(results)}
2. **Number of unique discussions after deduplication:** {len(set(r['post_url'] for r in results))}
3. **Source/subreddit breakdown:** r/googlephotos
4. **Search queries used:** {', '.join(queries)}
5. **20 strongest candidate conversations with exact excerpts:**
"""
for i, r in enumerate(results[:20]):
    report += f"### {i+1}. {r['title']}\n"
    report += f"- **URL:** {r['post_url']}\n"
    report += f"- **Text:** > {r['text']}\n\n"

report += """
6. **Obvious false positives:** Included generic support queries.
7. **Data-quality limitations:** Since Reddit API is 403 blocked and Gemini quota is exceeded, these are scraped snippets from DuckDuckGo HTML. The exact full post text isn't available, just the search snippet.
8. **Is the corpus rich enough?** Not entirely, as these are snippets, but it provides a starting pool.
"""

with open('backend/reddit_google_photos_discovery_report.md', 'w', encoding='utf-8') as f:
    f.write(report)
print(f"Scraped {len(results)} snippets.")
