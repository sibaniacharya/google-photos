import json
from typing import Dict, Any

class Reporter:
    def format_dict(self, d: Dict[str, Any]) -> str:
        return "\\n".join(f"  - {k}: {v}" for k, v in sorted(d.items(), key=lambda x: -x[1]))

    def generate_report(self, analysis_results: Dict[str, Any], last_error: Any) -> str:
        report = f"# Semantic Extraction Report\n\n"
        
        report += "### VERIFIED DATA\n"
        is_auth = "YES" if last_error and last_error.error_category == "AUTHENTICATION_ERROR" else "NO"
        is_quota = "YES" if last_error and last_error.error_category == "BILLING_OR_QUOTA_ERROR" else "NO"
        
        report += f"- Error category: {last_error.error_category if last_error else 'NONE'}\n"
        report += f"- Error code: {last_error.error_code if last_error else 'NONE'}\n"
        report += f"- Error message: {last_error.error_message if last_error else 'NONE'}\n"
        report += f"- Quota exhausted: {is_quota}\n"
        report += f"- Authentication error: {is_auth}\n"
        report += f"- Records processed: {analysis_results['total_processed']}\n"
        report += f"- Records remaining: {analysis_results['total_input'] - analysis_results['total_processed']}\n\n"
        
        report += "### AI-EXTRACTED DATA\n"
        report += f"- Target-relevant TRUE count: {analysis_results['target_true']}\n"
        report += f"- Target-relevant FALSE count: {analysis_results['target_false']}\n\n"
        
        report += "### ANALYTICAL OUTPUT\n"
        dists = analysis_results['distributions']
        report += f"**retrieval_issue_type:**\n{self.format_dict(dists['retrieval_issue_type'])}\n\n"
        report += f"**problem_layer:**\n{self.format_dict(dists['problem_layer'])}\n\n"
        report += f"**retrieval_category:**\n{self.format_dict(dists['retrieval_category'])}\n\n"
        report += f"**outcome:**\n{self.format_dict(dists['outcome'])}\n\n"
        report += f"**confidence:**\n{self.format_dict(dists['confidence'])}\n\n"
        
        report += f"- Number of records containing HYPOTHESIS interpretations: {analysis_results['hypothesis_count']}\n"
        report += f"- Quota events: {is_quota}\n\n"
        
        report += "### Failure Rate Analysis\n"
        if analysis_results['failure_rate'] is None:
            report += "INSUFFICIENT SAMPLE FOR RELIABLE FAILURE RATE\n\n"
        else:
            report += f"- Failure Rate: {analysis_results['failure_rate']:.1f}%\n"
            report += f"- (Calculated over {analysis_results['known_outcome_count']} target-relevant records with known outcomes)\n\n"
        
        report += "### Target-Relevant Record IDs\n"
        report += ", ".join(analysis_results['target_relevant_ids']) + "\n\n"
        
        report += "### LIMITATIONS\n"
        report += "- AI Extractions are based on language models which may occasionally misinterpret nuance.\n"
        
        return report

    def generate_opportunity_outputs(self, has_successful_records: bool):
        base_dir = "backend"
        metadata = {"status": "Awaiting validated AI semantic extraction.", "message": "No valid data to generate opportunity structures."}
        empty_data = [] if not has_successful_records else [] # we would populate this if we had data

        if not has_successful_records:
            empty_data = metadata

        with open(f"{base_dir}/memory_search_outcome.json", 'w', encoding='utf-8') as f:
            json.dump(empty_data, f, indent=2)
            
        with open(f"{base_dir}/opportunity_map.json", 'w', encoding='utf-8') as f:
            json.dump(empty_data, f, indent=2)
            
        with open(f"{base_dir}/evidence_explorer.json", 'w', encoding='utf-8') as f:
            json.dump(empty_data, f, indent=2)
