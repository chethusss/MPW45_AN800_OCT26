@echo off
setlocal

echo ==========================================
echo Environment Setup for gdsfactory
echo ==========================================
echo.

REM ==========================================================
REM Check for Python 3.12.10
REM ==========================================================

echo Checking for Python 3.12.10...

set "PYTHON_EXE="
set "PYTHON_VERSION="

REM Try to find Python 3.12 using the Python Launcher
for /f "delims=" %%P in ('py -3.12 -c "import sys; print(sys.executable)" 2^>nul') do (
    set "PYTHON_EXE=%%P"
)

if defined PYTHON_EXE (
    for /f "delims=" %%V in ('"%PYTHON_EXE%" --version') do (
        set "PYTHON_VERSION=%%V"
    )
)

if "%PYTHON_VERSION%"=="Python 3.12.10" (
    echo Found Python 3.12.10:
    echo %PYTHON_EXE%
    echo.
    goto PYTHON_READY
)

echo Python 3.12.10 was not found.
echo.

REM ==========================================================
REM Check for WinGet
REM ==========================================================

echo Checking for WinGet...

where winget >nul 2>&1

if errorlevel 1 (
    echo.
    echo ERROR: Python 3.12.10 is not installed and WinGet
    echo was not found on this computer.
    echo.
    echo Please install Python 3.12.10 manually from:
    echo https://www.python.org/downloads/release/python-31210/
    echo.
    pause
    exit /b 1
)

REM ==========================================================
REM Install Python 3.12.10 using WinGet
REM ==========================================================

echo Installing Python 3.12.10 using WinGet...
echo.

winget install --id Python.Python.3.12 ^
    --exact ^
    --version 3.12.10 ^
    --source winget ^
    --scope user ^
    --accept-source-agreements ^
    --accept-package-agreements

if errorlevel 1 (
    echo.
    echo ERROR: Failed to install Python 3.12.10.
    echo.
    pause
    exit /b 1
)

echo.
echo Python installation completed.
echo.

REM ==========================================================
REM Locate Python 3.12.10 after installation
REM ==========================================================

set "PYTHON_EXE="
set "PYTHON_VERSION="

for /f "delims=" %%P in ('py -3.12 -c "import sys; print(sys.executable)" 2^>nul') do (
    set "PYTHON_EXE=%%P"
)

if not defined PYTHON_EXE (
    echo.
    echo ERROR: Python 3.12.10 was installed but could not
    echo be detected by the Python Launcher.
    echo.
    echo Please close this window, open a new Command Prompt,
    echo and run setup.bat again.
    echo.
    pause
    exit /b 1
)

for /f "delims=" %%V in ('"%PYTHON_EXE%" --version') do (
    set "PYTHON_VERSION=%%V"
)

if not "%PYTHON_VERSION%"=="Python 3.12.10" (
    echo.
    echo ERROR: Wrong Python version detected:
    echo %PYTHON_VERSION%
    echo.
    echo Required:
    echo Python 3.12.10
    echo.
    pause
    exit /b 1
)

:PYTHON_READY

echo.
echo ==========================================
echo Python 3.12.10 is ready.
echo ==========================================
echo.

echo Python:
"%PYTHON_EXE%" --version

echo.
echo Python executable:
echo %PYTHON_EXE%

REM ==========================================================
REM Create virtual environment
REM ==========================================================

echo.
echo Checking virtual environment...

if exist ".venv\Scripts\python.exe" (
    echo Existing .venv detected.
    echo Skipping virtual environment creation.
) else (
    echo Creating virtual environment...
    echo.

    "%PYTHON_EXE%" -m venv .venv

    if errorlevel 1 (
        echo.
        echo ERROR: Failed to create virtual environment.
        echo.
        pause
        exit /b 1
    )

    echo Virtual environment created successfully.
)

REM ==========================================================
REM Activate virtual environment
REM ==========================================================

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

REM ==========================================================
REM Verify virtual environment Python
REM ==========================================================

echo.
echo Virtual environment Python:

python --version

if errorlevel 1 (
    echo.
    echo ERROR: Could not run Python from .venv.
    echo.
    pause
    exit /b 1
)

REM ==========================================================
REM Upgrade pip
REM ==========================================================

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

REM ==========================================================
REM Install project dependencies
REM ==========================================================

echo.
echo Installing project dependencies from requirements.txt...
echo.

python -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERROR: Dependency installation failed.
    echo.
    pause
    exit /b 1
)

REM ==========================================================
REM Final verification
REM ==========================================================

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
echo ==========================================
echo Your environment is ready!
echo ==========================================
echo.

pause