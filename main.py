from agent import LinkedInSourcingAgent
from scoring import score_candidates
from outreach import generate_outreach

if __name__ == "__main__":
    job_description = input("Enter job description: ")
    agent = LinkedInSourcingAgent()

    print("\n[1] Searching for candidates...")
    candidates = agent.search_linkedin(job_description)
    for c in candidates:
        print(c)

    print("\n[2] Scoring candidates...")
    scored = score_candidates(candidates, job_description)
    for s in scored:
        print(s)

    print("\n[3] Generating outreach messages...")
    messages = generate_outreach(scored[:5], job_description)
    for m in messages:
        print(m)
