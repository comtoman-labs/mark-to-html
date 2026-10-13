"""
MarkToHTML - Application Styles & Themes
Modern Dark QSS for PySide6 Desktop Interface.
"""

APP_DARK_QSS = """
/* Global Window & Fonts */
QWidget {
    font-family: "Pretendard", "Segoe UI", -apple-system, sans-serif;
    font-size: 10pt;
    color: #e1e4e8;
    background-color: #1e1e24;
}

/* Main Splitter */
QSplitter::handle {
    background-color: #2b2d38;
    width: 2px;
}
QSplitter::handle:hover {
    background-color: #3b82f6;
    width: 4px;
}

/* Headers & Panels */
QFrame#panelHeader {
    background-color: #252733;
    border-bottom: 1px solid #303342;
    padding: 2px 8px;
}

QLabel#panelTitle {
    font-size: 13px;
    font-weight: 700;
    color: #f3f4f6;
    letter-spacing: 0.5px;
}

QLabel#badgeLabel {
    background-color: #242938;
    color: #60a5fa;
    border: 1px solid #3b82f6;
    border-radius: 6px;
    padding: 2px 10px;
    font-weight: 600;
    font-size: 12px;
}

/* Push Buttons */
QPushButton {
    background-color: #2d3142;
    border: 1px solid #3d4257;
    border-radius: 6px;
    color: #f3f4f6;
    padding: 4px 10px;
    font-weight: 500;
    font-size: 12px;
}
QPushButton:hover {
    background-color: #383c50;
    border-color: #4b526d;
}
QPushButton:pressed {
    background-color: #232634;
}

/* Primary Action Buttons */
QPushButton#primaryButton {
    background-color: #2563eb;
    border: 1px solid #3b82f6;
    color: #ffffff;
    font-weight: 600;
}
QPushButton#primaryButton:hover {
    background-color: #1d4ed8;
    border-color: #60a5fa;
}
QPushButton#primaryButton:pressed {
    background-color: #1e40af;
}

/* Success / Export Buttons */
QPushButton#exportButton {
    background-color: #15803d;
    border: 1px solid #22c55e;
    color: #ffffff;
    font-weight: 600;
}
QPushButton#exportButton:hover {
    background-color: #166534;
    border-color: #4ade80;
}
QPushButton#exportButton:pressed {
    background-color: #14532d;
}

/* Edit & Save Mode Buttons */
QPushButton#editButton {
    background-color: #1e3a8a;
    border: 1px solid #3b82f6;
    color: #ffffff;
    font-weight: 600;
}
QPushButton#editButton:hover {
    background-color: #2563eb;
    border-color: #60a5fa;
}

QPushButton#saveButtonActive {
    background-color: #16a34a;
    border: 1px solid #22c55e;
    color: #ffffff;
    font-weight: 700;
}
QPushButton#saveButtonActive:hover {
    background-color: #15803d;
    border-color: #4ade80;
}

QPushButton#cancelButton {
    background-color: #374151;
    border: 1px solid #4b5563;
    color: #e5e7eb;
}
QPushButton#cancelButton:hover {
    background-color: #4b5563;
    color: #ffffff;
}

/* Markdown Source Code Editor */
QPlainTextEdit#markdownEditor {
    background-color: #1e1e20;
    color: #e4e4e7;
    border: none;
    font-family: "Cascadia Code", "Consolas", "SF Mono", "Fira Code", monospace;
    font-size: 14px;
    padding: 16px 20px;
    selection-background-color: #264f78;
    selection-color: #ffffff;
}

/* Line Edit / Search Input */
QLineEdit {
    background-color: #181920;
    border: 1px solid #303342;
    border-radius: 6px;
    padding: 6px 10px;
    color: #f3f4f6;
    font-size: 12px;
}
QLineEdit:focus {
    border-color: #3b82f6;
    background-color: #1c1e27;
}

/* ComboBox */
QComboBox {
    background-color: #252733;
    border: 1px solid #3d4257;
    border-radius: 6px;
    padding: 5px 12px;
    color: #f3f4f6;
    font-size: 12px;
    min-width: 110px;
}
QComboBox:hover {
    border-color: #4b526d;
}
QComboBox::drop-down {
    border: none;
    width: 20px;
}
QComboBox QAbstractItemView {
    background-color: #252733;
    border: 1px solid #3d4257;
    selection-background-color: #3b82f6;
    selection-color: #ffffff;
    color: #f3f4f6;
    padding: 4px;
}

/* TreeView (File Explorer) */
QTreeView {
    background-color: #181920;
    border: none;
    color: #e1e4e8;
    font-size: 13px;
    outline: none;
}
QTreeView::item {
    height: 28px;
    padding: 2px 4px;
    border-radius: 4px;
}
QTreeView::item:hover {
    background-color: #252733;
}
QTreeView::item:selected {
    background-color: #1e3a8a;
    color: #ffffff;
}
QTreeView::branch:has-children:!has-siblings:closed,
QTreeView::branch:closed:has-children:has-siblings {
    border-image: none;
}

QHeaderView::section {
    background-color: #20222c;
    color: #9ca3af;
    padding: 5px;
    border: none;
    border-bottom: 1px solid #303342;
    font-weight: 600;
    font-size: 11px;
}

/* Status Bar */
QStatusBar {
    background-color: #181920;
    color: #9ca3af;
    border-top: 1px solid #282a36;
    font-size: 12px;
    padding: 4px 8px;
}
QStatusBar QLabel {
    color: #9ca3af;
    background: transparent;
}

/* Scrollbars */
QScrollBar:vertical {
    border: none;
    background: #181920;
    width: 8px;
    margin: 0px;
}
QScrollBar::handle:vertical {
    background: #343746;
    min-height: 20px;
    border-radius: 4px;
}
QScrollBar::handle:vertical:hover {
    background: #4b526d;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
QScrollBar:horizontal {
    border: none;
    background: #181920;
    height: 8px;
    margin: 0px;
}
QScrollBar::handle:horizontal {
    background: #343746;
    min-width: 20px;
    border-radius: 4px;
}
QScrollBar::handle:horizontal:hover {
    background: #4b526d;
}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}

/* Tooltip */
QToolTip {
    background-color: #2d3142;
    color: #ffffff;
    border: 1px solid #4b526d;
    padding: 6px 10px;
    border-radius: 4px;
    font-size: 12px;
}
"""
