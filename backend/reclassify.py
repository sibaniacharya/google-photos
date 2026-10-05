import json
import re

def process_records(input_file, output_file, report_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    insights = data.get('insights', [])
    
    previous_relevant_count = sum(1 for r in insights if r.get('is_retrieval_relevant'))
    
    new_target_relevant_count = 0
    changed_records = []
    
    # Metrics
    outcomes = []
    memory_gap_count = 0
    search_gap_count = 0
    both_count = 0
    taxonomy_distribution = {
        "INCOMPLETE_MEMORY_RETRIEVAL": 0,
        "SEARCH_FUNCTIONALITY": 0,
        "NAVIGATION": 0,
        "ORGANIZATION": 0,
        "METADATA_LABEL_RETRIEVAL": 0,
        "BACKUP": 0,
        "OTHER": 0
    }
    
    for r in insights:
        text = r.get('original_text', '').lower()
        forgot = r.get('forgotten_information', [])
        gap_forgot = r.get('memory_search_gap', {}).get('what_user_forgot', []) if r.get('memory_search_gap') else []
        outcome = r.get('retrieval_outcome', 'UNKNOWN')
        is_relevant = r.get('is_retrieval_relevant', False)
        
        target_relevant = False
        issue_type = "OTHER"
        problem_layer = "UNKNOWN"
        
        # Check explicit extraction fields first
        has_memory_gap = (
            len(forgot) > 0 or 
            len(gap_forgot) > 0 or 
            bool(re.search(r'\b(forgot|remember|don\'t know|cant remember|date|when|exact)\b', text))
        )
        search_failed = outcome in ['FAILURE', 'ABANDONED', 'PARTIAL_SUCCESS'] or bool(re.search(r'\b(search|find|retrieve)\b', text))
        
        # Determine issue type
        if re.search(r'\b(filename|tag|tags|label|labels|metadata|name of file)\b', text):
            issue_type = "METADATA_LABEL_RETRIEVAL"
        elif re.search(r'\b(album|albums|folder|folders|organize|sort)\b', text):
            issue_type = "ORGANIZATION"
        elif re.search(r'\b(layout|ui|navigate|floating|interface|button)\b', text):
            issue_type = "NAVIGATION"
        elif re.search(r'\b(backup|sync|backed up|cloud)\b', text):
            issue_type = "BACKUP"
        elif re.search(r'\b(search|find|looking for|retrieve)\b', text):
            if has_memory_gap:
                issue_type = "INCOMPLETE_MEMORY_RETRIEVAL"
            else:
                issue_type = "SEARCH_FUNCTIONALITY"
        elif has_memory_gap:
            issue_type = "INCOMPLETE_MEMORY_RETRIEVAL"
        else:
            issue_type = "OTHER"
            
        if issue_type == "INCOMPLETE_MEMORY_RETRIEVAL":
            target_relevant = True
            
        # Refine problem_layer for target relevant
        if issue_type in ["INCOMPLETE_MEMORY_RETRIEVAL", "SEARCH_FUNCTIONALITY", "METADATA_LABEL_RETRIEVAL"]:
            if has_memory_gap and search_failed:
                problem_layer = "BOTH"
            elif has_memory_gap:
                problem_layer = "MEMORY_GAP"
            elif search_failed:
                problem_layer = "SEARCH_GAP"
                
        # Save to record
        r['target_problem_relevant'] = target_relevant
        r['retrieval_issue_type'] = issue_type
        r['problem_layer'] = problem_layer
        
        # Track changes
        if is_relevant != target_relevant:
            changed_records.append({
                "record_id": r.get('record_id'),
                "old_relevance": is_relevant,
                "new_relevance": target_relevant,
                "issue_type": issue_type,
                "text_snippet": r.get('original_text', '')[:60] + "..."
            })
            
        # Metrics
        taxonomy_distribution[issue_type] += 1
        if target_relevant:
            new_target_relevant_count += 1
            if outcome in ['SUCCESS', 'PARTIAL_SUCCESS', 'FAILURE', 'ABANDONED']:
                outcomes.append(outcome)
            
            if problem_layer == "MEMORY_GAP": memory_gap_count += 1
            elif problem_layer == "SEARCH_GAP": search_gap_count += 1
            elif problem_layer == "BOTH": both_count += 1

    # Calculate metrics
    successful = outcomes.count('SUCCESS')
    partial = outcomes.count('PARTIAL_SUCCESS')
    failed = outcomes.count('FAILURE')
    abandoned = outcomes.count('ABANDONED')
    known = successful + partial + failed + abandoned
    
    failure_rate = ((failed + abandoned) / known * 100) if known > 0 else 0
    
    # Save reclassified records
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({"insights": insights}, f, indent=2)
        
    # Generate Validation Report
    report = f"# Reclassification Validation Report\n\n"
    report += f"## 1. Relevance Counts\n"
    report += f"- Previous relevant count (Old definition): {previous_relevant_count}\n"
    report += f"- New target-relevant count (Incomplete Memory): {new_target_relevant_count}\n\n"
    
    report += f"## 2. Changed Records\n"
    report += f"{len(changed_records)} records changed classification.\n\n"
    for c in changed_records[:15]:
        report += f"- **Record {c['record_id']}**: {c['old_relevance']} -> {c['new_relevance']}\n"
        report += f"  - Classified as: {c['issue_type']}\n"
        report += f"  - Snippet: \"{c['text_snippet']}\"\n"
    if len(changed_records) > 15:
        report += f"- ... and {len(changed_records) - 15} more.\n"
    report += "\n"
    
    report += f"## 3. New Target-Problem Metrics (from {new_target_relevant_count} records)\n"
    report += f"- Total Target Records: {new_target_relevant_count}\n"
    report += f"- Known Outcomes: {known}\n"
    report += f"- Successful: {successful}\n"
    report += f"- Partial Successes: {partial}\n"
    report += f"- Failed: {failed}\n"
    report += f"- Abandoned: {abandoned}\n"
    report += f"- **New Failure Rate:** {failure_rate:.1f}%\n\n"
    
    report += f"## 4. Problem Layer Distribution (Target Relevant Only)\n"
    report += f"- Memory Gap Only: {memory_gap_count}\n"
    report += f"- Search Gap Only: {search_gap_count}\n"
    report += f"- Both (Memory + Search Gap): {both_count}\n\n"
    
    report += f"## 5. Taxonomy Distribution (All 100 records)\n"
    for k, v in taxonomy_distribution.items():
        report += f"- {k}: {v}\n"
        
    report += "\n## 6. Ambiguities\n"
    report += "Rules-based NLP classification over unstructured reviews is prone to ambiguities. For instance, distinguishing 'SEARCH_FUNCTIONALITY' from 'INCOMPLETE_MEMORY_RETRIEVAL' heavily depends on explicitly detecting memory gaps (e.g., 'forgot', 'remember'). If a user simply says 'search is broken' but doesn't mention *why* they are searching, it is classified as SEARCH_FUNCTIONALITY rather than INCOMPLETE_MEMORY_RETRIEVAL. Similarly, some records discussing albums AND search might be biased toward ORGANIZATION due to keyword overlap.\n"
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
        
if __name__ == "__main__":
    process_records("backend/extracted_records.json", "backend/reclassified_records.json", "reclassification_validation_report.md")
