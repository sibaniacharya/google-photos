import json

dataset_path = 'c:/Users/siban/OneDrive/Desktop/NextLeap/M3_7/data/normalized_reviews.json'
with open(dataset_path, 'r', encoding='utf-8') as f:
    data = json.load(f)
reviews = data.get('reviews', [])

total_records = len(reviews)

intent_keywords = [
    "find", "search", "looking", "locate", "retrieve"
]

memory_keywords = [
    "remember", "forget", "forgot", "when", "where", "date", "year", 
    "month", "time", "memory", "memories", "vague", "exact"
]

context_keywords = [
    "birthday", "wedding", "trip", "vacation", "childhood", "school", "college",
    "concert", "festival", "family", "old", "friend", "pet", "dog", "cat", 
    "screenshot", "place", "location"
]

candidates = []

for idx, rev in enumerate(reviews):
    text = rev.get('content', '').lower()
    if not text:
        text = rev.get('text', '').lower()
        
    if not text:
        continue
        
    intent_matched = [k for k in intent_keywords if k in text]
    memory_matched = [k for k in memory_keywords if k in text]
    context_matched = [k for k in context_keywords if k in text]
    
    has_intent = len(intent_matched) > 0
    has_memory = len(memory_matched) > 0
    has_context = len(context_matched) > 0
    
    # Needs at least one intent word and either a memory or context word
    if has_intent and (has_memory or has_context):
        
        # Categorize
        # Strong: has explicit "forgot/remember" OR combinations like "find" + "old"
        if has_memory and any(k in text for k in ["remember", "forget", "forgot", "memory", "memories"]):
            category = "STRONG"
        elif has_context and has_memory:
            category = "POSSIBLE"
        else:
            category = "WEAK"
            
        candidates.append({
            "id": rev.get('reviewId', f"raw_{idx}")[:8] if rev.get('reviewId') else f"raw_{idx}",
            "text": rev.get('content', rev.get('text', '')),
            "url": rev.get('url', f"https://play.google.com/store/apps/details?id=com.google.android.apps.photos&reviewId={rev.get('reviewId')}"),
            "category": category,
            "signals": list(set(intent_matched + memory_matched + context_matched))
        })

# Sort for output
strong = [c for c in candidates if c['category'] == 'STRONG']
possible = [c for c in candidates if c['category'] == 'POSSIBLE']
weak = [c for c in candidates if c['category'] == 'WEAK']

# Write markdown
md = f"# Retrieval Candidate Pool\n\n"
md += f"**Total raw records searched:** {total_records}\n"
md += f"**Number of candidate records found:** {len(candidates)}\n\n"

md += f"## Summary\n"
md += f"- **STRONG candidates:** {len(strong)}\n"
md += f"- **POSSIBLE candidates:** {len(possible)}\n"
md += f"- **WEAK candidates:** {len(weak)}\n\n"

md += f"## 10 Strongest Candidate Examples\n\n"
for i, c in enumerate(strong[:10]):
    md += f"### {i+1}. Record ID: {c['id']}\n"
    md += f"- **Source URL:** {c['url']}\n"
    md += f"- **Signals Triggered:** {', '.join(c['signals'])}\n"
    md += f"- **Original Review Text:**\n  > {c['text'].replace(chr(10), ' ')}\n\n"

md += f"## All Candidates\n\n"
for c in candidates[:50]:
    md += f"**[{c['category']}] ID {c['id']}** | Signals: {', '.join(c['signals'])}\n"
    md += f"> {c['text'][:300].replace(chr(10), ' ')}...\n\n"
    
if len(candidates) > 50:
    md += f"\n*... and {len(candidates) - 50} more candidates not shown here to save space.*\n"

with open('backend/retrieval_candidate_pool.md', 'w', encoding='utf-8') as f:
    f.write(md)
    
print(f"Total: {len(candidates)}, Strong: {len(strong)}, Possible: {len(possible)}, Weak: {len(weak)}")
