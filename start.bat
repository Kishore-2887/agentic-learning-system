@echo off
python run_cli.py %*
if %errorlevel% neq 0 (
    echo.
    echo [TIP] If python failed, make sure Python is installed and added to PATH.
)
pause

