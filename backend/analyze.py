import json
import argparse
from typing import Dict, List, Any
from collections import defaultdict

def analyze_data(input_file: str, output_file: str):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    insights = data.get('insights', [])
    relevant_insights = [i for i in insights if i.get('is_retrieval_relevant')]
    
    total_records = len(insights)
    relevant_count = len(relevant_insights)
    
    # Aggregations
    sources_count = defaultdict(int)
    unique_urls = set()
    outcomes = {"SUCCESS": 0, "PARTIAL_SUCCESS": 0, "FAILURE": 0, "ABANDONED": 0, "UNKNOWN": 0}
    categories = defaultdict(list)
    memory_cues = defaultdict(int)
    forgotten_info = defaultdict(int)
    search_strategies = defaultdict(int)
    failure_reasons = defaultdict(int)
    
    known_outcome_count = 0
    failure_count = 0
    
    # Gap Flows Tracking
    gap_flows = []
    
    for item in relevant_insights:
        sources_count[item.get('source', 'Unknown')] += 1
        if item.get('source_url'):
            unique_urls.add(item['source_url'])
            
        # Outcomes
        outcome = item.get('retrieval_outcome', 'UNKNOWN')
        outcomes[outcome] += 1
        
        if outcome in ["SUCCESS", "PARTIAL_SUCCESS", "FAILURE", "ABANDONED"]:
            known_outcome_count += 1
            if outcome in ["FAILURE", "ABANDONED"]:
                failure_count += 1
            
        # Categories
        for cat in item.get('retrieval_categories', []):
            categories[cat].append(item)
            
        # Memory cues (from remembered_information)
        for cue in item.get('remembered_information', []):
            memory_cues[cue] += 1
            
        # Forgotten info
        for info in item.get('forgotten_information', []):
            forgotten_info[info] += 1
            
        # Search strategy
        for strat in item.get('search_classification', []):
            search_strategies[strat] += 1
            
        # Failure reasons
        fail_reason = item.get('primary_failure_reason')
        if fail_reason:
            failure_reasons[fail_reason] += 1
            
        # Extract Flow Data
        gap = item.get('memory_search_gap', {})
        if gap:
            remembers = gap.get('what_user_remembers', ['Unknown'])
            forgot = gap.get('what_user_forgot', ['Unknown'])
            searches = gap.get('what_user_searches', ['Unknown'])
            result = gap.get('what_result_they_get', 'UNKNOWN')
            
            gap_flows.append({
                "source": remembers[0] if remembers else "Unknown",
                "target1": forgot[0] if forgot else "Unknown",
                "target2": searches[0] if searches else "Unknown",
                "outcome": result
            })
            
    # Calculate global failure rate
    global_failure_rate = (failure_count / known_outcome_count * 100) if known_outcome_count > 0 else None
            
    clusters = []
    for cat, cluster_records in categories.items():
        # Cluster level metrics
        cluster_known_outcomes = sum(1 for i in cluster_records if i.get('retrieval_outcome') in ["SUCCESS", "PARTIAL_SUCCESS", "FAILURE", "ABANDONED"])
        cluster_failures = sum(1 for i in cluster_records if i.get('retrieval_outcome') in ['FAILURE', 'ABANDONED'])
        cluster_failure_rate = (cluster_failures / cluster_known_outcomes * 100) if cluster_known_outcomes > 0 else None
        
        total_attempts = sum(i.get('retrieval_attempts', 0) for i in cluster_records)
        workaround_count = sum(1 for i in cluster_records if i.get('workaround_used'))
        
        # Source distribution in cluster
        cluster_sources = defaultdict(int)
        for i in cluster_records:
            cluster_sources[i.get('source', 'Unknown')] += 1
            
        clusters.append({
            "cluster_name": cat,
            "description": f"Issues related to {cat}",
            "record_count": len(cluster_records),
            "percentage_of_relevant": round((len(cluster_records) / relevant_count * 100), 1) if relevant_count > 0 else 0,
            "observed_failure_count": cluster_failures,
            "known_outcome_count": cluster_known_outcomes,
            "retrieval_failure_rate": round(cluster_failure_rate, 1) if cluster_failure_rate is not None else "Insufficient sample",
            "total_search_attempts": total_attempts,
            "workarounds_used": workaround_count,
            "source_distribution": dict(cluster_sources),
            "representative_records": [
                {
                    "source": i.get('source'),
                    "source_url": i.get('source_url'),
                    "date": i.get('date', 'Unknown'),
                    "quote": i.get('original_text', '')[:200] + "...",
                    "hypothesis": i.get('memory_search_gap', {}).get('where_the_gap_occurs_hypothesis', 'No hypothesis available') if i.get('memory_search_gap') else 'No hypothesis available',
                    "observation": i.get('memory_search_gap', {}).get('where_the_gap_occurs_observed', 'No observation available') if i.get('memory_search_gap') else 'No observation available',
                    "outcome": i.get('retrieval_outcome', 'UNKNOWN')
                } for i in cluster_records[:5]
            ]
        })
        
    dashboard_data = {
        "overview": {
            "total_records": total_records,
            "relevant_records": relevant_count,
            "known_outcomes": known_outcome_count,
            "global_failures": failure_count,
            "global_failure_rate": round(global_failure_rate, 1) if global_failure_rate is not None else "Insufficient sample",
            "sources_count": dict(sources_count),
            "unique_source_urls": len(unique_urls)
        },
        "outcomes": outcomes,
        "memory_cues": dict(memory_cues),
        "forgotten_info": dict(forgotten_info),
        "search_strategies": dict(search_strategies),
        "failure_reasons": dict(failure_reasons),
        "clusters": clusters,
        "gap_flows": gap_flows[:50] # Top 50 flows for visualization
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(dashboard_data, f, indent=2)
        
    print(f"Generated robust dashboard data and saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze extracted insights and generate evidence-based metrics")
    parser.add_argument("--input", default="extracted_records.json", help="Input extracted JSON file")
    parser.add_argument("--output", default="dashboard_data.json", help="Output dashboard JSON file")
    
    args = parser.parse_args()
    analyze_data(args.input, args.output)
