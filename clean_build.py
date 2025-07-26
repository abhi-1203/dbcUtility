#!/usr/bin/env python3
"""
Quick script to clean build directories
"""

import os
import shutil

def clean_build():
    """Clean build and dist directories"""
    dirs_to_clean = ['build', 'dist']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"Cleaning {dir_name} directory...")
            shutil.rmtree(dir_name)
            print(f"✓ Cleaned {dir_name}")
        else:
            print(f"✓ {dir_name} directory doesn't exist (already clean)")
    
    print("\n=== Clean Complete ===")
    print("You can now run 'python build_exe.py' to build a fresh executable.")

if __name__ == "__main__":
    clean_build() 