"""
MarkToHTML - Right Web Previewer Component
Embeds QWebEngineView to render converted Markdown HTML with theme switcher,
export tools, and a toggleable raw Markdown source editor.
"""

import os
import tempfile
import time
from PySide6.QtCore import Qt, Signal, QUrl, QTimer
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QFileDialog, QFrame, QMessageBox, QApplication,
    QStackedWidget, QPlainTextEdit
)
from PySide6.QtGui import QDesktopServices
from PySide6.QtWebEngineWidgets import QWebEngineView

from converter import convert_markdown_to_html, get_empty_placeholder_html, THEMES


class WebPreviewerWidget(QWidget):
    """Right-pane widget with live HTML preview and raw Markdown editor."""

    status_message = Signal(str)      # Emits status bar text
    file_dropped = Signal(str)        # Emits path when a file is dropped here

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_file_path = None
        self.current_raw_md = ""
        self.current_theme = "Modern Charcoal (모던 차콜)"
        self.current_html = ""
        self.is_editing = False
        self.setAcceptDrops(True)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 1. Header Frame (Compact Toolbar)
        header_frame = QFrame()
        header_frame.setObjectName("panelHeader")
        header_frame.setFixedHeight(48)
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(12, 4, 12, 4)
        header_layout.setSpacing(8)
        header_layout.setAlignment(Qt.AlignVCenter)

        # Active File Badge
        self.file_badge = QLabel("선택된 파일 없음")
        self.file_badge.setObjectName("badgeLabel")
        self.file_badge.setFixedHeight(28)
        self.file_badge.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.file_badge.setToolTip("현재 미리보기 중인 파일")
        header_layout.addWidget(self.file_badge)

        # Edit / Save Toggle Button
        self.btn_edit_toggle = QPushButton("✏️ 편집")
        self.btn_edit_toggle.setObjectName("editButton")
        self.btn_edit_toggle.setFixedHeight(28)
        self.btn_edit_toggle.setToolTip("마크다운 원본 소스코드를 직접 편집합니다")
        self.btn_edit_toggle.clicked.connect(self._on_toggle_edit)
        header_layout.addWidget(self.btn_edit_toggle)

        # Cancel Edit Button (hidden initially)
        self.btn_cancel_edit = QPushButton("취소")
        self.btn_cancel_edit.setObjectName("cancelButton")
        self.btn_cancel_edit.setFixedHeight(28)
        self.btn_cancel_edit.setToolTip("편집을 취소하고 원래 미리보기로 돌아갑니다")
        self.btn_cancel_edit.clicked.connect(self._on_cancel_edit)
        self.btn_cancel_edit.hide()
        header_layout.addWidget(self.btn_cancel_edit)

        header_layout.addStretch()

        # Theme Selector
        self.theme_label = QLabel("🎨 테마:")
        self.theme_label.setStyleSheet("color: #9ca3af; font-size: 12px;")
        header_layout.addWidget(self.theme_label)

        self.theme_combo = QComboBox()
        self.theme_combo.setFixedHeight(28)
        self.theme_combo.addItems(list(THEMES.keys()))
        self.theme_combo.setCurrentText(self.current_theme)
        self.theme_combo.currentTextChanged.connect(self._on_theme_changed)
        header_layout.addWidget(self.theme_combo)

        # Style Config Button
        self.btn_open_config = QPushButton("⚙️ 설정")
        self.btn_open_config.setFixedHeight(28)
        self.btn_open_config.setToolTip("style_config.json 설정 파일을 메모장 등으로 열어 글자 크기/색상을 직접 편집합니다")
        self.btn_open_config.clicked.connect(self._on_open_config)
        header_layout.addWidget(self.btn_open_config)

        # Action Buttons
        self.btn_copy_html = QPushButton("📋 HTML 복사")
        self.btn_copy_html.setFixedHeight(28)
        self.btn_copy_html.setToolTip("변환된 HTML 코드를 클립보드에 복사합니다")
        self.btn_copy_html.clicked.connect(self._on_copy_html)
        header_layout.addWidget(self.btn_copy_html)

        self.btn_open_browser = QPushButton("🌐 브라우저 열기")
        self.btn_open_browser.setFixedHeight(28)
        self.btn_open_browser.setToolTip("기본 웹 브라우저(Edge, Chrome 등)에서 엽니다 (Ctrl+B)")
        self.btn_open_browser.clicked.connect(self._on_open_browser)
        header_layout.addWidget(self.btn_open_browser)

        self.btn_save_html = QPushButton("💾 HTML로 저장")
        self.btn_save_html.setObjectName("exportButton")
        self.btn_save_html.setFixedHeight(28)
        self.btn_save_html.setToolTip("완결형 단일 HTML 파일로 저장합니다")
        self.btn_save_html.clicked.connect(self._on_save_html)
        header_layout.addWidget(self.btn_save_html)

        layout.addWidget(header_frame, 0)

        # 2. Stacked Content (Page 0: WebEngineView, Page 1: Source Editor)
        self.stack = QStackedWidget()

        # Page 0: Chromium WebEngineView
        self.web_view = QWebEngineView()
        self.web_view.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.stack.addWidget(self.web_view)

        # Page 1: Raw Markdown Editor
        self.source_editor = QPlainTextEdit()
        self.source_editor.setObjectName("markdownEditor")
        self.source_editor.setPlaceholderText("여기에 마크다운 내용을 입력하세요...")
        self.stack.addWidget(self.source_editor)

        layout.addWidget(self.stack, 1)

        # Initial Welcome Screen
        self._show_placeholder()

    def _show_placeholder(self):
        """Displays welcome placeholder screen."""
        self.current_html = get_empty_placeholder_html(self.current_theme)
        self.current_raw_md = ""
        self._set_edit_mode_ui(False)
        self.web_view.setHtml(self.current_html)
        self.file_badge.setText("선택된 파일 없음")
        self.file_badge.setToolTip("")

    def _set_edit_mode_ui(self, editing: bool):
        """Toggles header UI and stack view between preview and edit mode."""
        self.is_editing = editing
        if editing:
            self.btn_edit_toggle.setText("💾 저장")
            self.btn_edit_toggle.setObjectName("saveButtonActive")
            self.btn_edit_toggle.setToolTip("수정된 마크다운을 저장하고 웹 뷰어로 돌아갑니다 (Ctrl+S)")
            self.btn_cancel_edit.show()
            self.stack.setCurrentIndex(1)
            self.source_editor.setFocus()
            if self.current_file_path:
                self.file_badge.setText(f"✏️ {os.path.basename(self.current_file_path)} [편집 중]")
        else:
            self.btn_edit_toggle.setText("✏️ 편집")
            self.btn_edit_toggle.setObjectName("editButton")
            self.btn_edit_toggle.setToolTip("마크다운 원본 소스코드를 직접 편집합니다")
            self.btn_cancel_edit.hide()
            self.stack.setCurrentIndex(0)
            if self.current_file_path:
                self.file_badge.setText(f"📄 {os.path.basename(self.current_file_path)}")

        # Refresh button stylesheet
        self.style().unpolish(self.btn_edit_toggle)
        self.style().polish(self.btn_edit_toggle)

    def _on_toggle_edit(self):
        """Handles click on the Edit/Save toggle button."""
        if not self.is_editing:
            # Entering Edit Mode
            if not self.current_file_path or not os.path.isfile(self.current_file_path):
                QMessageBox.information(self, "알림", "먼저 좌측 파일 탐색창에서 편집할 마크다운(.md) 파일을 선택해주세요.")
                return

            self.source_editor.setPlainText(self.current_raw_md)
            self._set_edit_mode_ui(True)
            self.status_message.emit("✏️ 편집 모드: 마크다운 소스코드를 수정한 후 [저장] 버튼을 누르세요. (Ctrl+S)")
        else:
            # Saving in Edit Mode
            self.save_editor_content()

    def save_editor_content(self) -> bool:
        """Saves edited markdown text back to the file and refreshes preview."""
        if not self.current_file_path:
            return False

        new_md = self.source_editor.toPlainText()
        try:
            with open(self.current_file_path, "w", encoding="utf-8") as f:
                f.write(new_md)
        except Exception as e:
            QMessageBox.critical(self, "저장 오류", f"파일을 저장하는 중 오류가 발생했습니다:\n{e}")
            return False

        self.current_raw_md = new_md

        # Re-render HTML with new markdown
        file_name = os.path.basename(self.current_file_path)
        base_dir = os.path.dirname(self.current_file_path)
        title = os.path.splitext(file_name)[0]
        self.current_html = convert_markdown_to_html(new_md, title=title, theme_name=self.current_theme)

        base_url = QUrl.fromLocalFile(base_dir + os.sep)
        self.web_view.setHtml(self.current_html, base_url)

        # Return to preview mode
        self._set_edit_mode_ui(False)
        self.status_message.emit(f"💾 마크다운 파일 저장 및 웹뷰 갱신 완료: {file_name}")
        return True

    def _on_cancel_edit(self):
        """Cancels editing and discards unsaved changes."""
        if self.source_editor.toPlainText() != self.current_raw_md:
            reply = QMessageBox.question(
                self, "편집 취소",
                "수정한 내용이 저장되지 않았습니다. 수정을 취소하시겠습니까?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply != QMessageBox.Yes:
                return

        self._set_edit_mode_ui(False)
        self.status_message.emit("편집 취소됨")

    def _on_cancel_edit_force(self):
        """Forcibly cancels edit mode without prompt."""
        self._set_edit_mode_ui(False)

    def load_file(self, file_path: str):
        """Loads and converts a markdown file to HTML, rendering it in the webview."""
        if not file_path or not os.path.isfile(file_path):
            self._show_placeholder()
            return

        # If currently editing with unsaved changes, prompt first
        if self.is_editing and self.source_editor.toPlainText() != self.current_raw_md:
            reply = QMessageBox.question(
                self, "파일 전환",
                "현재 파일에 저장되지 않은 수정 내용이 있습니다. 저장하고 이동하시겠습니까?",
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                QMessageBox.Cancel
            )
            if reply == QMessageBox.Cancel:
                return
            elif reply == QMessageBox.Yes:
                if not self.save_editor_content():
                    return
            else:
                self._on_cancel_edit_force()
        else:
            self._on_cancel_edit_force()

        start_time = time.time()
        self.current_file_path = os.path.abspath(file_path)
        file_name = os.path.basename(self.current_file_path)
        base_dir = os.path.dirname(self.current_file_path)

        try:
            with open(self.current_file_path, "r", encoding="utf-8", errors="replace") as f:
                md_text = f.read()
        except Exception as e:
            QMessageBox.critical(self, "오류", f"파일을 읽는 중 오류가 발생했습니다:\n{e}")
            return

        self.current_raw_md = md_text
        title = os.path.splitext(file_name)[0]
        self.current_html = convert_markdown_to_html(md_text, title=title, theme_name=self.current_theme)

        # Use local file base URL so relative images resolve correctly!
        base_url = QUrl.fromLocalFile(base_dir + os.sep)
        self.web_view.setHtml(self.current_html, base_url)

        # Update Badge
        self.file_badge.setText(f"📄 {file_name}")
        self.file_badge.setToolTip(self.current_file_path)

        # Calculate Stats
        elapsed_ms = (time.time() - start_time) * 1000
        char_count = len(md_text)
        file_size_kb = os.path.getsize(self.current_file_path) / 1024
        status = f"✅ 변환 완료: {file_name} ({file_size_kb:.1f} KB | {char_count:,} 자 | 변환 {elapsed_ms:.1f}ms)"
        self.status_message.emit(status)

    def reload_current_file(self):
        """Re-reads the current file and refreshes preview."""
        if self.current_file_path:
            self.load_file(self.current_file_path)

    def _on_theme_changed(self, new_theme: str):
        self.current_theme = new_theme
        if self.current_file_path and os.path.isfile(self.current_file_path):
            self.load_file(self.current_file_path)
        else:
            self._show_placeholder()

    def _on_open_config(self):
        """Opens style_config.json in the default system editor (e.g. Notepad)."""
        from config_manager import get_config_path, load_style_config
        cfg_path = get_config_path()
        if not os.path.exists(cfg_path):
            load_style_config()
        QDesktopServices.openUrl(QUrl.fromLocalFile(cfg_path))
        self.status_message.emit("⚙️ style_config.json 설정 파일을 열었습니다. 수정 후 저장하고 새로고침(F5)을 누르세요.")

    def _on_copy_html(self):
        """Copies the converted HTML string to clipboard."""
        if not self.current_html:
            return
        
        clipboard = QApplication.clipboard()
        clipboard.setText(self.current_html)
        
        original_text = self.btn_copy_html.text()
        self.btn_copy_html.setText("✅ 복사 완료!")
        self.status_message.emit("📋 클립보드에 HTML 코드가 복사되었습니다.")
        QTimer.singleShot(1500, lambda: self.btn_copy_html.setText(original_text))

    def _on_save_html(self):
        """Exports the current rendered document to an HTML file."""
        if not self.current_html or not self.current_file_path:
            QMessageBox.information(self, "알림", "먼저 좌측에서 변환할 마크다운 파일을 선택해주세요.")
            return

        default_dir = os.path.dirname(self.current_file_path)
        base_name = os.path.splitext(os.path.basename(self.current_file_path))[0]
        default_save_path = os.path.join(default_dir, f"{base_name}.html")

        save_path, _ = QFileDialog.getSaveFileName(
            self,
            "HTML 파일로 저장",
            default_save_path,
            "HTML Files (*.html *.htm)"
        )

        if not save_path:
            return

        try:
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(self.current_html)
            self.status_message.emit(f"💾 저장 성공: {save_path}")
            QMessageBox.information(self, "저장 완료", f"HTML 파일이 성공적으로 저장되었습니다:\n{save_path}")
        except Exception as e:
            QMessageBox.critical(self, "저장 실패", f"파일을 저장하는 중 오류가 발생했습니다:\n{e}")

    def _on_open_browser(self):
        """Opens the converted HTML in the system's default browser."""
        if not self.current_html:
            return

        # Write to a clean temp file
        temp_dir = tempfile.gettempdir()
        file_name = os.path.basename(self.current_file_path) if self.current_file_path else "preview.md"
        base_name = os.path.splitext(file_name)[0]
        temp_path = os.path.join(temp_dir, f"{base_name}_preview.html")

        try:
            with open(temp_path, "w", encoding="utf-8") as f:
                f.write(self.current_html)
            QDesktopServices.openUrl(QUrl.fromLocalFile(temp_path))
            self.status_message.emit(f"🌐 기본 웹 브라우저에서 열었습니다: {temp_path}")
        except Exception as e:
            QMessageBox.critical(self, "오류", f"브라우저를 여는 중 오류가 발생했습니다:\n{e}")

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
        
        file_path = urls[0].toLocalFile()
        if os.path.isfile(file_path):
            ext = os.path.splitext(file_path)[1].lower()
            if ext in {".md", ".markdown", ".mdown", ".mkd", ".txt"}:
                self.file_dropped.emit(file_path)
                self.load_file(file_path)
        event.acceptProposedAction()
