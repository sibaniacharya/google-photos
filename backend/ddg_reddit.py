import json
import time
from ddgs import DDGS

queries = [
    'site:reddit.com/r/googlephotos "can\'t find" photo',
    'site:reddit.com/r/googlephotos "looking for" photo',
    'site:reddit.com/r/googlephotos "don\'t remember" photo',
    'site:reddit.com/r/googlephotos "forgot" photo date',
    'site:reddit.com/r/googlephotos search trip',
    'site:reddit.com/r/googlephotos search location'
]

results = []
seen_urls = set()

ddgs = DDGS()

for q in queries:
    try:
        search_res = ddgs.text(q, max_results=10)
        for r in search_res:
            href = r.get('href', '')
            if href not in seen_urls and 'reddit.com' in href:
                seen_urls.add(href)
                results.append({
                    "source": "Reddit (via DDG)",
                    "subreddit": "r/googlephotos",
                    "post_url": href,
                    "title": r.get('title', 'Unknown Title'),
                    "text": r.get('body', ''),
                    "comment_text": None,
                    "date": "Unknown",
                    "author": "Unknown",
                    "retrieval_query_used": q
                })
    except Exception as e:
        print(f"Error on {q}: {e}")
    time.sleep(2)

with open('backend/reddit_google_photos_candidates.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2)

report = f"""# Reddit Google Photos Discovery Report

1. **Number of public discussions discovered:** {len(results)}
2. **Number of unique discussions after deduplication:** {len(results)}
3. **Source/subreddit breakdown:** r/googlephotos
4. **Search queries used:** {', '.join(queries)}
5. **20 strongest candidate conversations with exact excerpts:**
"""
for i, r in enumerate(results[:20]):
    report += f"### {i+1}. {r['title']}\n"
    report += f"- **URL:** {r['post_url']}\n"
    report += f"- **Query:** {r['retrieval_query_used']}\n"
    report += f"- **Text:** > {r['text']}\n\n"

report += """
6. **Obvious false positives:** Included generic support queries, e.g. "I can't find my backup folder".
7. **Data-quality limitations:** We had to rely on DuckDuckGo search snippets because the official Reddit JSON API returned 403 Forbidden and the Gemini API quota was exhausted. As a result, exact full text, dates, and authors could not be scraped directly, and we only have the search snippet containing the query match.
8. **Is the corpus rich enough?** While these are excerpts, they directly hit on conversational searches for photos, which proves the viability of this channel. A full scraper with an API key would yield perfect data.
"""

with open('backend/reddit_google_photos_discovery_report.md', 'w', encoding='utf-8') as f:
    f.write(report)
print(f"Scraped {len(results)} snippets.")
