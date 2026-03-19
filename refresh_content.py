import os
import re
import json
from datetime import datetime

# Definitive marker-based injection
def inject_content(filename, content_dict):
    if not os.path.exists(filename):
        return
    
    with open(filename, 'r') as f:
        html = f.read()

    # 1. Header/Footer (Simplified)
    try:
        with open('header.html', 'r') as f: header = f.read()
        with open('footer.html', 'r') as f: footer = f.read()
        html = re.sub(r'<header id="header-container">.*?</header>', f'<header id="header-container">{header}</header>', html, flags=re.DOTALL)
        html = re.sub(r'<footer id="footer-container">.*?</footer>', f'<footer id="footer-container">{footer}</footer>', html, flags=re.DOTALL)
    except: pass

    # 2. Blogs
    if 'blogs' in content_dict:
        blog_html = ""
        # index.html gets 3, blog.html gets all
        limit = 3 if filename == 'index.html' else 999
        for i, b in enumerate(content_dict['blogs'][:limit]):
            img_url = b.get('image') or ""
            card = f"""
            <div class="blog-card animate-in" style="animation-delay: {i * 0.1}s">
                <div class="blog-img" style="background: {f"url('{img_url}') center/cover" if img_url else f"linear-gradient(135deg, hsl({265 + i * 15}, 70%, 50%), hsl({225 + i * 15}, 70%, 40%))"};">
                    {"" if img_url else '<div class="img-overlay"></div>'}
                </div>
                <div class="blog-content">
                    <span class="blog-tag">Insight</span>
                    <h3>{b['title']}</h3>
                    <p>{b['subtitle'][:100]}...</p>
                    <a href="blog/{b['id']}/" class="read-more">Read Insight <i class="fas fa-arrow-right"></i></a>
                </div>
            </div>"""
            blog_html += card
        
        # DEFINITIVE REPLACEMENT: Replaces everything between markers
        html = re.sub(r'<!-- BLOG_START -->.*?<!-- BLOG_END -->', f'<!-- BLOG_START -->{blog_html}<!-- BLOG_END -->', html, flags=re.DOTALL)

    # 3. Cases (only for index.html)
    if 'cases' in content_dict and filename == 'index.html':
        case_html = ""
        for i, c in enumerate(content_dict['cases']):
            case_html += f"""
            <div class="case-card">
                <div class="case-header">
                    <span class="case-badge">Impact Analysis</span>
                    <h3>{c['title']}</h3>
                </div>
                <p>{c['subtitle']}</p>
                <a href="case/{c['id']}/" class="read-more">View Full Breakdown <i class="fas fa-arrow-right"></i></a>
            </div>"""
        html = re.sub(r'<!-- CASES_START -->.*?<!-- CASES_END -->', f'<!-- CASES_START -->{case_html}<!-- CASES_END -->', html, flags=re.DOTALL)

    with open(filename, 'w') as f:
        f.write(html)
    print(f"✅ Polished {filename}")

# Load data and run
if __name__ == "__main__":
    if os.path.exists('content.json'):
        with open('content.json', 'r') as f:
            data = json.load(f)
        inject_content('index.html', data)
        inject_content('blog.html', data)
