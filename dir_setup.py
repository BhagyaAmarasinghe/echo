#!/usr/bin/env python3
"""
Echo Project Directory Structure Creator
---------------------------------------
This script creates the directory structure for the Echo project,
a smart Linux package recommendation system.
"""

import os
import sys
from pathlib import Path

# Base project structure
PROJECT_STRUCTURE = [
    # Root files
    "LICENSE",
    "README.md",
    "pyproject.toml",
    "requirements.txt",
    "setup.py",
    
    # Source directory
    "src/echo/__init__.py",
    "src/echo/config.py",
    "src/echo/cli.py",
    "src/echo/main.py",
    
    # Database module
    "src/echo/database/__init__.py",
    "src/echo/database/models.py",
    "src/echo/database/database.py",
    
    # Services module
    "src/echo/services/__init__.py",
    "src/echo/services/package_detector.py",
    "src/echo/services/package_manager.py",
    "src/echo/services/log_analyzer.py",
    "src/echo/services/ai_recommender.py",
    "src/echo/services/similarity_analyzer.py",
    
    # Utils module
    "src/echo/utils/__init__.py",
    "src/echo/utils/logger.py",
    "src/echo/utils/system.py",
    
    # Reports module
    "src/echo/reports/__init__.py",
    "src/echo/reports/report_generator.py",
    
    # Tests
    "tests/__init__.py",
    "tests/conftest.py",
    "tests/test_cli.py",
    "tests/test_services/__init__.py",
    "tests/test_services/test_package_detector.py",
    "tests/test_services/test_package_manager.py",
    "tests/test_services/test_log_analyzer.py",
    "tests/test_services/test_ai_recommender.py",
    "tests/test_services/test_similarity_analyzer.py",
    
    # Examples
    "examples/basic_usage.py",
    "examples/cli_usage.py",
    
    # Documentation
    "docs/README.md",
    "docs/cli.md",
    "docs/installation.md",
    "docs/api.md",
]

def create_directory_structure(base_path="."):
    """Create the Echo project directory structure."""
    base_path = Path(base_path)
    
    print(f"Creating Echo project structure in {base_path.absolute()}")
    print("=" * 50)
    
    # Create directories and files
    for item in PROJECT_STRUCTURE:
        path = base_path / item
        
        # Create parent directories if needed
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create empty file if it doesn't exist
        if not path.exists():
            path.touch()
            print(f"Created file: {path}")
        else:
            print(f"File already exists: {path}")
    
    print("\nDirectory structure created successfully!")
    print("\nNext steps:")
    print("1. Implement the code for each file")
    print("2. Install development dependencies: pip install -r requirements.txt")
    print("3. Install the package in development mode: pip install -e .")

if __name__ == "__main__":
    # Get base path from command line argument or use current directory
    base_path = sys.argv[1] if len(sys.argv) > 1 else "."
    create_directory_structure(base_path)