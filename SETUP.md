# Setup Guide for Different Operating Systems

## 🪟 Windows

### Requirements

- Python 3.8+
- Command Prompt atau PowerShell

### Installation & Running

#### GUI Mode (Recommended)

```bash
run_gui.bat
```

#### Command Line Mode

```bash
run_script.bat
```

### Notes

- Virtual environment akan dibuat di `.venv`
- Batch script otomatis install dependencies

---

## 🍎 macOS

### Requirements

- Python 3.8+
- Terminal

### Installation

#### Step 1: Install Python (if not already installed)

```bash
# Using Homebrew
brew install python3

# Verify installation
python3 --version
```

#### Step 2: Make shell scripts executable

```bash
cd CONVERT_IMG_PDF
chmod +x run_gui.sh
chmod +x run_convert.sh
```

#### Step 3: Running the Application

**GUI Mode (Recommended):**

```bash
./run_gui.sh
```

**Command Line Mode:**

```bash
./run_convert.sh
```

### Troubleshooting macOS

#### Problem: "Command not found: python3"

```bash
# Install Python via Homebrew
brew install python3

# Or download from python.org
```

#### Problem: "Permission denied" when running .sh script

```bash
chmod +x run_gui.sh
chmod +x run_convert.sh
```

#### Problem: Module not found (pillow, imageio)

```bash
# Remove virtual environment and reinstall
rm -rf .venv
./run_gui.sh  # This will reinstall everything
```

---

## 🐧 Linux (Ubuntu/Debian/Fedora)

### Requirements

- Python 3.8+
- Terminal

### Installation

#### Step 1: Install Python & Dependencies

**Ubuntu/Debian:**

```bash
sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv

# Verify installation
python3 --version
```

**Fedora:**

```bash
sudo dnf install python3 python3-pip

# Verify installation
python3 --version
```

#### Step 2: Make shell scripts executable

```bash
cd CONVERT_IMG_PDF
chmod +x run_gui.sh
chmod +x run_convert.sh
```

#### Step 3: Running the Application

**GUI Mode (Recommended):**

```bash
./run_gui.sh
```

**Command Line Mode:**

```bash
./run_convert.sh
```

### Troubleshooting Linux

#### Problem: "python3: command not found"

```bash
# Ubuntu/Debian
sudo apt-get install python3

# Fedora
sudo dnf install python3
```

#### Problem: "pip: command not found"

```bash
# Ubuntu/Debian
sudo apt-get install python3-pip

# Fedora
sudo dnf install python3-pip
```

#### Problem: Virtual environment creation failed

```bash
# Ubuntu/Debian - Install venv
sudo apt-get install python3-venv

# Then try again
./run_gui.sh
```

#### Problem: "Permission denied" when running .sh script

```bash
chmod +x run_gui.sh
chmod +x run_convert.sh
```

#### Problem: Tkinter not found (GUI won't start)

```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter
```

---

## 🌐 Cross-Platform Comparison

| Feature     | Windows        | macOS            | Linux            |
| ----------- | -------------- | ---------------- | ---------------- |
| GUI Mode    | run_gui.bat    | ./run_gui.sh     | ./run_gui.sh     |
| CLI Mode    | run_script.bat | ./run_convert.sh | ./run_convert.sh |
| Virtual Env | Automatic      | Automatic        | Automatic        |
| Python      | python         | python3          | python3          |
| Shell       | CMD/PowerShell | bash/zsh         | bash/sh          |

---

## Manual Setup (All Platforms)

Jika ingin setup manual tanpa menggunakan script:

```bash
# 1. Clone atau extract repository
cd CONVERT_IMG_PDF

# 2. Create virtual environment
python -m venv .venv  # Windows
python3 -m venv .venv  # macOS/Linux

# 3. Activate virtual environment
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run application
# GUI Mode
python init_gui.py

# CLI Mode
python init.py
```

---

## Environment Variables (Optional)

Anda bisa set environment variables untuk custom path:

```bash
# Linux/macOS
export INPUT_FOLDER="/path/to/input"
export OUTPUT_FOLDER="/path/to/output"

# Windows
set INPUT_FOLDER=C:\path\to\input
set OUTPUT_FOLDER=C:\path\to\output
```

---

## Deactivating Virtual Environment

Untuk menonaktifkan virtual environment:

```bash
# All platforms
deactivate
```

---

## Cleaning Up

Untuk menghapus virtual environment dan reinstall:

```bash
# Remove .venv folder
rm -rf .venv  # Linux/macOS
rmdir /s .venv  # Windows

# Reinstall dengan menjalankan script
./run_gui.sh  # Linux/macOS
run_gui.bat  # Windows
```

---

## Python Version Check

Cek versi Python yang terinstall:

```bash
# Windows
python --version

# macOS/Linux
python3 --version
```

Minimum required: **Python 3.8**

---

## Support Matrix

| OS      | Version   | Status       | Notes                  |
| ------- | --------- | ------------ | ---------------------- |
| Windows | 7 & above | ✅ Supported | Batch scripts provided |
| macOS   | 10.12+    | ✅ Supported | Shell scripts provided |
| Linux   | Any       | ✅ Supported | Shell scripts provided |

---

## Next Steps

1. Pilih OS Anda di atas
2. Follow installation steps
3. Jalankan application dengan script yang sesuai
4. Jika ada masalah, cek troubleshooting section

Untuk informasi lengkap, lihat [README.md](README.md) atau [NOTE.txt](NOTE.txt)
