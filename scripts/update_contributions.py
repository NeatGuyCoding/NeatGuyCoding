#!/usr/bin/env python3
"""
Script to update README.md repository contributions section
"""

import os
import re
import requests
from datetime import datetime
import json

# GitHub API configuration
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
USERNAME = 'NeatGuyCoding'
API_BASE = 'https://api.github.com'

def get_github_headers():
    """Get headers for GitHub API requests"""
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'NeatGuyCoding-Contribution-Updater'
    }
    if GITHUB_TOKEN:
        headers['Authorization'] = f'token {GITHUB_TOKEN}'
    return headers

def get_user_contributions():
    """Get user contributions from GitHub API"""
    headers = get_github_headers()
    
    # Get user's public repositories
    repos_url = f"{API_BASE}/users/{USERNAME}/repos"
    repos_response = requests.get(repos_url, headers=headers)
    
    if repos_response.status_code != 200:
        print(f"Failed to get repositories: {repos_response.status_code}")
        return []
    
    repos = repos_response.json()
    
    # Get contributions from repositories where user has contributed
    contributions = []
    
    for repo in repos:
        if repo['fork']:
            continue
            
        # Get commits by user
        commits_url = f"{API_BASE}/repos/{repo['full_name']}/commits"
        params = {'author': USERNAME}
        commits_response = requests.get(commits_url, headers=headers, params=params)
        
        if commits_response.status_code == 200:
            commits = commits_response.json()
            if commits:
                # Get repository details
                repo_details = {
                    'name': repo['name'],
                    'full_name': repo['full_name'],
                    'description': repo['description'] or 'No description available',
                    'language': repo['language'],
                    'stars': repo['stargazers_count'],
                    'forks': repo['forks_count'],
                    'url': repo['html_url'],
                    'contributions': len(commits)
                }
                contributions.append(repo_details)
    
    # Sort by contributions count (descending)
    contributions.sort(key=lambda x: x['contributions'], reverse=True)
    
    # Get external contributions (repositories where user contributed but doesn't own)
    # This is a simplified approach - in practice you might want to use GraphQL API
    # to get more comprehensive contribution data
    
    return contributions[:20]  # Limit to top 20

def get_language_badge(language):
    """Get language badge for README"""
    if not language:
        return ""
    
    language_colors = {
        'Java': 'ED8B00',
        'Python': '3776AB',
        'JavaScript': 'F7DF1E',
        'TypeScript': '3178C6',
        'Go': '00ADD8',
        'C++': '00599C',
        'C': 'A8B9CC',
        'Rust': '000000',
        'Ruby': 'CC342D',
        'PHP': '777BB4',
        'Kotlin': '0095D5',
        'Swift': 'FA7343',
        'Scala': 'DC322F'
    }
    
    color = language_colors.get(language, '000000')
    return f"![{language}](https://img.shields.io/badge/-{language}-{color}?style=flat-square&logo={language.lower()}&logoColor=white)"

def format_contributions_table(contributions):
    """Format contributions as markdown table"""
    table = """| Project                                                                      | Description                                                                                                                                                                                                                                     | Technologies                                                                                                                                                                                                                                                                                                                           | Stars                                                                                                               | Forks                                                                                                               | My Contributions                                                                                        |
|------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------|"""
    
    for repo in contributions:
        # Truncate description if too long
        description = repo['description']
        if len(description) > 200:
            description = description[:197] + "..."
        
        # Get language badge
        language_badge = get_language_badge(repo['language'])
        
        # Format stars and forks
        stars_badge = f"![Stars](https://img.shields.io/github/stars/{repo['full_name']}?style=flat-square&labelColor=343b41)"
        forks_badge = f"![Forks](https://img.shields.io/github/forks/{repo['full_name']}?style=flat-square&labelColor=343b41)"
        
        # Format contributions link
        contributions_link = f"[My Contribution](https://github.com/{repo['full_name']}/commits/main/?author={USERNAME})"
        
        table += f"\n| [{repo['name']}]({repo['url']})                                   | {description} | {language_badge}                                                                                                                                                                                                                                               | {stars_badge}                                                                                                               | {forks_badge}                                                                                                               | {contributions_link}                   |"
    
    return table

def update_readme():
    """Update README.md with new contributions data"""
    readme_path = 'README.md'
    
    # Read current README
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Get new contributions data
    contributions = get_user_contributions()
    
    if not contributions:
        print("No contributions found")
        return
    
    # Format new contributions table
    new_table = format_contributions_table(contributions)
    
    # Find and replace the contributions section
    pattern = r'(## 👨‍💻 Repository Contributions\n\n)(.*?)(\n\n## 📊 GitHub Stats)'
    replacement = r'\1' + new_table + r'\3'
    
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    if new_content != content:
        # Write updated content
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated README.md with {len(contributions)} contributions")
    else:
        print("No changes needed in README.md")

def main():
    """Main function"""
    print("Starting README contributions update...")
    
    if not GITHUB_TOKEN:
        print("Warning: GITHUB_TOKEN not set. API rate limits may apply.")
    
    try:
        update_readme()
        print("README update completed successfully!")
    except Exception as e:
        print(f"Error updating README: {e}")
        exit(1)

if __name__ == "__main__":
    main()
