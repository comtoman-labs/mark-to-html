@echo off
set "PYTHON_EXE=D:\workspace\venv_com\Scripts\pythonw.exe"

if not exist "%PYTHON_EXE%" (
    set "PYTHON_EXE=D:\workspace\venv_com\Scripts\python.exe"
)

if not exist "%PYTHON_EXE%" (
    echo [ERROR] Python not found at D:\workspace\venv_com\Scripts\
    pause
    exit /b 1
)

cd /d "%~dp0"
start "" "%PYTHON_EXE%" main.py
exit
