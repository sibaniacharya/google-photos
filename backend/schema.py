from pydantic import BaseModel, Field
from typing import List, Optional, Literal

# Raw input schema
class RawRecord(BaseModel):
    record_id: str
    source: str
    source_url: str
    author_id: str
    date: str
    rating: Optional[int] = None
    title: str
    text: str
    language: str
    metadata: dict = {}

# Extracted structures
class Evidence(BaseModel):
    evidence_quote: str = Field(description="Short quote supporting the finding. MUST be an exact match from the text.")
    source_url: str

class ConfidenceLevel(BaseModel):
    level: Literal["HIGH", "MEDIUM", "LOW"]
    reason: str

class MemorySearchGap(BaseModel):
    what_user_remembers: List[str] = Field(description="List of things the user remembered (e.g. event, place).")
    what_user_forgot: List[str] = Field(description="List of things the user forgot (e.g. exact date).")
    what_user_searches: List[str] = Field(description="The actual queries or search strategies attempted.")
    what_result_they_get: Literal["SUCCESS", "PARTIAL_SUCCESS", "FAILURE", "ABANDONED", "UNKNOWN"]
    where_the_gap_occurs_observed: str = Field(description="Observed reason for the gap (e.g. 'User searched for ticket but text wasn't detected').")
    where_the_gap_occurs_hypothesis: str = Field(description="Hypothesis for why the system failed to bridge the gap.")

class ExtractedInsight(BaseModel):
    record_id: str
    source: str
    source_url: str
    original_text: str
    is_retrieval_relevant: bool
    relevance_confidence: ConfidenceLevel
    relevance_reason: str
    
    # Only populate the rest if is_retrieval_relevant is true
    retrieval_intent: Optional[str] = None
    memory_trigger: Optional[str] = None
    remembered_information: List[str] = Field(default_factory=list, description="person, relationship, place, time, event, etc.")
    forgotten_information: List[str] = Field(default_factory=list, description="exact date, exact location, person's name, etc.")
    search_formulation: List[str] = Field(default_factory=list, description="What the user actually searched for")
    search_classification: List[str] = Field(default_factory=list, description="keyword, natural language, person, place, etc.")
    
    retrieval_attempts: int = Field(0, description="Number of attempts or distinct strategies used")
    workaround_used: bool = Field(False, description="Did the user mention a workaround? (e.g. manual scrolling, asking a friend)")
    
    retrieval_outcome: Optional[Literal["SUCCESS", "PARTIAL_SUCCESS", "FAILURE", "ABANDONED", "UNKNOWN"]] = None
    
    primary_failure_reason: Optional[str] = Field(None, description="Observed reason for failure (e.g., 'Missing date', 'Missing exact keywords')")
    
    memory_search_gap: Optional[MemorySearchGap] = None
    
    retrieval_categories: List[str] = Field(default_factory=list, description="Event-Based, Context-Based, Place-Based, etc.")
    
    underlying_need_observed: Optional[str] = Field(None, description="Observed unmet need")
    underlying_need_hypothesis: Optional[str] = Field(None, description="Hypothesis for the underlying need")
    underlying_need_evidence: Optional[Evidence] = None

class BatchExtractionResponse(BaseModel):
    insights: List[ExtractedInsight]
