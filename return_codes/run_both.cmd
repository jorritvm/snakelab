@echo off
python crashes.py
echo Wrapper sees return code from first python script: %ERRORLEVEL%
python works_fine.py
echo Wrapper sees return code from second python script: %ERRORLEVEL%
