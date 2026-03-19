import google.generativeai as genai
import os
import json
import sys
import asyncio
from dotenv import load_dotenv
from scripts.seo_agent import get_seo_strategy, discover_next_topic

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

    async def run_autonomous(self):
        """Phase 1: Discovery. Phase 2: SEO Strategy. Phase 3: Writing."""
        print("🧠 SEO Agent is searching for the perfect topic...")
        discovery = await discover_next_topic()
        
        print(f"\n🎯 Topic Found: {discovery.title}")
        print(f"💡 Justification: {discovery.justification}")
        print(f"👥 Target: {discovery.target_audience}")
        
        await self.create_blog_post(discovery.title)

    async def create_blog_post(self, title):
        """Generate a full blog post and SEO strategy."""
        print(f"\n🚀 Phase 2: SEO Optimization for '{title}'...")
        seo_strategy = await get_seo_strategy(title)
        
        print(f"✅ Strategy: {seo_strategy.primary_keyword}")
        
        print(f"\n✍️ Phase 3: Writing 700-word authoritative post...")
        
        prompt = f"""
        Write a professional 700-word blog post titled: "{title}".
        Target: Developers & Business Leaders.
        
        SEO Meta:
        - Primary Keyword: {seo_strategy.primary_keyword}
        - Description: {seo_strategy.meta_description}
        
        Structure: H1, Subtitle, Intro, Technical Deep Dive, ROI Analysis, Conclusion.
        Include a sample code snippet.
        """

        if self.model:
            response = self.model.generate_content(prompt)
            content = response.text
            
            slug = title.lower().replace(' ', '-').replace(':', '').replace('?', '').replace('&', 'and')
            filepath = f"blogs/{slug}.md"
            with open(filepath, 'w') as f:
                f.write(content)
            print(f"✨ Published: {filepath}")
        else:
            print("Gemini API key missing.")

if __name__ == "__main__":
    planner = ContentPlanner()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--auto":
        asyncio.run(planner.run_autonomous())
    elif len(sys.argv) > 1 and sys.argv[1] == "--create":
        target_title = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "Agentic AI"
        asyncio.run(planner.create_blog_post(target_title))
    else:
        print("Usage: --auto (Let AI decide) or --create 'Title' (You decide)")
