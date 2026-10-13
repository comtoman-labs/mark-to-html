"""
MarkToHTML - Left File Explorer Component
Provides directory navigation and markdown file selection with filtering and drag-and-drop.
"""

import os
from PySide6.QtCore import Qt, Signal, QDir, QModelIndex, QSortFilterProxyModel
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QTreeView, QFileDialog, QFrame, QCheckBox,
    QFileSystemModel
)


class MarkdownFileFilterProxyModel(QSortFilterProxyModel):
    """Filters tree items to optionally only show Markdown files and folders."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.md_only = True
        self.search_text = ""
        self.md_extensions = {".md", ".markdown", ".mdown", ".mkd"}

    def set_md_only(self, enabled: bool):
        self.md_only = enabled
        self.invalidateFilter()

    def set_search_text(self, text: str):
        self.search_text = text.lower().strip()
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row: int, source_parent: QModelIndex) -> bool:
        source_model: QFileSystemModel = self.sourceModel()
        index = source_model.index(source_row, 0, source_parent)
        file_path = source_model.filePath(index)
        file_name = source_model.fileName(index).lower()

        # Always accept directories so the user can navigate folders
        if source_model.isDir(index):
            return True

        # Search filter
        if self.search_text and self.search_text not in file_name:
            return False

        # Extension filter
        if self.md_only:
            ext = os.path.splitext(file_name)[1]
            return ext in self.md_extensions

        return True


class FileExplorerWidget(QWidget):
    """Sidebar file explorer widget for browsing directories and picking MD files."""
    
    file_selected = Signal(str)      # Emits absolute file path
    folder_changed = Signal(str)     # Emits current root folder path

    def __init__(self, initial_path: str = None, parent=None):
        super().__init__(parent)
        self.current_folder = initial_path or os.getcwd()
        self.setAcceptDrops(True)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 1. Header Frame
        header_frame = QFrame()
        header_frame.setObjectName("panelHeader")
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(12, 10, 12, 10)
        header_layout.setSpacing(8)

        # Title & Open Folder Button row
        top_row = QHBoxLayout()
        top_row.setSpacing(8)

        self.title_label = QLabel("📂 파일 탐색기")
        self.title_label.setObjectName("panelTitle")
        top_row.addWidget(self.title_label)

        top_row.addStretch()

        self.btn_open_folder = QPushButton("폴더 열기")
        self.btn_open_folder.setToolTip("탐색할 폴더를 선택합니다 (Ctrl+O)")
        self.btn_open_folder.clicked.connect(self._on_choose_folder)
        top_row.addWidget(self.btn_open_folder)

        self.btn_refresh = QPushButton("새로고침")
        self.btn_refresh.setToolTip("파일 목록 새로고침 (F5)")
        self.btn_refresh.clicked.connect(self.refresh)
        top_row.addWidget(self.btn_refresh)

        header_layout.addLayout(top_row)

        # Current Folder Path label
        self.path_label = QLabel(self._shorten_path(self.current_folder))
        self.path_label.setToolTip(self.current_folder)
        self.path_label.setStyleSheet("color: #9ca3af; font-size: 11px;")
        header_layout.addWidget(self.path_label)

        # Search Bar & Filter Options
        search_row = QHBoxLayout()
        search_row.setSpacing(8)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 파일 검색...")
        self.search_input.textChanged.connect(self._on_search_changed)
        search_row.addWidget(self.search_input)

        self.chk_md_only = QCheckBox("MD만")
        self.chk_md_only.setChecked(True)
        self.chk_md_only.setToolTip("체크 시 마크다운(.md) 파일만 표시합니다")
        self.chk_md_only.toggled.connect(self._on_filter_toggled)
        self.chk_md_only.setStyleSheet("color: #cbd5e1; font-size: 12px;")
        search_row.addWidget(self.chk_md_only)

        header_layout.addLayout(search_row)
        layout.addWidget(header_frame, 0)

        # 2. File Tree View
        self.file_model = QFileSystemModel()
        self.file_model.setRootPath(self.current_folder)
        self.file_model.setFilter(QDir.AllDirs | QDir.Files | QDir.NoDotAndDotDot)

        self.proxy_model = MarkdownFileFilterProxyModel(self)
        self.proxy_model.setSourceModel(self.file_model)

        self.tree_view = QTreeView()
        self.tree_view.setModel(self.proxy_model)
        self.tree_view.setRootIndex(self.proxy_model.mapFromSource(self.file_model.index(self.current_folder)))
        
        # Column styling (0: Name, 1: Size, 2: Type, 3: Date)
        self.tree_view.setColumnWidth(0, 210)
        self.tree_view.setColumnWidth(1, 70)
        self.tree_view.setColumnHidden(2, True)  # Hide Type
        self.tree_view.setColumnHidden(3, True)  # Hide Date for compact sidebar look
        
        self.tree_view.setAnimated(True)
        self.tree_view.setIndentation(16)
        self.tree_view.setSortingEnabled(True)
        self.tree_view.sortByColumn(0, Qt.AscendingOrder)
        self.tree_view.setHeaderHidden(False)

        # Selection signals
        self.tree_view.clicked.connect(self._on_item_clicked)
        self.tree_view.doubleClicked.connect(self._on_item_clicked)
        self.tree_view.selectionModel().currentChanged.connect(self._on_item_clicked)

        layout.addWidget(self.tree_view, 1)

    def _shorten_path(self, path: str, max_len: int = 38) -> str:
        if len(path) <= max_len:
            return path
        return "..." + path[-(max_len - 3):]

    def set_root_folder(self, folder_path: str):
        """Changes the root directory of the explorer."""
        if not os.path.isdir(folder_path):
            return
        
        self.current_folder = os.path.abspath(folder_path)
        self.path_label.setText(self._shorten_path(self.current_folder))
        self.path_label.setToolTip(self.current_folder)
        
        source_idx = self.file_model.setRootPath(self.current_folder)
        proxy_idx = self.proxy_model.mapFromSource(source_idx)
        self.tree_view.setRootIndex(proxy_idx)
        self.folder_changed.emit(self.current_folder)

    def refresh(self):
        """Reloads file system model."""
        self.set_root_folder(self.current_folder)

    def _on_choose_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self, "탐색할 폴더 선택", self.current_folder
        )
        if folder:
            self.set_root_folder(folder)

    def _on_search_changed(self, text: str):
        self.proxy_model.set_search_text(text)

    def _on_filter_toggled(self, checked: bool):
        self.proxy_model.set_md_only(checked)

    def _on_item_clicked(self, proxy_index: QModelIndex, *args):
        if not proxy_index.isValid():
            return
        source_index = self.proxy_model.mapToSource(proxy_index)
        if not source_index.isValid():
            return
        
        file_path = self.file_model.filePath(source_index)
        if os.path.isfile(file_path):
            ext = os.path.splitext(file_path)[1].lower()
            if ext in {".md", ".markdown", ".mdown", ".mkd", ".txt"}:
                self.file_selected.emit(os.path.abspath(file_path))

    # Drag & Drop Support
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if not urls:
            return
        
        first_path = urls[0].toLocalFile()
        if os.path.isdir(first_path):
            self.set_root_folder(first_path)
        elif os.path.isfile(first_path):
            parent_dir = os.path.dirname(first_path)
            self.set_root_folder(parent_dir)
            ext = os.path.splitext(first_path)[1].lower()
            if ext in {".md", ".markdown", ".mdown", ".mkd", ".txt"}:
                self.file_selected.emit(os.path.abspath(first_path))
        event.acceptProposedAction()
