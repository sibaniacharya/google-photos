from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import json
import os
import math
import re
from typing import List, Dict, Any

from ai_engine.mvp_schemas import MemoryCues, SearchCandidate, SearchResponse, RefineRequest, RefineResponse
from ai_engine.mvp_prompts import MVP_EXTRACTION_PROMPT
from ai_engine.config import CONFIG
from ai_engine.gemini_provider import GeminiProvider
from ai_engine.openai_provider import OpenAIProvider
from ai_engine.groq_provider import GroqProvider

router = APIRouter()

def get_provider():
    provider_name = CONFIG.get("AI_PROVIDER", "groq")
    model_name = CONFIG.get("AI_MODEL", "openai/gpt-oss-120b")
    
    if provider_name.lower() == "gemini":
        return GeminiProvider(model_name, CONFIG.get("GEMINI_API_KEY", ""))
    elif provider_name.lower() == "openai":
        return OpenAIProvider(model_name, CONFIG.get("OPENAI_API_KEY", ""))
    elif provider_name.lower() == "groq":
        return GroqProvider(model_name, CONFIG.get("GROQ_API_KEY", ""))
    else:
        raise ValueError(f"Unsupported provider: {provider_name}")

class SearchRequest(BaseModel):
    memory: str

def load_demo_library():
    path = os.path.join(os.path.dirname(__file__), "demo_library.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return []

def rank_candidates(cues: MemoryCues, library: List[Dict[str, Any]], rejected_candidate: str = None) -> List[SearchCandidate]:
    candidates = []
    
    # Pre-filter UNKNOWNs
    people = [p for p in cues.people if p.upper() != "UNKNOWN"]
    place = cues.place if cues.place.upper() != "UNKNOWN" else ""
    event = cues.event if cues.event.upper() != "UNKNOWN" else ""
    time = cues.approximate_time if cues.approximate_time.upper() != "UNKNOWN" else ""
    visual = [v for v in cues.visual_details if v.upper() != "UNKNOWN"]
    objects = [o for o in cues.objects if o.upper() != "UNKNOWN"]

    for photo in library:
        if rejected_candidate and photo["photo_id"] == rejected_candidate:
            continue
            
        score = 0
        max_possible = 0
        matched = []
        uncertain = []
        
        # very simple keyword matching for MVP, but with word boundaries
        text_fields = f"{photo.get('location','')} {photo.get('event','')} {photo.get('approximate_time','')} {photo.get('visual_description','')} {photo.get('context','')} {' '.join(photo.get('people',[]))} {' '.join(photo.get('objects',[]))}".lower()
        
        def is_match(cue: str, text: str) -> bool:
            pattern = r'\b' + re.escape(cue.lower()) + r'\b'
            return bool(re.search(pattern, text))
        
        if people:
            max_possible += 25
            for p in people:
                if is_match(p, text_fields):
                    score += (25 / len(people))
                    matched.append(p)
                else:
                    uncertain.append(p)
                    
        if place:
            max_possible += 20
            if is_match(place, text_fields):
                score += 20
                matched.append(place)
            else:
                uncertain.append(place)
                
        if event:
            max_possible += 15
            if is_match(event, text_fields):
                score += 15
                matched.append(event)
            else:
                uncertain.append(event)
                
        if time:
            max_possible += 15
            if is_match(time, text_fields):
                score += 15
                matched.append(time)
            else:
                uncertain.append(time)

        if visual:
            max_possible += 15
            for v in visual:
                if is_match(v, text_fields):
                    score += (15 / len(visual))
                    matched.append(v)
                else:
                    uncertain.append(v)
                    
        if objects:
            max_possible += 10
            for obj in objects:
                if is_match(obj, text_fields):
                    score += (10 / len(objects))
                    matched.append(obj)
                else:
                    uncertain.append(obj)

        if max_possible == 0:
            match_pct = 50 # Base if no specific cues
        else:
            match_pct = int((score / max_possible) * 100)

        if match_pct >= 75:
            match_level = "Strong match"
        elif match_pct >= 50:
            match_level = "Possible match"
        else:
            match_level = "Weak match"
            
        # remove duplicates preserving order
        matched = list(dict.fromkeys(matched))
        uncertain = list(dict.fromkeys(uncertain))
        
        # create explanation
        if matched and uncertain:
            reason = f"Matches: {', '.join(matched)}. Uncertain: {', '.join(uncertain)}."
        elif matched:
            reason = f"Matches: {', '.join(matched)}."
        elif uncertain:
            reason = f"Could not verify: {', '.join(uncertain)}."
        else:
            reason = "Semantic similarity match based on overall context."

        candidates.append({
            "photo_id": photo["photo_id"],
            "image": photo["image"],
            "match_level": match_level,
            "matched_cues": matched,
            "uncertain_cues": uncertain,
            "reason": reason,
            "score": score
        })
        
    # sort by score descending
    candidates.sort(key=lambda x: x["score"], reverse=True)
    
    # remove 'score' from output
    for c in candidates:
        del c["score"]
        
    return [SearchCandidate(**c) for c in candidates[:3]] # return top 3

def determine_refinement_question(cues: MemoryCues) -> str:
    if not cues.people:
        return "Was anyone else with you?"
    if not cues.approximate_time:
        return "Do you remember approximately when this was (e.g. summer, last year)?"
    if not cues.place:
        return "Do you remember anything about the location or where this was?"
    if not cues.event:
        return "Do you remember what happened before or after this photo?"
    return "Are there any other specific visual details you remember?"

@router.get("/api/retrieval/library")
def get_library():
    return {"library": load_demo_library()}

@router.post("/api/retrieval/search", response_model=SearchResponse)
def search_memory(req: SearchRequest):
    provider = get_provider()
    if not provider.is_available():
        raise HTTPException(status_code=500, detail="AI provider not available")
        
    prompt = f"Extract memory cues from the following user description:\n\n\"{req.memory}\""
    
    # generate structured output
    # Since we need to extract structured data for a single record, we can wrap it
    try:
        results = provider.generate_batch(prompt, MemoryCues, MVP_EXTRACTION_PROMPT)
        if not results:
            raise ValueError("No cues extracted")
        cues_dict = results[0]
        cues = MemoryCues(**cues_dict)
    except Exception as e:
        print(f"Extraction error: {e}")
        # fallback
        cues = MemoryCues(
            retrieval_intent="Find photo",
            people=[], event="", place="", approximate_time="",
            visual_details=[], objects=[], context="", unknown_information=[], confidence=0.5
        )
        
    library = load_demo_library()
    candidates = rank_candidates(cues, library)
    
    return SearchResponse(cues=cues, candidates=candidates)

@router.post("/api/retrieval/refine", response_model=RefineResponse)
def refine_memory(req: RefineRequest):
    provider = get_provider()
    
    if not req.additional_memory.strip():
        # If no new details, just reuse cues and get question
        cues = req.previous_cues
    else:
        prompt = f"Previous extracted memory cues:\n{req.previous_cues.model_dump_json(indent=2)}\n\nNew detail from user: \"{req.additional_memory}\"\n\nUpdate the memory cues with this new detail. Preserve all previous cues unless contradicted by the new detail. If the user says they don't know something, update that specific field to 'UNKNOWN'."
        try:
            results = provider.generate_batch(prompt, MemoryCues, MVP_EXTRACTION_PROMPT)
            cues_dict = results[0]
            cues = MemoryCues(**cues_dict)
        except Exception as e:
            print(f"Extraction error: {e}")
            cues = req.previous_cues
        
    library = load_demo_library()
    candidates = rank_candidates(cues, library, req.rejected_candidate)
    question = determine_refinement_question(cues)
    
    return RefineResponse(cues=cues, candidates=candidates, refinement_question=question)
