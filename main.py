#!/usr/bin/env python3

"""
DBC Utility - CAN Database Editor
Copyright (C) 2025 Abhijith Purohit

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

Main entry point for DBC Utility
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.DBCUtility import MainWindow
from PyQt5 import QtWidgets, QtGui
from src.resource_utils import get_resource_path

def main():
    """Main entry point for the application."""
    app = QtWidgets.QApplication(sys.argv)
    
    # Set application icon at the QApplication level first
    try:
        icon_path = get_resource_path("icons/app_icon.ico")
        if os.path.exists(icon_path):
            app_icon = QtGui.QIcon(icon_path)
            app.setWindowIcon(app_icon)
    except Exception as e:
        print(f"Could not load application icon: {e}")
    
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 