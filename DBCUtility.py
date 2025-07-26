#!/usr/bin/env python3

"""
Author: Abhijith Purohit
Date: 15, July - 2025

Description:
    PyQt5 GUI to View and Edit DBC files.

Version: v1.1

Features:
    1. User can view and edit the DBC file.
    2. CAN Messages can be exported to C++ Map.
    4. Helps Search signals for ease of access
    5. Able to edit both Messages and Signals.
    6. TODO: Add ability to view CAN dumps ?

"""

import sys
import json
import subprocess
import os

def show_import_error(pkg):
    try:
        from PyQt5.QtWidgets import QMessageBox, QApplication
        app = QApplication(sys.argv)
        QMessageBox.critical(None, "Missing Dependency",
            f"Required package '{pkg}' is not installed.\n"
            "Please install it using:\n"
            f"    pip install {pkg}\n"
            "and then restart the application.")
    except Exception:
        print(f"Required package '{pkg}' is not installed. Please install it using: pip install {pkg}")
    sys.exit(1)

try:
    from PyQt5 import QtWidgets, QtCore, QtGui
except ImportError:
    show_import_error('PyQt5')

try:
    import cantools
except ImportError:
    show_import_error('cantools')

try:
    from PIL import Image
except ImportError:
    show_import_error('Pillow')

from search_module import UnifiedSearchWidget
from dbc_editor_ui import DBCEditorWidget

def read_requirements():
    """Read requirements from requirements.txt file."""
    requirements = []
    try:
        with open('requirements.txt', 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    # Extract package name (remove version specifiers)
                    package_name = line.split('>=')[0].split('==')[0].split('<=')[0].strip()
                    requirements.append(package_name)
    except FileNotFoundError:
        print("Warning: requirements.txt not found. Using default packages.")
        requirements = ['PyQt5', 'cantools', 'Pillow']
    return requirements

def install_package(package_name):
    """Installs a package using pip."""
    try:
        # Check if the package is already installed
        __import__(package_name)
        print(f"✓ {package_name} is already installed.")
    except ImportError:
        print(f"Installing {package_name}...")
        try:
            # Install the package using pip
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
            print(f"✓ {package_name} installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"✗ Error installing {package_name}: {e}")
            sys.exit(1)

def check_and_install_requirements():
    """Check and install required packages from requirements.txt."""
    print("Checking required packages...")
    required_packages = read_requirements()
    
    for package in required_packages:
        install_package(package)
    
    print("All required packages are ready!")

# Check and install required packages
check_and_install_requirements()

class EmptyWidget(QtWidgets.QWidget):
    """A placeholder widget for empty menu pages."""
    def __init__(self, text="This page is under construction.", parent=None):
        super().__init__(parent)
        layout = QtWidgets.QVBoxLayout(self)
        label = QtWidgets.QLabel(text)
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setFont(QtGui.QFont("Arial", 16, QtGui.QFont.Bold))
        layout.addWidget(label)
        self.setLayout(layout)

class DBCProcessor:
    """
    Handles the logic for loading DBC files and extracting data.
    Separated from the UI for better modularity.
    """
    def __init__(self):
        self.db = None
        self._extracted_data = []

    def load_dbc_file(self, dbc_path):
        """Loads a DBC file and populates _extracted_data."""
        if not dbc_path:
            raise ValueError("No DBC file path provided.")
        try:
            self.db = cantools.database.load_file(dbc_path)
        except Exception as e:
            raise RuntimeError(f"Failed to load DBC file: {e}")
        self._extracted_data = []
        for msg in self.db.messages:
            message_info = {
                "message_name": msg.name,
                "senders": [str(s) for s in msg.senders],
                "frame_id": msg.frame_id,
                "signals": []
            }
            for sig in msg.signals:
                cleaned_comments = str(sig.comments).strip('\0').replace('\n', ' ') if sig.comments else ""
                signal_info = {
                    "signal_name": sig.name,
                    "comments": cleaned_comments,
                    "receivers": [str(r) for r in sig.receivers],
                    "is_signed": sig.is_signed,
                    "minimum": sig.minimum,
                    "maximum": sig.maximum,
                    "item_text": f"{msg.name}.{sig.name}"
                }
                message_info["signals"].append(signal_info)
            self._extracted_data.append(message_info)
        return list(self._extracted_data)

    def get_extracted_data(self):
        return list(self._extracted_data)

    def convert_to_cpp_map_entries(self):
        cpp_map_entries = []
        cpp_map_entries.append("// C++ Signal Definition (example, adjust as needed):")
        cpp_map_entries.append("// struct SignalAttributes {")
        cpp_map_entries.append("//     double min_val;")
        cpp_map_entries.append("//     double max_val;")
        cpp_map_entries.append("//     bool is_signed;")
        cpp_map_entries.append("//     std::string comment;")
        cpp_map_entries.append("// };")
        cpp_map_entries.append("// std::map<std::string, SignalAttributes> signalMap = {")
        for msg in self._extracted_data:
            for sig in msg["signals"]:
                signal_name = sig["signal_name"]
                min_val = sig["minimum"]
                max_val = sig["maximum"]
                is_signed = "true" if sig["is_signed"] else "false"
                comments = sig["comments"].replace('"', '\\"')
                entry = (
                    f'    {{"{signal_name}", '
                    f'{{static_cast<double>({min_val}), static_cast<double>({max_val}), {is_signed}, "{comments}"}}'
                    f'}},'
                )
                cpp_map_entries.append(entry)
        cpp_map_entries.append("// };")
        return "\n".join(cpp_map_entries)

class ConverterWindow(QtWidgets.QWidget):
    """
    Main DBC viewer interface with error handling and improved readability.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.dbc_processor = DBCProcessor()
        self._full_data = []
        self._setup_ui()

    def _setup_ui(self):
        main_h_layout = QtWidgets.QHBoxLayout()
        left_v_layout = QtWidgets.QVBoxLayout()
        dbc_layout = QtWidgets.QHBoxLayout()
        self.dbc_label = QtWidgets.QLabel("DBC File:")
        self.dbc_line_edit = QtWidgets.QLineEdit()
        self.dbc_browse_btn = QtWidgets.QPushButton("Browse...")
        self.load_signals_btn = QtWidgets.QPushButton("Load Signals")
        
        # Set button icons
        self._set_button_icon(self.dbc_browse_btn, "icons/browse.ico")
        self._set_button_icon(self.load_signals_btn, "icons/load.ico")
        
        dbc_layout.addWidget(self.dbc_label)
        dbc_layout.addWidget(self.dbc_line_edit)
        dbc_layout.addWidget(self.dbc_browse_btn)
        dbc_layout.addWidget(self.load_signals_btn)
        left_v_layout.addLayout(dbc_layout)
        self.message_label = QtWidgets.QLabel("Status messages will appear here.")
        self.message_label.setAlignment(QtCore.Qt.AlignLeft)
        self.message_label.setWordWrap(True)
        self.message_label.setStyleSheet("font-weight: bold; color: #34495E;")
        left_v_layout.addWidget(self.message_label)
        left_v_layout.addSpacing(10)
        self.search_widget = UnifiedSearchWidget(self, mode="view")
        self.search_widget.search_edit.setPlaceholderText("Search messages, signals, or frame IDs...")
        self.search_widget.searchChanged.connect(self._apply_filter_to_tree)
        left_v_layout.addWidget(self.search_widget)
        self.tree_widget = QtWidgets.QTreeWidget()
        self.tree_widget.setHeaderLabels(["Key", "Value", "Type"])
        self.tree_widget.header().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.tree_widget.setAlternatingRowColors(True)
        left_v_layout.addWidget(self.tree_widget)
        main_h_layout.addLayout(left_v_layout, 2)
        right_v_layout = QtWidgets.QVBoxLayout()
        self.refresh_btn = QtWidgets.QPushButton("Refresh")
        self.refresh_btn.setStyleSheet("background-color: #3498db; color: white; border-radius: 5px; padding: 5px 10px;")
        self.refresh_btn.setFixedWidth(80)
        self.convert_to_map_btn = QtWidgets.QPushButton("Export to C++ Map")
        self.exitBtn = QtWidgets.QPushButton("Exit")
        self.exitBtn.setStyleSheet("background-color: #e74c3c; color: white; border-radius: 5px; padding: 5px 10px;")
        self.exitBtn.setFixedWidth(80)
        
        # Set button icons
        # self._set_button_icon(self.refresh_btn, "icons/refresh.ico")
        self._set_button_icon(self.convert_to_map_btn, "icons/convert.ico")
        self._set_button_icon(self.exitBtn, "icons/exit.ico")
        
        top_buttons_layout = QtWidgets.QHBoxLayout()
        top_buttons_layout.addStretch()
        top_buttons_layout.addWidget(self.refresh_btn)
        top_buttons_layout.addWidget(self.convert_to_map_btn)
        top_buttons_layout.addWidget(self.exitBtn)
        right_v_layout.addLayout(top_buttons_layout)
        self.details_widget = QtWidgets.QFrame()
        self.details_widget.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.details_widget.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.details_widget_layout = QtWidgets.QVBoxLayout(self.details_widget)
        self.details_title_label = QtWidgets.QLabel("Item Details")
        self.details_title_label.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Bold))
        self.details_title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.details_widget_layout.addWidget(self.details_title_label)
        self.details_text_edit = QtWidgets.QTextEdit()
        self.details_text_edit.setReadOnly(True)
        self.details_text_edit.setFont(QtGui.QFont("Monospace", 10))
        self.details_widget_layout.addWidget(self.details_text_edit)
        right_v_layout.addWidget(self.details_widget)
        main_h_layout.addLayout(right_v_layout, 1)
        self.setLayout(main_h_layout)
        self.dbc_browse_btn.clicked.connect(self.select_dbc_file)
        self.load_signals_btn.clicked.connect(self.load_and_display_signals)
        self.refresh_btn.clicked.connect(self.load_and_display_signals)
        self.convert_to_map_btn.clicked.connect(self.save_cpp_map_file)
        self.exitBtn.clicked.connect(self.parent().close)
        self.tree_widget.itemClicked.connect(self.display_item_details)

    def _set_button_icon(self, button, icon_path):
        """Set icon for a button if the icon file exists."""
        try:
            if os.path.exists(icon_path):
                icon = QtGui.QIcon(icon_path)
                button.setIcon(icon)
                # Set icon size
                button.setIconSize(QtCore.QSize(16, 16))
        except Exception as e:
            print(f"Could not load icon {icon_path}: {e}")

    def select_dbc_file(self):
        try:
            file_name, _ = QtWidgets.QFileDialog.getOpenFileName(
                self, "Select DBC File", "", "DBC Files (*.dbc);;All Files (*)"
            )
            if file_name:
                self.dbc_path = file_name
                self.dbc_line_edit.setText(file_name)
                self.message_label.setText("DBC file selected.")
                self.tree_widget.clear()
                self.details_text_edit.clear()
                self.details_title_label.setText("Item Details")
                self.search_widget.clear_search()
                self.dbc_processor._extracted_data = []
                self._full_data = []
        except Exception as e:
            self._show_error(f"Error selecting DBC file: {e}")

    def load_and_display_signals(self):
        if not hasattr(self, 'dbc_path') or not self.dbc_path:
            self._show_error("Please select a DBC file first.")
            return
        try:
            self.message_label.setText("Loading DBC file and extracting data...")
            self._full_data = self.dbc_processor.load_dbc_file(self.dbc_path)
            self._apply_filter_to_tree()
            self.message_label.setText("DBC file loaded and data displayed successfully.")
            self.details_text_edit.clear()
            self.details_title_label.setText("Item Details")
        except Exception as e:
            self._show_error(f"Error loading DBC file: {e}")

    def _apply_filter_to_tree(self, search_query="", filter_type="all"):
        try:
            if not self._full_data:
                self._populate_tree_widget([])
                return
            search_query_lower = search_query.lower().strip()
            filtered_results = []
            if not search_query_lower and filter_type == "all":
                filtered_results = list(self._full_data)
            else:
                for msg_data in self._full_data:
                    message_matches = False
                    signals_matching = []
                    if filter_type == "all" or filter_type == "message":
                        if search_query_lower in msg_data["message_name"].lower():
                            message_matches = True
                    if filter_type == "all" or filter_type == "frame_id":
                        if search_query_lower in str(hex(msg_data["frame_id"])).lower() or \
                           search_query_lower in str(msg_data["frame_id"]).lower():
                            message_matches = True
                    for sig_data in msg_data["signals"]:
                        signal_level_match = False
                        if filter_type == "all" or filter_type == "signal":
                            if (search_query_lower in sig_data["signal_name"].lower() or
                                search_query_lower in sig_data["comments"].lower() or
                                search_query_lower in ",".join(sig_data["receivers"]).lower() or
                                search_query_lower in str(sig_data.get("minimum", "")).lower() or
                                search_query_lower in str(sig_data.get("maximum", "")).lower()):
                                signal_level_match = True
                        if filter_type == "frame_id" and (search_query_lower in str(hex(msg_data["frame_id"])).lower() or \
                                                          search_query_lower in str(msg_data["frame_id"]).lower()):
                            if not search_query_lower or signal_level_match:
                                signals_matching.append(sig_data)
                        elif signal_level_match:
                            signals_matching.append(sig_data)
                    if message_matches:
                        filtered_results.append(msg_data)
                    elif signals_matching:
                        temp_msg_data = msg_data.copy()
                        temp_msg_data["signals"] = signals_matching
                        filtered_results.append(temp_msg_data)
            self._populate_tree_widget(filtered_results)
        except Exception as e:
            self._show_error(f"Error filtering data: {e}")

    def _populate_tree_widget(self, data):
        self.tree_widget.clear()
        if not data:
            item = QtWidgets.QTreeWidgetItem(self.tree_widget)
            item.setText(0, "No matching data found.")
            return
        for msg_data in data:
            msg_item = QtWidgets.QTreeWidgetItem(self.tree_widget)
            msg_item.setText(0, msg_data["message_name"])
            msg_item.setText(1, f"Frame ID: {hex(msg_data['frame_id'])}")
            msg_item.setText(2, "Message")
            msg_item.setData(0, QtCore.Qt.UserRole, msg_data)
            senders_item = QtWidgets.QTreeWidgetItem(msg_item)
            senders_item.setText(0, "Senders")
            senders_item.setText(1, ", ".join(msg_data["senders"]))
            senders_item.setText(2, "List")
            senders_item.setData(0, QtCore.Qt.UserRole, {"Type": "Senders List", "Senders": msg_data["senders"]})
            signals_root_item = QtWidgets.QTreeWidgetItem(msg_item)
            signals_root_item.setText(0, "Signals")
            signals_root_item.setText(2, "Collection")
            for sig_data in msg_data["signals"]:
                sig_item = QtWidgets.QTreeWidgetItem(signals_root_item)
                sig_item.setText(0, sig_data["signal_name"])
                sig_item.setText(2, "Signal")
                sig_item.setData(0, QtCore.Qt.UserRole, sig_data)
                for key, value in sig_data.items():
                    attr_item = QtWidgets.QTreeWidgetItem(sig_item)
                    attr_item.setText(0, key.replace('_', ' ').title())
                    if key == "comments":
                        displayed_comment = str(value)
                        if len(displayed_comment) > 50:
                            displayed_comment = displayed_comment[:50] + "..."
                        attr_item.setText(1, displayed_comment)
                    else:
                        attr_item.setText(1, str(value))
                    attr_item.setText(2, type(value).__name__)
        self.tree_widget.expandAll()

    def display_item_details(self, item, column):
        try:
            item_data = item.data(0, QtCore.Qt.UserRole)
            details_html = []
            # Set the title label appropriately
            if item_data:
                if "message_name" in item_data:
                    self.details_title_label.setText(f"Message: {item_data['message_name']}")
                    details_html.append("<div style='background-color:#f7fafc; border-radius:8px; padding:18px 18px 10px 18px; margin-bottom:10px; border:1px solid #e0e0e0;'>")
                    details_html.append(f"<div style='margin-bottom:8px;'><b>Frame ID:</b> <span style='color:#E67E22;'>{hex(item_data['frame_id'])}</span></div>")
                    details_html.append(f"<div style='margin-bottom:8px;'><b>Senders:</b> <span style='color:#2980B9;'>{', '.join(item_data['senders'])}</span></div>")
                    if item_data.get('comments'):
                        details_html.append(f"<div style='margin-bottom:8px;'><b>Comments:</b> <span style='color:#888;'>{item_data['comments']}</span></div>")
                    details_html.append("</div>")
                    if item_data["signals"]:
                        details_html.append("<div style='margin-top:18px;'><span style='font-size:14pt; color:#2C3E50; font-weight:bold;'>Signals</span></div>")
                        for sig in item_data["signals"]:
                            details_html.append("<div style='background-color:#f0f4f8; border-radius:6px; padding:10px 12px; margin:10px 0 10px 0; border-left: 4px solid #3498DB;'>")
                            details_html.append(f"<div style='font-size:12pt; color:#16A085; font-weight:bold;'>{sig['signal_name']}</div>")
                            if sig.get('comments'):
                                details_html.append(f"<div style='margin-bottom:4px; color:#888;'><b>Comments:</b> {sig['comments']}</div>")
                            details_html.append(f"<div><b>Receivers:</b> {', '.join(sig['receivers'])}</div>")
                            details_html.append(f"<div><b>Is Signed:</b> {sig['is_signed']}</div>")
                            details_html.append(f"<div><b>Minimum:</b> {sig['minimum']}</div>")
                            details_html.append(f"<div><b>Maximum:</b> {sig['maximum']}</div>")
                            details_html.append("</div>")
                    else:
                        details_html.append("<div style='font-style:italic; color:#7F8C8D; margin-top:10px;'>No signals for this message.</div>")
                elif "signal_name" in item_data:
                    self.details_title_label.setText(f"Signal: {item_data['signal_name']}")
                    details_html.append("<div style='background-color:#f7fafc; border-radius:8px; padding:18px 18px 10px 18px; margin-bottom:10px; border:1px solid #e0e0e0;'>")
                    for key, value in item_data.items():
                        if isinstance(value, list):
                            details_html.append(f"<div style='margin-bottom:8px;'><b>{key.replace('_', ' ').title()}:</b> {', '.join(map(str, value))}</div>")
                        else:
                            details_html.append(f"<div style='margin-bottom:8px;'><b>{key.replace('_', ' ').title()}:</b> {value}</div>")
                    details_html.append("</div>")
                elif "Type" in item_data and item_data["Type"] == "Senders List":
                    self.details_title_label.setText("Senders List")
                    details_html.append("<div style='background-color:#f7fafc; border-radius:8px; padding:18px; border:1px solid #e0e0e0;'>")
                    details_html.append(f"<div><b>Senders:</b> {', '.join(item_data['Senders'])}</div>")
                    details_html.append("</div>")
                else:
                    self.details_title_label.setText("Item Details")
                    details_html.append("<div style='text-align:center; color:#7F8C8D;'><i>Select an item from the tree to view its details.</i></div>")
            else:
                self.details_title_label.setText("Item Details")
                details_html.append("<div style='text-align:center; color:#7F8C8D;'><i>Select an item from the tree to view its details.</i></div>")
            self.details_text_edit.setHtml("".join(details_html))
        except Exception as e:
            self._show_error(f"Error displaying item details: {e}")

    def save_cpp_map_file(self):
        if not self.dbc_processor.get_extracted_data():
            self._show_error("No data loaded to convert. Please load a DBC file first.")
            return
        cpp_content = self.dbc_processor.convert_to_cpp_map_entries()
        try:
            file_name, _ = QtWidgets.QFileDialog.getSaveFileName(
                self, "Save C++ Map File", "signal_map.txt", "Text Files (*.txt);;All Files (*)"
            )
            if file_name:
                with open(file_name, 'w') as f:
                    f.write(cpp_content)
                self.message_label.setText(f"C++ map entries saved to: <font color='green'>{file_name}</font>")
        except Exception as e:
            self._show_error(f"Error saving file: {e}")

    def _show_error(self, message):
        QtWidgets.QMessageBox.critical(self, "Error", message)
        self.message_label.setText(f"<font color='red'>{message}</font>")

class MainWindow(QtWidgets.QMainWindow):
    APP_NAME = "CAN DBC Utility"
    APP_VERSION = "v1.1"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(self.APP_NAME)
        self.resize(1200, 750)
        self.setStyleSheet("QMainWindow { border: 1px solid lightgray; }")

        # Set application icon
        self._set_app_icon()

        self.tab_widget = QtWidgets.QTabWidget()
        self.setCentralWidget(self.tab_widget)

        self.view_dbc_page = ConverterWindow(self)
        self.edit_dbc_page = DBCEditorWidget(self)
        self.view_can_bus_page = EmptyWidget("Coming Soon: CAN Bus Viewer.")

        # Add tabs with icons
        self.tab_widget.addTab(self.view_dbc_page, self._get_tab_icon("icons/view.ico"), "View DBC")
        self.tab_widget.addTab(self.edit_dbc_page, self._get_tab_icon("icons/edit.ico"), "Edit DBC")
        self.tab_widget.addTab(self.view_can_bus_page, self._get_tab_icon("icons/can_bus.ico"), "CAN Bus Viewer")

        self._create_status_bar()

    def _set_app_icon(self):
        """Set the application icon if the icon file exists."""
        try:
            icon_path = "icons/app_icon.png"
            if os.path.exists(icon_path):
                icon = QtGui.QIcon(icon_path)
                self.setWindowIcon(icon)
                # Set for the application to appear in taskbar
                QtWidgets.QApplication.setWindowIcon(icon)
                # Also set for the application instance
                app = QtWidgets.QApplication.instance()
                if app:
                    app.setWindowIcon(icon)
        except Exception as e:
            print(f"Could not load application icon {icon_path}: {e}")

    def _get_tab_icon(self, icon_path):
        """Get icon for tab if the icon file exists."""
        try:
            if os.path.exists(icon_path):
                return QtGui.QIcon(icon_path)
        except Exception as e:
            print(f"Could not load tab icon {icon_path}: {e}")
        return QtGui.QIcon()  # Return empty icon if file doesn't exist

    def _create_status_bar(self):
        status_bar = self.statusBar()
        app_name_label = QtWidgets.QLabel(f"{self.APP_NAME}")
        app_version_label = QtWidgets.QLabel(f"Version: {self.APP_VERSION}")
        status_bar.addWidget(app_name_label)
        status_bar.addPermanentWidget(app_version_label)
        status_bar.setStyleSheet("QStatusBar{padding-left:8px;background:#f0f0f0;color:black;}")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    
    # Set application icon early for taskbar
    try:
        icon_path = "icons/app_icon.png"
        if os.path.exists(icon_path):
            icon = QtGui.QIcon(icon_path)
            app.setWindowIcon(icon)
    except Exception as e:
        print(f"Could not load application icon {icon_path}: {e}")
    
    main_window = MainWindow() # Create an instance of MainWindow
    main_window.show()
    sys.exit(app.exec_())