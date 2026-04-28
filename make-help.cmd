@echo off
setlocal
cd /d "%~dp0"
where python >nul 2>&1 && python scripts\make_help.py && exit /b %ERRORLEVEL%
where py >nul 2>&1 && py -3 scripts\make_help.py && exit /b %ERRORLEVEL%
echo Не найден Python. Установите Python 3.12+ и добавьте в PATH, либо используйте Git Bash: make help
exit /b 1
