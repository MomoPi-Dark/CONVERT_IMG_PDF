# Image to PDF Converter

Aplikasi untuk mengkonversi gambar (image) ke format PDF dengan mudah. Dilengkapi dengan interface GUI yang user-friendly dan mendukung berbagai format gambar.

## 📋 Daftar Isi

- [Fitur](#-fitur)
- [Requirements](#-requirements)
- [Instalasi](#-instalasi)
- [Cara Penggunaan](#-cara-penggunaan)
- [Struktur Project](#-struktur-project)
- [Troubleshooting](#-troubleshooting)
- [License](#-license)

## ✨ Fitur

### GUI Mode

- ✅ Interface yang user-friendly dan intuitif
- ✅ Pemilihan folder/file yang mudah dengan file browser
- ✅ Dukungan batch processing (folder/subfolder)
- ✅ Custom output PDF name
- ✅ Merge multiple images menjadi satu file
- ✅ Progress bar real-time
- ✅ Validasi input otomatis
- ✅ Notifikasi status dan error handling

### Supported Formats

- **Input**: PNG, JPG, JPEG, GIF, BMP, TIFF, HEIC
- **Output**: PDF

## 📦 Requirements

- **Python**: 3.8 atau lebih tinggi
- **pip**: Python package installer
- **OS**: Windows, macOS, atau Linux
- **Dependencies**:
  - `pillow` - Image processing
  - `imageio` - Image to PDF conversion
  - `pillow-heif` - HEIC/HEIF support (otomatis terpasang oleh launcher)

### OS-Specific Requirements

**Windows:**

- Command Prompt atau PowerShell
- Batch file support (.bat)

**macOS:**

- Homebrew (optional, untuk install Python)
- bash/zsh shell

**Linux:**

- bash/sh shell
- Tkinter (untuk GUI mode)

## 🚀 Instalasi

### Quick Start (Recommended)

Untuk instruksi detail per OS, lihat [SETUP.md](SETUP.md)

### Step 1: Download/Clone Repository

```bash
# Jika pakai Git
git clone <repository-url>
cd CONVERT_IMG_PDF

# Atau ekstrak file ZIP langsung
```

### Step 2: Check Python Installation

```bash
# Windows
python --version  # Pastikan Python 3.8+
pip --version     # Pastikan pip terinstall

# macOS/Linux
python3 --version
pip3 --version
```

Jika belum terinstall, download dari [python.org](https://www.python.org/downloads/)

### Step 3: Run the Application

**Windows:**

```bash
WRun.bat
```

**macOS/Linux:**

```bash
chmod +x LMRun.sh
./LMRun.sh
```

Script akan otomatis:

1. ✅ Membuat virtual environment (`.venv`)
2. ✅ Install semua dependencies dari `requirements.txt`
3. ✅ Menjalankan aplikasi

### Step 4: Manual Setup (Optional)

Jika ingin setup manual:

```bash
# Create virtual environment
python -m venv .venv        # Windows
python3 -m venv .venv       # macOS/Linux

# Activate virtual environment
# Windows:
.venv\Scripts\activate

# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run GUI application
python init.py
```

## 💻 Cara Penggunaan

### Opsi 1: GUI Mode (Recommended)

**Langkah:**

1. Jalankan GUI application:

   - **Windows**: Double-click `WRun.bat`
   - **macOS/Linux**: ` ./LMRun.sh`

2. GUI window akan terbuka dengan beberapa opsi:

   - **Select Input Folder**: Pilih folder yang berisi gambar
   - **Select Output Folder**: Pilih folder untuk menyimpan PDF
   - **Merge Files**: Gabung multiple images menjadi satu PDF
   - **Custom Name**: Beri nama custom untuk output PDF

3. Klik tombol **Convert** untuk memulai proses

4. Tunggu hingga proses selesai (progress bar akan menunjukkan status)

5. File PDF akan tersimpan di folder output yang dipilih

6. Tutup aplikasi dengan klik tombol X atau Close

## 📁 Struktur Project

```
CONVERT_IMG_PDF/
├── init.py                 # GUI application (Tkinter)
├── requirements.txt        # Python dependencies
│
├── Windows Scripts:
│   └── WRun.bat          # Launcher untuk GUI mode
│
├── Unix/Linux/macOS Scripts:
│   └── LMRun.sh           # Launcher untuk GUI mode
│
├── Dokumentasi:
│   ├── README.md            # Dokumentasi project (English & Bahasa)
│   ├── NOTE.txt             # Installation guide (Bahasa Indonesia)
│   ├── SETUP.md             # Setup guide per OS
│   └── LICENSE              # Project license
│
├── Folders:
│   └── .venv/               # Virtual environment (dibuat otomatis)
```

## 🔧 Konfigurasi

### Virtual Environment

- Terletak di folder `.venv` (hidden folder)
- Dibuat otomatis oleh batch script
- Bisa di-reset dengan menghapus folder `.venv` jika ada masalah

## 🐛 Troubleshooting

### General Issues

#### Problem: "Python is not recognized"

**Windows Solusi:**

1. Pastikan Python sudah terinstall
2. Tambahkan Python ke PATH:
   - Control Panel → System → Advanced System Settings
   - Environment Variables → Path → New
   - Tambah: `C:\Users\YourName\AppData\Local\Programs\Python\Python311\`
   - Restart Command Prompt

**macOS Solusi:**

```bash
brew install python3
```

**Linux Solusi:**

```bash
# Ubuntu/Debian
sudo apt-get install python3

# Fedora
sudo dnf install python3
```

#### Problem: "pip is not recognized"

**Solusi:**

```bash
python -m pip --version  # Check if pip exists
python -m ensurepip --upgrade  # Reinstall pip if needed
```

#### Problem: Virtual environment error

**Solusi:**

```bash
# Windows
rmdir /s .venv
WRun.bat

# macOS/Linux
rm -rf .venv
./LMRun.sh
```

#### Problem: "requirements.txt not found"

**Solusi:**

- Pastikan file `requirements.txt` ada di folder project
- Jangan hapus file ini

### Platform-Specific Issues

#### macOS: "Permission denied" when running .sh

```bash
chmod +x LMRun.sh
```

#### Linux: Tkinter not found (GUI error)

```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter
```

#### Linux: venv creation failed

```bash
# Ubuntu/Debian
sudo apt-get install python3-venv

# Then retry
./LMRun.sh
```

### Conversion Issues

#### Problem: Gambar tidak ter-convert

**Solusi:**

1. Pastikan format gambar supported (PNG, JPG, JPEG, GIF, BMP, TIFF, HEIC)
2. Pastikan folder output punya write permission
3. Coba dengan gambar lain untuk test
4. Cek error message di console

#### Problem: PDF hasil kualitas rendah

**Solusi:**

- Kualitas PDF tergantung dari kualitas gambar original
- Gunakan gambar dengan resolusi tinggi untuk hasil terbaik

### More Help

Untuk troubleshooting detail per OS, lihat [SETUP.md](SETUP.md)

## 📊 Performance

- **Kecepatan**: ~1-2 detik per gambar (tergantung ukuran)
- **Memory usage**: Rendah, ~50-100 MB
- **File size**: Tergantung jumlah dan ukuran gambar original

## 🔐 Security & Privacy

- ✅ Tidak memerlukan internet connection
- ✅ Semua processing dilakukan local di computer
- ✅ Tidak ada data yang dikirim ke server
- ✅ File original gambar tidak dihapus

## 📝 File Dependencies

### requirements.txt

```
pillow          # Python Imaging Library untuk image processing
imageio         # General image IO (fallback for HEIC)
pillow-heif     # HEIC/HEIF support for Pillow
```

#### "Already running" warning

Jika Anda mencoba membuka aplikasi dua kali, launcher/aplikasi akan menampilkan peringatan bahwa aplikasi sudah berjalan. Tutup jendela aplikasi yang ada sebelum menjalankan lagi.

### Virtual Environment

- Semua dependencies diinstall di folder `.venv`
- Terisolasi dari Python system global
- Bisa di-clean dengan menghapus `.venv`

## 🤝 Contributing

Jika ada bug atau saran improvement:

1. Buat issue dengan deskripsi jelas
2. Sertakan error message (jika ada)
3. Jelaskan langkah untuk reproduce bug

## 📄 License

Silakan sesuaikan dengan lisensi project Anda (MIT, Apache 2.0, dll)

## 📞 Support

Untuk masalah teknis:

1. Cek file `NOTE.txt` untuk quick troubleshooting
2. Baca section Troubleshooting di README ini
3. Pastikan semua dependencies sudah diinstall dengan benar

## 📚 Documentation

- [README.md](README.md) - Project documentation (English & Bahasa)
- [NOTE.txt](NOTE.txt) - Quick start guide (Bahasa Indonesia)
- [SETUP.md](SETUP.md) - Detailed setup per OS

---

**Last Updated**: December 2025  
**Version**: 1.1
**Supported OS**: Windows, macOS, Linux
