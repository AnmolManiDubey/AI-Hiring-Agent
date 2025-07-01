def generate_outreach(scored_candidates, job_description):
    messages = []
    for c in scored_candidates:
        message = (
            f"Hi {c['name']}, I came across your profile and was impressed by your background in software and ML. "
            f"We’re working on some exciting LLM research roles at Windsurf — would love to connect!"
        )
        messages.append({"candidate": c["name"], "message": message})
    return messages
