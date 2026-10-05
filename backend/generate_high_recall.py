import json
import re

def run():
    input_file = "c:/Users/siban/OneDrive/Desktop/NextLeap/Graduation Project/Second Attempt/Google photos/backend/google_photos_expanded.json"
    output_json = "c:/Users/siban/OneDrive/Desktop/NextLeap/Graduation Project/Second Attempt/Google photos/backend/high_recall_candidate_pool.json"
    output_md = "c:/Users/siban/OneDrive/Desktop/NextLeap/Graduation Project/Second Attempt/Google photos/backend/high_recall_candidate_report.md"

    try:
        with open(input_file, "r", encoding="utf-8") as f:
            records = json.load(f)
    except Exception as e:
        print(f"Error loading {input_file}: {e}")
        return

    signals = {
        "search_intent": [
            "can't find", "cannot find", "looking for", "trying to find", 
            "where is", "find my", "lost", "missing", "disappeared", "search", "locate",
            "can't locate"
        ],
        "memory_cues": [
            "old photo", "old picture", "previous photo", "memories", "memory",
            "remember", "forgot", "forgotten", "trip", "vacation", "birthday", 
            "wedding", "school", "college", "family", "friend", "baby", "child", 
            "place", "location", "screenshot", "document", "receipt", "medicine", 
            "food", "car", "house", "event", "clothes", "shirt", "dress", "color", "appearance"
        ]
    }

    candidates = []
    
    # Process each record
    for record in records:
        text = record.get("review_text", "").lower()
        
        found_search = []
        for s in signals["search_intent"]:
            if s in text:
                found_search.append(s)
                
        found_memory = []
        for s in signals["memory_cues"]:
            if s in text:
                found_memory.append(s)
                
        total_signals = len(found_search) + len(found_memory)
        if total_signals > 0:
            candidates.append({
                "record": record,
                "score": total_signals,
                "found_search": found_search,
                "found_memory": found_memory
            })

    # Prioritize those with both search and memory signals
    strong_candidates = [c for c in candidates if len(c["found_search"]) > 0 and len(c["found_memory"]) > 0]
    other_candidates = [c for c in candidates if c not in strong_candidates]
    
    strong_candidates.sort(key=lambda x: x["score"], reverse=True)
    other_candidates.sort(key=lambda x: x["score"], reverse=True)
    
    selected_pool = (strong_candidates + other_candidates)[:300]
    
    final_json = []
    signal_distribution = {"search_intent": 0, "memory_cues": 0, "both": 0}
    
    for c in selected_pool:
        r = c["record"]
        final_json.append({
            "record_id": r.get("record_id"),
            "source": r.get("source"),
            "source_url": r.get("source_url"),
            "review_date": r.get("review_date"),
            "rating": r.get("rating"),
            "review_text": r.get("review_text"),
            "signals_matched": c["found_search"] + c["found_memory"]
        })
        if len(c["found_search"]) > 0 and len(c["found_memory"]) > 0:
            signal_distribution["both"] += 1
        elif len(c["found_search"]) > 0:
            signal_distribution["search_intent"] += 1
        else:
            signal_distribution["memory_cues"] += 1
            
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(final_json, f, indent=2)

    report = f"""# High-Recall Candidate Discovery Report

## Overview
- **Total Source Records:** {len(records):,}
- **Number of Candidates Selected:** {len(final_json)}

## Candidate Selection Methodology
A high-recall, non-evaluative keyword matching approach was used to scan the full {len(records):,}-record corpus. The goal was strictly to generate a broad candidate pool for subsequent AI semantic extraction, not to identify confirmed problems at this stage.

Records were prioritized based on the presence of terms from two broad signal groups. We selected up to 300 records with the highest signal density, heavily favoring records that contained at least one search intent signal AND one memory/object signal to ensure diversity across retrieval intents and memory cues.

## Signal Groups Used
1. **Search & Action Intent:** `can't find`, `cannot find`, `looking for`, `trying to find`, `where is`, `find my`, `lost`, `missing`, `disappeared`, `search`, `locate`, `can't locate`
2. **Memory & Object Cues:** `old photo`, `old picture`, `previous photo`, `memories`, `memory`, `remember`, `forgot`, `forgotten`, `trip`, `vacation`, `birthday`, `wedding`, `school`, `college`, `family`, `friend`, `baby`, `child`, `place`, `location`, `screenshot`, `document`, `receipt`, `medicine`, `food`, `car`, `house`, `event`, `clothes`, `shirt`, `dress`, `color`, `appearance`

## Candidate Distribution
- **Search Intent + Memory Cues (Both):** {signal_distribution['both']}
- **Search Intent Only:** {signal_distribution['search_intent']}
- **Memory Cues Only:** {signal_distribution['memory_cues']}

## Examples of Candidate Types
* **Search for Events:** e.g., "looking for wedding photos"
* **Missing People/Places:** e.g., "family vacation pictures missing"
* **Forgotten Specifics:** e.g., "can't find screenshots of receipts"
* **Broad Memory Retrieval:** e.g., "searching for old memories"

## Limitations & Disclaimer
- **High Recall, Low Precision:** A keyword match does **NOT** mean the record is a retrieval problem. For example, the word "lost" might refer to losing a phone, and "search" might refer to praise for the search feature.
- **No Confirmation:** At this stage, NO candidates are claimed to be confirmed opportunities. The candidate pool is exclusively a high-recall input for the next AI semantic extraction stage.
- **Traceability Preserved:** The original review text, dates, ratings, and URLs have been strictly preserved with no alteration.
"""

    with open(output_md, "w", encoding="utf-8") as f:
        f.write(report)
        
    print(f"Total Source Records: {len(records)}")
    print(f"Number of Candidates Selected: {len(final_json)}")
    print(f"Signal Distribution: {signal_distribution}")

if __name__ == "__main__":
    run()
