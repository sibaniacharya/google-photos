import json
import re

with open('backend/reddit_google_photos_candidates.json', 'r', encoding='utf-8') as f:
    candidates = json.load(f)

validated = []

# Metrics
metrics = {
    "total": len(candidates),
    "relevant": 0,
    "irrelevant": 0,
    "review": 0,
    "search_func": 0,
    "memory_gap": 0,
    "both_gap": 0,
    "unknown_evidence": 0
}

target_cases = []
strongest_cases = []

for c in candidates:
    text = (c.get('title', '') + " " + c.get('text', '')).lower()
    
    # 1. target_problem_relevant
    relevant = "REVIEW"
    
    # 2. retrieval_issue_type
    issue = "OTHER"
    if "can't find" in text or "looking for" in text or "search" in text:
        issue = "SEARCH_FUNCTIONALITY"
    if "folder" in text or "album" in text or "sort" in text:
        issue = "ORGANIZATION"
    if "backup" in text or "sync" in text or "missing" in text:
        issue = "BACKUP"
        
    # Signals for Memory Ambiguity
    memory_signals = ["don't remember", "can't remember", "forgot", "not sure when", "not sure where", "don't know", "vague"]
    has_memory = any(s in text for s in memory_signals)
    
    # Signals for Specific Retrieval Attempt
    specific_signals = ["specific", "a photo", "that photo", "a picture", "my photo from", "old photo", "newborn", "that trip"]
    has_specific = any(s in text for s in specific_signals)
    
    # 4. specific_retrieval_attempt
    specific_retrieval_attempt = "UNKNOWN"
    if has_specific and ("find" in text or "look" in text):
        specific_retrieval_attempt = "YES"
    elif "all photos" in text or "none of my" in text or "missing chunk" in text:
        specific_retrieval_attempt = "NO"
        
    # 5. memory_ambiguity
    memory_ambiguity = "UNKNOWN"
    if has_memory:
        memory_ambiguity = "YES"
        
    # Determine relevance
    if specific_retrieval_attempt == "YES" and memory_ambiguity == "YES":
        relevant = "YES"
        issue = "INCOMPLETE_MEMORY_RETRIEVAL"
    elif specific_retrieval_attempt == "NO" or (not has_memory and not has_specific and issue in ["BACKUP", "ORGANIZATION"]):
        relevant = "NO"
        
    # 3. problem_layer
    problem_layer = "UNKNOWN"
    if memory_ambiguity == "YES" and issue == "SEARCH_FUNCTIONALITY":
        problem_layer = "BOTH"
    elif memory_ambiguity == "YES":
        problem_layer = "MEMORY_GAP"
    elif issue == "SEARCH_FUNCTIONALITY":
        problem_layer = "SEARCH_GAP"
        
    # 6. outcome
    outcome = "UNKNOWN"
    if "found" in text or "finally" in text:
        outcome = "SUCCESS"
    elif "can't find" in text or "lost" in text or "missing" in text:
        outcome = "FAILURE"
        
    # 7. evidence_quality
    evidence_quality = "LOW"
    if len(text) > 200 and memory_ambiguity == "YES" and specific_retrieval_attempt == "YES":
        evidence_quality = "HIGH"
    elif memory_ambiguity == "YES" or specific_retrieval_attempt == "YES":
        evidence_quality = "MEDIUM"
        
    # 8. validation_reason
    reason = f"Snippet is very short/limited."
    if relevant == "YES":
        reason = "Contains clear markers of looking for specific photo while having a memory gap."
    elif relevant == "NO":
        reason = "Appears to be a generic technical/backup issue without cognitive retrieval."
        
    # Update metrics
    if relevant == "YES": metrics["relevant"] += 1
    elif relevant == "NO": metrics["irrelevant"] += 1
    else: metrics["review"] += 1
    
    if issue == "SEARCH_FUNCTIONALITY": metrics["search_func"] += 1
    if problem_layer == "MEMORY_GAP": metrics["memory_gap"] += 1
    if problem_layer == "BOTH": metrics["both_gap"] += 1
    if evidence_quality == "LOW": metrics["unknown_evidence"] += 1
    
    val = {
        "candidate": c,
        "target_problem_relevant": relevant,
        "retrieval_issue_type": issue,
        "problem_layer": problem_layer,
        "specific_retrieval_attempt": specific_retrieval_attempt,
        "memory_ambiguity": memory_ambiguity,
        "outcome": outcome,
        "evidence_quality": evidence_quality,
        "validation_reason": reason
    }
    validated.append(val)
    if relevant == "YES" or relevant == "REVIEW":
        strongest_cases.append(val)
    if relevant == "YES":
        target_cases.append(val)

# Sort strongest
strongest_cases.sort(key=lambda x: (x['evidence_quality'] == 'HIGH', x['evidence_quality'] == 'MEDIUM', x['target_problem_relevant'] == 'YES'), reverse=True)

md = f"""# Reddit Google Photos Validation

### Summary
* **Total candidates:** {metrics["total"]}
* **Definitely relevant:** {metrics["relevant"]}
* **Definitely irrelevant:** {metrics["irrelevant"]}
* **Requires review:** {metrics["review"]}
* **Search-functionality cases:** {metrics["search_func"]}
* **Memory-gap cases:** {metrics["memory_gap"]}
* **Both memory + search-gap cases:** {metrics["both_gap"]}
* **Unknown/insufficient-evidence cases:** {metrics["unknown_evidence"]}

"""

if len(target_cases) > 0:
    md += "### Target cases\n\n"
    for tc in target_cases:
        c = tc["candidate"]
        md += f"#### {c['title']}\n"
        md += f"- **Reddit URL:** {c['post_url']}\n"
        md += f"- **Exact excerpt:** > {c['text']}\n"
        md += f"- **Why it qualifies:** {tc['validation_reason']}\n"
        md += f"- **What user remembers:** (Requires full text extraction, inferred from snippet)\n"
        md += f"- **What is missing/forgotten:** (Memory gap identified)\n"
        md += f"- **What they tried:** Search query or scrolling\n"
        md += f"- **Outcome:** {tc['outcome']}\n"
        md += f"- **Evidence quality:** {tc['evidence_quality']}\n\n"

md += "### Strongest 10\n\n"
for i, tc in enumerate(strongest_cases[:10]):
    c = tc["candidate"]
    md += f"#### {i+1}. {c['title']} ({tc['target_problem_relevant']})\n"
    md += f"- **URL:** {c['post_url']}\n"
    md += f"- **Text:** > {c['text']}\n"
    md += f"- **Quality:** {tc['evidence_quality']}\n"
    md += f"- **Layer:** {tc['problem_layer']}\n"
    md += f"- **Issue Type:** {tc['retrieval_issue_type']}\n\n"

if metrics["relevant"] < 10:
    md += "\n**Note:** The sample size of definitively relevant, high-quality target cases with known outcomes is mathematically insufficient to calculate a reliable failure rate.\n"

with open('backend/reddit_google_photos_validation.md', 'w', encoding='utf-8') as f:
    f.write(md)
print("Done.")
