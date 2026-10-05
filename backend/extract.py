import json
import os
import argparse
from pydantic import TypeAdapter
from google import genai
from google.genai import types
from schema import RawRecord, BatchExtractionResponse
from dotenv import load_dotenv
import time

env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(env_path)

SYSTEM_INSTRUCTION = """
You are an expert AI extraction system for Google Photos product research.
Analyze the provided user conversations/reviews about Google Photos.

For each record:
1. Determine if it is relevant to photo/video RETRIEVAL problems. (Ignore general complaints like crashing or backups).
2. If relevant, extract the user's retrieval behavior based strictly on the provided text.
3. Identify the Memory-to-Search Gap: WHAT USER REMEMBERS -> WHAT USER FORGOT -> WHAT USER SEARCHES -> WHAT RESULT THEY GET -> WHERE THE GAP OCCURS.
4. Classify the retrieval problem into categories: Event-Based, Context-Based, Place-Based, Person-Based, Time-Based, Visual-Attribute, Object-Based, Screenshot/Document, Sequence-Based, Multi-Cue.
5. Provide evidence quotes for insights. Ensure quotes exactly match the text.
6. Evaluate confidence levels (HIGH, MEDIUM, LOW) for your inferences.
7. CRITICAL: Separate OBSERVATION from HYPOTHESIS. Do NOT claim technical causes (e.g. 'OCR failed', 'uses strict intersection') unless supported by authoritative evidence. State what was observed ('user searched passport, found nothing') and what the hypothesis is ('The search system may not effectively extract text from this image').
8. CRITICAL: Do NOT use absolute words such as 'overwhelmingly', 'majority', 'most', or 'dominant'.

Output strictly according to the requested JSON schema.
"""

def extract_insights(input_file: str, output_file: str):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set.")
        return

    client = genai.Client(api_key=api_key)
    
    with open(input_file, 'r', encoding='utf-8') as f:
        all_data = json.load(f)
    
    existing_insights = []
    processed_ids = set()
    
    if os.path.exists(output_file):
        try:
            with open(output_file, 'r', encoding='utf-8') as f:
                output_data = json.load(f)
                existing_insights = output_data.get("insights", [])
                for ins in existing_insights:
                    if "record_id" in ins:
                        processed_ids.add(ins["record_id"])
            print(f"Loaded {len(existing_insights)} existing insights. Resuming...")
        except Exception as e:
            print(f"Could not load existing output: {e}")
            
    data_to_process = [r for r in all_data if r.get("record_id") not in processed_ids]
    print(f"Total records to process: {len(data_to_process)} out of {len(all_data)}")
    
    all_insights = existing_insights
    chunk_size = 50
    
    for i in range(0, len(data_to_process), chunk_size):
        chunk = data_to_process[i:i+chunk_size]
        print(f"Processing records {i} to {i+len(chunk)} (chunk size {len(chunk)})...")
        
        prompt = f"Extract insights from the following user records:\n\n{json.dumps(chunk, indent=2)}"
        
        retries = 100
        while retries > 0:
            try:
                response = client.models.generate_content(
                    model='gemini-flash-latest',
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_INSTRUCTION,
                        response_mime_type="application/json",
                        response_schema=BatchExtractionResponse,
                        temperature=0.1,
                    ),
                )
                
                if response.text:
                    parsed_data = BatchExtractionResponse.model_validate_json(response.text)
                    all_insights.extend([insight.model_dump() for insight in parsed_data.insights])
                    print(f"Successfully processed {len(parsed_data.insights)} insights in this chunk.")
                    
                    with open(output_file, 'w', encoding='utf-8') as f:
                        json.dump({"insights": all_insights}, f, indent=2)
                    print(f"Saved {len(all_insights)} total insights incrementally.")
                    
                    time.sleep(10)
                    break
                else:
                    print("Empty response from LLM for this chunk.")
                    break
            except Exception as e:
                error_msg = str(e)
                print(f"Error processing chunk: {error_msg}")
                if "GenerateRequestsPerDayPerProjectPerModel-FreeTier" in error_msg:
                    print("Daily quota exhausted. Stopping extraction completely to preserve progress.")
                    print(f"Total insights successfully extracted so far: {len(all_insights)}")
                    return
                elif "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                    print("Rate limit hit. Retrying in 65s...")
                    time.sleep(65)
                elif "503" in error_msg or "UNAVAILABLE" in error_msg:
                    print(f"Service unavailable (503). Retrying in 65s... (Retries left: {retries-1})")
                    time.sleep(65)
                else:
                    print(f"Network or other error. Retrying in 30s... (Retries left: {retries-1})")
                    time.sleep(30)
                retries -= 1

    print(f"Successfully finished extraction. Total insights: {len(all_insights)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract Google Photos Retrieval Insights")
    parser.add_argument("--input", default="backend/real_data.json", help="Input raw JSON file")
    parser.add_argument("--output", default="backend/extracted_records.json", help="Output structured JSON file")
    
    args = parser.parse_args()
    extract_insights(args.input, args.output)

