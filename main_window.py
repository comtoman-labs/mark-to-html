"""
MarkToHTML - Main Application Window
Coordinates FileExplorerWidget and WebPreviewerWidget in a responsive split layout.
"""

import os
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow, QSplitter, QStatusBar, QLabel
)
from PySide6.QtGui import QKeySequence, QShortcut

from explorer import FileExplorerWidget
from previewer import WebPreviewerWidget
from styles import APP_DARK_QSS


class MainWindow(QMainWindow):
    """Main application window for MarkToHTML."""

    def __init__(self, start_dir: str = None):
        super().__init__()
        self.setWindowTitle("MarkToHTML - 마크다운 웹 뷰어 & HTML 변환기")
        self.resize(1280, 820)
        self.setMinimumSize(800, 500)
        
        # Apply Dark Style
        self.setStyleSheet(APP_DARK_QSS)

        # Default workspace folder
        self.start_dir = start_dir or os.path.dirname(os.path.abspath(__file__))

        self._init_ui()
        self._setup_shortcuts()

        # Load initial sample if available
        sample_file = os.path.join(self.start_dir, "sample_documents", "01_시작하기.md")
        if os.path.isfile(sample_file):
            self.previewer.load_file(sample_file)

    def _init_ui(self):
        # Splitter Layout
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.setHandleWidth(2)

        # Left: File Explorer
        self.explorer = FileExplorerWidget(initial_path=self.start_dir)
        self.splitter.addWidget(self.explorer)

        # Right: Web Previewer
        self.previewer = WebPreviewerWidget()
        self.splitter.addWidget(self.previewer)

        # Splitter Ratios (Left sidebar: 280px, Right web view: expands)
        self.splitter.setStretchFactor(0, 0)
        self.splitter.setStretchFactor(1, 1)
        self.splitter.setSizes([280, 1600])

        self.setCentralWidget(self.splitter)

        # Status Bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.status_info = QLabel("🚀 준비 완료 | 좌측에서 마크다운(.md) 파일을 선택하세요.")
        self.status_bar.addWidget(self.status_info)

        # Signal Connections
        self.explorer.file_selected.connect(self.previewer.load_file)
        self.explorer.folder_changed.connect(self._on_folder_changed)
        self.previewer.status_message.connect(self._on_status_message)
        self.previewer.file_dropped.connect(self._on_file_dropped)

    def _setup_shortcuts(self):
        """Configures handy desktop shortcuts."""
        # Ctrl+O: Open folder
        sc_open = QShortcut(QKeySequence("Ctrl+O"), self)
        sc_open.activated.connect(self.explorer._on_choose_folder)

        # Ctrl+S: Save Markdown (in edit mode) or Export HTML (in preview mode)
        sc_save = QShortcut(QKeySequence("Ctrl+S"), self)
        sc_save.activated.connect(self._on_save_shortcut)

        # Ctrl+E: Toggle Edit Mode
        sc_edit = QShortcut(QKeySequence("Ctrl+E"), self)
        sc_edit.activated.connect(self.previewer._on_toggle_edit)

        # Esc: Cancel edit mode if editing
        sc_esc = QShortcut(QKeySequence("Esc"), self)
        sc_esc.activated.connect(self._on_esc_shortcut)

        # Ctrl+B: Open in browser
        sc_browser = QShortcut(QKeySequence("Ctrl+B"), self)
        sc_browser.activated.connect(self.previewer._on_open_browser)

        # F5 or Ctrl+R: Refresh current file & tree
        sc_refresh1 = QShortcut(QKeySequence("F5"), self)
        sc_refresh1.activated.connect(self._on_refresh)

        sc_refresh2 = QShortcut(QKeySequence("Ctrl+R"), self)
        sc_refresh2.activated.connect(self._on_refresh)

    def _on_save_shortcut(self):
        if self.previewer.is_editing:
            self.previewer.save_editor_content()
        else:
            self.previewer._on_save_html()

    def _on_esc_shortcut(self):
        if self.previewer.is_editing:
            self.previewer._on_cancel_edit()

    def _on_folder_changed(self, folder_path: str):
        self.status_info.setText(f"📂 폴더 열림: {folder_path}")

    def _on_status_message(self, message: str):
        self.status_info.setText(message)

    def _on_file_dropped(self, file_path: str):
        # Ensure explorer navigates near this file
        parent_dir = os.path.dirname(file_path)
        self.explorer.set_root_folder(parent_dir)

    def _on_refresh(self):
        self.explorer.refresh()
        self.previewer.reload_current_file()
        self.status_info.setText("🔄 새로고침 완료")
