#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "======================================="
echo "   IMAGE TO PDF CONVERTER"
echo "======================================="
echo ""

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}Virtual environment not found. Installing dependencies...${NC}"
    echo ""
    
    # Check Python installation
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}ERROR: Python3 is not installed!${NC}"
        echo "Please install Python 3.8 or higher:"
        echo "  - macOS (Homebrew): brew install python3"
        echo "  - Ubuntu/Debian: sudo apt-get install python3 python3-pip"
        echo "  - Fedora: sudo dnf install python3"
        exit 1
    fi
    
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
echo -e "${GREEN}Starting Image to PDF Converter...${NC}"
echo ""

# Run the Python script
python3 init.py

# Exit code
EXIT_CODE=$?

echo ""
echo "======================================="
echo ""

exit $EXIT_CODE
