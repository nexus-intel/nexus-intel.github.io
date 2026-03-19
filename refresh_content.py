import os
import json
import re
from datetime import datetime

def extract_metadata(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
    subtitle_match = re.search(r'^> (.+)$', content, re.MULTILINE)
    
    # Extract first paragraph for meta description (strip markdown)
    paragraphs = re.findall(r'^(?!#|>|\-|\*|```|\|)(.{50,})', content, re.MULTILINE)
    description = paragraphs[0][:160] if paragraphs else "Read more on Nexus Intelligence."
    
    title = title_match.group(1) if title_match else os.path.basename(filepath).replace('.md','').replace('-',' ').title()
    subtitle = subtitle_match.group(1) if subtitle_match else "Click to read more..."
    
    # Get file modification time
    mtime = os.path.getmtime(filepath)
    date_str = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')
    
    return {
        "id": os.path.basename(filepath).replace('.md', ''),
        "title": title,
        "subtitle": subtitle,
        "description": description,
        "date": date_str
    }

def refresh():
    data = {
        "blogs": [],
        "cases": []
    }
    
    blog_dir = 'blogs'
    case_dir = 'cases'
    
    if os.path.exists(blog_dir):
        for f in sorted(os.listdir(blog_dir)):
            if f.endswith('.md'):
                data["blogs"].append(extract_metadata(os.path.join(blog_dir, f)))
                
    if os.path.exists(case_dir):
        for f in sorted(os.listdir(case_dir)):
            if f.endswith('.md'):
                data["cases"].append(extract_metadata(os.path.join(case_dir, f)))
                
    with open('content.json', 'w') as f:
        json.dump(data, f, indent=4)
    print(f"✅ Refreshed content.json ({len(data['blogs'])} blogs, {len(data['cases'])} cases)")
    
    # Auto-generate sitemap.xml
    generate_sitemap(data)

def generate_sitemap(data):
    base_url = "https://nexus-intel.github.io"
    today = datetime.now().strftime('%Y-%m-%d')
    
    urls = [
        {"loc": f"{base_url}/", "priority": "1.0", "changefreq": "weekly"},
        {"loc": f"{base_url}/blog.html", "priority": "0.9", "changefreq": "weekly"},
        {"loc": f"{base_url}/about.html", "priority": "0.7", "changefreq": "monthly"},
        {"loc": f"{base_url}/privacy.html", "priority": "0.3", "changefreq": "yearly"},
    ]
    
    for blog in data.get("blogs", []):
        urls.append({
            "loc": f"{base_url}/post.html?blog={blog['id']}",
            "priority": "0.8",
            "changefreq": "monthly"
        })
    
    for case in data.get("cases", []):
        urls.append({
            "loc": f"{base_url}/study.html?id={case['id']}",
            "priority": "0.8",
            "changefreq": "monthly"
        })
    
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url in urls:
        xml += f'    <url>\n'
        xml += f'        <loc>{url["loc"]}</loc>\n'
        xml += f'        <lastmod>{today}</lastmod>\n'
        if "changefreq" in url:
            xml += f'        <changefreq>{url["changefreq"]}</changefreq>\n'
        xml += f'        <priority>{url["priority"]}</priority>\n'
        xml += f'    </url>\n'
    xml += '</urlset>\n'
    
    with open('sitemap.xml', 'w') as f:
        f.write(xml)
    print(f"✅ Auto-generated sitemap.xml ({len(urls)} URLs)")

if __name__ == "__main__":
    refresh()
