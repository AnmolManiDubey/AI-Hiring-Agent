ELITE_SCHOOLS = ["mit", "stanford", "harvard", "caltech", "princeton", "berkeley", "oxford", "cambridge", "yale"]
STRONG_SCHOOLS = ["cmu", "cornell", "ucla", "ucsd", "columbia", "duke", "uchicago", "umich", "uw"]
TOP_TECH_COMPANIES = ["google", "meta", "facebook", "amazon", "apple", "microsoft", "openai", "deepmind", "netflix", "linkedin"]
RELEVANT_INDUSTRY = ["fintech", "ai", "ml", "cloud", "saas", "startup"]

import re

def score_candidates(candidates, job_description):
    job_desc = job_description.lower()
    required_skills = re.findall(r"[A-Za-z0-9\+\#\.]+", job_desc)
    location_keywords = ["mountain view", "bay area", "california", "remote"]

    scored = []
    for c in candidates:
        headline = c.get("headline", "").lower()
        title = c.get("title", "").lower()
        breakdown = {}

        # Education (20%)
        if any(s in headline for s in ELITE_SCHOOLS):
            breakdown["education"] = 9
        elif any(s in headline for s in STRONG_SCHOOLS):
            breakdown["education"] = 7
        elif "university" in headline or "institute" in headline:
            breakdown["education"] = 5
        else:
            breakdown["education"] = 4

        # Career Trajectory (20%)
        if any(x in headline for x in ["lead", "head", "director", "manager", "founder", "chief", "cxo"]):
            breakdown["trajectory"] = 8
        elif any(x in headline for x in ["senior", "staff", "principal"]):
            breakdown["trajectory"] = 7
        elif any(x in headline for x in ["intern", "junior"]):
            breakdown["trajectory"] = 4
        else:
            breakdown["trajectory"] = 6

        # Company Relevance (15%)
        if any(cmp in headline for cmp in TOP_TECH_COMPANIES):
            breakdown["company"] = 9
        elif any(ind in headline for ind in RELEVANT_INDUSTRY):
            breakdown["company"] = 7
        elif "engineer" in headline or "developer" in headline:
            breakdown["company"] = 6
        else:
            breakdown["company"] = 5

        # Experience Match (25%)
        skill_matches = sum(1 for skill in required_skills if skill in headline or skill in title)
        if skill_matches >= 3:
            breakdown["experience"] = 9
        elif skill_matches == 2:
            breakdown["experience"] = 7
        elif skill_matches == 1:
            breakdown["experience"] = 6
        else:
            breakdown["experience"] = 5

        # Location Match (10%)
        if any(loc in headline for loc in location_keywords):
            breakdown["location"] = 10
        elif "remote" in headline:
            breakdown["location"] = 6
        else:
            breakdown["location"] = 7

        # Tenure (10%)
        if any(x in headline for x in ["years", "yr", "yrs", "since"]):
            breakdown["tenure"] = 9
        elif any(x in headline for x in ["months", "mo", "job hopping"]):
            breakdown["tenure"] = 5
        else:
            breakdown["tenure"] = 7

        # Weighted sum
        score = (
            breakdown["education"] * 0.2 +
            breakdown["trajectory"] * 0.2 +
            breakdown["company"] * 0.15 +
            breakdown["experience"] * 0.25 +
            breakdown["location"] * 0.1 +
            breakdown["tenure"] * 0.1
        )
        scored.append({
            "name": c["name"],
            "linkedin_url": c["linkedin_url"],
            "headline": c.get("headline", ""),
            "score": round(score, 2),
            "breakdown": breakdown
        })
    return scored
