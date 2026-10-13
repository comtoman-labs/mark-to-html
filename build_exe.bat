@echo off
setlocal
title Build MarkToHTML Single EXE

echo ========================================================
echo   MarkToHTML - Building Standalone Single EXE File
echo ========================================================
echo.

set "PYINSTALLER=D:\workspace\venv_com\Scripts\pyinstaller.exe"

if not exist "%PYINSTALLER%" (
    echo [ERROR] PyInstaller not found at: %PYINSTALLER%
    pause
    exit /b 1
)

cd /d "%~dp0"

echo [1/2] Cleaning previous build files...
if exist "build" rmdir /s /q "build" 2>nul

echo [2/2] Packaging single standalone EXE (--onefile)...
echo       Packaging Python runtime, PySide6, Chromium WebEngine, and styles.
echo       This usually takes about 1-2 minutes. Please wait...
echo.

"%PYINSTALLER%" --noconsole --name "MarkToHTML" --icon="icon.ico" --onefile --add-data "icon.ico;." --add-data "style_config.json;." --clean -y main.py

if errorlevel 1 (
    echo.
    echo [FAILED] Build failed with errors.
    pause
    exit /b 1
)

copy /y "%~dp0style_config.json" "%~dp0dist\style_config.json" >nul 2>&1

echo.
echo ========================================================
echo [SUCCESS] Single standalone executable built successfully!
echo File location: dist\MarkToHTML.exe
echo Config file:   dist\style_config.json
echo ========================================================
echo (You can now copy just this single file to any PC!)
echo ========================================================
echo.

if exist "%~dp0dist" (
    explorer.exe "%~dp0dist"
)

pause
exit /b 0
