#!/usr/bin/env python3
"""
Advanced script to update README.md with latest repository contributions using GraphQL API
"""

import os
import re
import json
import requests
from datetime import datetime, timedelta

# GitHub username to track
USERNAME = "NeatGuyCoding"

def get_github_token():
    """Get GitHub token from environment variable"""
    token = os.environ.get('GITHUB_TOKEN')
    if not token:
        raise ValueError("GITHUB_TOKEN environment variable is required")
    return token

def get_user_contributions_graphql(token, username):
    """Get user's contributions using GraphQL API for more accurate data"""
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
    }
    
    # GraphQL query to get user contributions
    query = """
    query($username: String!, $after: String) {
      user(login: $username) {
        contributionsCollection {
          totalCommitContributions
          totalIssueContributions
          totalPullRequestContributions
          totalRepositoryContributions
          commitContributionsByRepository(maxRepositories: 100, after: $after) {
            repository {
              nameWithOwner
              description
              stargazerCount
              forkCount
              primaryLanguage {
                name
                color
              }
              languages(first: 5) {
                nodes {
                  name
                  color
                }
              }
            }
            contributions {
              totalCount
            }
          }
          issueContributionsByRepository(maxRepositories: 100, after: $after) {
            repository {
              nameWithOwner
              description
              stargazerCount
              forkCount
              primaryLanguage {
                name
                color
              }
              languages(first: 5) {
                nodes {
                  name
                  color
                }
              }
            }
            contributions {
              totalCount
            }
          }
          pullRequestContributionsByRepository(maxRepositories: 100, after: $after) {
            repository {
              nameWithOwner
              description
              stargazerCount
              forkCount
              primaryLanguage {
                name
                color
              }
              languages(first: 5) {
                nodes {
                  name
                  color
                }
              }
            }
            contributions {
              totalCount
            }
          }
        }
        repositories(first: 100, after: $after) {
          nodes {
            nameWithOwner
            description
            stargazerCount
            forkCount
            primaryLanguage {
              name
              color
            }
            languages(first: 5) {
              nodes {
                name
                color
              }
            }
          }
        }
      }
    }
    """
    
    try:
        response = requests.post(
            'https://api.github.com/graphql',
            headers=headers,
            json={'query': query, 'variables': {'username': username}}
        )
        
        if response.status_code == 200:
            data = response.json()
            return process_graphql_data(data, username)
        else:
            print(f"GraphQL API error: {response.status_code} - {response.text}")
            return []
            
    except Exception as e:
        print(f"Error calling GraphQL API: {e}")
        return []

def process_graphql_data(data, username):
    """Process GraphQL response data"""
    if 'data' not in data or 'user' not in data['data']:
        return []
    
    user_data = data['data']['user']
    contributions = {}
    
    # Process commit contributions
    if 'contributionsCollection' in user_data:
        contrib_collection = user_data['contributionsCollection']
        
        # Process commit contributions
        if 'commitContributionsByRepository' in contrib_collection:
            for repo_contrib in contrib_collection['commitContributionsByRepository']:
                repo = repo_contrib['repository']
                repo_name = repo['nameWithOwner']
                
                if repo_name not in contributions:
                    contributions[repo_name] = {
                        'name': repo_name,
                        'description': repo.get('description', 'No description available'),
                        'technologies': [],
                        'stars': repo.get('stargazerCount', 0),
                        'forks': repo.get('forkCount', 0),
                        'contribution_types': set(),
                        'total_contributions': 0
                    }
                
                contributions[repo_name]['contribution_types'].add('commits')
                contributions[repo_name]['total_contributions'] += repo_contrib['contributions']['totalCount']
                
                # Add technologies
                if repo.get('primaryLanguage'):
                    lang_name = repo['primaryLanguage']['name']
                    if lang_name not in contributions[repo_name]['technologies']:
                        contributions[repo_name]['technologies'].append(lang_name)
                
                if repo.get('languages'):
                    for lang in repo['languages']['nodes']:
                        lang_name = lang['name']
                        if lang_name not in contributions[repo_name]['technologies']:
                            contributions[repo_name]['technologies'].append(lang_name)
        
        # Process issue contributions
        if 'issueContributionsByRepository' in contrib_collection:
            for repo_contrib in contrib_collection['issueContributionsByRepository']:
                repo = repo_contrib['repository']
                repo_name = repo['nameWithOwner']
                
                if repo_name not in contributions:
                    contributions[repo_name] = {
                        'name': repo_name,
                        'description': repo.get('description', 'No description available'),
                        'technologies': [],
                        'stars': repo.get('stargazerCount', 0),
                        'forks': repo.get('forkCount', 0),
                        'contribution_types': set(),
                        'total_contributions': 0
                    }
                
                contributions[repo_name]['contribution_types'].add('issues')
                contributions[repo_name]['total_contributions'] += repo_contrib['contributions']['totalCount']
                
                # Add technologies
                if repo.get('primaryLanguage'):
                    lang_name = repo['primaryLanguage']['name']
                    if lang_name not in contributions[repo_name]['technologies']:
                        contributions[repo_name]['technologies'].append(lang_name)
        
        # Process pull request contributions
        if 'pullRequestContributionsByRepository' in contrib_collection:
            for repo_contrib in contrib_collection['pullRequestContributionsByRepository']:
                repo = repo_contrib['repository']
                repo_name = repo['nameWithOwner']
                
                if repo_name not in contributions:
                    contributions[repo_name] = {
                        'name': repo_name,
                        'description': repo.get('description', 'No description available'),
                        'technologies': [],
                        'stars': repo.get('stargazerCount', 0),
                        'forks': repo.get('forkCount', 0),
                        'contribution_types': set(),
                        'total_contributions': 0
                    }
                
                contributions[repo_name]['contribution_types'].add('pull_requests')
                contributions[repo_name]['total_contributions'] += repo_contrib['contributions']['totalCount']
                
                # Add technologies
                if repo.get('primaryLanguage'):
                    lang_name = repo['primaryLanguage']['name']
                    if lang_name not in contributions[repo_name]['technologies']:
                        contributions[repo_name]['technologies'].append(lang_name)
    
    # Process owned repositories
    if 'repositories' in user_data:
        for repo in user_data['repositories']['nodes']:
            repo_name = repo['nameWithOwner']
            
            if repo_name not in contributions:
                contributions[repo_name] = {
                    'name': repo_name,
                    'description': repo.get('description', 'No description available'),
                    'technologies': [],
                    'stars': repo.get('stargazerCount', 0),
                    'forks': repo.get('forkCount', 0),
                    'contribution_types': set(['owner']),
                    'total_contributions': 0
                }
            
            # Add technologies
            if repo.get('primaryLanguage'):
                lang_name = repo['primaryLanguage']['name']
                if lang_name not in contributions[repo_name]['technologies']:
                    contributions[repo_name]['technologies'].append(lang_name)
            
            if repo.get('languages'):
                for lang in repo['languages']['nodes']:
                    lang_name = lang['name']
                    if lang_name not in contributions[repo_name]['technologies']:
                        contributions[repo_name]['technologies'].append(lang_name)
    
    # Convert to list and sort by total contributions
    contributions_list = list(contributions.values())
    contributions_list.sort(key=lambda x: x['total_contributions'], reverse=True)
    
    return contributions_list[:25]  # Return top 25 contributions

def generate_contribution_badges(technologies):
    """Generate technology badges for README"""
    if not technologies:
        return ""
    
    badge_template = "![{tech}](https://img.shields.io/badge/-{tech}-{color}?style=flat-square&logo={tech_lower}&logoColor=white)"
    
    # Color mapping for technologies
    color_map = {
        'Java': '007396',
        'Python': '3776AB',
        'Go': '00ADD8',
        'JavaScript': 'F7DF1E',
        'TypeScript': '3178C6',
        'Rust': '000000',
        'C++': '00599C',
        'Ruby': 'CC342D',
        'PHP': '777BB4',
        'Kotlin': '0095D5',
        'Swift': 'FA7343',
        'Scala': 'DC322F',
        'HTML': 'E34F26',
        'CSS': '1572B6',
        'Shell': '4EAA25',
        'Dockerfile': '2496ED',
        'Makefile': '6C5CE7',
        'Vue': '4FC08D',
        'React': '61DAFB',
        'Angular': 'DD0031'
    }
    
    badges = []
    for tech in technologies[:3]:  # Limit to 3 technologies
        color = color_map.get(tech, '000000')
        tech_lower = tech.lower().replace('+', '%2B').replace('#', '')
        badges.append(badge_template.format(
            tech=tech, 
            color=color, 
            tech_lower=tech_lower
        ))
    
    return " ".join(badges)

def generate_contribution_table(contributions):
    """Generate contribution table for README"""
    if not contributions:
        return "| Project | Description | Technologies | Stars | Forks | My Contributions |\n|---------|-------------|--------------|-------|-------|------------------|\n| No recent contributions found | - | - | - | - | - |"
    
    table_rows = []
    table_rows.append("| Project | Description | Technologies | Stars | Forks | My Contributions |")
    table_rows.append("|---------|-------------|--------------|-------|-------|------------------|")
    
    for contrib in contributions:
        repo_name = contrib['name']
        repo_url = f"https://github.com/{repo_name}"
        display_name = repo_name.split('/')[-1]
        
        description = contrib['description'][:100] + "..." if len(contrib['description']) > 100 else contrib['description']
        
        technologies = generate_contribution_badges(contrib['technologies'])
        if not technologies:
            technologies = "![Generic](https://img.shields.io/badge/-Generic-000000?style=flat-square)"
        
        stars = contrib['stars']
        forks = contrib['forks']
        
        # Generate contribution link based on contribution types
        contribution_types = list(contrib['contribution_types'])
        if 'commits' in contribution_types:
            contrib_url = f"https://github.com/{repo_name}/commits/main/?author={USERNAME}"
        elif 'pull_requests' in contribution_types:
            contrib_url = f"https://github.com/{repo_name}/pulls?q=author%3A{USERNAME}"
        elif 'issues' in contribution_types:
            contrib_url = f"https://github.com/{repo_name}/issues?q=author%3A{USERNAME}"
        elif 'owner' in contribution_types:
            contrib_url = f"https://github.com/{repo_name}"
        else:
            contrib_url = f"https://github.com/{repo_name}"
        
        # Add contribution count to display
        contrib_count = contrib['total_contributions']
        contrib_display = f"[{contrib_count} contributions]({contrib_url})"
        
        table_rows.append(
            f"| [{display_name}]({repo_url}) | {description} | {technologies} | "
            f"![Stars](https://img.shields.io/github/stars/{repo_name}?style=flat-square&labelColor=343b41) | "
            f"![Forks](https://img.shields.io/github/forks/{repo_name}?style=flat-square&labelColor=343b41) | "
            f"{contrib_display} |"
        )
    
    return "\n".join(table_rows)

def update_readme(contributions):
    """Update README.md with new contribution data"""
    readme_path = "README.md"
    
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find the contribution table section
        start_pattern = r"## 👨‍💻 Repository Contributions\n\n"
        end_pattern = r"\n## 📊 GitHub Stats"
        
        start_match = re.search(start_pattern, content)
        end_match = re.search(end_pattern, content)
        
        if start_match and end_match:
            start_pos = start_match.end()
            end_pos = end_match.start()
            
            # Generate new contribution table
            new_table = generate_contribution_table(contributions)
            
            # Add last updated timestamp and summary
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
            total_repos = len(contributions)
            total_contribs = sum(c['total_contributions'] for c in contributions)
            
            summary = f"\n\n*Last updated: {timestamp}*  \n"
            summary += f"*Total repositories: {total_repos}*  \n"
            summary += f"*Total contributions: {total_contribs}*"
            
            new_table += summary
            
            # Replace the old table with new one
            new_content = (
                content[:start_pos] + 
                new_table + 
                "\n\n" + 
                content[end_pos:]
            )
            
            # Write back to file
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"Successfully updated README.md with {len(contributions)} contributions")
            return True
            
        else:
            print("Could not find contribution table section in README.md")
            return False
            
    except Exception as e:
        print(f"Error updating README.md: {e}")
        return False

def main():
    """Main function"""
    try:
        # Get GitHub token
        token = get_github_token()
        
        print(f"Fetching contributions for user: {USERNAME}")
        
        # Get user contributions using GraphQL API
        contributions = get_user_contributions_graphql(token, USERNAME)
        
        if contributions:
            print(f"Found {len(contributions)} contributions")
            
            # Update README.md
            success = update_readme(contributions)
            
            if success:
                print("README.md updated successfully!")
            else:
                print("Failed to update README.md")
        else:
            print("No contributions found")
            
    except Exception as e:
        print(f"Error in main: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
