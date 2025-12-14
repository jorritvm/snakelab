@echo off
python crashes.py
if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%
python works_fine.py
if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%