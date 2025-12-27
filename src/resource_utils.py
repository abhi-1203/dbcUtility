#!/usr/bin/env python3
"""
Shared resource helpers.

Why this exists:
- In development, resources live in the repo (e.g. ./icons).
- In a PyInstaller build, resources are extracted into a temp directory pointed to by sys._MEIPASS.

Centralizing this avoids duplicating the same logic across multiple modules.
"""

from __future__ import annotations

import os
import sys


def get_resource_path(relative_path: str) -> str:
    """
    Return an absolute path for a resource file.

    - PyInstaller: resolves relative to sys._MEIPASS
    - Dev: resolves relative to the project root (one level above this file's directory)
    """
    base_path = getattr(sys, "_MEIPASS", None)
    if base_path:
        return os.path.join(base_path, relative_path)

    # Dev mode: project root = ../ (since this file lives in ./src)
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    return os.path.join(project_root, relative_path)


