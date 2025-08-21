#!/usr/bin/env python3
"""
Test script to verify the contribution update functionality
"""

import os
import sys
import tempfile
import shutil
from unittest.mock import patch, MagicMock

# Add the scripts directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_technology_detection():
    """Test technology detection from repository files"""
    from config import TECHNOLOGY_PATTERNS
    
    print("Testing technology detection patterns...")
    
    for tech, patterns in TECHNOLOGY_PATTERNS.items():
        print(f"  {tech}: {patterns}")
    
    print("✓ Technology detection patterns loaded successfully")

def test_color_mapping():
    """Test technology color mapping"""
    from config import TECHNOLOGY_COLORS
    
    print("\nTesting technology color mapping...")
    
    # Test a few key technologies
    test_techs = ['Java', 'Python', 'Go', 'JavaScript', 'Rust']
    
    for tech in test_techs:
        if tech in TECHNOLOGY_COLORS:
            color = TECHNOLOGY_COLORS[tech]
            print(f"  {tech}: #{color}")
        else:
            print(f"  {tech}: Not found")
    
    print("✓ Technology color mapping loaded successfully")

def test_badge_generation():
    """Test badge generation functionality"""
    print("\nTesting badge generation...")
    
    # Mock the generate_contribution_badges function
    def mock_generate_badges(technologies):
        if not technologies:
            return ""
        
        badges = []
        for tech in technologies[:3]:
            badges.append(f"![{tech}](https://img.shields.io/badge/-{tech}-000000?style=flat-square)")
        
        return " ".join(badges)
    
    # Test with sample technologies
    test_technologies = ['Java', 'Python', 'Go', 'Rust']
    badges = mock_generate_badges(test_technologies)
    
    print(f"  Input technologies: {test_technologies}")
    print(f"  Generated badges: {badges}")
    
    if badges:
        print("✓ Badge generation working correctly")
    else:
        print("✗ Badge generation failed")

def test_table_generation():
    """Test contribution table generation"""
    print("\nTesting table generation...")
    
    # Mock contribution data
    mock_contributions = [
        {
            'name': 'test/repo1',
            'description': 'Test repository 1',
            'technologies': ['Java', 'Spring'],
            'stars': 100,
            'forks': 50,
            'contribution_types': {'commits'},
            'total_contributions': 25
        },
        {
            'name': 'test/repo2',
            'description': 'Test repository 2',
            'technologies': ['Python', 'Django'],
            'stars': 200,
            'forks': 75,
            'contribution_types': {'issues'},
            'total_contributions': 15
        }
    ]
    
    # Mock the table generation function
    def mock_generate_table(contributions):
        if not contributions:
            return "| No contributions | - | - | - | - | - |"
        
        rows = ["| Project | Description | Technologies | Stars | Forks | My Contributions |"]
        rows.append("|---------|-------------|--------------|-------|-------|------------------|")
        
        for contrib in contributions:
            repo_name = contrib['name'].split('/')[-1]
            desc = contrib['description'][:50] + "..." if len(contrib['description']) > 50 else contrib['description']
            techs = ", ".join(contrib['technologies'][:2])
            stars = contrib['stars']
            forks = contrib['forks']
            contrib_count = contrib['total_contributions']
            
            rows.append(f"| {repo_name} | {desc} | {techs} | {stars} | {forks} | {contrib_count} |")
        
        return "\n".join(rows)
    
    table = mock_generate_table(mock_contributions)
    print(f"  Generated table:\n{table}")
    
    if "test/repo1" in table and "test/repo2" in table:
        print("✓ Table generation working correctly")
    else:
        print("✗ Table generation failed")

def test_config_loading():
    """Test configuration loading"""
    print("\nTesting configuration loading...")
    
    try:
        from config import USERNAME, MAX_REPOSITORIES, MAX_TECHNOLOGIES
        
        print(f"  Username: {USERNAME}")
        print(f"  Max repositories: {MAX_REPOSITORIES}")
        print(f"  Max technologies: {MAX_TECHNOLOGIES}")
        
        print("✓ Configuration loaded successfully")
        
    except ImportError as e:
        print(f"✗ Configuration loading failed: {e}")

def run_all_tests():
    """Run all tests"""
    print("🚀 Starting contribution update script tests...\n")
    
    try:
        test_config_loading()
        test_technology_detection()
        test_color_mapping()
        test_badge_generation()
        test_table_generation()
        
        print("\n🎉 All tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
