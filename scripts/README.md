# Repository Contributions Update Script

This script automatically updates the README.md file with the latest repository contributions from the NeatGuyCoding GitHub account.

## Features

- Automatically detects repositories where NeatGuyCoding has contributed
- Identifies contribution types (commits, issues, pull requests, forks)
- Detects technologies used in each repository
- Updates the contribution table in README.md
- Adds timestamps for last updates
- Runs daily via GitHub Actions

## How it works

1. **GitHub Action Trigger**: The script runs automatically every day at 2:00 AM UTC via GitHub Actions
2. **Contribution Detection**: Uses GitHub API to find repositories where the user has contributed
3. **Technology Detection**: Analyzes repository files to identify programming languages and frameworks
4. **README Update**: Replaces the existing contribution table with fresh data
5. **Auto-commit**: Changes are automatically committed and pushed to the repository

## Manual Execution

You can also run the script manually:

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set environment variable:
   ```bash
   export GITHUB_TOKEN=your_github_token_here
   ```

3. Run the script:
   ```bash
   python update_contributions.py
   ```

## Configuration

- **Username**: Change `USERNAME` variable in the script to track different GitHub users
- **Schedule**: Modify the cron schedule in `.github/workflows/update-contributions.yml`
- **Contribution Limit**: Adjust the limit in `get_user_contributions()` function (currently 20)

## Requirements

- Python 3.11+
- GitHub Personal Access Token with appropriate permissions
- Required packages: `requests`, `PyGithub`

## Notes

- The script respects GitHub API rate limits
- Only public repositories are accessible
- Technology detection is based on common configuration files
- The script automatically handles errors and continues processing other repositories
