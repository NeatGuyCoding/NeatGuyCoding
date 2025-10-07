#!/usr/bin/env python3
"""
GitHub Actions README.md update script
Specifically designed for updating README.md in GitHub Actions environment
"""

import yaml
import os
import sys
import requests
import time
from typing import Dict, Optional


def load_config(config_path: str) -> Dict:
    """Load configuration file"""
    with open(config_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)


def get_github_token() -> Optional[str]:
    """Get GitHub token from environment variables"""
    return os.getenv('GITHUB_TOKEN') or os.getenv('GH_TOKEN')


def make_github_request(url: str, token: Optional[str] = None) -> Optional[Dict]:
    """Make a request to GitHub API with rate limiting"""
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'README-Generator/1.0'
    }
    
    if token:
        headers['Authorization'] = f'token {token}'
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        # Handle rate limiting
        if response.status_code == 403 and 'rate limit' in response.text.lower():
            print("⚠️ GitHub API rate limit reached, using cached data")
            return None
        
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.RequestException as e:
        print(f"⚠️ GitHub API request failed: {e}")
        return None


def get_user_issues_prs_count(owner: str, repo: str, username: str, token: Optional[str] = None) -> int:
    """Get the number of pull requests created by the user in the repository"""
    url = f"https://api.github.com/search/issues?q=repo:{owner}/{repo}+author:{username}"
    data = make_github_request(url, token)
    
    if data and 'total_count' in data:
        print(f"   - Found {data['total_count']} issues/PRs by {username} in {owner}/{repo}")
        return data['total_count']
    
    return 0


def get_repository_stats(owner: str, repo: str, username: str, token: Optional[str] = None) -> Dict[str, int]:
    """Get user's issues and PRs count for a repository"""
    print(f"📊 Fetching stats for {owner}/{repo}...")
    
    # Add small delay to respect rate limits
    time.sleep(1)
    
    issues_prs_count = get_user_issues_prs_count(owner, repo, username, token)
    
    return {
        'issues_prs_count': issues_prs_count,
    }


def generate_typing_svg_url(config: Dict) -> str:
    """Generate typing effect SVG URL"""
    typing_config = config['typing_svg']
    
    # Build parameters
    params = []
    params.append(f"font={typing_config['font']}")
    params.append(f"pause={typing_config['pause']}")
    params.append(f"color={typing_config['color']}")
    params.append(f"center={str(typing_config['center']).lower()}")
    params.append(f"vCenter={str(typing_config['vCenter']).lower()}")
    params.append(f"width={typing_config['width']}")
    
    # Add multi-line text
    lines_param = "&lines=".join(typing_config['lines'])
    params.append(f"lines={lines_param}")
    
    # Build complete URL
    base_url = "https://readme-typing-svg.herokuapp.com"
    query_string = "&".join(params)
    
    return f"{base_url}?{query_string}"


def generate_title_section(config: Dict) -> str:
    """Generate title section"""
    title = config['title']['main']
    typing_url = generate_typing_svg_url(config)
    
    section = f"""# {title}

<div align="center">
  <img src="{typing_url}" alt="Typing SVG" />
</div>
"""
    return section


def generate_about_me_section(config: Dict) -> str:
    """Generate About Me section"""
    about_config = config['about_me']
    title = about_config['title']
    
    # Generate list items
    items = []
    for item in about_config['items']:
        items.append(f"- {item['icon']} {item['text']}")
    
    items_text = "\n".join(items)
    
    section = f"""## {title}

{items_text}
"""
    return section


def generate_tech_stack_section(config: Dict) -> str:
    """Generate Tech Stack section"""
    tech_config = config['tech_stack']
    title = tech_config['title']
    
    # Generate table header
    table_header = """<table class="tech-table">
  <thead>
    <tr>
      <th>Category</th>
      <th>Technologies</th>
    </tr>
  </thead>
  <tbody>"""
    
    # Generate table rows
    table_rows = []
    for category in tech_config['categories']:
        category_name = category['name']
        
        # Generate technology badges
        badges = []
        for tech in category['technologies']:
            badge_url = f"https://img.shields.io/badge/-{tech['name']}-{tech['color']}?style=flat-square&logo={tech['logo']}&logoColor={tech['logoColor']}"
            badge = f'        <img src="{badge_url}" alt="{tech["name"]}">'
            badges.append(badge)
        
        badges_text = "\n".join(badges)
        
        # Generate table row
        row = f"""    <tr>
      <td class="category-column">{category_name}</td>
      <td class="technologies-column">
{badges_text}
      </td>
    </tr>"""
        table_rows.append(row)
    
    # Generate table footer
    table_footer = """  </tbody>
</table>"""
    
    # Combine complete section
    section = f"""## {title}

{table_header}
{chr(10).join(table_rows)}
{table_footer}
"""
    return section


def generate_repository_contributions_section(config: Dict) -> str:
    """Generate Repository Contributions section"""
    repo_config = config['repository_contributions']
    title = repo_config['title']
    username = repo_config['username']
    
    # Get GitHub token for API requests
    token = get_github_token()
    if token:
        print("🔑 Using GitHub token for API requests")
    else:
        print("⚠️ No GitHub token found, API requests will be rate limited")
    
    # Generate table header with new columns
    table_header = f"""| Project                                                                      | Description                                                                                                                                                                                                                                     | Technologies                                                                                                                                                                                                                                                                                                                           | Stars                                                                                                               | Forks                                                                                                               | Issues + PRs                                                                                                              | My Contributions                                                                                        |
|------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------|"""
    
    # Generate table rows
    table_rows = []
    for repo in repo_config['repositories']:
        repo_name = repo['name']
        repo_owner = repo['owner']
        repo_actual_name = repo.get('repo_name', repo_name.lower().replace(' ', '-'))
        description = repo['description']
        
        # Generate project link
        project_link = f"[{repo_name}](https://github.com/{repo_owner}/{repo_actual_name})"
        
        # Generate technology badges
        tech_badges = []
        for tech in repo['technologies']:
            badge_url = f"https://img.shields.io/badge/-{tech['name']}-{tech['color']}?style=flat-square&logo={tech['logo']}&logoColor={tech['logoColor']}"
            badge = f"![{tech['name']}]({badge_url})"
            tech_badges.append(badge)
        tech_badges_text = " ".join(tech_badges)
        
        # Generate Stars and Forks badges
        stars_badge = f"![Stars](https://img.shields.io/github/stars/{repo_owner}/{repo_actual_name}?style=flat-square&labelColor=343b41)"
        forks_badge = f"![Forks](https://img.shields.io/github/forks/{repo_owner}/{repo_actual_name}?style=flat-square&labelColor=343b41)"
        
        # Get user's issues and PRs count from GitHub API
        stats = get_repository_stats(repo_owner, repo_actual_name, username, token)
        issues_prs_count = stats['issues_prs_count']
        
        # Generate Issues and PRs badges
        issues_prs_badge = f"![My Issues + PRs Count](https://img.shields.io/badge/Contributions-{issues_prs_count}-blue?style=flat-square&labelColor=343b41)"

        # Generate contribution link
        contribution_type = repo.get('contribution_type', 'issues')
        if contribution_type == 'commits':
            contribution_link = f"[My Contribution](https://github.com/{repo_owner}/{repo_actual_name}/commits/main/?author={username})"
        else:
            contribution_link = f"[My Contribution](https://github.com/{repo_owner}/{repo_actual_name}/issues?q=author%3A{username})"
        
        # Generate table row with new columns
        row = f"| {project_link:<70} | {description:<200} | {tech_badges_text:<200} | {stars_badge:<50} | {forks_badge:<50} | {issues_prs_badge:<50} | {contribution_link:<50} |"
        table_rows.append(row)
    
    # Combine complete section
    section = f"""## {title}

{table_header}
{chr(10).join(table_rows)}
"""
    return section


def generate_github_stats_section(config: Dict) -> str:
    """Generate GitHub Stats section"""
    stats_config = config['github_stats']
    title = stats_config['title']
    
    # Generate statistics images
    stats_images = []
    for stat in stats_config['stats']:
        # Build parameters
        params = []
        for key, value in stat['params'].items():
            params.append(f"{key}={value}")
        
        query_string = "&".join(params)
        image_url = f"{stat['url']}?{query_string}"
        
        # Generate image tag
        if 'height' in stat:
            image_tag = f'  <img src="{image_url}" alt="{stat["alt"]}" height="{stat["height"]}"/>'
        else:
            image_tag = f'  <img src="{image_url}" alt="{stat["alt"]}" />'
        
        stats_images.append(image_tag)
    
    # Combine complete section
    section = f"""## {title}

<div align="center">
{chr(10).join(stats_images)}
</div>
"""
    return section


def generate_github_trophies_section(config: Dict) -> str:
    """Generate GitHub Trophies section"""
    trophies_config = config['github_trophies']
    title = trophies_config['title']
    
    # Build parameters
    params = []
    for key, value in trophies_config['params'].items():
        params.append(f"{key}={value}")
    
    query_string = "&".join(params)
    image_url = f"{trophies_config['url']}?{query_string}"
    
    # Combine complete section
    section = f"""## {title}

<div align="center">
  <img src="{image_url}" alt="{trophies_config['alt']}" />
</div>
"""
    return section


def generate_footer_section(config: Dict) -> str:
    """Generate footer section"""
    footer_config = config['footer']
    
    section = f"""{footer_config['separator']}

<div align="center">
  <i>{footer_config['message']}</i> {footer_config['emoji']}
</div>
"""
    return section


def main():
    """Main function"""
    config_path = "config.yaml"
    
    try:
        # Check environment variables
        github_actions = os.getenv('GITHUB_ACTIONS', 'false').lower() == 'true'
        if github_actions:
            print("🚀 Running in GitHub Actions environment")
        
        # Load configuration
        config = load_config(config_path)
        
        # Generate each section
        title_section = generate_title_section(config)
        about_section = generate_about_me_section(config)
        tech_stack_section = generate_tech_stack_section(config)
        repo_contributions_section = generate_repository_contributions_section(config)
        github_stats_section = generate_github_stats_section(config)
        github_trophies_section = generate_github_trophies_section(config)
        footer_section = generate_footer_section(config)
        
        # Combine all sections
        full_content = (title_section + "\n" + about_section + "\n" + tech_stack_section + 
                       "\n" + repo_contributions_section + "\n" + github_stats_section + 
                       "\n" + github_trophies_section + "\n" + footer_section)
        
        # Save to README.md file
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(full_content)
        
        print("✅ README.md updated successfully")
        
        if github_actions:
            print("📝 README.md content generated and saved")
        
    except FileNotFoundError:
        print(f"❌ Error: Configuration file {config_path} not found")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"❌ Error: YAML configuration file format error - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
