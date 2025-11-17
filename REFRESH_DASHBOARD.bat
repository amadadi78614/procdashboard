@echo off
REM ================================================================
REM  PROCUREMENT DASHBOARD - ONE-CLICK REFRESH (WINDOWS)
REM ================================================================

echo.
echo ======================================================================
echo    PROCUREMENT DASHBOARD - DAILY REFRESH
echo ======================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.x from https://www.python.org/
    pause
    exit /b 1
)

REM Check if Consolidated.xlsx exists
if not exist "Consolidated.xlsx" (
    echo ERROR: Consolidated.xlsx not found!
    echo.
    echo Please place your Consolidated.xlsx file in this folder:
    echo %CD%
    echo.
    pause
    exit /b 1
)

echo Found: Consolidated.xlsx
echo.
echo Starting refresh process...
echo.

REM Run the refresh script
python refresh_dashboard.py

echo.
echo ======================================================================
echo Press any key to close this window...
pause >nul
