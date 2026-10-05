import json
import os
import time
from typing import List, Dict, Any
from .config import CONFIG
from .schemas import BatchExtractionResponse
from .prompts import SYSTEM_INSTRUCTION
from .validator import Validator
from .analyzer import Analyzer
from .reporter import Reporter
from .gemini_provider import GeminiProvider
from .openai_provider import OpenAIProvider
from .groq_provider import GroqProvider

class ExtractorEngine:
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.provider_name = CONFIG["AI_PROVIDER"]
        self.model_name = CONFIG["AI_MODEL"]
        self.batch_size = CONFIG["AI_BATCH_SIZE"]
        self.validator = Validator()
        self.reporter = Reporter()
        
        if self.provider_name.lower() == "gemini":
            self.provider = GeminiProvider(self.model_name, CONFIG["GEMINI_API_KEY"])
        elif self.provider_name.lower() == "openai":
            self.provider = OpenAIProvider(self.model_name, CONFIG["OPENAI_API_KEY"])
        elif self.provider_name.lower() == "groq":
            self.provider = GroqProvider(self.model_name, CONFIG["GROQ_API_KEY"])
        else:
            raise ValueError(f"Unsupported provider: {self.provider_name}")

    def load_data(self, input_file: str, output_file: str):
        with open(input_file, 'r', encoding='utf-8') as f:
            self.all_input_data = json.load(f)
            
        self.all_data_map = {r['record_id']: r for r in self.all_input_data}
        self.existing_records = []
        self.processed_ids = set()
        
        if os.path.exists(output_file):
            try:
                with open(output_file, 'r', encoding='utf-8') as f:
                    self.existing_records = json.load(f)
                    for rec in self.existing_records:
                        if "record_id" in rec:
                            self.processed_ids.add(rec["record_id"])
            except Exception as e:
                print(f"Could not load existing output: {e}")
                
        self.data_to_process = [r for r in self.all_input_data if r.get("record_id") not in self.processed_ids]

    def run(self, input_file: str, output_file: str, report_file: str):
        self.load_data(input_file, output_file)
        
        print(f"Total candidate records detected: {len(self.all_input_data)}")
        print(f"Records already processed: {len(self.processed_ids)}")
        print(f"Records remaining to process: {len(self.data_to_process)}")
        print(f"Provider: {self.provider_name.upper()} | Model: {self.model_name} | Batch size: {self.batch_size}")
        
        if self.dry_run:
            print("\n--- DRY RUN MODE ---")
            has_key = self.provider.is_available()
            key_str = "YES" if has_key else "NO"
            print(f"OPENAI_API_KEY detected: {key_str}")
            print(f"{len(self.all_input_data)} candidate records")
            print(f"{len(self.data_to_process)} remaining")
            print("No API calls made")
            return

        if not self.provider.is_available():
            print(f"Provider {self.provider_name} is not available (missing API keys).")
            return

        all_extracted = list(self.existing_records)
        quota_exhausted = False
        
        for i in range(0, len(self.data_to_process), self.batch_size):
            chunk = self.data_to_process[i:i+self.batch_size]
            print(f"Processing records {i} to {i+len(chunk)}...")
            
            prompt = f"Extract fields for these records:\n\n{json.dumps(chunk, indent=2)}"
            
            retries = 10
            while retries > 0:
                try:
                    results = self.provider.generate_batch(prompt, BatchExtractionResponse, SYSTEM_INSTRUCTION)
                    
                    chunk_map = {r['record_id']: r for r in chunk}
                    extracted_list = []
                    
                    for ex_dict in results:
                        rec_id = ex_dict['record_id']
                        if rec_id in chunk_map:
                            orig = chunk_map[rec_id]
                            ex_dict = self.validator.fix_evidence_quote(ex_dict, orig)
                            
                            merged = {**orig, **ex_dict}
                            merged['review_text'] = orig['review_text']
                            merged['source_url'] = orig['source_url']
                            
                            extracted_list.append(merged)
                    
                    all_extracted.extend(extracted_list)
                    print(f"Successfully processed {len(extracted_list)} records in this batch.")
                    
                    with open(output_file, 'w', encoding='utf-8') as f:
                        json.dump(all_extracted, f, indent=2)
                        
                    time.sleep(2)
                    break
                except Exception as e:
                    error_class = self.provider.classify_error(e)
                    print(f"Error: {error_class.error_message}")
                    print(f"Category: {error_class.error_category}")
                    
                    self.last_error_class = error_class
                    
                    if error_class.should_stop_immediately:
                        print(f"Stopping immediately due to: {error_class.error_category}")
                        break
                    elif error_class.is_temporary_server_error or error_class.is_rate_limit:
                        print(f"Rate limit / Temp error. Retrying in {error_class.retry_after}s... (Retries left: {retries-1})")
                        time.sleep(error_class.retry_after)
                    else:
                        print(f"Other error. Retrying in {error_class.retry_after}s... (Retries left: {retries-1})")
                        time.sleep(error_class.retry_after)
                    retries -= 1
                    
            if hasattr(self, 'last_error_class') and self.last_error_class.should_stop_immediately:
                break
            elif retries == 0:
                print("Stopping due to repeated errors.")
                break

        print("\nRunning Quality Checks...")
        errors = self.validator.check_quality(all_extracted, self.all_data_map)
        if errors:
            for e in errors:
                print(f"FAIL: {e}")
        else:
            print("PASS: All quality checks passed.")

        analyzer = Analyzer(all_extracted, self.all_input_data)
        analysis_results = analyzer.analyze()
        
        last_error = getattr(self, 'last_error_class', None)
        
        report_content = self.reporter.generate_report(analysis_results, last_error)
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
            
        self.reporter.generate_opportunity_outputs(len(all_extracted) > 0)
        
        print(f"\n{self.provider_name.upper()} EXTRACTION COMPLETE")
        
        is_auth = "YES" if last_error and last_error.error_category == "AUTHENTICATION_ERROR" else "NO"
        is_quota = "YES" if last_error and last_error.error_category == "BILLING_OR_QUOTA_ERROR" else "NO"
        
        print(f"Error category: {last_error.error_category if last_error else 'NONE'}")
        print(f"Error code: {last_error.error_code if last_error else 'NONE'}")
        print(f"Error message: {last_error.error_message if last_error else 'NONE'}")
        print(f"Quota exhausted: {is_quota}")
        print(f"Authentication error: {is_auth}")
        print(f"Records processed: {analysis_results['total_processed']}")
        print(f"Records remaining: {len(self.all_input_data) - analysis_results['total_processed']}")
