import json
import random
import argparse
from collections import Counter

def generate_audit(input_file: str, output_file: str, sample_size: int = 30):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    insights = data.get('insights', [])
    
    # Select random sample
    sample_size = min(sample_size, len(insights))
    sample = random.sample(insights, sample_size)
    
    audit_md = f"# Extraction Audit\n\nRandom sample of {sample_size} records from true LLM extraction.\n\n"
    
    for i, record in enumerate(sample, 1):
        is_relevant = record.get('is_retrieval_relevant', False)
        
        audit_md += f"## Record {i}: {record.get('record_id')}\n"
        audit_md += f"- **Source:** {record.get('source', 'Unknown')}\n"
        audit_md += f"- **Original Source URL:** {record.get('source_url', 'Unknown')}\n"
        audit_md += f"- **Original User Text:** \"{record.get('original_text', '')}\"\n"
        audit_md += f"- **Retrieval Relevance:** {is_relevant}\n"
        
        if is_relevant:
            audit_md += f"- **What User Remembers:** {', '.join(record.get('remembered_information', []))}\n"
            audit_md += f"- **What User Forgot:** {', '.join(record.get('forgotten_information', []))}\n"
            audit_md += f"- **Search Query/Strategy:** {', '.join(record.get('search_formulation', []))} ({', '.join(record.get('search_classification', []))})\n"
            audit_md += f"- **Retrieval Outcome:** {record.get('retrieval_outcome', 'UNKNOWN')}\n"
            audit_md += f"- **Failure Reason:** {record.get('primary_failure_reason', 'N/A')}\n"
            audit_md += f"- **Retrieval Category:** {', '.join(record.get('retrieval_categories', []))}\n"
            audit_md += f"- **Underlying User Need:** {record.get('underlying_need_observed', 'N/A')}\n"
            
            gap = record.get('memory_search_gap', {})
            if gap:
                audit_md += "- **Memory-to-Search Gap:**\n"
                audit_md += f"  - Observed Evidence: {gap.get('where_the_gap_occurs_observed', '')}\n"
                audit_md += f"  - Hypothesis: {gap.get('where_the_gap_occurs_hypothesis', '')}\n"
                
            evidence = record.get('underlying_need_evidence', {})
            if evidence:
                audit_md += f"- **Observed Evidence (Need):** \"{evidence.get('evidence_quote', '')}\"\n"
                
            conf = record.get('relevance_confidence', {})
            if isinstance(conf, dict):
                audit_md += f"- **Confidence:** {conf.get('level', 'UNKNOWN')} ({conf.get('reason', '')})\n"
            
        audit_md += "\n---\n\n"
        
    # Generate Audit Summary from all existing records
    audit_md += "## Audit Summary (Based on All Extracted Records)\n\n"
    
    total_records = len(insights)
    relevant_records = [r for r in insights if r.get('is_retrieval_relevant')]
    
    outcomes = [r.get('retrieval_outcome') for r in relevant_records if r.get('retrieval_outcome')]
    successful = outcomes.count('SUCCESS') + outcomes.count('PARTIAL_SUCCESS')
    failed = outcomes.count('FAILURE')
    abandoned = outcomes.count('ABANDONED')
    known_outcomes = successful + failed + abandoned
    
    failure_rate = (failed + abandoned) / known_outcomes * 100 if known_outcomes > 0 else 0
    
    # Most common cues, forgotten, categories, failure modes
    memory_cues = []
    forgotten = []
    categories = []
    failure_modes = []
    
    for r in relevant_records:
        memory_cues.extend(r.get('remembered_information', []))
        forgotten.extend(r.get('forgotten_information', []))
        categories.extend(r.get('retrieval_categories', []))
        fm = r.get('primary_failure_reason')
        if fm and fm != 'N/A':
            failure_modes.append(fm)
            
    top_cues = [f"{k} ({v})" for k, v in Counter(memory_cues).most_common(5)]
    top_forgotten = [f"{k} ({v})" for k, v in Counter(forgotten).most_common(5)]
    top_categories = [f"{k} ({v})" for k, v in Counter(categories).most_common(5)]
    top_failures = [f"{k} ({v})" for k, v in Counter(failure_modes).most_common(5)]
    
    audit_md += f"- **Total Extracted Records:** {total_records}\n"
    audit_md += f"- **Relevant Retrieval Records:** {len(relevant_records)}\n"
    audit_md += f"- **Records with Known Outcomes:** {known_outcomes}\n"
    audit_md += f"- **Successful Retrievals:** {successful}\n"
    audit_md += f"- **Failed Retrievals:** {failed}\n"
    audit_md += f"- **Abandoned Retrievals:** {abandoned}\n"
    audit_md += f"- **Retrieval Failure Rate:** {failure_rate:.1f}%\n"
    
    audit_md += f"\n### Most Common Attributes\n"
    audit_md += f"- **Most Common Memory Cues:** {', '.join(top_cues) if top_cues else 'None'}\n"
    audit_md += f"- **Most Common Forgotten Information:** {', '.join(top_forgotten) if top_forgotten else 'None'}\n"
    audit_md += f"- **Most Common Retrieval Categories:** {', '.join(top_categories) if top_categories else 'None'}\n"
    audit_md += f"- **Most Common Failure Modes:** {', '.join(top_failures) if top_failures else 'None'}\n"

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(audit_md)
        
    print(f"Generated extraction audit saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="backend/extracted_records.json")
    parser.add_argument("--output", default="extraction_audit.md")
    args = parser.parse_args()
    
    generate_audit(args.input, args.output)
