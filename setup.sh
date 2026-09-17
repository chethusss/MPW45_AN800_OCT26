#!/bin/bash

set -e

PYTHON_VERSION="3.12.10"
VENV_DIR=".venv"
PYTHON_PKG="/tmp/python-${PYTHON_VERSION}.pkg"
PYTHON_URL="https://www.python.org/ftp/python/3.12.10/python-3.12.10-macos11.pkg"

echo "=========================================="
echo "AN800 MPW45 Layout Environment Setup"
echo "=========================================="
echo

# ==========================================================
# Check whether exact Python version already exists
# ==========================================================

echo "Checking for Python ${PYTHON_VERSION}..."

PYTHON_EXE=""

for CMD in python3.12 python3 python; do
    if command -v "$CMD" >/dev/null 2>&1; then
        VERSION=$("$CMD" --version 2>&1)

        if [ "$VERSION" = "Python ${PYTHON_VERSION}" ]; then
            PYTHON_EXE=$(command -v "$CMD")
            break
        fi
    fi
done

# Also check the standard Python.org installation location
if [ -z "$PYTHON_EXE" ] && [ -x "/usr/local/bin/python3.12" ]; then
    VERSION=$(/usr/local/bin/python3.12 --version 2>&1)

    if [ "$VERSION" = "Python ${PYTHON_VERSION}" ]; then
        PYTHON_EXE="/usr/local/bin/python3.12"
    fi
fi

# ==========================================================
# Install exact Python version if necessary
# ==========================================================

if [ -z "$PYTHON_EXE" ]; then

    echo "Python ${PYTHON_VERSION} was not found."
    echo
    echo "Downloading official Python ${PYTHON_VERSION} installer..."
    echo

    curl -L --fail "$PYTHON_URL" -o "$PYTHON_PKG"

    echo
    echo "Installing Python ${PYTHON_VERSION}..."
    echo
    echo "Administrator permission may be requested."
    echo

    sudo installer \
        -pkg "$PYTHON_PKG" \
        -target /

    rm -f "$PYTHON_PKG"

    echo
    echo "Python installation completed."
    echo

    # Standard location used by the Python.org installer
    PYTHON_EXE="/usr/local/bin/python3.12"

    if [ ! -x "$PYTHON_EXE" ]; then
        echo "ERROR: Python ${PYTHON_VERSION} was installed,"
        echo "but ${PYTHON_EXE} could not be found."
        exit 1
    fi
fi

# ==========================================================
# Verify exact Python version
# ==========================================================

VERSION=$("$PYTHON_EXE" --version 2>&1)

if [ "$VERSION" != "Python ${PYTHON_VERSION}" ]; then
    echo
    echo "ERROR: Wrong Python version:"
    echo "$VERSION"
    echo
    echo "Required:"
    echo "Python ${PYTHON_VERSION}"
    exit 1
fi

echo "Using:"
echo "$PYTHON_EXE"
echo "$VERSION"
echo

# ==========================================================
# Remove existing virtual environment
# ==========================================================

if [ -d "$VENV_DIR" ]; then
    echo "Removing existing .venv..."
    rm -rf "$VENV_DIR"
    echo
fi

# ==========================================================
# Create virtual environment
# ==========================================================

echo "Creating virtual environment..."

"$PYTHON_EXE" -m venv "$VENV_DIR"

echo "Virtual environment created."
echo

# ==========================================================
# Activate virtual environment
# ==========================================================

echo "Activating virtual environment..."

source "$VENV_DIR/bin/activate"

echo

# ==========================================================
# Verify virtual environment Python
# ==========================================================

echo "Virtual environment Python:"
python --version

echo
echo "Python executable:"
which python

echo

# ==========================================================
# Fix / bootstrap pip
# ==========================================================

echo "Checking pip..."

if ! python -m pip --version >/dev/null 2>&1; then

    echo "pip is missing."
    echo "Bootstrapping pip..."

    python -m ensurepip --upgrade
fi

echo
echo "Upgrading pip..."

python -m pip install --upgrade pip

echo
echo "pip:"
python -m pip --version

echo

# ==========================================================
# Install requirements
# ==========================================================

if [ ! -f "requirements.txt" ]; then
    echo "ERROR: requirements.txt was not found."
    exit 1
fi

echo "Installing project dependencies..."
echo

python -m pip install -r requirements.txt

echo

# ==========================================================
# Final verification
# ==========================================================

echo "=========================================="
echo "Setup completed successfully!"
echo "=========================================="
echo

echo "Python:"
python --version

echo
echo "Python executable:"
which python

echo
echo "pip:"
python -m pip --version

echo
echo "GDSFactory:"
python -c "import gdsfactory as gf; print(gf.__version__)"

echo
echo "Virtual environment:"
echo "$PWD/.venv"

# ==========================================================
# Configure VS Code Python interpreter
# ==========================================================

echo
echo "Configuring VS Code Python interpreter..."

mkdir -p .vscode

cat > .vscode/settings.json << 'EOF'
{
    "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
    "python.terminal.activateEnvironment": true
}
EOF

echo "VS Code configured to use:"
echo ".venv/bin/python"


echo
echo "=========================================="
echo "Environment is ready!"
echo "=========================================="