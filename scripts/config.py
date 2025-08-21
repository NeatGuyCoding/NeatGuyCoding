#!/usr/bin/env python3
"""
Configuration file for the repository contributions update script
"""

# GitHub username to track
USERNAME = "NeatGuyCoding"

# Maximum number of repositories to display
MAX_REPOSITORIES = 25

# Maximum number of technologies to show per repository
MAX_TECHNOLOGIES = 3

# Contribution types to track
CONTRIBUTION_TYPES = [
    'commits',
    'issues', 
    'pull_requests',
    'fork',
    'owner'
]

# Technology color mapping for badges
TECHNOLOGY_COLORS = {
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
    'Angular': 'DD0031',
    'Spring': '6DB33F',
    'Spring Boot': '6DB33F',
    'Spring Cloud': '6DB33F',
    'Quarkus': '4695EB',
    'MyBatis': '000000',
    'Netty': '2C2D72',
    'Hibernate': '59666C',
    'Celery': '37814A',
    'SQLAlchemy': 'D71F00',
    'Pydantic': 'E92063',
    'NumPy': '013243',
    'SciPy': '8CAAE6',
    'Keras': 'D00000',
    'Flask': 'F12345',
    'Django': 'AC1289',
    'FastAPI': '009688',
    'Gin': '00ADD8',
    'Kratos': '00ADD8',
    'SQLX': '00ADD8',
    'Cobra': '00ADD8',
    'Testify': '00ADD8',
    'Echo': '00ADD8',
    'Next.js': '000000',
    'TailwindCSS': '38B2AC',
    'HeadlessUI': '66E3FF',
    'Lexical': '61DAFB',
    'Svelte': 'FF3E00'
}

# Repository file patterns for technology detection
TECHNOLOGY_PATTERNS = {
    'Java': ['pom.xml', 'build.gradle', 'gradle.properties'],
    'Python': ['requirements.txt', 'setup.py', 'pyproject.toml', 'Pipfile'],
    'Go': ['go.mod', 'go.sum'],
    'JavaScript': ['package.json', 'yarn.lock', 'pnpm-lock.yaml'],
    'Rust': ['Cargo.toml', 'Cargo.lock'],
    'Scala': ['build.sbt', 'project/plugins.sbt'],
    'Ruby': ['Gemfile', 'Gemfile.lock'],
    'PHP': ['composer.json', 'composer.lock'],
    'Swift': ['Package.swift', '*.swift'],
    'Docker': ['Dockerfile', 'docker-compose.yml', 'docker-compose.yaml'],
    'Kubernetes': ['*.yaml', '*.yml'],
    'Terraform': ['*.tf', '*.tfvars'],
    'Ansible': ['playbook.yml', 'inventory.yml'],
    'Helm': ['Chart.yaml', 'values.yaml']
}

# GitHub API settings
GITHUB_API_BASE_URL = "https://api.github.com"
GITHUB_GRAPHQL_URL = "https://api.github.com/graphql"

# Rate limiting settings
MAX_REQUESTS_PER_HOUR = 5000
REQUEST_DELAY = 1  # seconds between requests

# Output settings
README_PATH = "README.md"
BACKUP_PATH = "README.md.backup"
LOG_LEVEL = "INFO"

# Table formatting
TABLE_HEADERS = [
    "Project",
    "Description", 
    "Technologies",
    "Stars",
    "Forks",
    "My Contributions"
]

# Description truncation
MAX_DESCRIPTION_LENGTH = 100
DESCRIPTION_SUFFIX = "..."

# Badge settings
BADGE_STYLE = "flat-square"
BADGE_LOGO_COLOR = "white"
