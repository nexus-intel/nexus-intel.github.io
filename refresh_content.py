import os
import json
import re

def extract_metadata(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Simple regex for H1 and Blockquote (subtitle)
    title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
    subtitle_match = re.search(r'^> (.+)$', content, re.MULTILINE)
    
    title = title_match.group(1) if title_match else os.path.basename(filepath)
    subtitle = subtitle_match.group(1) if subtitle_match else "Click to read more..."
    
    return {
        "id": os.path.basename(filepath).replace('.md', ''),
        "title": title,
        "subtitle": subtitle,
        "date": "2026-03-19" # In a real app, use file mtime
    }

def refresh():
    data = {
        "blogs": [],
        "cases": []
    }
    
    blog_dir = 'blogs'
    case_dir = 'cases'
    
    if os.path.exists(blog_dir):
        for f in os.listdir(blog_dir):
            if f.endswith('.md'):
                data["blogs"].append(extract_metadata(os.path.join(blog_dir, f)))
                
    if os.path.exists(case_dir):
        for f in os.listdir(case_dir):
            if f.endswith('.md'):
                data["cases"].append(extract_metadata(os.path.join(case_dir, f)))
                
    with open('content.json', 'w') as f:
        json.dump(data, f, indent=4)
    print("Successfully refreshed content.json")

if __name__ == "__main__":
    refresh()
