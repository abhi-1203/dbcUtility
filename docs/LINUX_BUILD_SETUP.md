# Linux Build Setup Guide

This guide will help you build and distribute the DBC Utility for Linux systems. Whether you're a developer wanting to create a Linux version or a user looking to understand the build process, this guide covers everything you need to know.

## What You'll Need

Before you start, make sure you have:

- **A Linux system** (Ubuntu, Debian, Fedora, etc.)
- **Python 3.8 or later**
- **Git** (to clone the repository)
- **Basic command line knowledge**

## Getting Started

### 1. Clone the Repository

First, get the source code:

```bash
git clone https://github.com/yourusername/dbcViewer.git
cd dbcViewer
```

### 2. Install Dependencies

The build system will check for required packages, but you can install them manually:

```bash
# On Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv

# On Fedora
sudo dnf install python3 python3-pip

# On Arch Linux
sudo pacman -S python python-pip
```

### 3. Install Python Dependencies

```bash
pip3 install -r requirements.txt
```

## Building the Linux Distribution

### Quick Build

The easiest way to build is using our automated script:

```bash
python3 scripts/build_linux.py
```

This will:
- Check your system for required dependencies
- Build the application using PyInstaller
- Create a complete distribution folder
- Generate installation scripts and desktop integration

### What Gets Created

After a successful build, you'll find a new folder in `linuxBuilds/` containing:

- **DBCUtility** - The main executable
- **Icons and resources** - All application assets
- **install.sh** - System-wide installation script
- **uninstall.sh** - Removal script
- **launch-dbc-utility.sh** - Portable launcher
- **Desktop integration files** - Menu entries and icons

## Installation Options

### Option 1: System-wide Installation (Recommended)

This installs the application system-wide so it appears in your applications menu:

```bash
cd linuxBuilds/DBCUtility-Linux-x86_64
chmod +x install.sh
./install.sh
```

After installation, you can:
- Launch from your applications menu
- Run `dbc-utility` from anywhere in the terminal
- Uninstall later using the provided script

### Option 2: Portable Usage

If you prefer not to install system-wide:

```bash
cd linuxBuilds/DBCUtility-Linux-x86_64
chmod +x launch-dbc-utility.sh
./launch-dbc-utility.sh
```

This runs the application without installing anything.

### Option 3: Direct Execution

You can also run the executable directly:

```bash
cd linuxBuilds/DBCUtility-Linux-x86_64
chmod +x DBCUtility
./DBCUtility
```

## Creating a Release Package

To create a distributable package for sharing:

```bash
python3 scripts/release_linux.py
```

This creates:
- A versioned release folder
- A compressed `.tar.gz` package
- Release notes and documentation
- Checksums for file integrity

## Troubleshooting

### Common Issues

**"PyQt5 not found"**
```bash
pip3 install PyQt5
```

**"cantools not found"**
```bash
pip3 install cantools
```

**"Permission denied"**
```bash
chmod +x scripts/build_linux.py
chmod +x scripts/release_linux.py
```

**"PyInstaller not found"**
```bash
pip3 install pyinstaller
```

### Build Fails

If the build process fails:

1. **Check dependencies**: Run `python3 scripts/test_linux_build.py`
2. **Clean build**: Remove `build/` and `dist/` folders, then try again
3. **Check Python version**: Ensure you're using Python 3.8+
4. **Check disk space**: Ensure you have at least 500MB free

### Application Won't Start

If the built application doesn't start:

1. **Check permissions**: `chmod +x DBCUtility`
2. **Run from terminal**: See error messages
3. **Check dependencies**: Some systems may need additional libraries
4. **Try portable mode**: Use `launch-dbc-utility.sh`

## Distribution

### For Users

The `.tar.gz` package is ready for distribution. Users can:

1. Download and extract the package
2. Run `./install.sh` for system installation
3. Or use `./launch-dbc-utility.sh` for portable use

### For Developers

To distribute your build:

1. Test on target systems
2. Create a release using `scripts/release_linux.py`
3. Upload the `.tar.gz` file to your distribution platform
4. Include the generated release notes

## Supported Systems

The Linux build has been tested on:

- **Ubuntu** 20.04 LTS and later
- **Debian** 11 and later
- **Fedora** 35 and later
- **CentOS** 8 and later
- **Arch Linux**
- **openSUSE** Leap 15.3 and later

## Getting Help

If you encounter issues:

1. Check this guide first
2. Look at the error messages in the terminal
3. Try the troubleshooting steps above
4. Check the main project README
5. Create an issue on the project repository

## Advanced Topics

### Custom Builds

You can customize the build by modifying `scripts/build_linux.py`:

- Change the application name
- Add additional files
- Modify the installation location
- Customize desktop integration

### Cross-Platform Building

For building on different architectures:

- The build automatically detects your system architecture
- Builds are named accordingly (e.g., `x86_64`, `aarch64`)
- Test on target systems before distribution

### Continuous Integration

For automated builds:

- The scripts are designed to work in CI environments
- Use the test script to verify the build environment
- Check exit codes for automation integration

---

That's it! You should now be able to build and distribute the DBC Utility for Linux. The process is designed to be straightforward while providing flexibility for different use cases. 