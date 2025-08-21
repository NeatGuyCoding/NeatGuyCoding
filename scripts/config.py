#!/usr/bin/env python3
"""
Configuration file for the repository contributions update script
"""

# Configuration file for repository contributions updater

# GitHub username to track
USERNAME = 'NeatGuyCoding'

# GitHub API configuration
API_BASE = 'https://api.github.com'
GRAPHQL_URL = 'https://api.github.com/graphql'

# Repository limits
MAX_REPOSITORIES = 20
MAX_DESCRIPTION_LENGTH = 200

# Language colors for badges
LANGUAGE_COLORS = {
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
    'Scala': 'DC322F',
    'HTML': 'E34F26',
    'CSS': '1572B6',
    'Shell': '4EAA25',
    'Dockerfile': '2496ED',
    'Makefile': '6C5CE7'
}

# README section markers
CONTRIBUTIONS_SECTION_START = '## 👨‍💻 Repository Contributions'
CONTRIBUTIONS_SECTION_END = '## 📊 GitHub Stats'

# Badge configuration
BADGE_STYLE = 'flat-square'
BADGE_LABEL_COLOR = '343b41'
