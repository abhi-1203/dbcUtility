#!/usr/bin/env python3

"""
Create zip package for DBC Utility release
"""

import os
import sys
import zipfile
from datetime import datetime

def create_zip_package(version):
    """Create a zip package for the release"""
    print(f"=== Creating Zip Package for v{version} ===")
    
    # Source directory
    release_dir = f"release-v{version}"
    
    # Zip file name
    zip_filename = f"DBCUtility-v{version}.zip"
    
    if not os.path.exists(release_dir):
        print(f"✗ Release directory not found: {release_dir}")
        print("Please run 'python scripts/release.py' first")
        return False
    
    # Create zip file
    try:
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add all files from release directory
            for root, dirs, files in os.walk(release_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    # Add file to zip with relative path
                    arcname = os.path.relpath(file_path, release_dir)
                    zipf.write(file_path, arcname)
                    print(f"✓ Added: {arcname}")
        
        # Get file size
        file_size = os.path.getsize(zip_filename)
        size_mb = file_size / (1024 * 1024)
        
        print(f"✓ Zip package created: {zip_filename}")
        print(f"✓ File size: {size_mb:.1f} MB")
        print(f"✓ Location: {os.path.abspath(zip_filename)}")
        
        return True
        
    except Exception as e:
        print(f"✗ Failed to create zip: {e}")
        return False

def main():
    """Main function"""
    print("=== DBC Utility Zip Package Creator ===")
    
    # Get version from command line or default
    if len(sys.argv) > 1:
        version = sys.argv[1]
    else:
        version = "1.0.0"
    
    print(f"Creating zip for version: {version}")
    
    if create_zip_package(version):
        print(f"\n=== Zip Package Complete ===")
        print(f"Zip file: DBCUtility-v{version}.zip")
        print("Ready for upload to GitHub Releases!")
    else:
        print("\n=== Zip Creation Failed ===")
        sys.exit(1)

if __name__ == "__main__":
    main() 