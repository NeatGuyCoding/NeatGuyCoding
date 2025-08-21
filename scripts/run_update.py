#!/usr/bin/env python3
"""
Main script to run the repository contributions update
"""

import os
import sys
import argparse
from pathlib import Path

def main():
    """Main function with command line argument parsing"""
    parser = argparse.ArgumentParser(
        description='Update README.md with latest repository contributions'
    )
    parser.add_argument(
        '--script', 
        choices=['basic', 'advanced'], 
        default='advanced',
        help='Choose which script to run (default: advanced)'
    )
    parser.add_argument(
        '--test', 
        action='store_true',
        help='Run test script instead of update script'
    )
    parser.add_argument(
        '--dry-run', 
        action='store_true',
        help='Show what would be updated without making changes'
    )
    
    args = parser.parse_args()
    
    # Change to repository root directory
    repo_root = Path(__file__).parent.parent
    os.chdir(repo_root)
    
    if args.test:
        print("Running test script...")
        os.system(f"python {Path(__file__).parent}/test_script.py")
        return
    
    if args.dry_run:
        print("DRY RUN MODE - No changes will be made")
        print("To actually update, run without --dry-run flag")
        return
    
    # Choose script to run
    if args.script == 'basic':
        script_path = Path(__file__).parent / 'update_contributions.py'
    else:
        script_path = Path(__file__).parent / 'update_contributions_advanced.py'
    
    if not script_path.exists():
        print(f"Error: Script {script_path} not found")
        return 1
    
    print(f"Running {args.script} contribution update script...")
    print(f"Script: {script_path}")
    print(f"Repository: {repo_root}")
    print()
    
    # Run the selected script
    result = os.system(f"python {script_path}")
    
    if result == 0:
        print("\n✓ Contribution update completed successfully!")
    else:
        print(f"\n✗ Contribution update failed with exit code {result}")
        return result
    
    return 0

if __name__ == "__main__":
    exit(main())
