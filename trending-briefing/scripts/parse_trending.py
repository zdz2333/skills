#!/usr/bin/env python3
"""
parse_trending.py — Parse GitHub Trending HTML and output structured list
Usage: python3 parse_trending.py [html_file]
"""

import os, re, json, sys
from pathlib import Path

def parse_trending(html_content):
    """Extract repo info from GitHub Trending HTML"""
    # Find all article blocks
    articles = re.findall(r'<article class="Box-row">(.*?)</article>', html_content, re.DOTALL)
    
    # Skip patterns for hrefs
    skip_prefixes = ('/sponsors', '/login', '/apps', '/features', '/collections',
                     '/explore', '/settings', '/notifications', '/pulls', '/issues',
                     '/actions', '/packages', '/wiki', '/trending')
    
    results = []
    for article in articles[:14]:
        # Extract ALL hrefs, then filter for repo paths
        all_hrefs = re.findall(r'href="(/[a-zA-Z0-9_-]+/[a-zA-Z0-9_.-]+)"', article)
        repo_path = None
        for href in all_hrefs:
            if (href.count('/') == 2 and 
                not any(href.startswith(s) for s in skip_prefixes) and
                '/login?return_to=' not in href):
                repo_path = href
                break
        
        if not repo_path:
            continue
        
        owner, name = repo_path.lstrip('/').split('/')
        
        # Extract description
        desc_match = re.search(r'<p[^>]*>\s*([^<]{20,200})\s*</p>', article)
        desc = desc_match.group(1).strip() if desc_match else ""
        
        # Extract language
        lang_match = re.search(r'<span[^>]*programmingLanguage[^>]*>\s*([^<]+)\s*</span>', article)
        lang = lang_match.group(1).strip() if lang_match else ""
        
        # Extract "X stars today" count (most reliable for unauthenticated)
        star_match = re.search(r'(\d[\d,]*) stars today', article)
        stars = star_match.group(1).replace(',', '') if star_match else "0"
        
        results.append({
            "name": name,
            "owner": owner,
            "path": repo_path,
            "desc": desc[:150],
            "lang": lang,
            "stars": int(stars) if stars.isdigit() else 0
        })
    
    return results

def main():
    if len(sys.argv) > 1:
        html_path = Path(sys.argv[1])
    else:
        home = os.path.expanduser("~")
        html_path = Path(home) / ".hermes" / "trending-briefing" / "trending.html"
    
    if not html_path.exists():
        print(f"Error: {html_path} not found. Run the fetch step first.")
        sys.exit(1)
    
    with open(html_path) as f:
        html = f.read()
    
    repos = parse_trending(html)
    
    if not repos:
        print("No repos found. GitHub HTML structure may have changed.")
        sys.exit(1)
    
    # Sort by stars
    repos.sort(key=lambda x: x['stars'], reverse=True)
    
    # Output formatted
    print(f"\n=== GitHub Trending ({len(repos)} repos) ===\n")
    for i, r in enumerate(repos, 1):
        print(f"{i:2}. [{r['lang']:<12}] {r['name']:<30} ⭐ {r['stars']:>6}")
        if r['desc']:
            print(f"    {r['desc'][:80]}")
        print()
    
    # Also output JSON for programmatic use
    json_path = html_path.parent / "trending_repos.json"
    with open(json_path, 'w') as f:
        json.dump(repos, f, indent=2)
    print(f"JSON saved to: {json_path}")

if __name__ == "__main__":
    main()
