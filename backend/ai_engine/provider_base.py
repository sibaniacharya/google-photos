from typing import List, Dict, Any, Literal

class APIErrorClassification:
    def __init__(self, 
                 error_category: Literal["AUTHENTICATION_ERROR", "BILLING_OR_QUOTA_ERROR", "RATE_LIMIT_ERROR", "SERVER_ERROR", "MODEL_ERROR", "OTHER_ERROR"] = "OTHER_ERROR",
                 error_code: str = "",
                 is_quota_exhausted: bool = False, 
                 is_rate_limit: bool = False, 
                 is_temporary_server_error: bool = False, 
                 retry_after: int = 10, 
                 error_message: str = ""):
        self.error_category = error_category
        self.error_code = error_code
        self.is_quota_exhausted = is_quota_exhausted
        self.is_rate_limit = is_rate_limit
        self.is_temporary_server_error = is_temporary_server_error
        self.retry_after = retry_after
        self.error_message = error_message

    @property
    def should_stop_immediately(self) -> bool:
        return self.error_category in ["AUTHENTICATION_ERROR", "BILLING_OR_QUOTA_ERROR", "MODEL_ERROR"]

class LLMProvider:
    def __init__(self, model_name: str):
        self.model_name = model_name

    def generate_batch(self, prompt: str, schema: Any, system_instruction: str) -> List[Dict[str, Any]]:
        """
        Generates a batch of structured extraction results based on the provided schema.
        Should return a list of dictionaries matching the schema.
        """
        raise NotImplementedError("generate_batch must be implemented by the provider.")

    def is_available(self) -> bool:
        """
        Checks if the provider is correctly configured and the API key is present.
        """
        raise NotImplementedError("is_available must be implemented by the provider.")

    def classify_error(self, error: Exception) -> APIErrorClassification:
        """
        Classifies an API error (quota, rate limit, temp error) and extracts retry details.
        """
        raise NotImplementedError("classify_error must be implemented by the provider.")
