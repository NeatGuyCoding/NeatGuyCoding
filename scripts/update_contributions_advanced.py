#!/usr/bin/env python3
"""
Advanced script to update README.md repository contributions section using GraphQL API
"""

import os
import re
import requests
from datetime import datetime, timedelta
import json

# Import configuration
try:
    from config import *
except ImportError:
    # Fallback configuration if config.py is not available
    USERNAME = 'NeatGuyCoding'
    API_BASE = 'https://api.github.com'
    GRAPHQL_URL = 'https://api.github.com/graphql'
    MAX_REPOSITORIES = 20
    MAX_DESCRIPTION_LENGTH = 200
    LANGUAGE_COLORS = {
        'Java': 'ED8B00', 'Python': '3776AB', 'JavaScript': 'F7DF1E',
        'TypeScript': '3178C6', 'Go': '00ADD8', 'C++': '00599C'
    }
    CONTRIBUTIONS_SECTION_START = '## 👨‍💻 Repository Contributions'
    CONTRIBUTIONS_SECTION_END = '## 📊 GitHub Stats'

# GitHub API configuration
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')

def get_github_headers():
    """Get headers for GitHub API requests"""
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'NeatGuyCoding-Contribution-Updater'
    }
    if GITHUB_TOKEN:
        headers['Authorization'] = f'bearer {GITHUB_TOKEN}'
    return headers

def get_graphql_headers():
    """Get headers for GraphQL API requests"""
    headers = {
        'Authorization': f'bearer {GITHUB_TOKEN}',
        'Content-Type': 'application/json',
    }
    return headers

def get_user_contributions_graphql():
    """Get user contributions using GraphQL API for more comprehensive data"""
    if not GITHUB_TOKEN:
        print("GITHUB_TOKEN required for GraphQL API")
        return get_user_contributions_rest()
    
    # GraphQL query to get user contributions
    query = """
    query($username: String!, $after: String) {
      user(login: $username) {
        contributionsCollection {
          totalContributions
          contributionCalendar {
            totalContributions
          }
        }
        repositories(first: 100, after: $after, orderBy: {field: UPDATED_AT, direction: DESC}) {
          nodes {
            name
            description
            primaryLanguage {
              name
              color
            }
            stargazerCount
            forkCount
            url
            isFork
            defaultBranchRef {
              name
            }
          }
          pageInfo {
            hasNextPage
            endCursor
          }
        }
        pullRequests(first: 100, after: $after, orderBy: {field: CREATED_AT, direction: DESC}) {
          nodes {
            repository {
              nameWithOwner
              description
              primaryLanguage {
                name
                color
              }
              stargazerCount
              forkCount
              url
            }
            createdAt
            state
          }
        }
        issues(first: 100, after: $after, orderBy: {field: CREATED_AT, direction: DESC}) {
          nodes {
            repository {
              nameWithOwner
              description
              primaryLanguage {
                name
                color
              }
              stargazerCount
              forkCount
              url
            }
            createdAt
            state
          }
        }
      }
    }
    """
    
    try:
        response = requests.post(
            GRAPHQL_URL,
            json={'query': query, 'variables': {'username': USERNAME}},
            headers=get_graphql_headers()
        )
        
        if response.status_code == 200:
            data = response.json()
            return process_graphql_data(data)
        else:
            print(f"GraphQL API error: {response.status_code}")
            return get_user_contributions_rest()
            
    except Exception as e:
        print(f"GraphQL API error: {e}")
        return get_user_contributions_rest()

def process_graphql_data(data):
    """Process GraphQL API response data"""
    if 'data' not in data or 'user' not in data['data']:
        return []
    
    user_data = data['data']['user']
    contributions = []
    
    # Process repositories
    if 'repositories' in user_data and 'nodes' in user_data['repositories']:
        for repo in user_data['repositories']['nodes']:
            if repo and not repo.get('isFork', False):
                repo_info = {
                    'name': repo['name'],
                    'full_name': repo['name'],  # For user's own repos
                    'description': repo.get('description') or 'No description available',
                    'language': repo.get('primaryLanguage', {}).get('name'),
                    'stars': repo.get('stargazerCount', 0),
                    'forks': repo.get('forkCount', 0),
                    'url': repo['url'],
                    'contributions': 1,  # User owns this repo
                    'type': 'repository'
                }
                contributions.append(repo_info)
    
    # Process pull requests
    if 'pullRequests' in user_data and 'nodes' in user_data['pullRequests']:
        for pr in user_data['pullRequests']['nodes']:
            if pr and pr['repository']:
                repo = pr['repository']
                repo_info = {
                    'name': repo['nameWithOwner'].split('/')[-1],
                    'full_name': repo['nameWithOwner'],
                    'description': repo.get('description') or 'No description available',
                    'language': repo.get('primaryLanguage', {}).get('name'),
                    'stars': repo.get('stargazerCount', 0),
                    'forks': repo.get('forkCount', 0),
                    'url': repo['url'],
                    'contributions': 1,
                    'type': 'pull_request',
                    'created_at': pr['createdAt']
                }
                contributions.append(repo_info)
    
    # Process issues
    if 'issues' in user_data and 'nodes' in user_data['issues']:
        for issue in user_data['issues']['nodes']:
            if issue and issue['repository']:
                repo = issue['repository']
                repo_info = {
                    'name': repo['nameWithOwner'].split('/')[-1],
                    'full_name': repo['nameWithOwner'],
                    'description': repo.get('description') or 'No description available',
                    'language': repo.get('primaryLanguage', {}).get('name'),
                    'stars': repo.get('stargazerCount', 0),
                    'forks': repo.get('forkCount', 0),
                    'url': repo['url'],
                    'contributions': 1,
                    'type': 'issue',
                    'created_at': issue['createdAt']
                }
                contributions.append(repo_info)
    
    # Remove duplicates and sort by contributions
    unique_contributions = {}
    for contrib in contributions:
        key = contrib['full_name']
        if key not in unique_contributions:
            unique_contributions[key] = contrib
        else:
            unique_contributions[key]['contributions'] += 1
    
    # Convert to list and sort
    contributions_list = list(unique_contributions.values())
    contributions_list.sort(key=lambda x: x['contributions'], reverse=True)
    
    return contributions_list[:MAX_REPOSITORIES]  # Limit to configured number

def get_user_contributions_rest():
    """Fallback to REST API for getting user contributions"""
    headers = get_github_headers()
    
    # Get user's public repositories
    repos_url = f"{API_BASE}/users/{USERNAME}/repos"
    repos_response = requests.get(repos_url, headers=headers)
    
    if repos_response.status_code != 200:
        print(f"Failed to get repositories: {repos_response.status_code}")
        return []
    
    repos = repos_response.json()
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
                repo_details = {
                    'name': repo['name'],
                    'full_name': repo['full_name'],
                    'description': repo['description'] or 'No description available',
                    'language': repo['language'],
                    'stars': repo['stargazers_count'],
                    'forks': repo['forks_count'],
                    'url': repo['html_url'],
                    'contributions': len(commits),
                    'type': 'repository'
                }
                contributions.append(repo_details)
    
    # Sort by contributions count
    contributions.sort(key=lambda x: x['contributions'], reverse=True)
    return contributions[:MAX_REPOSITORIES]

def get_language_badge(language):
    """Get language badge for README"""
    if not language:
        return ""
    
    color = LANGUAGE_COLORS.get(language, '000000')
    return f"![{language}](https://img.shields.io/badge/-{language}-{color}?style=flat-square&logo={language.lower()}&logoColor=white)"

def format_contributions_table(contributions):
    """Format contributions as markdown table"""
    table = """| Project                                                                      | Description                                                                                                                                                                                                                                     | Technologies                                                                                                                                                                                                                                                                                                                           | Stars                                                                                                               | Forks                                                                                                               | My Contributions                                                                                        |
|------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------|"""
    
    for repo in contributions:
        # Truncate description if too long
        description = repo['description']
        if len(description) > MAX_DESCRIPTION_LENGTH:
            description = description[:MAX_DESCRIPTION_LENGTH-3] + "..."
        
        # Get language badge
        language_badge = get_language_badge(repo['language'])
        
        # Format stars and forks
        stars_badge = f"![Stars](https://img.shields.io/github/stars/{repo['full_name']}?style=flat-square&labelColor=343b41)"
        forks_badge = f"![Forks](https://img.shields.io/github/forks/{repo['full_name']}?style=flat-square&labelColor=343b41)"
        
        # Format contributions link based on type
        if repo['type'] == 'repository':
            contributions_link = f"[My Contribution](https://github.com/{repo['full_name']}/commits/main/?author={USERNAME})"
        elif repo['type'] == 'pull_request':
            contributions_link = f"[My Contribution](https://github.com/{repo['full_name']}/pulls?q=author%3A{USERNAME})"
        elif repo['type'] == 'issue':
            contributions_link = f"[My Contribution](https://github.com/{repo['full_name']}/issues?q=author%3A{USERNAME})"
        else:
            contributions_link = f"[My Contribution](https://github.com/{repo['full_name']})"
        
        table += f"\n| [{repo['name']}]({repo['url']})                                   | {description} | {language_badge}                                                                                                                                                                                                                                               | {stars_badge}                                                                                                               | {forks_badge}                                                                                                               | {contributions_link}                   |"
    
    return table

def update_readme():
    """Update README.md with new contributions data"""
    readme_path = 'README.md'
    
    # Read current README
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Get new contributions data
    contributions = get_user_contributions_graphql()
    
    if not contributions:
        print("No contributions found")
        return
    
    # Format new contributions table
    new_table = format_contributions_table(contributions)
    
    # Find and replace the contributions section
    pattern = rf'({re.escape(CONTRIBUTIONS_SECTION_START)}\n\n)(.*?)(\n\n{re.escape(CONTRIBUTIONS_SECTION_END)})'
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
    print("Starting advanced README contributions update...")
    
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
