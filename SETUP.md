# Setup Guide for Different Operating Systems

## 🪟 Windows

### Requirements

- Python 3.8+
- Command Prompt atau PowerShell

### Installation & Running

#### GUI Mode

```bash
WRun.bat
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
chmod +x LMRun.sh
```

#### Step 3: Running the Application

#### Step 2: Make launcher executable

**GUI Mode:**

chmod +x LMRun.sh
./LMRun.sh

````
#### Step 3: Running the Application

```bash
./LMRun.sh
````

brew install python3

#### Step 2: Make launcher executable

# Or download from python.org

````
chmod +x LMRun.sh
#### Problem: "Permission denied" when running .sh script in macOS

**GUI Mode:**

```bash
./LMRun.sh
````

---

## 🐧 Linux (Ubuntu/Debian/Fedora)

chmod +x LMRun.sh

### Requirements

./LMRun.sh # This will reinstall everything

- Terminal

#### Step 2: Make launcher executable

#### Step 1: Install Python & Dependencies

chmod +x LMRun.sh
**Ubuntu/Debian:**

**GUI Mode:**

```bash
./LMRun.sh
```

# Then try again

./LMRun.sh

````
#### Step 2: Make shell scripts executable
chmod +x LMRun.sh
```bash
cd CONVERT_IMG_PDF
./LMRun.sh  # Linux/macOS
````

#### Step 3: Running the Application

**GUI Mode:**

```bash
./LMRun.sh
```

Or use the recommended launcher:

```bash
chmod +x LMRun.sh
./LMRun.sh
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
./LMRun.sh
```

#### Problem: "Permission denied" when running .sh script in Linux

```bash
chmod +x LMRun.sh
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

| Feature     | Windows        | macOS      | Linux      |
| ----------- | -------------- | ---------- | ---------- |
| GUI Mode    | WRun.bat       | ./LMRun.sh | ./LMRun.sh |
| Virtual Env | Automatic      | Automatic  | Automatic  |
| Python      | python         | python3    | python3    |
| Shell       | CMD/PowerShell | bash/zsh   | bash/sh    |

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

# 5. Run GUI application
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
./LMRun.sh  # Linux/macOS
WRun.bat  # Windows
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
