# Repository Contributions Auto-Updater

This directory contains scripts to automatically update the README.md file with the latest repository contributions from NeatGuyCoding.

## Files

- `update_contributions.py` - Basic script using REST API
- `update_contributions_advanced.py` - Advanced script using GraphQL API (recommended)
- `test_script.py` - Test script to verify functionality
- `README.md` - This documentation file

## How It Works

The system automatically:

1. Fetches contribution data from GitHub API
2. Processes repository information (stars, forks, languages, descriptions)
3. Updates the "## 👨‍💻 Repository Contributions" section in README.md
4. Preserves all other content in the README

## GitHub Action

The `.github/workflows/update-contributions.yml` file sets up an automated workflow that:

- Runs daily at 2:00 AM UTC
- Can be triggered manually via workflow_dispatch
- Updates the README.md file automatically
- Commits and pushes changes

## Setup

1. Ensure you have a GitHub token with appropriate permissions
2. The token should be set as `GITHUB_TOKEN` secret in your repository
3. Install dependencies: `pip install -r requirements.txt`

## Usage

### Manual Update
```bash
python scripts/update_contributions_advanced.py
```

### Test Script
```bash
python scripts/test_script.py
```

## Dependencies

- `requests` - For HTTP API calls
- Standard Python libraries (re, datetime, json, os)

## API Rate Limits

- Unauthenticated: 60 requests/hour
- Authenticated: 5,000 requests/hour
- GraphQL: 5,000 requests/hour

## Notes

- The script only updates the contributions section
- All other README content remains unchanged
- Repository data is sorted by contribution count
- Limited to top 20 repositories to avoid overly long tables
