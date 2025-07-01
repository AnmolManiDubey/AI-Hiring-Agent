from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Dict, Any
import sys
import os

# Add parent directory to path to import our agent
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent import LinkedInSourcingAgent
from scoring import score_candidates
from outreach import generate_outreach

app = FastAPI(title="LinkedIn Sourcing Agent API", version="1.0.0")

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

# Initialize the agent
agent = LinkedInSourcingAgent()

class JobDescription(BaseModel):
    description: str

class CandidateResponse(BaseModel):
    name: str
    linkedin_url: str
    headline: str
    title: str = ""

class ScoredCandidate(BaseModel):
    name: str
    linkedin_url: str
    headline: str
    score: float
    breakdown: Dict[str, int]

class OutreachMessage(BaseModel):
    candidate: str
    message: str

@app.get("/")
async def root():
    return {"message": "LinkedIn Sourcing Agent API"}

@app.get("/frontend")
async def serve_frontend():
    """Serve the frontend HTML file"""
    return FileResponse("frontend/index.html")

@app.post("/search", response_model=List[CandidateResponse])
async def search_candidates(job: JobDescription):
    """Search for LinkedIn candidates based on job description"""
    try:
        candidates = agent.search_linkedin(job.description)
        return candidates
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.post("/score", response_model=List[ScoredCandidate])
async def score_candidates_endpoint(job: JobDescription, candidates: List[CandidateResponse]):
    """Score candidates based on job description"""
    try:
        # Convert Pydantic models to dicts
        candidates_dict = [c.dict() for c in candidates]
        scored = score_candidates(candidates_dict, job.description)
        return scored
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scoring failed: {str(e)}")

@app.post("/outreach", response_model=List[OutreachMessage])
async def generate_outreach_endpoint(job: JobDescription, scored_candidates: List[ScoredCandidate]):
    """Generate outreach messages for top candidates"""
    try:
        # Convert Pydantic models to dicts
        candidates_dict = [c.dict() for c in scored_candidates]
        messages = generate_outreach(candidates_dict, job.description)
        return messages
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Outreach generation failed: {str(e)}")

@app.post("/full-pipeline")
async def full_pipeline(job: JobDescription):
    """Run the complete pipeline: search -> score -> outreach"""
    try:
        # Step 1: Search
        candidates = agent.search_linkedin(job.description)
        
        # Step 2: Score
        scored = score_candidates(candidates, job.description)
        
        # Step 3: Generate outreach for top 5
        top_candidates = sorted(scored, key=lambda x: x['score'], reverse=True)[:5]
        messages = generate_outreach(top_candidates, job.description)
        
        return {
            "candidates": candidates,
            "scored_candidates": scored,
            "outreach_messages": messages
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 