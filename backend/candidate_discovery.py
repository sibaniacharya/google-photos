import json
import re
import os

# Combine datasets
input_files = ['backend/real_data.json', 'backend/google_photos_expanded.json']
corpus = []
seen_ids = set()

for fpath in input_files:
    if os.path.exists(fpath):
        with open(fpath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for rec in data:
                # Use source_url as unique id for deduplication just in case
                uid = rec.get('source_url', rec.get('record_id'))
                if uid not in seen_ids:
                    seen_ids.add(uid)
                    corpus.append(rec)

# Signal A: Retrieval Intent (must be somewhat specific)
signal_a_patterns = [
    r"(?:find|locate|search for|look(?:ing)? for|retrieve)\s+(?:a|an|the|that|my|old|particular|specific|certain)?\s*(?:photo|picture|image|video|pic)",
    r"can'?t find\s+(?:a|an|the|that|my|old|particular|specific|certain)?\s*(?:photo|picture|image|video|pic)",
    r"trying to find\s+(?:a|an|the|that|my|old|particular|specific|certain)?\s*(?:photo|picture|image|video|pic)",
    r"search(?:ing)? through photos",
    r"(?:find|search).*photo I took",
    r"(?:find|search).*photo someone sent",
    r"(?:find|search).*picture of"
]

# Signal B: Memory Ambiguity
signal_b_patterns = [
    r"don'?t remember",
    r"can'?t remember",
    r"forgot",
    r"not sure when",
    r"not sure where",
    r"don'?t know the date",
    r"don'?t know the name",
    r"approximate",
    r"vague",
    r"remember an event",
    r"don'?t remember the exact"
]

# Success signals
success_patterns = [
    r"found (?:a|an|the|that|my|old|particular)?\s*(?:photo|picture|image)",
    r"was able to find",
    r"successfully found",
    r"helped me find",
    r"finally found",
    r"glad I found"
]

candidates = []
excluded_count = 0
signal_distribution = {"A_only": 0, "B_only": 0, "Neither": 0, "A_and_B": 0}

false_positive_examples = []

for rec in corpus:
    text = rec.get('review_text', rec.get('text', '')).lower()
    if not text:
        excluded_count += 1
        continue
        
    matched_a = [p for p in signal_a_patterns if re.search(p, text)]
    matched_b = [p for p in signal_b_patterns if re.search(p, text)]
    matched_success = [p for p in success_patterns if re.search(p, text)]
    
    has_a = len(matched_a) > 0
    has_b = len(matched_b) > 0
    has_success = len(matched_success) > 0
    
    if has_a and has_b:
        signal_distribution["A_and_B"] += 1
        candidate_type = "INCOMPLETE_MEMORY_CANDIDATE"
        candidates.append({
            "record_id": rec.get("record_id"),
            "review_text": rec.get("review_text", rec.get("text", "")),
            "source": rec.get("source"),
            "source_url": rec.get("source_url"),
            "review_date": rec.get("review_date", rec.get("date")),
            "rating": rec.get("rating"),
            "matched_retrieval_signals": matched_a,
            "matched_memory_signals": matched_b,
            "candidate_type": candidate_type
        })
    elif has_success and (has_b or has_a): # Success implies retrieval attempt, combined with memory or generic retrieval
        # If it's a successful retrieval of something specific
        candidate_type = "SUCCESSFUL_RETRIEVAL_CANDIDATE"
        candidates.append({
            "record_id": rec.get("record_id"),
            "review_text": rec.get("review_text", rec.get("text", "")),
            "source": rec.get("source"),
            "source_url": rec.get("source_url"),
            "review_date": rec.get("review_date", rec.get("date")),
            "rating": rec.get("rating"),
            "matched_retrieval_signals": matched_success + matched_a,
            "matched_memory_signals": matched_b,
            "candidate_type": candidate_type
        })
    else:
        # Excluded
        excluded_count += 1
        if has_a and not has_b:
            signal_distribution["A_only"] += 1
        elif has_b and not has_a:
            signal_distribution["B_only"] += 1
        else:
            signal_distribution["Neither"] += 1
            
        # Collect false positives (had generic words but failed 2-signal)
        # e.g., if it has "find" and "old" but not in the specific pattern
        if "find" in text and "old" in text and not has_a and not has_b:
            if len(false_positive_examples) < 5:
                false_positive_examples.append(rec.get("review_text", rec.get("text", "")))
        if "remember" in text and not has_b:
            if len(false_positive_examples) < 10 and text not in false_positive_examples:
                false_positive_examples.append(rec.get("review_text", rec.get("text", "")))


# Save JSON
with open('backend/retrieval_candidate_pool_v2.json', 'w', encoding='utf-8') as f:
    json.dump(candidates, f, indent=2)

incomplete = [c for c in candidates if c["candidate_type"] == "INCOMPLETE_MEMORY_CANDIDATE"]
success = [c for c in candidates if c["candidate_type"] == "SUCCESSFUL_RETRIEVAL_CANDIDATE"]

# Generate Markdown
md = f"# Retrieval Candidate Pool v2 Report\n\n"
md += f"1. **Total input records:** {len(corpus)}\n"
md += f"2. **Number of incomplete-memory candidates:** {len(incomplete)}\n"
md += f"3. **Number of successful-retrieval candidates:** {len(success)}\n"
md += f"4. **Number of records excluded:** {excluded_count}\n"
md += f"5. **Signal distribution for excluded:**\n"
md += f"   - Retrieval Intent Only (A): {signal_distribution['A_only']}\n"
md += f"   - Memory Ambiguity Only (B): {signal_distribution['B_only']}\n"
md += f"   - Neither: {signal_distribution['Neither']}\n\n"

md += f"## 6. 20 Strongest Candidates\n\n"
for i, c in enumerate((incomplete + success)[:20]):
    md += f"### {i+1}. [{c['candidate_type']}] ID: {c['record_id']}\n"
    md += f"- **Matched Retrieval Signals:** {', '.join(c['matched_retrieval_signals'])}\n"
    md += f"- **Matched Memory Signals:** {', '.join(c['matched_memory_signals']) if c['matched_memory_signals'] else 'None'}\n"
    md += f"- **Original Quote:**\n  > {c['review_text'].replace(chr(10), ' ')}\n\n"

md += f"## 7. Examples of obvious false positives excluded by the 2-signal rule\n\n"
md += f"These reviews contain isolated words like 'find', 'old', or 'remember', but do not represent the target retrieval problem.\n\n"
for i, fp in enumerate(false_positive_examples[:5]):
    md += f"**False Positive {i+1}:**\n> {fp.replace(chr(10), ' ')}\n\n"

with open('backend/retrieval_candidate_pool_v2_report.md', 'w', encoding='utf-8') as f:
    f.write(md)

print("Done. V2 generated.")
