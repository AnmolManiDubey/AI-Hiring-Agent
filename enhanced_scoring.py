import os
import re
import json
from typing import Dict, List, Any
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Elite and strong schools for education scoring
ELITE_SCHOOLS = {
    "mit", "stanford", "harvard", "caltech", "princeton", "berkeley", "oxford", "cambridge", "yale",
    "massachusetts institute of technology", "university of california berkeley", "uc berkeley"
}

STRONG_SCHOOLS = {
    "cmu", "cornell", "ucla", "ucsd", "columbia", "duke", "uchicago", "umich", "uw", "georgia tech",
    "carnegie mellon", "university of michigan", "university of washington", "georgia institute of technology"
}

# Top tech companies for company relevance
TOP_TECH_COMPANIES = {
    "google", "meta", "facebook", "amazon", "apple", "microsoft", "openai", "deepmind", "netflix", "linkedin",
    "alphabet", "tesla", "nvidia", "salesforce", "uber", "airbnb", "stripe", "palantir", "databricks", "snowflake"
}

# Relevant industries
RELEVANT_INDUSTRIES = {
    "fintech", "ai", "ml", "cloud", "saas", "startup", "machine learning", "artificial intelligence",
    "software", "technology", "tech", "data science", "analytics"
}

# Location keywords for better matching
LOCATION_KEYWORDS = {
    "mountain view": 10,
    "palo alto": 10,
    "san francisco": 10,
    "bay area": 8,
    "california": 8,
    "sf": 10,
    "silicon valley": 8,
    "seattle": 8,
    "new york": 8,
    "nyc": 8,
    "remote": 6,
    "wfh": 6,
    "work from home": 6
}

# Career progression indicators
SENIOR_ROLES = {"lead", "head", "director", "manager", "founder", "chief", "cxo", "vp", "vice president"}
MID_LEVEL_ROLES = {"senior", "staff", "principal", "senior engineer", "staff engineer"}
JUNIOR_ROLES = {"intern", "junior", "associate", "entry level"}

# Skills keywords for better matching
TECH_SKILLS = {
    "python", "java", "javascript", "typescript", "react", "node.js", "aws", "docker", "kubernetes",
    "machine learning", "deep learning", "tensorflow", "pytorch", "scikit-learn", "sql", "nosql",
    "mongodb", "postgresql", "redis", "kafka", "spark", "hadoop", "git", "ci/cd", "microservices",
    "api", "rest", "graphql", "cloud", "azure", "gcp", "devops", "agile", "scrum"
}

class OptimizedScoring:
    def __init__(self):
        self.groq_api_key = os.getenv('GROQ_API_KEY')
        self.use_ai = bool(self.groq_api_key)
        if self.use_ai:
            self.groq_client = Groq(api_key=self.groq_api_key)
        
        # Pre-compile regex patterns for better performance
        self.skill_pattern = re.compile(r'\b[A-Za-z0-9\+\#\.]+\b')
        self.year_pattern = re.compile(r'\b(?:20\d{2}|19\d{2})\b')
        self.duration_pattern = re.compile(r'\b(\d+)\s*(?:years?|yrs?|months?|mos?)\b')

    def get_education_score(self, candidate: Dict[str, Any]) -> float:
        """Score education based on school prestige and progression"""
        education_list = [e.lower() for e in candidate.get("education", [])]
        headline = candidate.get("headline", "").lower()
        title = candidate.get("title", "").lower()
        
        # Check AI-extracted education first
        for school in ELITE_SCHOOLS:
            if any(school in edu for edu in education_list):
                return 9.5  # Elite school with clear progression
        
        for school in STRONG_SCHOOLS:
            if any(school in edu for edu in education_list):
                return 8.0  # Strong school
        
        # Fallback: check headline/title for school mentions
        for school in ELITE_SCHOOLS:
            if school in headline or school in title:
                return 9.0
        
        for school in STRONG_SCHOOLS:
            if school in headline or school in title:
                return 7.5
        
        # Check for any university/institute mention
        if any(word in headline or word in title for word in ["university", "institute", "college"]):
            return 6.0
        
        return 4.0  # No education info found

    def get_trajectory_score(self, candidate: Dict[str, Any]) -> float:
        """Score career trajectory based on role progression"""
        headline = candidate.get("headline", "").lower()
        
        # Check for senior leadership roles
        if any(role in headline for role in SENIOR_ROLES):
            return 8.5  # Steady growth to leadership
        
        # Check for mid-level progression
        if any(role in headline for role in MID_LEVEL_ROLES):
            return 7.0  # Good progression
        
        # Check for junior roles
        if any(role in headline for role in JUNIOR_ROLES):
            return 4.0  # Limited progression
        
        # Default for mid-level roles
        return 6.0

    def get_company_score(self, candidate: Dict[str, Any]) -> float:
        """Score company relevance based on tech companies and industry"""
        headline = candidate.get("headline", "").lower()
        companies = [c.lower() for c in candidate.get("companies", [])]
        
        # Check for top tech companies
        for company in TOP_TECH_COMPANIES:
            if company in headline or any(company in c for c in companies):
                return 9.5  # Top tech company experience
        
        # Check for relevant industry experience
        for industry in RELEVANT_INDUSTRIES:
            if industry in headline:
                return 7.5  # Relevant industry
        
        # Check for any engineering/tech role
        if any(word in headline for word in ["engineer", "developer", "scientist", "architect"]):
            return 6.0  # Tech experience
        
        return 5.0  # No relevant experience

    def get_experience_score(self, candidate: Dict[str, Any], job_description: str) -> float:
        """Score experience match based on skills and job requirements"""
        headline = candidate.get("headline", "").lower()
        title = candidate.get("title", "").lower()
        skills = [s.lower() for s in candidate.get("skills", [])]
        
        # Extract skills from job description
        job_desc = job_description.lower()
        required_skills = set(self.skill_pattern.findall(job_desc))
        
        # Count skill matches
        skill_matches = 0
        for skill in required_skills:
            if (skill in headline or skill in title or 
                skill in skills or any(skill in s for s in skills)):
                skill_matches += 1
        
        # Score based on matches
        if skill_matches >= 4:
            return 9.5  # Perfect skill match
        elif skill_matches >= 3:
            return 8.5  # Strong overlap
        elif skill_matches >= 2:
            return 7.0  # Good overlap
        elif skill_matches >= 1:
            return 6.0  # Some relevant skills
        else:
            return 5.0  # No clear skill match

    def get_location_score(self, candidate: Dict[str, Any]) -> float:
        """Score location match based on proximity to job location"""
        headline = candidate.get("headline", "").lower()
        location = candidate.get("location", "").lower()
        
        # Check for exact location matches
        for loc, score in LOCATION_KEYWORDS.items():
            if loc in headline or loc in location:
                return score
        
        # Default score for other locations
        return 7.0

    def get_tenure_score(self, candidate: Dict[str, Any]) -> float:
        """Score tenure based on job duration patterns"""
        headline = candidate.get("headline", "").lower()
        
        # Look for specific duration patterns
        duration_match = self.duration_pattern.search(headline)
        if duration_match:
            duration = int(duration_match.group(1))
            if duration >= 2:
                return 9.0  # 2+ years average
            elif duration >= 1:
                return 7.0  # 1-2 years
        
        # Check for year patterns (since 2021, etc.)
        year_match = self.year_pattern.search(headline)
        if year_match:
            year = int(year_match.group())
            if year >= 2021:
                return 8.0  # Recent but stable
        
        # Check for job hopping indicators
        if any(word in headline for word in ["months", "mo", "job hopping", "frequent"]):
            return 4.0  # Job hopping
        
        return 7.0  # Default stable tenure

    def score_candidate_basic(self, candidate: Dict[str, Any], job_description: str) -> Dict[str, Any]:
        """Fast basic scoring without AI"""
        breakdown = {
            "education": self.get_education_score(candidate),
            "trajectory": self.get_trajectory_score(candidate),
            "company": self.get_company_score(candidate),
            "experience": self.get_experience_score(candidate, job_description),
            "location": self.get_location_score(candidate),
            "tenure": self.get_tenure_score(candidate)
        }
        
        # Calculate weighted total score
        total_score = (
            breakdown["education"] * 0.20 +
            breakdown["trajectory"] * 0.20 +
            breakdown["company"] * 0.15 +
            breakdown["experience"] * 0.25 +
            breakdown["location"] * 0.10 +
            breakdown["tenure"] * 0.10
        )
        
        return {
            "score": round(total_score, 1),
            "breakdown": {k: round(v, 1) for k, v in breakdown.items()},
            "reasoning": {}
        }

    def score_candidate_with_ai(self, candidate: Dict[str, Any], job_description: str) -> Dict[str, Any]:
        """Enhanced scoring with AI analysis for top candidates"""
        if not self.use_ai:
            return self.score_candidate_basic(candidate, job_description)
        
        # Prepare candidate data
        candidate_info = {
            "name": candidate.get("name", ""),
            "headline": candidate.get("headline", ""),
            "education": candidate.get("education", []),
            "companies": candidate.get("companies", []),
            "skills": candidate.get("skills", []),
            "experience_years": candidate.get("experience_years", 0),
            "location": candidate.get("location", ""),
            "role_level": candidate.get("role_level", ""),
            "industry": candidate.get("industry", "")
        }
        
        prompt = f"""
        Score this candidate for the given job using this exact rubric:

        **Education (20%)**: Elite schools (MIT, Stanford, etc.): 9-10, Strong schools: 7-8, Standard universities: 5-6
        **Career Trajectory (20%)**: Steady growth: 6-8, Limited progression: 3-5  
        **Company Relevance (15%)**: Top tech companies: 9-10, Relevant industry: 7-8, Any experience: 5-6
        **Experience Match (25%)**: Perfect skill match: 9-10, Strong overlap: 7-8, Some relevant skills: 5-6
        **Location Match (10%)**: Exact city: 10, Same metro: 8, Remote-friendly: 6
        **Tenure (10%)**: 2-3 years average: 9-10, 1-2 years: 6-8, Job hopping: 3-5

        Job Description: {job_description}
        Candidate: {json.dumps(candidate_info, indent=2)}

        Return ONLY a JSON object: {{"total_score": 8.5, "breakdown": {{"education": 9.0, "trajectory": 8.0, "company": 8.5, "experience": 9.0, "location": 10.0, "tenure": 7.0}}}}
        """
        
        try:
            response = self.groq_client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=300
            )
            
            result = response.choices[0].message.content
            if result:
                result = result.strip()
            else:
                return self.score_candidate_basic(candidate, job_description)
            json_start = result.find('{')
            json_end = result.rfind('}') + 1
            
            if json_start != -1 and json_end != 0:
                scoring_result = json.loads(result[json_start:json_end])
                return {
                    "score": round(scoring_result.get("total_score", 5.0), 1),
                    "breakdown": {k: round(v, 1) for k, v in scoring_result.get("breakdown", {}).items()},
                    "reasoning": {}
                }
        except Exception as e:
            print(f"AI scoring failed for {candidate.get('name', 'Unknown')}: {e}")
        
        # Fallback to basic scoring
        return self.score_candidate_basic(candidate, job_description)

def score_candidates_enhanced(candidates: List[Dict[str, Any]], job_description: str, use_ai_for_top: bool = True) -> List[Dict[str, Any]]:
    """
    Enhanced scoring function with performance optimization
    
    Args:
        candidates: List of candidate dictionaries
        job_description: Job description text
        use_ai_for_top: Whether to use AI for top 5 candidates only (for performance)
    """
    scorer = OptimizedScoring()
    scored_candidates = []
    
    # Score all candidates with basic method first
    for candidate in candidates:
        scoring_result = scorer.score_candidate_basic(candidate, job_description)
        
        scored_candidate = {
            "name": candidate["name"],
            "linkedin_url": candidate["linkedin_url"],
            "headline": candidate.get("headline", ""),
            "score": scoring_result["score"],
            "breakdown": scoring_result["breakdown"],
            "reasoning": scoring_result.get("reasoning", {})
        }
        scored_candidates.append(scored_candidate)
    
    # Sort by score to identify top candidates
    scored_candidates.sort(key=lambda x: x["score"], reverse=True)
    
    # Use AI for top candidates if requested and available
    if use_ai_for_top and scorer.use_ai:
        top_count = min(5, len(scored_candidates))
        for i in range(top_count):
            ai_result = scorer.score_candidate_with_ai(candidates[i], job_description)
            scored_candidates[i].update({
                "score": ai_result["score"],
                "breakdown": ai_result["breakdown"],
                "reasoning": ai_result.get("reasoning", {})
            })
    
    return scored_candidates

def score_candidates_fast(candidates: List[Dict[str, Any]], job_description: str) -> List[Dict[str, Any]]:
    """Fast scoring without AI for performance"""
    return score_candidates_enhanced(candidates, job_description, use_ai_for_top=False) 