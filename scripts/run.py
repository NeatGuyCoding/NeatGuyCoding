#!/usr/bin/env python3
"""
Main runner script for updating repository contributions
"""

import os
import sys
import argparse
import logging
from datetime import datetime

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def setup_logging(level="INFO"):
    """Setup logging configuration"""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    return logging.getLogger(__name__)

def run_basic_update():
    """Run the basic contribution update script"""
    try:
        from update_contributions import main as basic_main
        logger.info("Running basic contribution update...")
        return basic_main()
    except ImportError as e:
        logger.error(f"Could not import basic script: {e}")
        return 1

def run_advanced_update():
    """Run the advanced contribution update script"""
    try:
        from update_contributions_advanced import main as advanced_main
        logger.info("Running advanced contribution update...")
        return advanced_main()
    except ImportError as e:
        logger.error(f"Could not import advanced script: {e}")
        return 1

def run_tests():
    """Run the test suite"""
    try:
        from test_script import run_all_tests
        logger.info("Running tests...")
        return 0 if run_all_tests() else 1
    except ImportError as e:
        logger.error(f"Could not import test script: {e}")
        return 1

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Repository Contributions Update Script",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run.py                    # Run advanced update (default)
  python run.py --basic           # Run basic update
  python run.py --test            # Run tests only
  python run.py --verbose         # Run with verbose logging
        """
    )
    
    parser.add_argument(
        '--basic',
        action='store_true',
        help='Use basic contribution update script'
    )
    
    parser.add_argument(
        '--test',
        action='store_true',
        help='Run tests only'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be updated without making changes'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    log_level = "DEBUG" if args.verbose else "INFO"
    global logger
    logger = setup_logging(log_level)
    
    logger.info("Starting repository contributions update")
    logger.info(f"Arguments: {args}")
    
    # Check for GitHub token
    if not os.environ.get('GITHUB_TOKEN'):
        logger.error("GITHUB_TOKEN environment variable is required")
        logger.info("Please set it with: export GITHUB_TOKEN=your_token_here")
        return 1
    
    # Run tests if requested
    if args.test:
        logger.info("Running tests only...")
        return run_tests()
    
    # Run appropriate update script
    if args.basic:
        logger.info("Using basic update script")
        return run_basic_update()
    else:
        logger.info("Using advanced update script (default)")
        return run_advanced_update()

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)
