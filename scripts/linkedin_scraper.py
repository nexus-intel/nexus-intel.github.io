import random
import requests
from bs4 import BeautifulSoup
import json
import time
import os
import re
class LinkedInScraper:
    def __init__(self, niche_keywords=None):
        self.base_url = "https://www.google.com/search?q="
        self.niche_keywords = niche_keywords or [
            "Agentic AI architecture", "AI Strategy for Enterprise", "AI Automation ROI",
            "pdf data extraction python", "OCR Business Process Efficiency", "invoice processing automation", 
            "AI Compliance 2026", "Local LLM for Data Privacy", "Cost reduction with AI agent"
        ]
        # Dynamically found models will be added here
        self.latest_models = ["Llama 4", "GPT-5.4", "Claude 4.6", "Gemini 3.1", "Qwen 3.5", "DeepSeek-V3.2"]
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0"
        ]
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def get_latest_models(self):
        """Fetch latest LLM models via search to keep keywords fresh."""
        query = "latest LLM models released 2026 open source closed source"
        search_url = self.base_url + requests.utils.quote(query)
        print("Discovering latest SOTA models...")
        try:
            response = requests.get(search_url, headers={"User-Agent": random.choice(self.user_agents)})
            if response.status_code == 200:
                # Simple extraction of capitalized words near 'Llama', 'GPT', 'Claude' etc.
                # In a real scenario, this would be more complex, but we'll use a seed list + discovery
                found = re.findall(r'(Llama \d+|GPT-\d+\.\d+|Claude \d+\.\d+|Gemini \d+\.\d+|Qwen \d+\.\d+)', response.text)
                if found:
                    self.latest_models = list(set(self.latest_models + found))
                    print(f"Updated model list: {', '.join(self.latest_models)}")
        except Exception as e:
            print(f"Model discovery failed: {e}. Using fallback list.")

    def find_posts(self, keyword):
        """Find recent LinkedIn posts via Search Dorking."""
        query = f'site:linkedin.com/posts/ "{keyword}" "latest"'
        search_url = self.base_url + requests.utils.quote(query)
        
        print(f"Searching for: {keyword}...")
        try:
            response = requests.get(search_url, headers=self.headers)
            response.raise_for_status()
            return self.parse_results(response.text)
        except Exception as e:
            print(f"Search failed for {keyword}: {e}")
            return []

    def parse_results(self, html):
        """Parse search results to get link and snippet."""
        soup = BeautifulSoup(html, 'html.parser')
        results = []
        seen_urls = set() # Track URLs in this specific search
        
        # Google search results are typically in class divs
        for g in soup.find_all('div'):
            # This is a generic way to find links containing /posts/
            link_tag = g.find('a')
            if link_tag:
                link = link_tag.get('href', '')
                if "/posts/" in link and "linkedin.com" in link and link not in seen_urls:
                    seen_urls.add(link)
                    snippet = g.get_text()[:300] # Grab some text context
                    results.append({
                        "url": link,
                        "snippet": snippet.strip(),
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                    })
        return results

    def run(self):
        """Run discovery with dynamic keyword expansion."""
        self.get_latest_models()
        
        # Combine static keywords with latest models
        active_keywords = self.niche_keywords + [f"{m} use cases" for m in self.latest_models]
        active_keywords += [f"{m} benchmark" for m in self.latest_models]

        all_leads = {}
        for kw in active_keywords:
            self.headers["User-Agent"] = random.choice(self.user_agents)
            posts = self.find_posts(kw)
            all_leads[kw] = posts
            
            # Shorter run for testing or randomized delay
            delay = random.uniform(10, 25)
            print(f"Waiting {delay:.2f}s to avoid detection...")
            time.sleep(delay)
        
        # Save to JSON
        output_file = 'scripts/linkedin_leads.json'
        with open(output_file, 'w') as f:
            json.dump(all_leads, f, indent=4)
        
        print(f"\nDone! Saved potential leads to {output_file}")

if __name__ == "__main__":
    # Ensure BeautifulSoup is available: pip install beautifulsoup4
    scraper = LinkedInScraper()
    scraper.run()
