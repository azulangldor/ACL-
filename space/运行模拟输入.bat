@echo off
chcp 65001 >nul
cd /d "%~dp0"
python "%~dp0模拟输入.py"
if errorlevel 1 pause
