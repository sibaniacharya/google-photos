from typing import List, Dict, Any

class Analyzer:
    def __init__(self, extracted_records: List[Dict[str, Any]], all_input_records: List[Dict[str, Any]]):
        self.extracted_records = extracted_records
        self.all_input_records = all_input_records
        
    def analyze(self) -> Dict[str, Any]:
        target_relevant = [r for r in self.extracted_records if r.get("target_problem_relevant") is True]
        target_not_relevant = [r for r in self.extracted_records if r.get("target_problem_relevant") is False]
        
        issue_counts = {}
        layer_counts = {}
        cat_counts = {}
        outcome_counts = {}
        conf_counts = {}
        ev_hyp_count = 0
        
        for r in self.extracted_records:
            issue = r.get("retrieval_issue_type")
            issue_counts[issue] = issue_counts.get(issue, 0) + 1
            
            layer = r.get("problem_layer")
            layer_counts[layer] = layer_counts.get(layer, 0) + 1
            
            c = r.get("retrieval_category")
            cat_counts[c] = cat_counts.get(c, 0) + 1
                
            outc = r.get("outcome")
            outcome_counts[outc] = outcome_counts.get(outc, 0) + 1
            
            conf = r.get("confidence")
            conf_counts[conf] = conf_counts.get(conf, 0) + 1
            
            ev_hyp = r.get("evidence_vs_hypothesis", "")
            if "HYPOTHESIS" in ev_hyp:
                ev_hyp_count += 1
                
        known_outcome_records = [r for r in target_relevant if r.get('outcome') in ['SUCCESS', 'PARTIAL', 'FAILURE', 'ABANDONED']]
        fail_rate = None
        if len(known_outcome_records) >= 10:
            failures = [r for r in known_outcome_records if r.get('outcome') in ['FAILURE', 'ABANDONED']]
            fail_rate = (len(failures) / len(known_outcome_records)) * 100
            
        return {
            "total_input": len(self.all_input_records),
            "total_processed": len(self.extracted_records),
            "target_true": len(target_relevant),
            "target_false": len(target_not_relevant),
            "distributions": {
                "retrieval_issue_type": issue_counts,
                "problem_layer": layer_counts,
                "retrieval_category": cat_counts,
                "outcome": outcome_counts,
                "confidence": conf_counts
            },
            "hypothesis_count": ev_hyp_count,
            "failure_rate": fail_rate,
            "known_outcome_count": len(known_outcome_records),
            "target_relevant_ids": [r.get("record_id") for r in target_relevant]
        }
