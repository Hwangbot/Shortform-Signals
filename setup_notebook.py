#!/usr/bin/env python3
"""
Setup script to copy CSV files to the Notebook directory for easy access
"""

import shutil
import os
from pathlib import Path

def setup_notebook_files():
    """Copy CSV files to the Notebook directory"""
    # Get the project root directory
    project_root = Path(__file__).parent
    notebook_dir = project_root / "Notebook"
    
    # CSV files to copy
    csv_files = [
        "shortform_videos.csv",
        "shortform_creators.csv", 
        "shortform_platforms.csv"
    ]
    
    print(" Setting up notebook files...")
    
    for file in csv_files:
        source = project_root / file
        destination = notebook_dir / file
        
        if source.exists():
            shutil.copy2(source, destination)
            print(f" Copied {file} to Notebook directory")
        else:
            print(f" Source file {file} not found")
    
    print(" Setup complete! You can now run the notebook from the Notebook directory.")

if __name__ == "__main__":
    setup_notebook_files() 