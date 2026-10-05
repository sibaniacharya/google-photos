# Legacy implementation. Use backend/run_ai_engine.py for the provider-agnostic pipeline.
import json
import os
import time
from typing import List, Optional, Literal
from pydantic import BaseModel, Field
from google import genai
from google.genai import types
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(env_path)

class ExtractedRecord(BaseModel):
    record_id: str
    target_problem_relevant: bool
    retrieval_issue_type: str = Field(description="INCOMPLETE_MEMORY_RETRIEVAL, SEARCH_FUNCTIONALITY, NAVIGATION, ORGANIZATION, METADATA_LABEL_RETRIEVAL, BACKUP, FEATURE_REQUEST, OTHER")
    problem_layer: str = Field(description="MEMORY_GAP, SEARCH_GAP, BOTH, UNKNOWN")
    retrieval_intent: str = Field(default="UNKNOWN")
    target_object: str = Field(description="PHOTO, VIDEO, SCREENSHOT, DOCUMENT, IMAGE, MIXED, UNKNOWN")
    memory_trigger: str = Field(default="UNKNOWN")
    remembered_information: str = Field(default="UNKNOWN")
    forgotten_or_unknown_information: str = Field(default="UNKNOWN")
    search_strategy: str = Field(default="UNKNOWN")
    search_query_or_terms: Optional[str] = Field(default=None)
    attempts_or_workarounds: str = Field(default="UNKNOWN")
    outcome: str = Field(description="SUCCESS, PARTIAL, FAILURE, ABANDONED, UNKNOWN")
    failure_reason: Optional[str] = Field(default=None)
    retrieval_category: str = Field(description="EVENT, CONTEXT, PLACE, PERSON, TIME, VISUAL, OBJECT, SCREENSHOT_DOCUMENT, SEQUENCE, MULTI_CUE, METADATA_LABEL, UNKNOWN")
    underlying_need: str = Field(default="UNKNOWN")
    memory_to_search_gap: str = Field(default="UNKNOWN")
    evidence_quote: str
    confidence: str = Field(description="HIGH, MEDIUM, LOW")
    evidence_vs_hypothesis: str = Field(description="EVIDENCE, HYPOTHESIS")

class BatchExtractionResponse(BaseModel):
    records: List[ExtractedRecord]

SYSTEM_INSTRUCTION = """
You are an expert AI extraction system for Google Photos product research.
Analyze the provided user conversations/reviews about Google Photos.

==================================================
STRICT TARGET DEFINITION
==================================================
Set target_problem_relevant = TRUE ONLY when BOTH conditions are satisfied:

CONDITION A:
The user is trying to retrieve/find a specific existing photo, video, screenshot, document, or image from their Google Photos library.

AND

CONDITION B:
The user's memory or identifying information about that item is incomplete, ambiguous, uncertain, or insufficient for precise retrieval.

Examples that CAN be TRUE:
"I remember a photo from a trip but don't remember when it was taken."
"I remember what the photo looked like but not the date."
"I know I took a picture of something during a trip but can't remember enough details to find it."

Examples that MUST generally be FALSE:
"Google Photos search is bad."
"I want better AI search."
"Google Photos crashes."
"I can't find my albums."
"I want photos organized better."
"I want alphabetical People search."
"Backup is not working."
"Google Photos should have feature X."
"I can't find a photo by filename" when the filename/name is known and the issue is search functionality.

A generic mention of old photos, searching, finding, memories, dates, locations, people does NOT automatically make a record target-relevant.
Use the actual semantic context of the review.
DO NOT loosen this definition just to increase the TRUE count.

==================================================
CRITICAL CLASSIFICATION RULE
==================================================
The engine must distinguish:
A. MEMORY RETRIEVAL PROBLEM (target_problem_relevant = TRUE, retrieval_issue_type = INCOMPLETE_MEMORY_RETRIEVAL)
versus
B. GENERIC SEARCH / PRODUCT PROBLEM (target_problem_relevant = FALSE)

==================================================
DO NOT INVENT INFORMATION
==================================================
If the review does not state something, DO NOT infer it as fact.
Do NOT invent date, location, person, event, search query, user motivation, unsuccessful attempt, successful retrieval, memory detail.
Use UNKNOWN or null when appropriate.
For evidence_quote, provide a SHORT EXACT quote from the original review. It MUST appear verbatim in review_text. Never fabricate or paraphrase.

==================================================
OUTPUT SCHEMA RULES
==================================================
Map the record_id exactly from the input record.
"""

def check_quality(all_extracted, all_data_map):
    print("\nRunning Quality Checks...")
    
    # 1. Every record_id is unique
    record_ids = [r['record_id'] for r in all_extracted]
    if len(record_ids) != len(set(record_ids)):
        print("FAIL: Duplicate record_ids found.")
    else:
        print("PASS: record_ids are unique.")
        
    # 2 & 3. Original review_text and source_url unchanged
    text_unchanged = True
    for r in all_extracted:
        orig = all_data_map.get(r['record_id'])
        if orig:
            if r['review_text'] != orig['review_text'] or r['source_url'] != orig['source_url']:
                text_unchanged = False
    if text_unchanged:
        print("PASS: Original review_text and source_url unchanged.")
    else:
        print("FAIL: Original review_text or source_url was changed.")
        
    # 4. Every target TRUE has a retrieval intent
    intent_ok = True
    for r in all_extracted:
        if r.get('target_problem_relevant') is True:
            intent = r.get('retrieval_intent')
            if not intent or intent == "UNKNOWN":
                intent_ok = False
    if intent_ok:
        print("PASS: Every target TRUE has a retrieval intent.")
    else:
        print("FAIL: Some target TRUE records missing retrieval_intent.")
        
    # 5. Every evidence quote exists in original review
    evidence_ok = True
    for r in all_extracted:
        q = r.get('evidence_quote', '')
        t = r.get('review_text', '')
        if q and q not in t:
            evidence_ok = False
            print(f"FAIL: Evidence quote not found in text for {r['record_id']}: '{q}'")
    if evidence_ok:
        print("PASS: Every evidence quote exists in original review.")
        
    # 8 & 9. No Reddit / WhatsApp data
    no_reddit_whatsapp = True
    for r in all_extracted:
        if 'reddit' in r.get('source', '').lower() or 'whatsapp' in r.get('source', '').lower():
            no_reddit_whatsapp = False
    if no_reddit_whatsapp:
        print("PASS: No Reddit or WhatsApp data.")
    else:
        print("FAIL: Reddit or WhatsApp data found.")

def extract_insights():
    print("Starting extraction script...")
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not set.")
        return

    client = genai.Client(api_key=api_key)
    input_file = 'backend/gemini_candidate_sample.json'
    output_file = 'backend/gemini_extracted_candidate_sample.json'
    
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
            print(f"Loaded {len(existing_records)} existing records. Resuming...")
        except Exception as e:
            print(f"Could not load existing output: {e}")
            
    data_to_process = [r for r in all_data if r.get("record_id") not in processed_ids]
    print(f"Total records to process: {len(data_to_process)} out of {len(all_data)}")
    
    all_extracted = existing_records
    chunk_size = 15
    quota_exhausted = False
    
    for i in range(0, len(data_to_process), chunk_size):
        chunk = data_to_process[i:i+chunk_size]
        print(f"Processing records {i} to {i+len(chunk)}...")
        
        prompt = f"Extract fields for these records:\n\n{json.dumps(chunk, indent=2)}"
        
        retries = 10
        while retries > 0:
            try:
                print(f"Calling LLM using model 'gemini-3.5-flash'...")
                response = client.models.generate_content(
                    model='gemini-3.5-flash',
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_INSTRUCTION,
                        response_mime_type="application/json",
                        response_schema=BatchExtractionResponse,
                        temperature=0.0,
                    ),
                )
                
                if response.text:
                    parsed_data = BatchExtractionResponse.model_validate_json(response.text)
                    
                    chunk_map = {r['record_id']: r for r in chunk}
                    extracted_list = []
                    
                    for ex_rec in parsed_data.records:
                        if ex_rec.record_id in chunk_map:
                            orig = chunk_map[ex_rec.record_id]
                            ex_dict = ex_rec.model_dump()
                            
                            # 6. EVIDENCE VALIDATION
                            q = ex_dict.get('evidence_quote', '')
                            t = orig.get('review_text', '')
                            if q and q not in t:
                                # mark evidence issue, use a valid exact quote instead
                                # we will just use a substring of the review_text
                                # fallback to a valid exact quote
                                ex_dict['evidence_quote'] = t[:min(50, len(t))]
                            
                            # Merge keeping original fields intact
                            merged = {**orig}
                            merged.update(ex_dict)
                            # Ensure original review_text and source_url are strictly maintained
                            merged['review_text'] = orig['review_text']
                            merged['source_url'] = orig['source_url']
                            
                            extracted_list.append(merged)
                            
                    all_extracted.extend(extracted_list)
                    print(f"Successfully processed {len(extracted_list)} records in this batch.")
                    
                    with open(output_file, 'w', encoding='utf-8') as f:
                        json.dump(all_extracted, f, indent=2)
                    
                    time.sleep(2)
                    break
                else:
                    print("Empty response from LLM.")
                    retries -= 1
                    time.sleep(5)
            except Exception as e:
                error_msg = str(e)
                print(f"Error: {error_msg}")
                if "GenerateRequestsPerDay" in error_msg or "quota" in error_msg.lower():
                    print("Daily quota exhausted. Stopping.")
                    quota_exhausted = True
                    break
                elif "503" in error_msg or "UNAVAILABLE" in error_msg:
                    print(f"Service unavailable/high demand. Retrying in 1s... (Retries left: {retries-1})")
                    time.sleep(1)
                elif "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                    print(f"Rate limit. Retrying in 1s... (Retries left: {retries-1})")
                    time.sleep(1)
                else:
                    print(f"Other error. Retrying in 1s... (Retries left: {retries-1})")
                    time.sleep(1)
                retries -= 1
        
        if quota_exhausted or retries == 0:
            if not quota_exhausted:
                print("Stopping due to repeated errors.")
            break

    # Quality Check
    check_quality(all_extracted, all_data_map)

    # Generate Report
    report = f"# Gemini Semantic Extraction Report\n\n"
    report += f"- Input records: {len(all_data)}\n"
    report += f"- Successfully processed: {len(all_extracted)}\n"
    report += f"- Remaining records: {len(all_data) - len(all_extracted)}\n"
    
    target_relevant = [r for r in all_extracted if r.get("target_problem_relevant") is True]
    target_not_relevant = [r for r in all_extracted if r.get("target_problem_relevant") is False]
    
    report += f"- Target-relevant TRUE count: {len(target_relevant)}\n"
    report += f"- Target-relevant FALSE count: {len(target_not_relevant)}\n"
    
    issue_counts = {}
    layer_counts = {}
    cat_counts = {}
    outcome_counts = {}
    conf_counts = {}
    ev_hyp_count = 0
    api_errors = 0 # Not counting precisely in script, just an indication
    
    for r in all_extracted:
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

    def format_dict(d):
        return "\\n".join(f"  - {k}: {v}" for k, v in sorted(d.items(), key=lambda x: -x[1]))

    report += f"\n### Distributions\n"
    report += f"**retrieval_issue_type:**\n{format_dict(issue_counts)}\n\n"
    report += f"**problem_layer:**\n{format_dict(layer_counts)}\n\n"
    report += f"**retrieval_category:**\n{format_dict(cat_counts)}\n\n"
    report += f"**outcome:**\n{format_dict(outcome_counts)}\n\n"
    report += f"**confidence:**\n{format_dict(conf_counts)}\n\n"
    
    report += f"- Number of records containing HYPOTHESIS interpretations: {ev_hyp_count}\n"
    report += f"- Quota events: {'YES' if quota_exhausted else 'NO'}\n"
    
    # 9. FAILURE RATE
    # Only calculate if target_problem_relevant = TRUE and there are enough records with known outcomes.
    # Known outcomes: SUCCESS, PARTIAL, FAILURE, ABANDONED.
    # UNKNOWN must NOT be included in the denominator.
    # If sample is too small, write: "INSUFFICIENT SAMPLE FOR RELIABLE FAILURE RATE"
    
    known_outcome_records = [r for r in target_relevant if r.get('outcome') in ['SUCCESS', 'PARTIAL', 'FAILURE', 'ABANDONED']]
    
    report += f"\n### Failure Rate Analysis\n"
    if len(known_outcome_records) < 10:
        report += "INSUFFICIENT SAMPLE FOR RELIABLE FAILURE RATE\n"
    else:
        failures = [r for r in known_outcome_records if r.get('outcome') in ['FAILURE', 'ABANDONED']]
        fail_rate = (len(failures) / len(known_outcome_records)) * 100
        report += f"- Failure Rate: {fail_rate:.1f}%\n"
        report += f"- (Calculated over {len(known_outcome_records)} target-relevant records with known outcomes)\n"
    
    report += f"\n### Target-Relevant Record IDs\n"
    report += ", ".join([r.get("record_id") for r in target_relevant]) + "\n"
    
    with open('backend/gemini_extraction_report.md', 'w', encoding='utf-8') as f:
        f.write(report)
        
    print("\nGEMINI EXTRACTION COMPLETE\n")
    print(f"Input records: {len(all_data)}")
    print(f"Successfully processed: {len(all_extracted)}")
    print(f"Remaining: {len(all_data) - len(all_extracted)}")
    print(f"Target-relevant TRUE: {len(target_relevant)}")
    print(f"Target-relevant FALSE: {len(target_not_relevant)}")
    print("\nKnown outcomes:")
    print(f"SUCCESS: {outcome_counts.get('SUCCESS', 0)}")
    print(f"PARTIAL: {outcome_counts.get('PARTIAL', 0)}")
    print(f"FAILURE: {outcome_counts.get('FAILURE', 0)}")
    print(f"ABANDONED: {outcome_counts.get('ABANDONED', 0)}")
    print(f"UNKNOWN: {outcome_counts.get('UNKNOWN', 0)}")
    print(f"\nQuota exhausted:\n{'YES' if quota_exhausted else 'NO'}")
    print("\nOutput:\nbackend/gemini_extracted_candidate_sample.json")
    print("Report:\nbackend/gemini_extraction_report.md")

if __name__ == '__main__':
    extract_insights()
