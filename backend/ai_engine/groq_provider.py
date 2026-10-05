from typing import List, Dict, Any
import json
from groq import Groq
from .provider_base import LLMProvider, APIErrorClassification

class GroqProvider(LLMProvider):
    def __init__(self, model_name: str, api_key: str):
        super().__init__(model_name)
        self.api_key = api_key
        if self.is_available():
            self.client = Groq(api_key=self.api_key)
        else:
            self.client = None

    def is_available(self) -> bool:
        return bool(self.api_key)

    def generate_batch(self, prompt: str, schema: Any, system_instruction: str) -> List[Dict[str, Any]]:
        if not self.client:
            raise ValueError("Groq Client not initialized. API key missing.")
        
        if "json" not in system_instruction.lower() and "json" not in prompt.lower():
            system_instruction += " Please output in JSON format."
            
        system_instruction += "\nYou MUST return a JSON object with a single key 'records', which contains an array of the extracted record objects."
        
        completion = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.0
        )
        
        parsed_data = json.loads(completion.choices[0].message.content)
        if parsed_data and 'records' in parsed_data:
            return parsed_data['records']
        print(f"DEBUG raw response: {completion.choices[0].message.content}")
        return []

    def classify_error(self, error: Exception) -> APIErrorClassification:
        error_msg = str(error).lower()
        
        if "401" in error_msg or "authentication" in error_msg or "invalid api key" in error_msg:
            category = "AUTHENTICATION_ERROR"
        elif "403" in error_msg or "billing" in error_msg or "insufficient" in error_msg:
            category = "BILLING_OR_QUOTA_ERROR"
        elif "429" in error_msg or "rate limit" in error_msg or "too many requests" in error_msg:
            category = "RATE_LIMIT_ERROR"
        elif "model" in error_msg and ("invalid" in error_msg or "not found" in error_msg or "does not exist" in error_msg):
            category = "MODEL_ERROR"
        elif "500" in error_msg or "502" in error_msg or "503" in error_msg or "504" in error_msg:
            category = "SERVER_ERROR"
        else:
            category = "OTHER_ERROR"
            
        retry_after = 10
        if category == "SERVER_ERROR" or category == "RATE_LIMIT_ERROR":
            retry_after = 60

        return APIErrorClassification(
            error_category=category,
            error_code=str(error),
            is_quota_exhausted=(category == "BILLING_OR_QUOTA_ERROR"),
            is_rate_limit=(category == "RATE_LIMIT_ERROR"),
            is_temporary_server_error=(category == "SERVER_ERROR"),
            retry_after=retry_after,
            error_message=str(error)
        )
