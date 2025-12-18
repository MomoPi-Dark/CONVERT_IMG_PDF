#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "======================================="
echo "   IMAGE TO PDF CONVERTER - GUI MODE"
echo "======================================="
echo ""

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Check if Python3 is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}ERROR: Python3 is not installed!${NC}"
    echo "Please install Python 3.8 or higher:"
    echo "  - macOS (Homebrew): brew install python3"
    echo "  - Ubuntu/Debian: sudo apt-get install python3 python3-pip"
    echo "  - Fedora: sudo dnf install python3"
    exit 1
fi

# System-level tkinter check and installation (required for venv to inherit it)
echo -e "${YELLOW}Checking for system tkinter...${NC}"
if ! python3 -c "import tkinter" 2>/dev/null; then
    echo -e "${YELLOW}System tkinter not found. Attempting to install...${NC}"
    
    if command -v apt-get &> /dev/null; then
        echo -e "${GREEN}Installing tkinter via apt (Ubuntu/Debian)...${NC}"
        sudo apt-get update && sudo apt-get install -y python3-tk
    elif command -v dnf &> /dev/null; then
        echo -e "${GREEN}Installing tkinter via dnf (Fedora)...${NC}"
        sudo dnf install -y python3-tkinter
    elif command -v yum &> /dev/null; then
        echo -e "${GREEN}Installing tkinter via yum (CentOS/RHEL)...${NC}"
        sudo yum install -y python3-tkinter
    elif command -v brew &> /dev/null; then
        echo -e "${GREEN}tkinter should come with Python on macOS...${NC}"
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
        echo -e "${RED}ERROR: Failed to install tkinter${NC}"
        exit 1
    fi
    echo -e "${GREEN}tkinter installed successfully!${NC}"
else
    echo -e "${GREEN}System tkinter is available${NC}"
fi

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}Virtual environment not found. Installing dependencies...${NC}"
    echo ""
    
    # Check if requirements.txt exists
    if [ ! -f "requirements.txt" ]; then
        echo -e "${RED}ERROR: requirements.txt not found!${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}Creating virtual environment...${NC}"
    python3 -m venv .venv
    
    if [ ! -d ".venv" ]; then
        echo -e "${RED}ERROR: Failed to create virtual environment!${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}Activating virtual environment...${NC}"
    source .venv/bin/activate
    
    echo -e "${GREEN}Installing required packages...${NC}"
    pip install --upgrade pip
    pip install -r requirements.txt
    
    if [ $? -ne 0 ]; then
        echo ""
        echo -e "${RED}ERROR: Failed to install dependencies!${NC}"
        echo "Please check your internet connection and try again."
        echo ""
        exit 1
    fi
    
    echo ""
    echo -e "${GREEN}Dependencies installed successfully!${NC}"
    echo ""
else
    echo -e "${GREEN}Virtual environment found. Activating...${NC}"
    source .venv/bin/activate
fi

echo ""
echo -e "${GREEN}Starting Image to PDF Converter (GUI)...${NC}"
echo ""

# Run the GUI script
python3 init_gui.py

# Exit code
EXIT_CODE=$?

echo ""
echo "======================================="
echo ""

exit $EXIT_CODE
