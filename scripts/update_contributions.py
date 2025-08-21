#!/usr/bin/env python3
"""
Script to update README.md with latest repository contributions from NeatGuyCoding
"""

import os
import re
import requests
from github import Github
from datetime import datetime, timedelta

# GitHub username to track
USERNAME = "NeatGuyCoding"

def get_github_token():
    """Get GitHub token from environment variable"""
    token = os.environ.get('GITHUB_TOKEN')
    if not token:
        raise ValueError("GITHUB_TOKEN environment variable is required")
    return token

def get_user_contributions(github_client, username):
    """Get user's contributions to repositories"""
    try:
        user = github_client.get_user(username)
        contributions = []
        
        # Get repositories where user has contributed
        # This includes forks, issues, pull requests, etc.
        events = user.get_events()
        
        # Track repositories and their contribution types
        repo_contributions = {}
        
        for event in events:
            if event.type in ['PushEvent', 'CreateEvent', 'IssuesEvent', 'PullRequestEvent', 'ForkEvent']:
                repo_name = event.repo.full_name
                
                if repo_name not in repo_contributions:
                    repo_contributions[repo_name] = {
                        'name': repo_name,
                        'description': '',
                        'technologies': [],
                        'stars': 0,
                        'forks': 0,
                        'contribution_types': set(),
                        'last_contribution': event.created_at
                    }
                
                # Add contribution type
                if event.type == 'PushEvent':
                    repo_contributions[repo_name]['contribution_types'].add('commits')
                elif event.type == 'IssuesEvent':
                    repo_contributions[repo_name]['contribution_types'].add('issues')
                elif event.type == 'PullRequestEvent':
                    repo_contributions[repo_name]['contribution_types'].add('pull_requests')
                elif event.type == 'ForkEvent':
                    repo_contributions[repo_name]['contribution_types'].add('fork')
        
        # Get repository details
        for repo_name, data in repo_contributions.items():
            try:
                repo = github_client.get_repo(repo_name)
                data['description'] = repo.description or 'No description available'
                data['stars'] = repo.stargazers_count
                data['forks'] = repo.forks_count
                
                # Try to detect technologies from repository
                data['technologies'] = detect_technologies(repo)
                
                contributions.append(data)
            except Exception as e:
                print(f"Error getting repo {repo_name}: {e}")
                continue
        
        # Sort by last contribution date (most recent first)
        contributions.sort(key=lambda x: x['last_contribution'], reverse=True)
        
        return contributions[:20]  # Limit to top 20 contributions
        
    except Exception as e:
        print(f"Error getting user contributions: {e}")
        return []

def detect_technologies(repo):
    """Detect technologies used in repository"""
    technologies = []
    
    try:
        # Check for common technology files
        contents = repo.get_contents("")
        
        for content in contents:
            filename = content.name.lower()
            
            if filename == 'pom.xml' or filename == 'build.gradle':
                technologies.append('Java')
            elif filename == 'requirements.txt' or filename == 'setup.py':
                technologies.append('Python')
            elif filename == 'go.mod':
                technologies.append('Go')
            elif filename == 'package.json':
                technologies.append('JavaScript')
            elif filename == 'cargo.toml':
                technologies.append('Rust')
            elif filename == 'build.sbt':
                technologies.append('Scala')
            elif filename == 'Gemfile':
                technologies.append('Ruby')
            elif filename == 'composer.json':
                technologies.append('PHP')
            elif filename == 'swift':
                technologies.append('Swift')
            elif filename == 'dockerfile':
                technologies.append('Docker')
            elif filename == 'kubernetes':
                technologies.append('Kubernetes')
            
            # Limit to avoid too many API calls
            if len(technologies) >= 5:
                break
                
    except Exception as e:
        print(f"Error detecting technologies for {repo.full_name}: {e}")
    
    return technologies

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
        'Scala': 'DC322F'
    }
    
    badges = []
    for tech in technologies[:3]:  # Limit to 3 technologies
        color = color_map.get(tech, '000000')
        tech_lower = tech.lower().replace('+', '%2B')
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
        
        # Generate contribution link
        contribution_types = list(contrib['contribution_types'])
        if 'commits' in contribution_types:
            contrib_url = f"https://github.com/{repo_name}/commits/main/?author={USERNAME}"
        elif 'pull_requests' in contribution_types:
            contrib_url = f"https://github.com/{repo_name}/pulls?q=author%3A{USERNAME}"
        elif 'issues' in contribution_types:
            contrib_url = f"https://github.com/{repo_name}/issues?q=author%3A{USERNAME}"
        else:
            contrib_url = f"https://github.com/{repo_name}"
        
        table_rows.append(
            f"| [{display_name}]({repo_url}) | {description} | {technologies} | "
            f"![Stars](https://img.shields.io/github/stars/{repo_name}?style=flat-square&labelColor=343b41) | "
            f"![Forks](https://img.shields.io/github/forks/{repo_name}?style=flat-square&labelColor=343b41) | "
            f"[My Contribution]({contrib_url}) |"
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
            
            # Add last updated timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
            new_table += f"\n\n*Last updated: {timestamp}*"
            
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
        
        # Initialize GitHub client
        github_client = Github(token)
        
        print(f"Fetching contributions for user: {USERNAME}")
        
        # Get user contributions
        contributions = get_user_contributions(github_client, USERNAME)
        
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
