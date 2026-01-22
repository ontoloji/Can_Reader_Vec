#!/usr/bin/env python3
"""
Validation script to check the application structure without requiring dependencies.
"""

import os
import sys
from pathlib import Path

def check_file_exists(filepath, description):
    """Check if a file exists."""
    if os.path.isfile(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description}: {filepath} NOT FOUND")
        return False

def check_directory_exists(dirpath, description):
    """Check if a directory exists."""
    if os.path.isdir(dirpath):
        print(f"✅ {description}: {dirpath}")
        return True
    else:
        print(f"❌ {description}: {dirpath} NOT FOUND")
        return False

def main():
    """Main validation function."""
    print("=" * 60)
    print("CAN Data Viewer - Structure Validation")
    print("=" * 60)
    print()
    
    all_ok = True
    
    # Check main files
    print("Main Files:")
    all_ok &= check_file_exists("main.py", "Entry point")
    all_ok &= check_file_exists("requirements.txt", "Dependencies")
    all_ok &= check_file_exists("README.md", "Documentation")
    all_ok &= check_file_exists(".gitignore", "Git ignore")
    print()
    
    # Check directories
    print("Directories:")
    all_ok &= check_directory_exists("data", "Data layer")
    all_ok &= check_directory_exists("gui", "GUI layer")
    all_ok &= check_directory_exists("utils", "Utils layer")
    all_ok &= check_directory_exists("resources", "Resources")
    print()
    
    # Check data layer files
    print("Data Layer:")
    all_ok &= check_file_exists("data/__init__.py", "Data package init")
    all_ok &= check_file_exists("data/blf_reader.py", "BLF reader")
    all_ok &= check_file_exists("data/dbc_parser.py", "DBC parser")
    all_ok &= check_file_exists("data/signal_processor.py", "Signal processor")
    print()
    
    # Check GUI layer files
    print("GUI Layer:")
    all_ok &= check_file_exists("gui/__init__.py", "GUI package init")
    all_ok &= check_file_exists("gui/main_window.py", "Main window")
    all_ok &= check_file_exists("gui/signal_selector.py", "Signal selector")
    all_ok &= check_file_exists("gui/graph_panel.py", "Graph panel")
    all_ok &= check_file_exists("gui/dialogs.py", "Dialogs")
    print()
    
    # Check utils layer files
    print("Utils Layer:")
    all_ok &= check_file_exists("utils/__init__.py", "Utils package init")
    all_ok &= check_file_exists("utils/config.py", "Configuration")
    all_ok &= check_file_exists("utils/workspace.py", "Workspace manager")
    all_ok &= check_file_exists("utils/export.py", "Export manager")
    print()
    
    # Check syntax of all Python files
    print("Syntax Check:")
    python_files = [
        "main.py",
        "data/__init__.py", "data/blf_reader.py", "data/dbc_parser.py", "data/signal_processor.py",
        "gui/__init__.py", "gui/main_window.py", "gui/signal_selector.py", "gui/graph_panel.py", "gui/dialogs.py",
        "utils/__init__.py", "utils/config.py", "utils/workspace.py", "utils/export.py"
    ]
    
    for pyfile in python_files:
        try:
            with open(pyfile, 'r') as f:
                compile(f.read(), pyfile, 'exec')
            print(f"✅ Syntax valid: {pyfile}")
        except SyntaxError as e:
            print(f"❌ Syntax error in {pyfile}: {e}")
            all_ok = False
    print()
    
    # Summary
    print("=" * 60)
    if all_ok:
        print("✅ ALL CHECKS PASSED - Application structure is valid!")
        print()
        print("Next steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Run the application: python main.py")
        return 0
    else:
        print("❌ SOME CHECKS FAILED - Please review the errors above")
        return 1

if __name__ == "__main__":
    sys.exit(main())
