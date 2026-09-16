@echo off
setlocal

echo ==========================================
echo AN800 MPW45 Layout Environment Setup
echo ==========================================
echo.

REM Check for Python 3.12
echo Checking for Python 3.12...

py -3.12 --version >nul 2>&1

if errorlevel 1 (
    echo.
    echo ERROR: Python 3.12 was not found.
    echo.
    echo Please install Python 3.12 and make sure
    echo the Python Launcher "py" is available.
    echo.
    pause
    exit /b 1
)

echo Python 3.12 found:
py -3.12 --version
echo.

REM Create virtual environment if it does not exist
if exist ".venv\Scripts\python.exe" (
    echo Existing .venv detected.
    echo Skipping virtual environment creation.
) else (
    echo Creating virtual environment...
    py -3.12 -m venv .venv

    if errorlevel 1 (
        echo.
        echo ERROR: Failed to create virtual environment.
        echo.
        pause
        exit /b 1
    )
)

echo.
echo Activating virtual environment...
call .venv\Scripts\activate.bat

if errorlevel 1 (
    echo.
    echo ERROR: Failed to activate virtual environment.
    echo.
    pause
    exit /b 1
)

echo.
echo Upgrading pip...
python -m pip install --upgrade pip

if errorlevel 1 (
    echo.
    echo ERROR: Failed to upgrade pip.
    echo.
    pause
    exit /b 1
)

echo.
echo Installing project dependencies...
python -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERROR: Dependency installation failed.
    echo.
    pause
    exit /b 1
)

echo.
echo ==========================================
echo Setup completed successfully!
echo ==========================================
echo.

echo Python:
python --version

echo.
echo GDSFactory:
python -c "import gdsfactory as gf; print(gf.__version__)"

echo.
echo Virtual environment:
echo %CD%\.venv

echo.
echo VS Code should use:
echo .venv\Scripts\python.exe

echo.
pause