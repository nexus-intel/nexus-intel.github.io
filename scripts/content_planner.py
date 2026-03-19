import json
import os
import sys
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class ContentPlanner:
    def __init__(self, leads_file='scripts/linkedin_leads.json'):
        self.leads_file = leads_file
        self.api_key = os.getenv("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-flash-latest')
        else:
            self.model = None

    def get_existing_articles(self):
        """Get titles of existing blogs and cases to avoid duplicates."""
        existing = []
        for folder in ['blogs', 'cases']:
            if os.path.exists(folder):
                for f in os.listdir(folder):
                    if f.endswith('.md'):
                        title = f.replace('.md', '').replace('-', ' ').title()
                        existing.append(title)
        return existing

    def plan_content(self):
        if not os.path.exists(self.leads_file):
            print("No leads file found. Run linkedin_scraper.py first.")
            return

        with open(self.leads_file, 'r') as f:
            leads = json.load(f)

        existing_titles = self.get_existing_articles()
        print(f"Found {len(existing_titles)} existing articles. Ensuring no duplicates...")
        
        all_snippets = []
        for niche, posts in leads.items():
            for post in posts:
                all_snippets.append(f"[{niche}] {post.get('snippet', '')}")

        top_snippets = all_snippets[:20] if len(all_snippets) > 20 else all_snippets
        context = "\n".join(top_snippets)
        
        prompt = f"""
        Analyze these trending AI/ML topics from LinkedIn and suggest 3 high-impact blog post outlines for an AI Agency website. 
        Target a mix of technical developers and business-focused CTOs/Managers.
        
        IMPORTANT: Do NOT propose any topics that overlap with these already published articles:
        {', '.join(existing_titles)}
        
        Trends Content from LinkedIn:
        {context}
        
        For each blog post, provide:
        1. Catchy Title (One Technical, One Strategic/ROI focused)
        2. Target Audience (e.g., Lead Developers vs Business Owners)
        3. 3-4 Bullet points for the key value propositions
        4. Why this matters in 2026 (Strategic context)
        
        Return in Markdown format.
        """

        print("Calling Gemini API for content planning...")
        if self.model:
            response = self.model.generate_content(prompt)
            content = response.text
        else:
            print("GEMINI_API_KEY not found. Please set it in .env")
            return

        with open('scripts/blog_proposals.md', 'w') as f:
            f.write(content)
        
        print("\nSuccessfully generated blog proposals in scripts/blog_proposals.md")

    def create_blog_post(self, title):
        """Generate a full blog post for a given title using Gemini."""
        print(f"\nGenerating full blog post for: {title}...")
        
        prompt = f"""
        Write a professional, high-impact technical blog post with 700 words for an AI Agency website titled: "{title}".
        
        The audience is a mix of developers (who want code/architecture) and business leaders (who want ROI/Strategy).
        
        Structure:
        1. H1 Title
        2. Blockquote subtitle (ROI focused)
        3. Introduction (The problem in 2026)
        4. Technical Deep Dive (Modern architectures like LangGraph, Vision LLMs, Agentic Workflows)
        5. Strategic Value (How this saves money/time)
        6. Conclusion & CTA
        
        Use clean Markdown. Avoid fluff. Be authoritative.
        Include a sample Python code snippet if relevant to the technical deep dive.
        """

        if self.model:
            response = self.model.generate_content(prompt)
            content = response.text
        else:
            print("GEMINI_API_KEY not found. Please set it in .env")
            return

        slug = title.lower().replace(' ', '-').replace(':', '').replace('?', '').replace('&', 'and')
        filepath = f"blogs/{slug}.md"
        
        with open(filepath, 'w') as f:
            f.write(content)
        
        print(f"Successfully created: {filepath}")
        return filepath

if __name__ == "__main__":
    planner = ContentPlanner()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--create":
        target_title = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "Agentic AI in 2026"
        planner.create_blog_post(target_title)
    else:
        planner.plan_content()
