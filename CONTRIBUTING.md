# Contributing to DBC Utility

Thank you for your interest in contributing to DBC Utility! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Pull Request Process](#pull-request-process)
- [Reporting Bugs](#reporting-bugs)
- [Feature Requests](#feature-requests)
- [License](#license)

## Code of Conduct

This project is committed to providing a welcoming and inclusive environment for all contributors. By participating in this project, you agree to:

- Be respectful and considerate of others
- Use welcoming and inclusive language
- Be collaborative and open to constructive feedback
- Focus on what is best for the community
- Show empathy towards other community members

## How Can I Contribute?

### Reporting Bugs

- Use the GitHub issue tracker
- Include a clear and descriptive title
- Provide detailed steps to reproduce the bug
- Include system information (OS, Python version, etc.)
- Attach relevant files (DBC files, error logs, screenshots)

### Suggesting Enhancements

- Use the GitHub issue tracker with the "enhancement" label
- Provide a clear description of the proposed feature
- Explain why this feature would be useful
- Include mockups or examples if applicable

### Pull Requests

- Fork the repository
- Create a feature branch (`git checkout -b feature/amazing-feature`)
- Make your changes following the coding standards
- Add tests if applicable
- Update documentation as needed
- Commit your changes (`git commit -m 'Add amazing feature'`)
- Push to the branch (`git push origin feature/amazing-feature`)
- Open a Pull Request

## Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- A code editor (VS Code, PyCharm, etc.)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/dbcViewer.git
   cd dbcViewer
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Run the application:
   ```bash
   python DBCUtility.py
   ```

### Building the Executable

To build the executable for distribution:

```bash
python build_exe.py
```

The executable will be created in the `dist/` directory.

## Coding Standards

### Python Code Style

- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings for all public functions and classes
- Keep functions focused and concise
- Use type hints where appropriate

### PyQt5 Guidelines

- Use Qt naming conventions for Qt-specific code
- Handle Qt signals and slots properly
- Ensure proper cleanup of Qt resources
- Use appropriate Qt widgets for the task

### File Organization

- Keep related functionality together
- Use clear, descriptive file names
- Separate UI logic from business logic
- Maintain consistent import organization

### Comments and Documentation

- Write clear, concise comments
- Document complex algorithms
- Explain the "why" not just the "what"
- Keep documentation up to date

## Pull Request Process

1. **Fork and Clone**: Fork the repository and clone your fork locally
2. **Create Branch**: Create a feature branch from `main`
3. **Make Changes**: Implement your changes following the coding standards
4. **Test**: Ensure your changes work correctly and don't break existing functionality
5. **Document**: Update documentation if needed
6. **Commit**: Write clear, descriptive commit messages
7. **Push**: Push your changes to your fork
8. **Submit PR**: Create a pull request with a clear description

### Commit Message Format

Use conventional commit format:

```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Pull Request Template

When creating a pull request, please include:

- **Description**: What does this PR do?
- **Type of Change**: Bug fix, feature, documentation, etc.
- **Testing**: How was this tested?
- **Screenshots**: If applicable
- **Checklist**: Ensure all requirements are met

## Testing

### Manual Testing

Before submitting a PR, please test:

- [ ] Application starts without errors
- [ ] DBC files can be loaded and viewed
- [ ] DBC files can be edited and saved
- [ ] All buttons and features work as expected
- [ ] No console errors or warnings

### Automated Testing

We encourage adding automated tests for new features:

- Unit tests for business logic
- Integration tests for UI components
- Test DBC files for validation

## Reporting Bugs

When reporting bugs, please include:

1. **Environment**:
   - Operating System and version
   - Python version
   - DBC Utility version

2. **Steps to Reproduce**:
   - Clear, step-by-step instructions
   - Sample DBC file if applicable

3. **Expected vs Actual Behavior**:
   - What you expected to happen
   - What actually happened

4. **Additional Information**:
   - Error messages or logs
   - Screenshots if helpful
   - Any workarounds you found

## Feature Requests

When requesting features, please include:

1. **Problem Statement**: What problem does this feature solve?
2. **Proposed Solution**: How should this feature work?
3. **Use Cases**: Who would benefit from this feature?
4. **Mockups**: Visual examples if applicable

## License

By contributing to DBC Utility, you agree that your contributions will be licensed under the GNU General Public License v3 (GPL v3).

## Questions?

If you have questions about contributing, please:

1. Check the existing issues and pull requests
2. Read the documentation
3. Open an issue for general questions
4. Contact the maintainers directly for urgent matters

Thank you for contributing to DBC Utility! 