from pydantic import BaseModel, Field
from typing import List, Optional

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
