from typing import List, Dict, Any
from google import genai
from google.genai import types
from .provider_base import LLMProvider, APIErrorClassification
import os

class GeminiProvider(LLMProvider):
    def __init__(self, model_name: str, api_key: str):
        super().__init__(model_name)
        self.api_key = api_key
        if self.is_available():
            self.client = genai.Client(api_key=self.api_key)
        else:
            self.client = None

    def is_available(self) -> bool:
        return bool(self.api_key)

    def generate_batch(self, prompt: str, schema: Any, system_instruction: str) -> List[Dict[str, Any]]:
        if not self.client:
            raise ValueError("Gemini Client not initialized. API key missing.")
        
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                response_schema=schema,
                temperature=0.0,
            ),
        )
        
        if response.text:
            parsed_data = schema.model_validate_json(response.text)
            return [ex_rec.model_dump() for ex_rec in parsed_data.records]
        return []

    def classify_error(self, error: Exception) -> APIErrorClassification:
        error_msg = str(error)
        is_quota_exhausted = "GenerateRequestsPerDay" in error_msg or "quota" in error_msg.lower()
        is_temp = "503" in error_msg or "UNAVAILABLE" in error_msg
        is_rate = "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg
        
        # Free tier explicitly throws quota error disguised as 429 in some metrics
        if is_rate and ("limit: 0" in error_msg or "free_tier_requests" in error_msg):
            is_quota_exhausted = True
            
        retry_after = 10
        if is_temp or is_rate:
            retry_after = 65

        return APIErrorClassification(
            is_quota_exhausted=is_quota_exhausted,
            is_rate_limit=is_rate,
            is_temporary_server_error=is_temp,
            retry_after=retry_after,
            error_message=error_msg
        )
