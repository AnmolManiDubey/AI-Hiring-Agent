import os
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

class LinkedInSourcingAgent:
    def __init__(self):
        self.api_key = os.getenv('GOOGLE_API_KEY')
        self.search_engine_id = os.getenv('GOOGLE_SEARCH_ENGINE_ID')
        
        if not self.api_key or not self.search_engine_id:
            print("Warning: Google API credentials not found. Using static data.")
            self.use_static = True
        else:
            self.use_static = False
            self.service = build("customsearch", "v1", developerKey=self.api_key)

    def search_linkedin(self, job_description):
        if self.use_static:
            return self._static_data()
        
        try:
            query = self._construct_query(job_description)

            results = self.service.cse().list(
                q=query,
                cx=self.search_engine_id,
                num=10
            ).execute()

            candidates = []
            for item in results.get('items', []):
                linkedin_url = item['link']
                headline = item.get('snippet', '').lower()

                # Filter only ML/AI profiles
                if not any(kw in headline for kw in ['ml', 'machine learning', 'ai', 'llm', 'research']):
                    continue

                name = self._extract_name_from_url(linkedin_url)
                candidates.append({
                    "name": name,
                    "linkedin_url": linkedin_url,
                    "headline": item.get('snippet', 'No headline available'),
                    "title": item.get('title', 'No title available')
                })

            return candidates if candidates else self._static_data()
        
        except Exception as e:
            print(f"Error searching LinkedIn: {e}")
            return self._static_data()

    def _construct_query(self, job_description):
        terms = set()

        job_titles = ["ML Engineer", "LLM Researcher", "Software Engineer", "AI Scientist"]
        companies = ["Windsurf", "Codeium"]
        locations = ["Mountain View", "California", "Bay Area"]
        techs = ["Python", "LLM", "AI", "Transformer", "Deep Learning"]

        lower_desc = job_description.lower()

        terms.update([t for t in job_titles if t.lower() in lower_desc])
        terms.update([c for c in companies if c.lower() in lower_desc])
        terms.update([l for l in locations if l.lower() in lower_desc])
        terms.update([tech for tech in techs if tech.lower() in lower_desc])

        titles = [t for t in terms if "engineer" in t.lower() or "scientist" in t.lower()]
        techs_found = [t for t in terms if t in techs]
        locs = [t for t in terms if t in locations]
        companies_found = [t for t in terms if t in companies]

        query = f'site:linkedin.com/in/ ({" OR ".join(titles)}) AND ({" OR ".join(techs_found)})'
        if companies_found:
            query += f' AND ({" OR ".join(companies_found)})'
        if locs:
            query += f' AND ({" OR ".join(locs)})'

        return query

    def _extract_name_from_url(self, linkedin_url):
        try:
            parts = linkedin_url.split('/in/')
            if len(parts) > 1:
                name_part = parts[1].split('/')[0].split('?')[0]
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
