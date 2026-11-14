@echo off
echo ========================================================
echo   Setting up Agentic Content System Dependencies...
echo ========================================================
echo.
python --version
if %errorlevel% neq 0 (
    echo [ERROR] Python is not found!
    echo Please install Python 3.10+ from https://www.python.org/downloads/
    echo Make sure to check the box "Add Python to PATH" during installation.
    pause
    exit /b 1
)

echo.
echo Installing required Python packages...
pip install -r requirements.txt

echo.
echo ========================================================
echo   Setup completed successfully!
echo   To run the system, simply double-click "start.bat"
echo   or run: python run_cli.py
echo ========================================================
pause

