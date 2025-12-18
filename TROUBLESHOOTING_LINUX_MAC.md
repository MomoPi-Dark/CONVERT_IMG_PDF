# Linux/macOS Troubleshooting Guide

## Quick Fix untuk GUI Error (tkinter not found)

### Masalah

```
ModuleNotFoundError: No module named 'tkinter'
```

### Solusi Otomatis (Recommended)

Script `run_gui.sh` sudah includes auto-install tkinter. Jalankan:

```bash
chmod +x run_gui.sh
./run_gui.sh
```

Script akan otomatis install tkinter jika tidak ditemukan.

### Solusi Manual

#### Ubuntu/Debian

```bash
sudo apt-get update
sudo apt-get install python3-tk
```

#### Fedora

```bash
sudo dnf install python3-tkinter
```

#### CentOS/RHEL

```bash
sudo yum install python3-tkinter
```

#### macOS

Tkinter sudah include dengan Python. Jika tidak ada:

```bash
brew install python-tk
```

### Verifikasi Instalasi

```bash
python3 -c "import tkinter; print('✓ tkinter available')"
```

## Virtual Environment Issues

### Rebuild Virtual Environment

```bash
# Remove old venv
rm -rf .venv

# Jalankan script lagi (akan create venv baru)
./run_gui.sh
```

### Manual Setup

```bash
# Create venv
python3 -m venv .venv

# Activate
source .venv/bin/activate

# Install dependencies
pip install pillow imageio

# Run GUI
python3 init_gui.py
```

## Permission Issues

### Script tidak executable

```bash
chmod +x run_gui.sh
chmod +x run_convert.sh
```

### Verify permissions

```bash
ls -la *.sh
```

Harus ada `x` di permissions:

```
-rwxr-xr-x  run_gui.sh
-rwxr-xr-x  run_convert.sh
```

## Dependencies Installation Issues

### Manual install dependencies

```bash
source .venv/bin/activate
pip install --upgrade pip
pip install pillow imageio
```

### Verify installation

```bash
python3 -c "from PIL import Image; import imageio; print('✓ All dependencies OK')"
```

## Common Errors

### 1. "python3: command not found"

Install Python:

- Ubuntu/Debian: `sudo apt-get install python3`
- Fedora: `sudo dnf install python3`
- macOS: `brew install python3`

### 2. "pip: command not found"

```bash
python3 -m ensurepip --upgrade
```

### 3. "venv: No module named venv"

Ubuntu/Debian:

```bash
sudo apt-get install python3-venv
```

### 4. Display/DISPLAY variable not set (SSH/Remote)

Jika menjalankan via SSH tanpa X11 forwarding:

```bash
# Use CLI mode instead
./run_convert.sh
```

Atau enable X11 forwarding:

```bash
ssh -X user@server
```

## Testing GUI without running full app

```bash
python3 -c "
import tkinter as tk
root = tk.Tk()
root.title('Test')
label = tk.Label(root, text='✓ Tkinter works!')
label.pack()
root.mainloop()
"
```

Jika window muncul, tkinter OK!

## Full Clean Install

```bash
# 1. Install system dependencies
sudo apt-get install python3 python3-pip python3-tk python3-venv

# 2. Clean workspace
cd CONVERT_IMG_PDF
rm -rf .venv

# 3. Run script (will setup everything)
./run_gui.sh
```

## WSL-Specific (Windows Subsystem for Linux)

WSL needs X server untuk GUI:

1. Install VcXsrv atau Xming di Windows
2. Set DISPLAY variable:

```bash
export DISPLAY=:0
```

3. Jalankan GUI:

```bash
./run_gui.sh
```

Atau gunakan CLI mode:

```bash
./run_convert.sh
```

## macOS-Specific

### M1/M2/M3 (Apple Silicon)

Pastikan pakai native Python (bukan Rosetta):

```bash
# Check architecture
python3 -c "import platform; print(platform.machine())"
# Should show: arm64
```

### Homebrew Python

```bash
# Install/reinstall Python via Homebrew
brew install python3
brew install python-tk
```

## Support

Jika masih error:

1. Cek [SETUP.md](SETUP.md) untuk troubleshooting lengkap
2. Cek [README.md](README.md) untuk dokumentasi
3. Pastikan Python version 3.8+

## Quick Command Reference

```bash
# Check Python version
python3 --version

# Check tkinter
python3 -c "import tkinter"

# Check dependencies
python3 -c "from PIL import Image; import imageio"

# Make scripts executable
chmod +x run_gui.sh run_convert.sh

# Run GUI
./run_gui.sh

# Run CLI
./run_convert.sh

# Clean rebuild
rm -rf .venv && ./run_gui.sh
```
