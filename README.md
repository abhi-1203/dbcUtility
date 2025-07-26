# DBC Viewer - CAN Database Editor

A simple PyQt5-based GUI application for viewing, editing, and managing CAN (Controller Area Network) DBC files.

## Features

- **DBC File Viewer**: Browse and inspect CAN messages and signals in a tree structure
- **DBC File Editor**: Full-featured editor for modifying messages and signals
- **Advanced Search**: Unified search functionality with filters for messages, signals, and frame IDs
- **C++ Export**: Convert CAN messages to C++ map entries for code generation
- **Signal Management**: Add, edit, and delete both messages and signals
- **File Management**: Load, save, and save-as functionality for DBC files
- **Modern UI**: Clean, intuitive interface with proper icons and status indicators

## Project Structure

```
dbcViewer/
├── DBCUtility.py          # Main application entry point
├── dbc_editor.py          # Core DBC file processing logic
├── dbc_editor_ui.py       # User interface components
├── search_module.py       # Unified search functionality
├── requirements.txt       # Python dependencies
├── dbc/                   # Sample DBC files
│   ├── sample1.dbc
│   ├── file.dbc
│   └── file_clean.dbc
├── icons/                 # Application icons
├── tests/                 # Test files and utilities
└── README.md
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd dbcViewer
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python DBCUtility.py
   ```

## Dependencies

- **PyQt5** (≥5.15.0) - GUI framework
- **cantools** (≥40.0.0) - DBC file parsing and manipulation
- **Pillow** (≥8.0.0) - Image processing for icons
- **pyinstaller** (≥5.0.0) - For creating executables

## Usage

### Main Interface
The application provides a tabbed interface with three main sections:

1. **View Tab**: Browse DBC files in a tree structure
2. **Edit Tab**: Full editing capabilities for messages and signals
3. **Export Option**: Export CAN messages to C++ Map

### Key Features

#### DBC File Operations
- **Load DBC**: Open and parse DBC files using cantools
- **Save Changes**: Save modifications back to DBC format
- **Save As**: Save to a new file location

#### Message Management
- **Add Messages**: Create new CAN messages with custom properties
- **Edit Messages**: Modify message name, frame ID, length, and other properties
- **Delete Messages**: Remove messages from the DBC file

#### Signal Management
- **Add Signals**: Create new signals within messages
- **Edit Signals**: Modify signal properties (start bit, length, scale, offset, etc.)
- **Delete Signals**: Remove signals from messages

#### Search and Filter
- **Unified Search**: Search across messages, signals, and frame IDs
- **Filter Options**: Filter by message type, signal type, or frame ID
- **Real-time Filtering**: Instant search results as you type

#### C++ Export
- **Code Generation**: Convert CAN messages to C++ map entries
- **Customizable Output**: Configure export format and options

## Development

### Code Structure

- **`DBCUtility.py`**: Main application with PyQt5 window management
- **`dbc_editor.py`**: Core DBC processing using cantools library
- **`dbc_editor_ui.py`**: UI components and dialog boxes
- **`search_module.py`**: Search and filtering functionality

### Testing

The `tests/` directory contains various test files for:
- DBC file parsing and saving
- UI component testing
- Signal and message manipulation
- Comment handling

## License

This project is licensed under the terms specified in the LICENSE file.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

---

**Simple. Clean. Working. Feature-rich DBC editor.** 