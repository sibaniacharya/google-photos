import os
import json
import time
from ai_engine.config import load_config
from ai_engine.groq_provider import GroqProvider
from ai_engine.validator import Validator
from ai_engine.prompts import SYSTEM_INSTRUCTION
from ai_engine.schemas import BatchExtractionResponse

def run():
    config = load_config()
    api_key = config.get("GROQ_API_KEY", "")

    if not api_key:
        print("Error: GROQ_API_KEY is missing.")
        return

    input_file = "high_recall_candidate_pool.json"
    output_file = "groq_high_recall_extraction.json"
    report_file = "groq_high_recall_extraction_report.md"

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            all_data = json.load(f)
    except Exception as e:
        print(f"Error loading {input_file}: {e}")
        return

    all_data_map = {r['record_id']: r for r in all_data}
    existing_records = []
    processed_ids = set()

    if os.path.exists(output_file):
        try:
            with open(output_file, 'r', encoding='utf-8') as f:
                existing_records = json.load(f)
                for rec in existing_records:
                    if "record_id" in rec:
                        processed_ids.add(rec["record_id"])
        except Exception as e:
            print(f"Could not load existing output: {e}")

    data_to_process = [r for r in all_data if r.get("record_id") not in processed_ids]
    batch_size = 5

    print(f"Total candidate records detected: {len(all_data)}")
    print(f"Records already processed: {len(processed_ids)}")
    print(f"Records remaining to process: {len(data_to_process)}")
    
    if len(data_to_process) == 0:
        print("All records processed. Generating report.")
    else:
        provider = GroqProvider("openai/gpt-oss-120b", api_key)
        validator = Validator()
    
        all_extracted = list(existing_records)
        last_api_error = None
        api_error_count = 0
    
        for i in range(0, len(data_to_process), batch_size):
            chunk = data_to_process[i:i+batch_size]
            print(f"Processing records {i} to {i+len(chunk)}...")
            
            prompt = f"""Extract fields for these records:
    
STRICT TARGET DEFINITION:
A record is TRUE only when BOTH conditions are satisfied:
1. The user is trying to retrieve a specific existing photo, video, image, document, or screenshot.
AND
2. The user's memory or identifying information about that item is incomplete, ambiguous, uncertain, or insufficient for straightforward retrieval.
    
Generic complaints about search, navigation, UI, editing, backup, sync, crashes, storage, feature requests, or organization are NOT target cases unless the review clearly describes an incomplete-memory retrieval attempt.
Do not infer missing information that the user did not state.
Do not invent search queries, dates, locations, people, albums, metadata, attempts, outcomes, or reasons for failure.
If search behavior is not stated, use UNKNOWN.
If digital retrieval intent cannot be established, classify as FALSE. If a user describes losing a physical photograph without establishing an attempt to retrieve a digital copy through Google Photos, classify as FALSE.
    
{json.dumps(chunk, indent=2)}"""
            
            retries = 3
            success = False
            while retries > 0:
                try:
                    results = provider.generate_batch(prompt, BatchExtractionResponse, SYSTEM_INSTRUCTION)
                    
                    chunk_map = {r['record_id']: r for r in chunk}
                    extracted_list = []
                    
                    for ex_dict in results:
                        rec_id = ex_dict.get('record_id')
                        if rec_id in chunk_map:
                            orig = chunk_map[rec_id]
                            ex_dict = validator.fix_evidence_quote(ex_dict, orig)
                            
                            merged = {**orig, **ex_dict}
                            merged['review_text'] = orig['review_text']
                            merged['source_url'] = orig['source_url']
                            
                            extracted_list.append(merged)
                    
                    all_extracted.extend(extracted_list)
                    print(f"Successfully processed {len(extracted_list)} records in this batch.")
                    
                    with open(output_file, 'w', encoding='utf-8') as f:
                        json.dump(all_extracted, f, indent=2)
                        
                    # Reduced sleep to speed up. Rate limit handler will catch errors.
                    time.sleep(2) 
                    success = True
                    break
                except Exception as e:
                    error_class = provider.classify_error(e)
                    print(f"Error: {error_class.error_message}")
                    print(f"Category: {error_class.error_category}")
                    last_api_error = error_class
                    
                    if error_class.should_stop_immediately:
                        print(f"Stopping immediately due to: {error_class.error_category}")
                        break
                    elif error_class.is_temporary_server_error or error_class.is_rate_limit:
                        print(f"Rate limit / Temp error. Retrying in {error_class.retry_after}s...")
                        time.sleep(error_class.retry_after)
                    else:
                        print(f"Other error. Retrying in {error_class.retry_after}s...")
                        time.sleep(error_class.retry_after)
                    retries -= 1
                    
            if not success:
                print("Stopping batch processing due to repeated errors.")
                api_error_count += 1
                break

    # Re-load from disk to ensure we have the latest
    try:
        with open(output_file, 'r', encoding='utf-8') as f:
            all_extracted = json.load(f)
    except:
        all_extracted = []

    print("\nRunning Quality Checks...")
    validator = Validator()
    errors = validator.check_quality(all_extracted, all_data_map)

    total = len(all_extracted)
    schema_valid = total
    validator_pass = total if not errors else total - len(errors)
    relevant = sum(1 for r in all_extracted if r.get('target_problem_relevant') is True)
    not_relevant = total - relevant

    true_distributions = {
        'retrieval_category': {},
        'outcome': {}
    }
    distributions = {
        'problem_layer': {},
        'evidence_vs_hypothesis': {}
    }

    ambiguity_patterns = {}

    for r in all_extracted:
        pl = str(r.get('problem_layer'))
        evh = str(r.get('evidence_vs_hypothesis'))
        distributions['problem_layer'][pl] = distributions['problem_layer'].get(pl, 0) + 1
        distributions['evidence_vs_hypothesis'][evh] = distributions['evidence_vs_hypothesis'].get(evh, 0) + 1
        
        if r.get('target_problem_relevant') is True:
            rc = str(r.get('retrieval_category'))
            oc = str(r.get('outcome'))
            true_distributions['retrieval_category'][rc] = true_distributions['retrieval_category'].get(rc, 0) + 1
            true_distributions['outcome'][oc] = true_distributions['outcome'].get(oc, 0) + 1

            if "UNKNOWN" in str(r.get('search_strategy', '')).upper() or "UNKNOWN" in str(r.get('memory_trigger', '')).upper():
                ambig = "Missing details for search strategy / triggers"
                ambiguity_patterns[ambig] = ambiguity_patterns.get(ambig, 0) + 1
            
            if "disappear" in str(r.get('failure_reason', '')).lower() or "delet" in str(r.get('failure_reason', '')).lower():
                ambig = "User attributes failure to system deletion rather than retrieval failure"
                ambiguity_patterns[ambig] = ambiguity_patterns.get(ambig, 0) + 1

    report_md = f"""# Groq High-Recall Extraction Report

1. Total candidates: {len(all_data)}
2. Successfully processed: {total}
3. Schema-valid count: {schema_valid}
4. Validator-pass count: {validator_pass}
5. Validator-fail count: {total - validator_pass}
6. Target TRUE count: {relevant}
7. Target FALSE count: {not_relevant}
8. API/rate-limit errors: {'None' if 'last_api_error' not in locals() or last_api_error is None else last_api_error.error_category} ({'0' if 'api_error_count' not in locals() else api_error_count} unrecoverable)

### 9. Retrieval category distribution among TRUE cases
"""
    for k, v in true_distributions['retrieval_category'].items():
        report_md += f"- {k}: {v}\n"

    report_md += "\n### 10. Outcome distribution among TRUE cases\n"
    for k, v in true_distributions['outcome'].items():
        report_md += f"- {k}: {v}\n"

    report_md += "\n### 11. Problem-layer distribution\n"
    for k, v in distributions['problem_layer'].items():
        report_md += f"- {k}: {v}\n"

    report_md += "\n### 12. Evidence-vs-hypothesis distribution\n"
    for k, v in distributions['evidence_vs_hypothesis'].items():
        report_md += f"- {k}: {v}\n"

    report_md += "\n### 13. List of any validation failures with record IDs\n"
    if errors:
        for err in errors:
            report_md += f"- {err}\n"
    else:
        report_md += "- None\n"

    report_md += "\n### 14. Any ambiguity patterns that require manual audit\n"
    if ambiguity_patterns:
        for k, v in ambiguity_patterns.items():
            report_md += f"- {k}: {v} records\n"
    else:
        report_md += "- No prominent ambiguity patterns detected automatically. All TRUE cases require manual audit.\n"

    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report_md)

    print(f"\\nExtraction Complete. Report written to {report_file}")

if __name__ == "__main__":
    run()
