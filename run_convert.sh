#!/bin/bash

# Get script directory (works anywhere)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Set working directory to script location
cd "$SCRIPT_DIR"

# Activate virtual environment if exists
if [ -d ".venv" ]; then
    source .venv/Scripts/activate
fi

# Path ke script Python
SCRIPT_PATH="$SCRIPT_DIR/init.py"

# Folder input dan output (optional - script akan ask jika tidak diberikan)
FOLDER_PATH="$SCRIPT_DIR/BAHAN"
RESULT_FOLDER="$SCRIPT_DIR/HASIL"
SELESAI_FOLDER="$SCRIPT_DIR/PEMBUANGAN"

echo "======================================="
echo "  IMAGE TO PDF CONVERTER"
echo "======================================="
echo ""

# Jalankan script Python
# Bisa dengan argumen (otomatis) atau tanpa argumen (interactive)
if [ -d "$FOLDER_PATH" ]; then
    echo "Running in automatic mode..."
    python "$SCRIPT_PATH" "$FOLDER_PATH" "$RESULT_FOLDER" "$SELESAI_FOLDER"
else
    echo "Running in interactive mode..."
    python "$SCRIPT_PATH"
fi

echo ""
echo "Press any key to exit..."
read -n 1 -s
