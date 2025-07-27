#!/usr/bin/env python3
"""
Make build scripts executable
"""

import os
import stat
from pathlib import Path

def make_executable():
    """Make build scripts executable"""
    script_dir = Path(__file__).parent
    
    scripts_to_make_executable = [
        "build_linux.py",
        "release_linux.py",
        "build_exe.py",
        "release.py",
        "clean_build.py",
        "create_zip.py",
        "test_linux_build.py"
    ]
    
    for script in scripts_to_make_executable:
        script_path = script_dir / script
        if script_path.exists():
            os.chmod(script_path, stat.S_IRWXU | stat.S_IRGRP | stat.S_IROTH)
            print(f"✓ Made {script} executable")
        else:
            print(f"⚠️  {script} not found")

if __name__ == "__main__":
    make_executable() 