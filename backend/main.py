from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import os
import json

from ai_engine.config import CONFIG
from ai_engine.gemini_provider import GeminiProvider
from ai_engine.openai_provider import OpenAIProvider
from ai_engine.groq_provider import GroqProvider
from ai_engine.schemas import BatchExtractionResponse
from ai_engine.prompts import SYSTEM_INSTRUCTION
from ai_engine.validator import Validator

app = FastAPI(title="Google Photos AI Discovery Engine API")

# Setup CORS
FRONTEND_URL = os.environ.get("FRONTEND_URL", "http://localhost:5173")
origins = [
    url.strip() for url in FRONTEND_URL.split(",") if url.strip()
] + [
    "http://localhost:5173",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

class ExtractRequest(BaseModel):
    records: List[Dict[str, Any]]

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/api/ai/extract")
def extract_records(req: ExtractRequest):
    if not req.records:
        raise HTTPException(status_code=400, detail="No records provided")
    
    try:
        provider = get_provider()
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    if not provider.is_available():
        raise HTTPException(status_code=401, detail=f"Provider {CONFIG.get('AI_PROVIDER')} is not configured or missing API key")

    prompt = f"Extract fields for these records:\n\n{json.dumps(req.records, indent=2)}"
    
    try:
        results = provider.generate_batch(prompt, BatchExtractionResponse, SYSTEM_INSTRUCTION)
        
        chunk_map = {r.get('record_id'): r for r in req.records if 'record_id' in r}
        validator = Validator()
        extracted_list = []
        
        for ex_dict in results:
            rec_id = ex_dict.get('record_id')
            if rec_id in chunk_map:
                orig = chunk_map[rec_id]
                ex_dict = validator.fix_evidence_quote(ex_dict, orig)
                
                merged = {**orig, **ex_dict}
                merged['review_text'] = orig.get('review_text', '')
                merged['source_url'] = orig.get('source_url', '')
                
                extracted_list.append(merged)
        
        return {"extracted": extracted_list}
        
    except Exception as e:
        error_class = provider.classify_error(e)
        if error_class.is_rate_limit:
            raise HTTPException(status_code=429, detail=f"Rate limit exceeded: {error_class.error_message}")
        elif error_class.is_temporary_server_error:
            raise HTTPException(status_code=503, detail=f"AI Provider unavailable: {error_class.error_message}")
        else:
            raise HTTPException(status_code=500, detail=f"AI Engine error: {error_class.error_message}")

from mvp_router import router as mvp_router
app.include_router(mvp_router)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
