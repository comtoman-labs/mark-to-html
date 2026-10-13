"""
MarkToHTML - Main Entry Point
Launches the PySide6 Markdown to HTML application.
"""

import sys
import os
import ctypes

# Fix for Windows Taskbar icon display
try:
    myappid = "marktohtml.viewer.app.1.0"
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except Exception:
    pass

# Ensure project root is in sys.path
if getattr(sys, "frozen", False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from main_window import MainWindow


def main():
    # High DPI scaling settings for Windows
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    app = QApplication(sys.argv)
    app.setApplicationName("MarkToHTML")
    app.setOrganizationName("MarkToHTML")

    # Prevent QFont pointSize <= 0 warning on Windows
    app_font = app.font()
    if app_font.pointSize() <= 0:
        app_font.setPointSize(10)
        app.setFont(app_font)

    # Set Application Icon
    icon_candidates = [
        os.path.join(BASE_DIR, "icon.ico"),
        os.path.join(os.path.dirname(sys.executable), "icon.ico"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.ico"),
    ]
    for ic in icon_candidates:
        if os.path.isfile(ic):
            app_icon = QIcon(ic)
            app.setWindowIcon(app_icon)
            break

    # Start with workspace folder maximized
    start_folder = os.getcwd() if getattr(sys, "frozen", False) else os.path.dirname(os.path.abspath(__file__))
    window = MainWindow(start_dir=start_folder)
    if not app.windowIcon().isNull():
        window.setWindowIcon(app.windowIcon())
        
    window.showMaximized()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
