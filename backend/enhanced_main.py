from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Dict, Any
import sys
import os

# Add parent directory to path to import our enhanced agent
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from groq_agent import EnhancedLinkedInSourcingAgent
from enhanced_scoring import score_candidates_enhanced, score_candidates_fast
from enhanced_outreach import generate_outreach_enhanced

app = FastAPI(title="Enhanced LinkedIn Sourcing Agent API", version="2.0.0")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Initialize the enhanced agent
agent = EnhancedLinkedInSourcingAgent()

class JobDescription(BaseModel):
    description: str

class CandidateResponse(BaseModel):
    name: str
    linkedin_url: str
    headline: str
    title: str = ""
    education: List[str] = []
    companies: List[str] = []
    skills: List[str] = []
    experience_years: int = 0
    location: str = ""
    role_level: str = ""
    industry: str = ""

class ScoredCandidate(BaseModel):
    name: str
    linkedin_url: str
    headline: str
    score: float
    breakdown: Dict[str, int]
    reasoning: Dict[str, str] = {}
    education: List[str] = []
    companies: List[str] = []
    skills: List[str] = []
    experience_years: int = 0
    location: str = ""
    role_level: str = ""
    industry: str = ""

class OutreachMessage(BaseModel):
    candidate: str
    message: str
    score: float = 0
    linkedin_url: str = ""

@app.get("/")
async def root():
    return {"message": "Enhanced LinkedIn Sourcing Agent API with Groq/Llama"}

@app.get("/frontend")
async def serve_frontend():
    """Serve the frontend HTML file"""
    return FileResponse("frontend/index.html")

@app.post("/search", response_model=List[CandidateResponse])
async def search_candidates(request: Request):
    data = await request.json()
    job_description = data.get("description", "")
    profile_count = int(data.get("profile_count", 10))
    try:
        candidates = agent.search_linkedin(job_description, use_ai_analysis=True, num_results=profile_count)
        return candidates
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.post("/search-fast", response_model=List[CandidateResponse])
async def search_candidates_fast(request: Request):
    data = await request.json()
    job_description = data.get("description", "")
    profile_count = int(data.get("profile_count", 10))
    try:
        candidates = agent.search_linkedin(job_description, use_ai_analysis=False, num_results=profile_count)
        return candidates
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.post("/score", response_model=List[ScoredCandidate])
async def score_candidates_endpoint(job: JobDescription, candidates: List[CandidateResponse]):
    """Score candidates using enhanced AI-powered scoring"""
    try:
        # Convert Pydantic models to dicts
        candidates_dict = [c.dict() for c in candidates]
        scored = score_candidates_enhanced(candidates_dict, job.description, use_ai_for_top=True)
        return scored
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scoring failed: {str(e)}")

@app.post("/score-fast", response_model=List[ScoredCandidate])
async def score_candidates_fast_endpoint(job: JobDescription, candidates: List[CandidateResponse]):
    """Score candidates using fast scoring without AI"""
    try:
        # Convert Pydantic models to dicts
        candidates_dict = [c.dict() for c in candidates]
        scored = score_candidates_fast(candidates_dict, job.description)
        return scored
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scoring failed: {str(e)}")

@app.post("/outreach", response_model=List[OutreachMessage])
async def generate_outreach_endpoint(job: JobDescription, scored_candidates: List[ScoredCandidate]):
    """Generate personalized outreach messages using AI"""
    try:
        # Convert Pydantic models to dicts
        candidates_dict = [c.dict() for c in scored_candidates]
        messages = generate_outreach_enhanced(candidates_dict, job.description)
        return messages
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Outreach generation failed: {str(e)}")

@app.post("/full-pipeline")
async def full_pipeline(request: Request):
    data = await request.json()
    job_description = data.get("description", "")
    profile_count = int(data.get("profile_count", 10))
    try:
        candidates = agent.search_linkedin(job_description, use_ai_analysis=True, num_results=profile_count)
        scored = score_candidates_enhanced(candidates, job_description, use_ai_for_top=True)
        top_candidates = sorted(scored, key=lambda x: x['score'], reverse=True)[:5]
        messages = generate_outreach_enhanced(top_candidates, job_description)
        return {
            "candidates": candidates,
            "scored_candidates": scored,
            "outreach_messages": messages
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline failed: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "groq_available": agent.use_groq,
        "google_available": not agent.use_static
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 