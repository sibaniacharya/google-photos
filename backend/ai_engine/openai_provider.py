from typing import List, Dict, Any
from openai import OpenAI
from pydantic import BaseModel
from .provider_base import LLMProvider, APIErrorClassification

class OpenAIProvider(LLMProvider):
    def __init__(self, model_name: str, api_key: str):
        super().__init__(model_name)
        self.api_key = api_key
        if self.is_available():
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = None

    def is_available(self) -> bool:
        return bool(self.api_key)

    def generate_batch(self, prompt: str, schema: Any, system_instruction: str) -> List[Dict[str, Any]]:
        if not self.client:
            raise ValueError("OpenAI Client not initialized. API key missing.")
        
        completion = self.client.beta.chat.completions.parse(
            model=self.model_name,
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": prompt}
            ],
            response_format=schema,
            temperature=0.0
        )
        
        parsed_data = completion.choices[0].message.parsed
        if parsed_data and hasattr(parsed_data, 'records'):
            return [ex_rec.model_dump() for ex_rec in parsed_data.records]
        return []

    def classify_error(self, error: Exception) -> APIErrorClassification:
        error_msg = str(error).lower()
        
        # Identify the main categories
        if "401" in error_msg or "invalid_api_key" in error_msg or "incorrect api key" in error_msg:
            category = "AUTHENTICATION_ERROR"
        elif "insufficient_quota" in error_msg or "billing" in error_msg:
            category = "BILLING_OR_QUOTA_ERROR"
        elif "429" in error_msg or "rate limit" in error_msg:
            category = "RATE_LIMIT_ERROR"
        elif "500" in error_msg or "502" in error_msg or "503" in error_msg or "504" in error_msg or "timeout" in error_msg:
            category = "SERVER_ERROR"
        elif "model" in error_msg and ("invalid" in error_msg or "not found" in error_msg):
            category = "MODEL_ERROR"
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
