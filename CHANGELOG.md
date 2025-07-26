# Changelog

All notable changes to DBC Utility will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive contribution guidelines (CONTRIBUTING.md)
- Code of Conduct (CODE_OF_CONDUCT.md)
- Security Policy (SECURITY.md)
- Proper copyright notices for GPL-licensed dependencies
- Automatic backup file cleanup functionality
- Enhanced icon handling for PyInstaller executables
- GPL v3 license compliance for PyQt5 compatibility
- **Project structure reorganization** with `src/` and `scripts/` folders

### Changed
- Updated README.md with detailed third-party license information
- Improved GPL compliance documentation
- Enhanced build script to clean existing executables
- **License changed from MIT to GPL v3 for PyQt5 compliance**
- **Project structure reorganized** for better maintainability
- **Build scripts moved** to `scripts/` directory
- **Source code moved** to `src/` package
- **New main entry point** (`main.py`) for cleaner imports

### Fixed
- None type handling for signal attributes (minimum, maximum, scale, offset, start_bit, length)
- Icon loading issues in PyInstaller executables
- Application icon consistency between executable and taskbar
- **Import structure issues** after project reorganization
- **Removed redundant main entry point** from src/DBCUtility.py

## [1.0.0] - 2025-01-XX

### Added
- Initial release of DBC Utility
- DBC file viewer with tree structure
- DBC file editor with full CRUD operations
- Advanced search functionality across messages and signals
- C++ export functionality
- PyQt5-based modern GUI
- Icon support for all buttons and tabs
- File management (load, save, save-as)
- Signal overlap detection (removed in later versions)
- Backup file creation during save operations

### Features
- **View Tab**: Browse DBC files in hierarchical structure
- **Edit Tab**: Full editing capabilities for messages and signals
- **Search**: Unified search with filters
- **Export**: C++ code generation
- **File Operations**: Load, save, and save-as functionality

### Technical Details
- Built with PyQt5 for cross-platform compatibility
- Uses cantools library for DBC file parsing
- PyInstaller integration for executable creation
- Comprehensive error handling and validation

---

## Version History

### Version 1.0.0
- **Release Date**: 2025-01-XX
- **Status**: Initial Release
- **Key Features**: Complete DBC viewer and editor with modern GUI

### Future Versions
- Planned features and improvements will be documented here
- Security updates and bug fixes will be tracked
- Major version releases will include migration guides

---

## Migration Guide

### From Development Versions
If you're upgrading from development versions:

1. **Backup your DBC files** before upgrading
2. **Test with sample files** to ensure compatibility
3. **Check for deprecated features** in the changelog
4. **Update any custom scripts** that may depend on specific behaviors

### Breaking Changes
- None in version 1.0.0
- Future breaking changes will be clearly documented here

---

## Contributing to the Changelog

When contributing to DBC Utility, please update this changelog by:

1. Adding your changes under the appropriate section
2. Using the correct format and categories
3. Including issue numbers when applicable
4. Following the existing style and structure

### Categories
- **Added**: New features
- **Changed**: Changes in existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security-related changes 