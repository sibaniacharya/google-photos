from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Union

class MemoryCues(BaseModel):
    retrieval_intent: str = Field(default="Find photo", description="The user's overall goal or intent.")
    people: List[str] = Field(default_factory=list, description="Names or descriptions of people mentioned. Leave empty if none.")
    event: str = Field(default="", description="The event or activity, e.g., 'seafood dinner'. Leave empty if none.")
    place: str = Field(default="", description="The location or setting, e.g., 'Amalfi Coast', 'indoors'. Leave empty if none.")
    approximate_time: str = Field(default="", description="Time of day, season, or year, e.g., 'summer', 'sunset'. Leave empty if none.")
    visual_details: List[str] = Field(default_factory=list, description="Visual descriptions, e.g., 'golden hour lighting', 'ocean view'. Leave empty if none.")
    objects: List[str] = Field(default_factory=list, description="Specific objects mentioned, e.g., 'yellow car', 'wine glasses'. Leave empty if none.")
    context: str = Field(default="", description="Broader context, e.g., 'summer trip'. Leave empty if none.")
    unknown_information: List[str] = Field(default_factory=list, description="Things the user explicitly says they don't know, or implicitly missing key cues (like missing time or place if it would help).")
    confidence: float = Field(default=0.5, description="Confidence score between 0.0 and 1.0 of how well the memory is understood.")

    @field_validator('people', 'visual_details', 'objects', 'unknown_information', mode='before')
    def ensure_list(cls, v):
        if isinstance(v, str):
            return [v] if v.strip() else []
        if v is None:
            return []
        return v

class SearchCandidate(BaseModel):
    photo_id: str
    image: str
    match_level: str
    matched_cues: List[str]
    uncertain_cues: List[str]
    reason: str

class SearchResponse(BaseModel):
    cues: MemoryCues
    candidates: List[SearchCandidate]

class RefineRequest(BaseModel):
    previous_cues: MemoryCues
    additional_memory: str
    rejected_candidate: Optional[str] = None

class RefineResponse(BaseModel):
    cues: MemoryCues
    candidates: List[SearchCandidate]
    refinement_question: Optional[str] = None
