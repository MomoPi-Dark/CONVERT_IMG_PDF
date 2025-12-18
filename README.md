# Image to PDF Converter

Aplikasi untuk mengkonversi gambar (image) ke format PDF dengan mudah. Mendukung dua mode operasi: GUI (Graphical User Interface) dan Command Line Interface.

## 📋 Daftar Isi

- [Fitur](#-fitur)
- [Requirements](#-requirements)
- [Instalasi](#-instalasi)
- [Cara Penggunaan](#-cara-penggunaan)
- [Struktur Project](#-struktur-project)
- [Troubleshooting](#-troubleshooting)
- [License](#-license)

## ✨ Fitur

### GUI Mode (`run_gui.bat`)

- ✅ Interface yang user-friendly dan intuitif
- ✅ Pemilihan folder/file yang mudah dengan file browser
- ✅ Preview gambar sebelum di-convert
- ✅ Dukungan batch processing (folder/subfolder)
- ✅ Custom output PDF name
- ✅ Merge multiple images/PDFs menjadi satu file
- ✅ Progress bar real-time
- ✅ Validasi input otomatis
- ✅ Notifikasi status dan error handling

### Command Line Mode (`run_script.bat`)

- ✅ Mode automation untuk batch processing
- ✅ Custom input/output path via command prompt
- ✅ Progress tracking dengan detail
- ✅ Otomatis process subfolder (opsional)
- ✅ Logging untuk setiap conversion

### Supported Formats

- **Input**: JPG, JPEG, PNG, BMP, GIF, TIFF, WebP
- **Output**: PDF

## 📦 Requirements

- **Python**: 3.8 atau lebih tinggi
- **pip**: Python package installer
- **Windows**: OS Windows (batch scripts)
- **Dependencies**:
  - `pillow` - Image processing
  - `imageio` - Image to PDF conversion

## 🚀 Instalasi

### Step 1: Download/Clone Repository

```bash
# Jika pakai Git
git clone <repository-url>
cd CONVERT_IMG_PDF

# Atau ekstrak file ZIP langsung
```

### Step 2: Check Python Installation

```bash
python --version  # Pastikan Python 3.8+
pip --version     # Pastikan pip terinstall
```

Jika belum terinstall, download dari [python.org](https://www.python.org/downloads/)

### Step 3: Automatic Setup (Recommended)

Cukup jalankan salah satu script di bawah, semua setup akan otomatis:

**GUI Mode:**

```bash
run_gui.bat
```

**Command Line Mode:**

```bash
run_script.bat
```

Script akan otomatis:

1. ✅ Membuat virtual environment (`.venv`)
2. ✅ Install semua dependencies dari `requirements.txt`
3. ✅ Menjalankan aplikasi

### Step 4: Manual Setup (Optional)

Jika ingin setup manual:

```bash
# Buat virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 💻 Cara Penggunaan

### Opsi 1: GUI Mode (Recommended)

**Langkah:**

1. Double-click `run_gui.bat` atau jalankan dari Command Prompt:

   ```bash
   run_gui.bat
   ```

2. GUI window akan terbuka dengan beberapa opsi:

   - **Select Input Folder**: Pilih folder yang berisi gambar
   - **Select Output Folder**: Pilih folder untuk menyimpan PDF
   - **Preview Mode**: Lihat preview gambar sebelum convert
   - **Merge Files**: Gabung multiple images menjadi satu PDF
   - **Custom Name**: Beri nama custom untuk output PDF

3. Klik tombol **Convert** untuk memulai proses

4. Tunggu hingga proses selesai (progress bar akan menunjukkan status)

5. File PDF akan tersimpan di folder output yang dipilih

### Opsi 2: Command Line Mode

**Langkah:**

1. Buka Command Prompt di folder project:

   ```bash
   run_script.bat
   ```

2. Program akan meminta input:

   - **Input folder**: Ketik path folder yang berisi gambar
   - **Output folder**: Ketik path folder untuk output PDF
   - **Process subfolders**: Tanya apakah ingin process subfolder (y/n)

3. Proses conversion akan dimulai otomatis

4. File PDF akan tersimpan dengan struktur folder original

**Contoh Input:**

```
Input folder (default: input): C:\Users\YourName\Pictures
Output folder (default: output): C:\Users\YourName\Downloads
Process subfolders? (y/n): y
```

## 📁 Struktur Project

```
CONVERT_IMG_PDF/
├── init.py                 # Command line script
├── init_gui.py             # GUI application (Tkinter)
├── requirements.txt        # Python dependencies
├── run_script.bat          # Windows batch untuk CLI mode
├── run_gui.bat             # Windows batch untuk GUI mode
├── run_convert.sh          # Shell script untuk Linux/Mac
├── NOTE.txt                # Installation & running guide (Indonesian)
├── README.md               # Dokumentasi project
├── input/                  # Default input folder (gambar)
└── output/                 # Default output folder (PDF hasil)
```

## 🔧 Konfigurasi

### Default Folders

Aplikasi menggunakan folder default:

- **Input**: `./input`
- **Output**: `./output`

Folder akan dibuat otomatis jika tidak ada.

### Custom Folders

Anda bisa:

- **GUI Mode**: Pilih custom folder di file browser
- **CLI Mode**: Input custom path saat program berjalan

### Virtual Environment

- Terletak di folder `.venv` (hidden folder)
- Dibuat otomatis oleh batch script
- Bisa di-reset dengan menghapus folder `.venv` jika ada masalah

## 🐛 Troubleshooting

### Problem: "Python is not recognized"

**Solusi:**

1. Pastikan Python sudah terinstall
2. Tambahkan Python ke PATH:
   - Control Panel → System → Advanced System Settings
   - Environment Variables → Path → New
   - Tambah: `C:\Users\YourName\AppData\Local\Programs\Python\Python311\`
   - Restart Command Prompt

### Problem: "pip is not recognized"

**Solusi:**

```bash
python -m pip --version  # Check if pip exists
python -m ensurepip --upgrade  # Reinstall pip if needed
```

### Problem: Virtual environment error

**Solusi:**

1. Delete folder `.venv`
2. Jalankan `run_gui.bat` atau `run_script.bat` lagi
3. Virtual environment baru akan dibuat otomatis

### Problem: "requirements.txt not found"

**Solusi:**

- Pastikan file `requirements.txt` ada di folder project
- Jangan hapus file ini

### Problem: Gambar tidak ter-convert

**Solusi:**

1. Pastikan format gambar supported (JPG, PNG, BMP, GIF, TIFF, WebP)
2. Pastikan folder output punya write permission
3. Coba dengan gambar lain untuk test
4. Cek error message di console

### Problem: PDF hasil kualitas rendah

**Solusi:**

- Kualitas PDF tergantung dari kualitas gambar original
- Gunakan gambar dengan resolusi tinggi untuk hasil terbaik

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
imageio         # Library untuk image to PDF conversion
```

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

## 🎯 Roadmap

Fitur yang akan datang:

- [ ] Support Linux dan macOS
- [ ] Web interface
- [ ] Batch scheduling
- [ ] Image compression options
- [ ] OCR integration
- [ ] Cloud storage support

---

**Last Updated**: December 2025  
**Version**: 1.0
