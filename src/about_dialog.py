#!/usr/bin/env python3
"""
About dialog for DBC Utility.
"""

from __future__ import annotations

import os
from typing import Optional

from PyQt5 import QtCore, QtGui, QtWidgets

from resource_utils import get_resource_path


class AboutDialog(QtWidgets.QDialog):
    def __init__(
        self,
        *,
        app_name: str,
        app_version: str,
        description: Optional[str] = None,
        creator: str,
        website: Optional[str] = None,
        github: Optional[str] = None,
        parent: Optional[QtWidgets.QWidget] = None,
    ) -> None:
        super().__init__(parent)
        self.setWindowTitle("About")
        self.setModal(True)
        self.setMinimumWidth(420)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 14)
        layout.setSpacing(12)

        header = QtWidgets.QHBoxLayout()
        header.setSpacing(12)

        icon_label = QtWidgets.QLabel()
        icon_label.setFixedSize(64, 64)
        icon_label.setAlignment(QtCore.Qt.AlignCenter)
        icon_path = get_resource_path("icons/app_icon.png")
        if os.path.exists(icon_path):
            pix = QtGui.QPixmap(icon_path)
            if not pix.isNull():
                icon_label.setPixmap(
                    pix.scaled(64, 64, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
                )

        title_col = QtWidgets.QVBoxLayout()
        title_col.setSpacing(2)

        name_label = QtWidgets.QLabel(app_name)
        name_font = name_label.font()
        name_font.setBold(True)
        name_font.setPointSize(max(12, name_font.pointSize() + 4))
        name_label.setFont(name_font)

        version_label = QtWidgets.QLabel(f"Version: {app_version}")

        title_col.addWidget(name_label)
        if description:
            desc_label = QtWidgets.QLabel(description)
            desc_label.setWordWrap(True)
            title_col.addWidget(desc_label)
        title_col.addWidget(version_label)
        title_col.addStretch()

        header.addWidget(icon_label)
        header.addLayout(title_col, 1)
        layout.addLayout(header)

        grid = QtWidgets.QFormLayout()
        grid.setLabelAlignment(QtCore.Qt.AlignLeft)
        grid.setFormAlignment(QtCore.Qt.AlignTop)

        creator_label = QtWidgets.QLabel(creator)
        grid.addRow("Created by:", creator_label)

        if website:
            website_label = QtWidgets.QLabel(f'<a href="{website}">{website}</a>')
            website_label.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
            website_label.setOpenExternalLinks(True)
            grid.addRow("Website:", website_label)
        else:
            grid.addRow("Website:", QtWidgets.QLabel("—"))

        if github:
            github_label = QtWidgets.QLabel(f'<a href="{github}">{github}</a>')
            github_label.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
            github_label.setOpenExternalLinks(True)
            grid.addRow("GitHub:", github_label)
        else:
            grid.addRow("GitHub:", QtWidgets.QLabel("—"))

        layout.addLayout(grid)

        buttons = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok)
        buttons.accepted.connect(self.accept)
        layout.addWidget(buttons)


