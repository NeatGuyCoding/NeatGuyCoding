#!/usr/bin/env python3
"""
Test script to verify contribution update functionality
"""

import os
import sys

# Add scripts directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if all required modules can be imported"""
    try:
        import requests
        print("✓ requests module imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import requests: {e}")
        return False
    
    try:
        import re
        print("✓ re module imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import re: {e}")
        return False
    
    try:
        from datetime import datetime
        print("✓ datetime module imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import datetime: {e}")
        return False
    
    return True

def test_github_token():
    """Test if GitHub token is available"""
    token = os.environ.get('GITHUB_TOKEN')
    if token:
        print("✓ GITHUB_TOKEN found in environment")
        return True
    else:
        print("⚠ GITHUB_TOKEN not found in environment (will use unauthenticated API)")
        return False

def test_readme_exists():
    """Test if README.md exists"""
    readme_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'README.md')
    if os.path.exists(readme_path):
        print("✓ README.md found")
        return True
    else:
        print("✗ README.md not found")
        return False

def test_contributions_section():
    """Test if contributions section exists in README"""
    readme_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'README.md')
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if '## 👨‍💻 Repository Contributions' in content:
            print("✓ Contributions section found in README.md")
            return True
        else:
            print("✗ Contributions section not found in README.md")
            return False
    except Exception as e:
        print(f"✗ Error reading README.md: {e}")
        return False

def main():
    """Run all tests"""
    print("Running contribution update script tests...\n")
    
    tests = [
        test_imports,
        test_github_token,
        test_readme_exists,
        test_contributions_section
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ Test {test.__name__} failed with error: {e}")
        print()
    
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✓ All tests passed! Script should work correctly.")
        return 0
    else:
        print("⚠ Some tests failed. Please check the issues above.")
        return 1

if __name__ == "__main__":
    exit(main())
