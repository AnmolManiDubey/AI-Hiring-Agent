import os
from groq import Groq
from dotenv import load_dotenv
import json

load_dotenv()

class EnhancedOutreach:
    def __init__(self):
        self.groq_api_key = os.getenv('GROQ_API_KEY')
        if self.groq_api_key:
            self.groq_client = Groq(api_key=self.groq_api_key)
            self.use_groq = True
        else:
            print("Warning: Groq API key not found. Using basic outreach.")
            self.use_groq = False

    def generate_personalized_message(self, candidate, job_description):
        """Use Groq/Llama to generate personalized outreach messages"""
        if not self.use_groq:
            return self._generate_basic_message(candidate, job_description)
        
        # Extract candidate details for personalization
        candidate_name = candidate.get("name", "").split()[0] if candidate.get("name") else "there"
        headline = candidate.get("headline", "")
        companies = candidate.get("companies", [])
        skills = candidate.get("skills", [])
        experience_years = candidate.get("experience_years", 0)
        role_level = candidate.get("role_level", "")
        industry = candidate.get("industry", "")
        
        prompt = f"""
        Generate a personalized LinkedIn outreach message for this candidate.
        
        Job Description: {job_description}
        
        Candidate Details:
        - Name: {candidate.get("name", "")}
        - Headline: {headline}
        - Companies: {', '.join(companies) if companies else 'Not specified'}
        - Skills: {', '.join(skills) if skills else 'Not specified'}
        - Experience: {experience_years} years
        - Role Level: {role_level}
        - Industry: {industry}
        
        Requirements:
        1. Start with a personalized greeting using their first name
        2. Reference something specific from their background (company, skills, experience)
        3. Connect it to the job opportunity
        4. Keep it professional but friendly
        5. Include a clear call-to-action
        6. Keep it under 150 words
        7. Make it sound natural and not overly salesy
        
        Return only the message text, no additional formatting.
        """
        
        try:
            response = self.groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=200
            )
            
            message = response.choices[0].message.content.strip()
            
            # Clean up the message
            if message.startswith('"') and message.endswith('"'):
                message = message[1:-1]
            
            return message if message else self._generate_basic_message(candidate, job_description)
                
        except Exception as e:
            print(f"Error generating message with Groq: {e}")
            return self._generate_basic_message(candidate, job_description)

    def _generate_basic_message(self, candidate, job_description):
        """Basic message generation (fallback)"""
        name = candidate.get("name", "").split()[0] if candidate.get("name") else "there"
        headline = candidate.get("headline", "")
        
        # Extract company from headline
        company = ""
        if " at " in headline:
            company = headline.split(" at ")[-1].split()[0]
        
        message = f"Hi {name}, I noticed your background as {headline}"
        if company:
            message += f" at {company}"
        message += ". I'd love to connect regarding a new opportunity that seems like a great fit for your experience. Would you be interested in a brief conversation?"
        
        return message

def generate_outreach_enhanced(scored_candidates, job_description):
    """Enhanced outreach generation using Groq API"""
    outreach_generator = EnhancedOutreach()
    messages = []
    
    for candidate in scored_candidates:
        message = outreach_generator.generate_personalized_message(candidate, job_description)
        
        messages.append({
            "candidate": candidate["name"],
            "message": message,
            "score": candidate.get("score", 0),
            "linkedin_url": candidate.get("linkedin_url", "")
        })
    
    return messages 
