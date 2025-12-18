#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

INFO="${BLUE}[INFO]${NC}"
ERROR="${RED}[ERROR]${NC}"
WARN="${YELLOW}[WARN]${NC}"
SUCCESS="${GREEN}[SUCCESS]${NC}"

# Venv paths
VENV_ROOT=".venv"
VENV_SCRIPTS="$VENV_ROOT/bin"
VENV_PY="$VENV_SCRIPTS/python3"
VENV_ACTIVATE="$VENV_SCRIPTS/activate"

echo "======================================="
echo "   IMAGE TO PDF CONVERTER - GUI MODE"
echo "======================================="
echo ""

echo -e "${INFO} Initializing environment..."

# Check if Python3 is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}ERROR: Python3 is not installed!${NC}"
    echo "Please install Python 3.8 or higher:"
    echo "  - macOS (Homebrew): brew install python3"
    echo "  - Ubuntu/Debian: sudo apt-get install python3 python3-pip"
    echo "  - Fedora: sudo dnf install python3"
    exit 1
fi

python3 - << 'EOF'
import sys
if sys.version_info < (3, 8):
    print("ERROR: Python 3.8 or higher is required!")
    sys.exit(1)
EOF

delete_venv() {
    echo -e "${INFO} Deleting existing virtual environment..."
    rm -rf "$VENV_ROOT"
}

create_venv() {
    echo -e "${INFO} Creating virtual environment..."
    python3 -m venv "$VENV_ROOT"
    
    echo -e "${INFO} Activating virtual environment and installing dependencies..."
    source "$VENV_ACTIVATE"

    pip install --upgrade pip
    pip install -r requirements.txt
}

if [ ! -d "$VENV_ROOT" ]; then
    create_venv
fi 

if [ ! -f "$VENV_PY" ]; then
    echo -e "${ERROR} Virtual environment setup failed!"
    delete_venv
    create_venv
    echo -e "${SUCCESS}Virtual environment created successfully!${NC}"
fi

# Activate virtual environment
source "$VENV_ACTIVATE"

# System-level tkinter check and installation (required for venv to inherit it)
echo -e "${INFO} ${YELLOW}Checking for system tkinter...${NC}"
if ! python3 -c "import tkinter" 2>/dev/null; then
    echo -e "${YELLOW}System tkinter not found. Attempting to install...${NC}"
    
    if command -v apt-get &> /dev/null; then
        echo -e "${INFO} ${GREEN}Installing tkinter via apt (Ubuntu/Debian)...${NC}"
        sudo apt-get update && sudo apt-get install -y python3-tk
    elif command -v dnf &> /dev/null; then
        echo -e "${INFO} ${GREEN}Installing tkinter via dnf (Fedora)...${NC}"
        sudo dnf install -y python3-tkinter
    elif command -v yum &> /dev/null; then
        echo -e "${INFO} ${GREEN}Installing tkinter via yum (CentOS/RHEL)...${NC}"
        sudo yum install -y python3-tkinter
    elif command -v brew &> /dev/null; then
        echo -e "${INFO} ${GREEN}tkinter should come with Python on macOS...${NC}"
    else
        echo -e "${RED}ERROR: Could not detect package manager${NC}"
        echo "Please install tkinter manually:"
        echo "  Ubuntu/Debian: sudo apt-get install python3-tk"
        echo "  Fedora: sudo dnf install python3-tkinter"
        echo "  CentOS: sudo yum install python3-tkinter"
        exit 1
    fi
    
    # Verify installation
    if ! python3 -c "import tkinter" 2>/dev/null; then
        echo -e " ${ERROR} Failed to install tkinter${NC}"
        exit 1
    fi
    echo -e "${SUCCESS}tkinter installed successfully!${NC}"
else
    echo -e "${INFO} ${GREEN}System tkinter is available${NC}"
fi

echo ""
echo -e "${GREEN}Starting Image to PDF Converter (GUI)...${NC}"
echo ""

# Run the GUI script
python3 init.py

# Exit code
EXIT_CODE=$?

echo ""
echo "======================================="
echo ""

exit $EXIT_CODE
