import os
import json
import time
from ai_engine.config import load_config
from ai_engine.groq_provider import GroqProvider
from ai_engine.validator import Validator
from ai_engine.prompts import SYSTEM_INSTRUCTION
from ai_engine.schemas import BatchExtractionResponse

config = load_config()
api_key = config.get("GROQ_API_KEY", "")

if not api_key:
    print("Error: GROQ_API_KEY is missing.")
    exit(1)

input_file = "gemini_candidate_sample.json"
output_file = "groq_extracted_candidate_sample.json"
report_file = "groq_extraction_report.md"

with open(input_file, 'r', encoding='utf-8') as f:
    all_data = json.load(f)

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

provider = GroqProvider("openai/gpt-oss-120b", api_key)
validator = Validator()

all_extracted = list(existing_records)
last_api_error = None
api_error_count = 0

for i in range(0, len(data_to_process), batch_size):
    chunk = data_to_process[i:i+batch_size]
    print(f"Processing records {i} to {i+len(chunk)}...")
    
    prompt = f"Extract fields for these records:\n\n{json.dumps(chunk, indent=2)}"
    
    retries = 3
    success = False
    while retries > 0:
        try:
            results = provider.generate_batch(prompt, BatchExtractionResponse, SYSTEM_INSTRUCTION)
            
            chunk_map = {r['record_id']: r for r in chunk}
            extracted_list = []
            
            for ex_dict in results:
                rec_id = ex_dict['record_id']
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
                
            time.sleep(35) # Sleep to avoid TPM limit
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

print("\nRunning Quality Checks...")
errors = validator.check_quality(all_extracted, all_data_map)

total = len(all_extracted)
schema_valid = total
validator_pass = total if not errors else total - len(errors)
relevant = sum(1 for r in all_extracted if r.get('target_problem_relevant') is True)
not_relevant = total - relevant

distributions = {
    'retrieval_issue_type': {},
    'problem_layer': {},
    'retrieval_category': {},
    'outcome': {},
    'confidence': {},
    'evidence_vs_hypothesis': {}
}

for r in all_extracted:
    for k in distributions.keys():
        val = str(r.get(k))
        distributions[k][val] = distributions[k].get(val, 0) + 1

report_md = f"""# Groq Semantic Extraction Report

- **Total input records:** {len(all_data)}
- **Successfully processed records:** {total}
- **Remaining records:** {len(all_data) - total}
- **Schema-valid records:** {schema_valid}
- **Validator-pass records:** {validator_pass}
- **Validator-fail records:** {total - validator_pass}
- **target_problem_relevant TRUE count:** {relevant}
- **target_problem_relevant FALSE count:** {not_relevant}

### Distributions

**Retrieval Issue Type:**
"""
for k, v in distributions['retrieval_issue_type'].items():
    report_md += f"- {k}: {v}\n"

report_md += "\n**Problem Layer:**\n"
for k, v in distributions['problem_layer'].items():
    report_md += f"- {k}: {v}\n"

report_md += "\n**Retrieval Category:**\n"
for k, v in distributions['retrieval_category'].items():
    report_md += f"- {k}: {v}\n"

report_md += "\n**Outcome:**\n"
for k, v in distributions['outcome'].items():
    report_md += f"- {k}: {v}\n"

report_md += "\n**Confidence:**\n"
for k, v in distributions['confidence'].items():
    report_md += f"- {k}: {v}\n"

report_md += "\n**Evidence vs Hypothesis:**\n"
for k, v in distributions['evidence_vs_hypothesis'].items():
    report_md += f"- {k}: {v}\n"

report_md += "\n### Errors\n"
report_md += f"- **Validation errors:** {errors}\n"
report_md += f"- **API/model errors:** {last_api_error.error_category if last_api_error else 'None'}\n"
report_md += f"- **Exact model used:** openai/gpt-oss-120b\n"

with open(report_file, 'w', encoding='utf-8') as f:
    f.write(report_md)

print("\nExtraction Complete. Report written to groq_extraction_report.md")
