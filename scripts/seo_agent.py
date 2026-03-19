import os
import json
from pydantic_ai import Agent, RunContext
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class SEORecommendations(BaseModel):
    primary_keyword: str
    secondary_keywords: list[str]
    meta_title: str
    meta_description: str
    internal_links: list[str]
    improvement_suggestions: str

# Define the SEO Specialist Agent
seo_agent = Agent(
    'google-gla:gemini-1.5-flash',
    result_type=SEORecommendations,
    system_prompt=(
        "You are a Senior SEO Specialist for a high-end AI Automation Agency. "
        "Your goal is to ensure every blog post ranks #1 on Google for high-intent keywords. "
        "Focus on: Technical SEO, semantic keywords, and structural clarity. "
        "Use the provided tools to research internal links and competition."
    ),
)

@seo_agent.tool
def get_existing_content(ctx: RunContext[None]) -> str:
    """Returns a list of existing blog titles and URLs for internal linking."""
    blogs_dir = 'blogs'
    existing = []
    if os.path.exists(blogs_dir):
        for f in os.listdir(blogs_dir):
            if f.endswith('.md'):
                title = f.replace('.md', '').replace('-', ' ').title()
                existing.append(f"{title} (url: /post.html?id={f.replace('.md', '')})")
    return "\n".join(existing) if existing else "No existing content found."

@seo_agent.tool
def analyze_competitors(ctx: RunContext[None], keyword: str) -> str:
    """Simulates competitor research for a given keyword."""
    # In a real scenario, this would call a search API.
    return f"Top competitors for '{keyword}' are focusing on: ROI metrics, specific LangGraph tutorials, and enterprise security."

async def get_seo_strategy(topic: str):
    """Entry point to get SEO strategy for a topic."""
    result = await seo_agent.run(f"Create an SEO strategy for a blog post titled: {topic}")
    return result.data
