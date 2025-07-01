import os
import requests
from googleapiclient.discovery import build
from dotenv import load_dotenv
from groq import Groq
import json
import time

load_dotenv()

class EnhancedLinkedInSourcingAgent:
    def __init__(self):
        self.api_key = os.getenv('GOOGLE_API_KEY')
        self.search_engine_id = os.getenv('GOOGLE_SEARCH_ENGINE_ID')
        self.groq_api_key = os.getenv('GROQ_API_KEY')
        
        if not self.api_key or not self.search_engine_id:
            print("Warning: Google API credentials not found. Using static data.")
            self.use_static = True
        else:
            self.use_static = False
            self.service = build("customsearch", "v1", developerKey=self.api_key)
        
        # Initialize Groq client
        if self.groq_api_key:
            self.groq_client = Groq(api_key=self.groq_api_key)
            self.use_groq = True
        else:
            print("Warning: Groq API key not found. Using basic functionality.")
            self.use_groq = False

    def extract_search_terms_with_ai(self, job_description):
        """Use Groq/Llama to intelligently extract search terms from job description"""
        if not self.use_groq:
            return self._extract_search_terms_basic(job_description)
        
        prompt = f"""
        Extract search terms from this job description for finding LinkedIn profiles.
        Focus on: job titles, required skills, technologies, location, company names.
        
        Job Description: {job_description}
        
        Return ONLY a JSON object like this:
        {{"job_titles": ["Software Engineer"], "skills": ["Python"], "location": ["Mountain View"], "companies": ["Windsurf"]}}
        """
        
        try:
            response = self.groq_client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=200
            )
            
            result = response.choices[0].message.content
            if result:
                result = result.strip()
                # Extract JSON from response
                json_start = result.find('{')
                json_end = result.rfind('}') + 1
                if json_start != -1 and json_end != 0:
                    try:
                        extracted_data = json.loads(result[json_start:json_end])
                        
                        # Build search query
                        terms = []
                        terms.extend(extracted_data.get('job_titles', []))
                        terms.extend(extracted_data.get('skills', []))
                        terms.extend(extracted_data.get('location', []))
                        terms.extend(extracted_data.get('companies', []))
                        
                        return " ".join(terms[:5])  # Limit to 5 most relevant terms
                    except json.JSONDecodeError:
                        return self._extract_search_terms_basic(job_description)
                else:
                    return self._extract_search_terms_basic(job_description)
            else:
                return self._extract_search_terms_basic(job_description)
                
        except Exception as e:
            print(f"Error with Groq API: {e}")
            return self._extract_search_terms_basic(job_description)

    def _extract_search_terms_basic(self, job_description):
        """Basic search term extraction (fallback)"""
        terms = set()
        
        job_titles = ["ML Engineer", "LLM Researcher", "Software Engineer", "AI Scientist", "Backend Engineer"]
        companies = ["Windsurf", "Codeium"]
        locations = ["Mountain View", "California", "Bay Area"]
        techs = ["Python", "LLM", "AI", "Transformer", "Deep Learning"]
        
        lower_desc = job_description.lower()
        
        terms.update([t for t in job_titles if t.lower() in lower_desc])
        terms.update([c for c in companies if c.lower() in lower_desc])
        terms.update([l for l in locations if l.lower() in lower_desc])
        terms.update([tech for tech in techs if tech.lower() in lower_desc])
        
        return " ".join(list(terms)[:5])

    def analyze_candidate_with_ai(self, candidate, job_description):
        """Use Groq/Llama to analyze candidate profile - OPTIMIZED VERSION"""
        if not self.use_groq:
            return self._analyze_candidate_basic(candidate)
        
        # Simplified prompt for faster processing
        prompt = f"""
        Analyze this LinkedIn profile for job matching.
        
        Candidate: {candidate['name']}
        Headline: {candidate['headline']}
        Job: {job_description[:200]}...
        
        Return ONLY a JSON object:
        {{"education": ["schools"], "companies": ["companies"], "skills": ["skills"], "experience_years": 0, "location": "location", "role_level": "level", "industry": "industry"}}
        """
        
        try:
            response = self.groq_client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=150
            )
            
            result = response.choices[0].message.content
            if result:
                result = result.strip()
                json_start = result.find('{')
                json_end = result.rfind('}') + 1
                if json_start != -1 and json_end != 0:
                    try:
                        return json.loads(result[json_start:json_end])
                    except json.JSONDecodeError:
                        return self._analyze_candidate_basic(candidate)
                else:
                    return self._analyze_candidate_basic(candidate)
            else:
                return self._analyze_candidate_basic(candidate)
                
        except Exception as e:
            print(f"Error analyzing candidate with Groq: {e}")
            return self._analyze_candidate_basic(candidate)

    def _analyze_candidate_basic(self, candidate):
        """Basic candidate analysis (fallback)"""
        headline = candidate.get('headline', '').lower()
        
        # Extract basic info from headline
        companies = []
        if " at " in headline:
            company_part = headline.split(" at ")[-1].split()[0]
            companies.append(company_part)
        
        skills = []
        if any(skill in headline for skill in ["python", "java", "javascript", "react", "node", "ml", "ai"]):
            skills = ["Technical Skills"]
        
        return {
            "education": [],
            "companies": companies,
            "skills": skills,
            "experience_years": 0,
            "location": "",
            "role_level": "mid",
            "industry": ""
        }

    def search_linkedin(self, job_description, use_ai_analysis=True, num_results=10):
        """Search for LinkedIn profiles with optional AI analysis and custom result count (supports pagination)"""
        if self.use_static:
            return self._static_data()
        
        try:
            search_terms = self.extract_search_terms_with_ai(job_description)
            query = f"site:linkedin.com/in/ {search_terms}"
            candidates = []
            start = 1
            per_page = 10
            while len(candidates) < num_results and start <= 30:
                results = self.service.cse().list(
                    q=query,
                    cx=self.search_engine_id,
                    num=min(per_page, num_results - len(candidates)),
                    start=start
                ).execute()
                items = results.get('items', [])
                for item in items:
                    linkedin_url = item['link']
                    headline = item.get('snippet', '').lower()
                    if not any(kw in headline for kw in ['ml', 'machine learning', 'ai', 'llm', 'research', 'engineer', 'developer']):
                        continue
                    name = self._extract_name_from_url(linkedin_url)
                    candidate_data = {
                        "name": name,
                        "linkedin_url": linkedin_url,
                        "headline": item.get('snippet', 'No headline available'),
                        "title": item.get('title', 'No title available')
                    }
                    if use_ai_analysis and len(candidates) < 3:
                        analysis = self.analyze_candidate_with_ai(candidate_data, job_description)
                        candidate_data.update(analysis)
                    else:
                        candidate_data.update(self._analyze_candidate_basic(candidate_data))
                    candidates.append(candidate_data)
                    time.sleep(0.05)
                    if len(candidates) >= num_results:
                        break
                if len(items) < per_page:
                    break  # No more results
                start += per_page
            return candidates if candidates else self._static_data()
        except Exception as e:
            print(f"Error searching LinkedIn: {e}")
            return self._static_data()

    def _extract_name_from_url(self, linkedin_url):
        """Extract name from LinkedIn URL"""
        try:
            parts = linkedin_url.split('/in/')
            if len(parts) > 1:
                name_part = parts[1].split('/')[0].split('?')[0]
                # Convert dashes and underscores to spaces, then title case
                name = name_part.replace('-', ' ').replace('_', ' ').title()
                return name
            return "Unknown"
        except:
            return "Unknown"

    def _static_data(self):
        return [
            {"name": "John Doe", "linkedin_url": "https://linkedin.com/in/johndoe", "headline": "Senior Backend Engineer at Fintech Co"},
            {"name": "Jane Smith", "linkedin_url": "https://linkedin.com/in/janesmith", "headline": "Software Engineer at BigTech"},
        ] 