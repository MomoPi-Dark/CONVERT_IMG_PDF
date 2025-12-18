import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image
import imageio.v2 as imageio
import shutil
from datetime import datetime
import threading

# Enable HEIC/HEIF support via pillow-heif when available
try:
    from pillow_heif import register_heif_opener  # type: ignore
    register_heif_opener()
    HEIF_SUPPORTED = True
except Exception:
    HEIF_SUPPORTED = False


class ImageToPDFConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Image to PDF Converter")
        self.root.geometry("850x700")
        self.root.resizable(True, True)
        
        # Get default documents folder
        import os.path
        documents_folder = os.path.join(os.path.expanduser("~"), "Documents")
        
        # Variables
        self.input_folder = tk.StringVar(value="")
        self.output_folder = tk.StringVar(value=os.path.join(documents_folder, "HASIL"))
        self.is_converting = False
        
        # Mode selection
        self.mode = tk.StringVar(value="folder")  # "folder" or "files"
        self.selected_files = []
        self.merge_files = tk.BooleanVar(value=False)
        self.custom_name = tk.StringVar(value="")
        
        # Folder mode merge option
        self.merge_folder_pdfs = tk.BooleanVar(value=False)
        self.folder_custom_name = tk.StringVar(value="")
        
        self.setup_ui()
        
    def setup_ui(self):
        # Fixed header (outside scrollable area)
        header_frame = tk.Frame(self.root, bg="#2c3e50", height=70)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        tk.Label(
            header_frame,
            text="IMAGE TO PDF CONVERTER",
            font=("Arial", 20, "bold"),
            bg="#2c3e50",
            fg="white"
        ).pack(pady=16)
        
        # Main content (scrollable)
        # Container holds a canvas + vertical scrollbar. Inside the canvas we place a real content frame.
        content_container = tk.Frame(self.root)
        content_container.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(content_container, highlightthickness=0)
        vscroll = tk.Scrollbar(content_container, orient=tk.VERTICAL, command=canvas.yview)
        canvas.configure(yscrollcommand=vscroll.set)

        vscroll.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # The actual content frame that will hold all widgets
        content_frame = tk.Frame(canvas, padx=20, pady=20)
        content_window = canvas.create_window((0, 0), window=content_frame, anchor="nw")

        # Ensure scrollregion tracks content size changes
        def _on_frame_configure(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))

        content_frame.bind("<Configure>", _on_frame_configure)

        # Make canvas window width follow the container width
        def _on_canvas_configure(event):
            # Stretch the inner frame to the canvas width
            canvas.itemconfigure(content_window, width=event.width)

        canvas.bind("<Configure>", _on_canvas_configure)

        # Mouse wheel support (Windows/macOS)
        def _on_mousewheel(event):
            delta = 0
            if hasattr(event, 'delta') and event.delta:
                delta = int(-1 * (event.delta / 120))
            if delta:
                canvas.yview_scroll(delta, "units")

        # Mouse wheel support (Linux)
        def _on_mousewheel_linux(event):
            if event.num == 4:
                canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                canvas.yview_scroll(1, "units")

        def _bind_wheel(_):
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
            canvas.bind_all("<Button-4>", _on_mousewheel_linux)
            canvas.bind_all("<Button-5>", _on_mousewheel_linux)

        def _unbind_wheel(_):
            canvas.unbind_all("<MouseWheel>")
            canvas.unbind_all("<Button-4>")
            canvas.unbind_all("<Button-5>")

        content_frame.bind("<Enter>", _bind_wheel)
        content_frame.bind("<Leave>", _unbind_wheel)
        
        # Mode Selection
        mode_frame = tk.LabelFrame(
            content_frame, 
            text="Mode Konversi", 
            font=("Arial", 12, "bold"),
            padx=15,
            pady=15
        )
        mode_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        tk.Radiobutton(
            mode_frame,
            text="📁 Convert dari Folder",
            variable=self.mode,
            value="folder",
            command=self.on_mode_change,
            font=("Arial", 11)
        ).pack(side=tk.LEFT, padx=(0, 30))
        
        tk.Radiobutton(
            mode_frame,
            text="📷 Pilih File Foto Individual",
            variable=self.mode,
            value="files",
            command=self.on_mode_change,
            font=("Arial", 11)
        ).pack(side=tk.LEFT)
        
        # Folder Mode Frame
        self.folder_frame = tk.Frame(content_frame)
        self.folder_frame.grid(row=1, column=0, sticky="ew")
        
        # Folder selection button
        tk.Label(
            self.folder_frame, 
            text="📁 Pilih Folder yang Berisi Gambar:", 
            font=("Arial", 11, "bold")
        ).grid(row=0, column=0, sticky="w", pady=(0, 10))
        
        tk.Button(
            self.folder_frame, 
            text="🔍 Pilih Folder", 
            command=self.select_folder_to_convert,
            bg="#3498db",
            fg="white",
            font=("Arial", 11, "bold"),
            cursor="hand2",
            padx=30,
            pady=10
        ).grid(row=1, column=0, pady=(0, 10))
        
        self.folder_status_label = tk.Label(
            self.folder_frame,
            text="Belum ada folder dipilih",
            font=("Arial", 9),
            fg="#7f8c8d",
            wraplength=600
        )
        self.folder_status_label.grid(row=2, column=0, sticky="w", pady=(0, 15))
        
        # Merge folder PDFs option
        self.folder_merge_check = tk.Checkbutton(
            self.folder_frame,
            text="🔗 Gabungkan foto menjadi 1 PDF",
            variable=self.merge_folder_pdfs,
            command=self.on_folder_merge_change,
            font=("Arial", 10, "bold"),
            fg="#2c3e50"
        )
        self.folder_merge_check.grid(row=3, column=0, sticky="w", pady=(0, 10))
        
        # Folder custom name field (for merged PDF)
        self.folder_custom_name_frame = tk.Frame(self.folder_frame)
        self.folder_custom_name_frame.grid(row=4, column=0, sticky="ew", pady=(0, 18))
        
        tk.Label(
            self.folder_custom_name_frame,
            text="📝 Nama PDF (opsional):",
            font=("Arial", 10)
        ).pack(side=tk.LEFT, padx=(20, 10))
        
        self.folder_custom_name_entry = tk.Entry(
            self.folder_custom_name_frame,
            textvariable=self.folder_custom_name,
            font=("Arial", 10),
            width=30
        )
        self.folder_custom_name_entry.pack(side=tk.LEFT)
        
        tk.Label(
            self.folder_custom_name_frame,
            text=".pdf",
            font=("Arial", 10, "bold"),
            fg="#7f8c8d"
        ).pack(side=tk.LEFT, padx=(2, 0))
        
        self.folder_custom_name_frame.grid_remove()  # Hide initially
        
        self.folder_frame.columnconfigure(0, weight=1)
        
        # Files Mode Frame
        self.files_frame = tk.Frame(content_frame)
        self.files_frame.grid(row=1, column=0, sticky="ew")
        
        tk.Label(
            self.files_frame, 
            text="📷 Pilih File Foto:", 
            font=("Arial", 10, "bold")
        ).grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        files_btn_frame = tk.Frame(self.files_frame)
        files_btn_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        
        tk.Button(
            files_btn_frame, 
            text="+ Pilih File Foto", 
            command=self.browse_files,
            bg="#3498db",
            fg="white",
            font=("Arial", 9, "bold"),
            cursor="hand2",
            padx=20,
            pady=5
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(
            files_btn_frame, 
            text="Clear All", 
            command=self.clear_files,
            bg="#e74c3c",
            fg="white",
            font=("Arial", 9),
            cursor="hand2",
            padx=15,
            pady=5
        ).pack(side=tk.LEFT)
        
        self.files_label = tk.Label(
            files_btn_frame,
            text="0 file dipilih",
            font=("Arial", 9),
            fg="#7f8c8d"
        )
        self.files_label.pack(side=tk.LEFT, padx=(15, 0))
        
        # Files list frame with scrollbar
        files_list_frame = tk.LabelFrame(
            self.files_frame,
            text="Daftar Foto",
            font=("Arial", 10, "bold"),
            padx=10,
            pady=10
        )
        files_list_frame.grid(row=2, column=0, sticky="ew", pady=(0, 15))
        
        # Create frame for listbox and scrollbar
        list_container = tk.Frame(files_list_frame)
        list_container.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(list_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Listbox for files
        self.files_listbox = tk.Listbox(
            list_container,
            font=("Arial", 9),
            height=6,
            yscrollcommand=scrollbar.set,
            selectmode=tk.SINGLE
        )
        self.files_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.files_listbox.yview)
        
        # Button frame for list actions
        list_actions = tk.Frame(files_list_frame)
        list_actions.pack(fill=tk.X, pady=(8, 0))
        
        tk.Button(
            list_actions,
            text="🗑️ Hapus Foto Dipilih",
            command=self.remove_selected_file,
            bg="#e74c3c",
            fg="white",
            font=("Arial", 9),
            cursor="hand2",
            padx=15,
            pady=4
        ).pack(side=tk.LEFT)
        
        tk.Label(
            list_actions,
            text="Klik foto untuk pilih, lalu klik tombol hapus",
            font=("Arial", 8),
            fg="#7f8c8d"
        ).pack(side=tk.LEFT, padx=(15, 0))
                # Merge option
        merge_check = tk.Checkbutton(
            self.files_frame,
            text="🔗 Gabung semua foto jadi 1 PDF",
            variable=self.merge_files,
            command=self.on_merge_change,
            font=("Arial", 10, "bold"),
            fg="#2c3e50"
        )
        merge_check.grid(row=3, column=0, sticky="w", pady=(0, 10))
        
        # Custom name field (for merged PDF)
        self.custom_name_frame = tk.Frame(self.files_frame)
        self.custom_name_frame.grid(row=4, column=0, sticky="ew", pady=(0, 18))
        
        tk.Label(
            self.custom_name_frame,
            text="📝 Nama PDF (opsional):",
            font=("Arial", 10)
        ).pack(side=tk.LEFT, padx=(20, 10))
        
        self.custom_name_entry = tk.Entry(
            self.custom_name_frame,
            textvariable=self.custom_name,
            font=("Arial", 10),
            width=30
        )
        self.custom_name_entry.pack(side=tk.LEFT)
        
        tk.Label(
            self.custom_name_frame,
            text=".pdf",
            font=("Arial", 10, "bold"),
            fg="#7f8c8d"
        ).pack(side=tk.LEFT, padx=(2, 0))
        
        self.custom_name_frame.grid_remove()  # Hide initially
        
        self.files_frame.columnconfigure(0, weight=1)
        self.files_frame.grid_remove()  # Hide initially
        
        # Output Folder
        output_info_frame = tk.LabelFrame(
            content_frame,
            text="💾 Lokasi Hasil PDF",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=12
        )
        output_info_frame.grid(row=3, column=0, sticky="ew", pady=(0, 25))
        
        output_path_frame = tk.Frame(output_info_frame)
        output_path_frame.pack(fill=tk.X)
        
        # Create a StringVar for the display path
        self.display_output_path = tk.StringVar(
            value=f'{self.output_folder.get().replace("\\", "/")}/{datetime.now().strftime("%Y-%m-%d")}'
        )
        
        tk.Entry(
            output_path_frame, 
            textvariable=self.display_output_path, 
            font=("Arial", 10),
            state="readonly"
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4)
        
        tk.Button(
            output_path_frame, 
            text="Ubah", 
            command=self.browse_output,
            bg="#95a5a6",
            fg="white",
            font=("Arial", 9),
            cursor="hand2",
            padx=15,
            pady=4
        ).pack(side=tk.RIGHT, padx=(8, 0))
        
        content_frame.columnconfigure(0, weight=1)
        
        # Progress section
        progress_frame = tk.LabelFrame(
            content_frame, 
            text="Progress", 
            font=("Arial", 12, "bold"),
            padx=15,
            pady=12
        )
        progress_frame.grid(row=4, column=0, sticky="ew", pady=(0, 20))
        
        self.progress_bar = ttk.Progressbar(
            progress_frame, 
            mode='determinate',
            length=600
        )
        self.progress_bar.pack(fill=tk.X, pady=(0, 8), ipady=3)
        
        self.status_label = tk.Label(
            progress_frame, 
            text="Ready to convert...",
            font=("Arial", 10),
            fg="#7f8c8d"
        )
        self.status_label.pack()
        
        # Buttons
        button_frame = tk.Frame(content_frame)
        button_frame.grid(row=5, column=0, pady=(0, 15))
        
        self.convert_btn = tk.Button(
            button_frame,
            text="🚀 START CONVERSION",
            command=self.start_conversion,
            bg="#27ae60",
            fg="white",
            font=("Arial", 13, "bold"),
            cursor="hand2",
            padx=40,
            pady=12,
            relief=tk.RAISED,
            bd=3
        )
        self.convert_btn.pack(side=tk.LEFT, padx=8)
        
        # Footer info
        info_label = tk.Label(
            content_frame,
            text="Format didukung: PNG, JPG, JPEG, GIF, BMP, TIFF, HEIC • File asli tidak akan dihapus",
            font=("Arial", 9),
            fg="#7f8c8d"
        )
        info_label.grid(row=6, column=0, pady=(12, 0))
        
    def select_folder_to_convert(self):
        folder = filedialog.askdirectory(title="Pilih Folder yang Berisi Gambar")
        if folder:
            self.input_folder.set(folder)
            self.folder_status_label.config(
                text=f"✓ Folder dipilih: {folder}",
                fg="#27ae60"
            )
    
    def browse_output(self):
        folder = filedialog.askdirectory(
            title="Pilih Lokasi Penyimpanan PDF",
            initialdir=self.output_folder.get()
        )
        if folder:
            self.output_folder.set(folder)
            # Update display path with new folder and current date
            self.display_output_path.set(f'{folder}\\{datetime.now().strftime("%Y-%m-%d")}')
    
    def on_mode_change(self):
        """Switch mode dan reset previous selection"""
        if self.mode.get() == "folder":
            # Switch to folder mode
            self.folder_frame.grid()
            self.files_frame.grid_remove()
            # Reset file mode selections
            self.clear_files()
            self.merge_files.set(False)
            self.custom_name_frame.grid_remove()
            # Reset folder merge options
            self.merge_folder_pdfs.set(False)
            self.folder_custom_name.set("")
            self.folder_custom_name_frame.grid_remove()
            self.status_label.config(text="Ready to convert...", fg="#7f8c8d")
        else:
            # Switch to file mode
            self.folder_frame.grid_remove()
            self.files_frame.grid()
            # Reset folder mode selection
            self.input_folder.set("")
            self.folder_status_label.config(
                text="Belum ada folder dipilih",
                fg="#7f8c8d"
            )
            # Reset folder merge options
            self.merge_folder_pdfs.set(False)
            self.folder_custom_name.set("")
            self.folder_custom_name_frame.grid_remove()
            self.status_label.config(text="Ready to convert...", fg="#7f8c8d")
            self.progress_bar['value'] = 0
    
    def on_merge_change(self):
        if self.merge_files.get():
            self.custom_name_frame.grid()
        else:
            self.custom_name_frame.grid_remove()
            self.custom_name.set("")
    
    def on_folder_merge_change(self):
        """Toggle folder custom name field visibility"""
        if self.merge_folder_pdfs.get():
            self.folder_custom_name_frame.grid()
        else:
            self.folder_custom_name_frame.grid_remove()
            self.folder_custom_name.set("")
    
    def browse_files(self):
        files = filedialog.askopenfilenames(
            title="Pilih File Foto",
            filetypes=[
                ("Image Files", "*.png *.jpg *.jpeg *.gif *.bmp *.tiff *.heic"),
                ("All Files", "*.*")
            ]
        )
        if files:
            for file in files:
                if file not in self.selected_files:
                    self.selected_files.append(file)
                    self.files_listbox.insert(tk.END, os.path.basename(file))
            self.files_label.config(text=f"{len(self.selected_files)} file dipilih")
    
    def remove_selected_file(self):
        """Remove selected file from list"""
        selection = self.files_listbox.curselection()
        if selection:
            index = selection[0]
            # Remove from listbox
            self.files_listbox.delete(index)
            # Remove from selected files
            del self.selected_files[index]
            # Update label
            self.files_label.config(text=f"{len(self.selected_files)} file dipilih")
            self.status_label.config(text="Foto dihapus dari list", fg="#e67e22")
        else:
            messagebox.showinfo("Info", "Pilih foto yang ingin dihapus dari list terlebih dahulu")
    
    def clear_files(self):
        self.selected_files = []
        self.files_listbox.delete(0, tk.END)
        self.files_label.config(text="0 file dipilih")
        self.custom_name.set("")
        self.status_label.config(text="Files cleared", fg="#e67e22")
    
    def start_conversion(self):
        if self.is_converting:
            return
        
        # Validate based on mode
        if self.mode.get() == "folder":
            if not self.input_folder.get():
                messagebox.showwarning("Warning", "Pilih folder yang berisi gambar terlebih dahulu!")
                return
            if not os.path.exists(self.input_folder.get()):
                messagebox.showerror("Error", "Folder yang dipilih tidak ditemukan!")
                return
        elif self.mode.get() == "files" and len(self.selected_files) == 0:
            messagebox.showwarning("Warning", "Pilih minimal 1 file foto terlebih dahulu!")
            return
        
        # Create output folder if not exist
        os.makedirs(self.output_folder.get(), exist_ok=True)
        
        # Start conversion in separate thread
        self.is_converting = True
        self.convert_btn.config(state=tk.DISABLED, bg="#95a5a6")
        
        if self.mode.get() == "folder":
            thread = threading.Thread(target=self.convert_images, daemon=True)
        else:
            thread = threading.Thread(target=self.convert_selected_files, daemon=True)
        thread.start()
    
    def convert_images(self):
        supported_formats = [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".heic"]
        
        folder_path = self.input_folder.get()
        result_folder = self.output_folder.get()
        
        # Validate folder path
        if not folder_path or not os.path.exists(folder_path):
            self.update_status("Error: Folder tidak valid!", "#e74c3c")
            self.is_converting = False
            self.convert_btn.config(state=tk.NORMAL, bg="#27ae60")
            return
        
        try:
            # Create result folder with date
            date_str = datetime.now().strftime("%Y-%m-%d")
            result_folder_with_date = os.path.join(result_folder, date_str)
            os.makedirs(result_folder_with_date, exist_ok=True)
            
            converted_files = []
            all_images = []  # For merge mode
            
            # JIKA MERGE DICENTANG - KUMPULKAN SEMUA IMAGE
            if self.merge_folder_pdfs.get():
                self.update_status("Mengumpulkan semua gambar...", "#3498db")
                
                # Kumpulkan semua image dari root folder
                try:
                    for item_name in os.listdir(folder_path):
                        item_path = os.path.join(folder_path, item_name)
                        
                        # File individual di root
                        if os.path.isfile(item_path) and any(item_name.lower().endswith(ext) for ext in supported_formats):
                            try:
                                if item_name.lower().endswith(".heic"):
                                    img = imageio.imread(item_path)
                                    img = Image.fromarray(img).convert("RGB")
                                else:
                                    img = Image.open(item_path).convert("RGB")
                                all_images.append(img)
                                self.update_status(f"Loading: {item_name}", "#3498db")
                            except Exception as e:
                                self.update_status(f"⚠️ Gagal load: {item_name}", "#e67e22")
                        
                        # Gambar dalam subfolder
                        elif os.path.isdir(item_path):
                            try:
                                subfolder_items = sorted(os.listdir(item_path))
                                for file_name in subfolder_items:
                                    file_path = os.path.join(item_path, file_name)
                                    if os.path.isfile(file_path) and any(file_name.lower().endswith(ext) for ext in supported_formats):
                                        try:
                                            if file_name.lower().endswith(".heic"):
                                                img = imageio.imread(file_path)
                                                img = Image.fromarray(img).convert("RGB")
                                            else:
                                                img = Image.open(file_path).convert("RGB")
                                            all_images.append(img)
                                            self.update_status(f"Loading: {file_name}", "#3498db")
                                        except:
                                            pass
                            except:
                                pass
                except Exception as e:
                    self.update_status(f"Error: {e}", "#e74c3c")
                    self.is_converting = False
                    self.convert_btn.config(state=tk.NORMAL, bg="#27ae60")
                    return
                
                # SIMPAN SEMUA JADI 1 PDF
                if all_images:
                    self.update_status("Menggabungkan semua gambar jadi 1 PDF...", "#3498db")
                    
                    # Get custom name
                    custom_name = self.folder_custom_name.get().strip()
                    if custom_name:
                        if custom_name.lower().endswith('.pdf'):
                            custom_name = custom_name[:-4]
                        custom_name = "".join(c for c in custom_name if c.isalnum() or c in (' ', '-', '_')).strip()
                        merged_pdf_name = f"{custom_name}.pdf"
                    else:
                        merged_pdf_name = f"Merged_All_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                    
                    merged_pdf_path = os.path.join(result_folder_with_date, merged_pdf_name)
                    
                    # Check if file already exists
                    if os.path.exists(merged_pdf_path):
                        counter = 1
                        base_name = os.path.splitext(merged_pdf_name)[0]
                        while os.path.exists(merged_pdf_path):
                            merged_pdf_name = f"{base_name}({counter}).pdf"
                            merged_pdf_path = os.path.join(result_folder_with_date, merged_pdf_name)
                            counter += 1
                    
                    # Save merged PDF
                    self.update_status("Menyimpan PDF gabungan...", "#3498db")
                    all_images[0].save(
                        merged_pdf_path,
                        save_all=True,
                        append_images=all_images[1:] if len(all_images) > 1 else []
                    )
                    
                    self.update_progress(100)
                    self.update_status(f"✓ Semua gambar berhasil digabung jadi 1 PDF!", "#27ae60")
                    messagebox.showinfo(
                        "Success!",
                        f"Semua gambar berhasil digabung!\n\nFile: {merged_pdf_name}\nJumlah halaman: {len(all_images)}\nLokasi: {result_folder_with_date}"
                    )
                else:
                    self.update_status("⚠️ Tidak ada gambar ditemukan!", "#e67e22")
                    messagebox.showwarning("Warning", "Tidak ada gambar ditemukan di folder")
                
                # Reset after merge
                self.is_converting = False
                self.convert_btn.config(state=tk.NORMAL, bg="#27ae60")
                self.progress_bar['value'] = 0
                self.reset_after_conversion()
            
            # JIKA MERGE TIDAK DICENTANG - PER FILE INDIVIDUAL
            else:
                self.update_status("Mengonversi gambar...", "#3498db")
                total_items = 0
                processed_items = 0
                items_list = []
                
                # Hitung total items
                try:
                    for item_name in os.listdir(folder_path):
                        item_path = os.path.join(folder_path, item_name)
                        if os.path.isfile(item_path) and any(item_name.lower().endswith(ext) for ext in supported_formats):
                            total_items += 1
                            items_list.append(("file", item_name, item_path))
                        elif os.path.isdir(item_path):
                            total_items += 1
                            items_list.append(("folder", item_name, item_path))
                except Exception as e:
                    self.update_status(f"Error: {e}", "#e74c3c")
                    self.is_converting = False
                    self.convert_btn.config(state=tk.NORMAL, bg="#27ae60")
                    return
                
                if total_items == 0:
                    self.update_status("⚠️ Tidak ada gambar di folder ini!", "#e67e22")
                    self.is_converting = False
                    self.convert_btn.config(state=tk.NORMAL, bg="#27ae60")
                    messagebox.showwarning("Warning", "Folder tidak berisi gambar atau subfolder dengan gambar")
                    return
                
                # Process individual files
                for item_type, item_name, item_path in items_list:
                    
                    if item_type == "file":
                        try:
                            self.update_status(f"Converting: {item_name}", "#3498db")
                            
                            base_name = os.path.splitext(item_name)[0]
                            output_pdf_path = os.path.join(result_folder_with_date, f"{base_name}.pdf")
                            
                            # Handle duplicate names
                            counter = 1
                            while os.path.exists(output_pdf_path):
                                output_pdf_path = os.path.join(result_folder_with_date, f"{base_name}({counter}).pdf")
                                counter += 1
                            
                            # Convert image
                            if item_name.lower().endswith(".heic"):
                                img = imageio.imread(item_path)
                                img = Image.fromarray(img).convert("RGB")
                            else:
                                img = Image.open(item_path).convert("RGB")
                            
                            img.save(output_pdf_path)
                            converted_files.append(output_pdf_path)
                            
                            processed_items += 1
                            progress = (processed_items / total_items) * 100
                            self.update_progress(progress)
                            
                        except Exception as e:
                            self.update_status(f"Error: {item_name} - {str(e)}", "#e74c3c")
                            processed_items += 1
                    
                    elif item_type == "folder":
                        try:
                            self.update_status(f"Processing folder: {item_name}", "#3498db")
                            
                            image_list = []
                            
                            try:
                                subfolder_items = sorted(os.listdir(item_path))
                            except:
                                processed_items += 1
                                continue
                            
                            for file_name in subfolder_items:
                                file_path = os.path.join(item_path, file_name)
                                
                                if os.path.isfile(file_path) and any(file_name.lower().endswith(ext) for ext in supported_formats):
                                    try:
                                        if file_name.lower().endswith(".heic"):
                                            img = imageio.imread(file_path)
                                            img = Image.fromarray(img).convert("RGB")
                                        else:
                                            img = Image.open(file_path).convert("RGB")
                                        
                                        image_list.append(img)
                                    except:
                                        pass
                            
                            if image_list:
                                output_pdf_path = os.path.join(result_folder_with_date, f"{item_name}.pdf")
                                
                                # Handle duplicate names
                                counter = 1
                                while os.path.exists(output_pdf_path):
                                    output_pdf_path = os.path.join(result_folder_with_date, f"{item_name}({counter}).pdf")
                                    counter += 1
                                
                                image_list[0].save(
                                    output_pdf_path,
                                    save_all=True,
                                    append_images=image_list[1:] if len(image_list) > 1 else []
                                )
                                converted_files.append(output_pdf_path)
                            
                            processed_items += 1
                            progress = (processed_items / total_items) * 100
                            self.update_progress(progress)
                            
                        except Exception as e:
                            self.update_status(f"Error: {item_name} - {str(e)}", "#e74c3c")
                            processed_items += 1
                
                # Regular completion message (no merge)
                self.update_progress(100)
                self.update_status(f"✓ Conversion complete! {len(converted_files)} PDFs created", "#27ae60")
                self.is_converting = False
                self.convert_btn.config(state=tk.NORMAL, bg="#27ae60")
                
                messagebox.showinfo(
                    "Success!", 
                    f"Conversion completed!\n\n{len(converted_files)} PDF files created in:\n{result_folder_with_date}"
                )
                self.progress_bar['value'] = 0
                self.reset_after_conversion()
            
        except Exception as e:
            self.update_status(f"Error: {str(e)}", "#e74c3c")
            self.is_converting = False
            self.convert_btn.config(state=tk.NORMAL, bg="#27ae60")
    
    def update_progress(self, value):
        self.progress_bar['value'] = value
        self.root.update_idletasks()
    
    def update_status(self, text, color="#000000"):
        self.status_label.config(text=text, fg=color)
        self.root.update_idletasks()
    
    def reset_after_conversion(self):
        """Reset UI after conversion complete"""
        # Reset folder mode
        self.input_folder.set("")
        self.folder_status_label.config(
            text="Belum ada folder dipilih",
            fg="#7f8c8d"
        )
        self.merge_folder_pdfs.set(False)
        self.folder_custom_name.set("")
        self.folder_custom_name_frame.grid_remove()
        
        # Reset file mode
        self.selected_files = []
        self.files_listbox.delete(0, tk.END)
        self.files_label.config(text="0 file dipilih")
        self.merge_files.set(False)
        self.custom_name.set("")
        self.custom_name_frame.grid_remove()
        
        # Reset progress
        self.progress_bar['value'] = 0
        self.status_label.config(text="Ready to convert...", fg="#7f8c8d")
        
        # Reset button
        self.is_converting = False
        self.convert_btn.config(state=tk.NORMAL, bg="#27ae60")
    
    def convert_selected_files(self):
        """Convert selected individual files"""
        result_folder = self.output_folder.get()
        
        # Create result folder with date
        date_str = datetime.now().strftime("%Y-%m-%d")
        result_folder_with_date = os.path.join(result_folder, date_str)
        os.makedirs(result_folder_with_date, exist_ok=True)
        
        total_files = len(self.selected_files)
        converted_files = []
        
        if self.merge_files.get():
            # Merge all files into 1 PDF
            self.update_status("Menggabungkan semua foto jadi 1 PDF...", "#3498db")
            
            image_list = []
            for i, file_path in enumerate(self.selected_files):
                try:
                    file_name = os.path.basename(file_path)
                    self.update_status(f"Loading: {file_name}", "#3498db")
                    
                    if file_name.lower().endswith(".heic") and HEIF_SUPPORTED:
                        # Prefer Pillow with pillow-heif if available
                        img = Image.open(file_path).convert("RGB")
                    else:
                        # Fallback to PIL for common formats and imageio for HEIC when pillow-heif is unavailable
                        if file_name.lower().endswith(".heic") and not HEIF_SUPPORTED:
                            arr = imageio.imread(file_path)
                            if getattr(arr, "size", 0) == 0:
                                raise ValueError("Gagal membaca file HEIC (kosong). Coba konversi ke JPG/PNG atau pasang pillow-heif.")
                            img = Image.fromarray(arr).convert("RGB")
                        else:
                            img = Image.open(file_path).convert("RGB")
                    
                    image_list.append(img)
                    
                    progress = ((i + 1) / total_files) * 80
                    self.update_progress(progress)
                    
                except Exception as e:
                    self.update_status(f"Error: {file_name} - {e}", "#e74c3c")
            
            if image_list:
                # Save as merged PDF
                custom_name = self.custom_name.get().strip()
                if custom_name:
                    # Remove .pdf extension if user added it
                    if custom_name.lower().endswith('.pdf'):
                        custom_name = custom_name[:-4]
                    # Clean filename from invalid characters
                    custom_name = "".join(c for c in custom_name if c.isalnum() or c in (' ', '-', '_')).strip()
                    output_pdf_name = f"{custom_name}.pdf"
                else:
                    output_pdf_name = f"Merged_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                
                output_pdf_path = os.path.join(result_folder_with_date, output_pdf_name)
                
                # Check if file already exists
                if os.path.exists(output_pdf_path):
                    counter = 1
                    base_name = os.path.splitext(output_pdf_name)[0]
                    while os.path.exists(output_pdf_path):
                        output_pdf_name = f"{base_name}({counter}).pdf"
                        output_pdf_path = os.path.join(result_folder_with_date, output_pdf_name)
                        counter += 1
                    self.update_status(f"⚠️ File sudah ada, disimpan sebagai: {output_pdf_name}", "#e67e22")
                
                self.update_status("Menyimpan PDF...", "#3498db")
                image_list[0].save(
                    output_pdf_path,
                    save_all=True,
                    append_images=image_list[1:] if len(image_list) > 1 else []
                )
                converted_files.append(output_pdf_path)
            
            self.update_progress(100)
            
        else:
            # Convert each file separately
            for i, file_path in enumerate(self.selected_files):
                try:
                    file_name = os.path.basename(file_path)
                    base_name = os.path.splitext(file_name)[0]
                    
                    self.update_status(f"Converting: {file_name}", "#3498db")
                    
                    output_pdf_path = os.path.join(result_folder_with_date, f"{base_name}.pdf")
                    
                    # Handle duplicate names
                    counter = 1
                    while os.path.exists(output_pdf_path):
                        output_pdf_path = os.path.join(result_folder_with_date, f"{base_name}({counter}).pdf")
                        counter += 1
                    
                    # Convert image
                    if file_name.lower().endswith(".heic") and HEIF_SUPPORTED:
                        img = Image.open(file_path).convert("RGB")
                    else:
                        if file_name.lower().endswith(".heic") and not HEIF_SUPPORTED:
                            arr = imageio.imread(file_path)
                            if getattr(arr, "size", 0) == 0:
                                raise ValueError("Gagal membaca file HEIC (kosong). Coba konversi ke JPG/PNG atau pasang pillow-heif.")
                            img = Image.fromarray(arr).convert("RGB")
                        else:
                            img = Image.open(file_path).convert("RGB")
                    
                    img.save(output_pdf_path)
                    converted_files.append(output_pdf_path)
                    
                    progress = ((i + 1) / total_files) * 100
                    self.update_progress(progress)
                    
                except Exception as e:
                    self.update_status(f"Error: {file_name} - {e}", "#e74c3c")
        
        # Done
        self.update_progress(100)
        self.update_status(f"✓ Conversion complete! {len(converted_files)} PDF created", "#27ae60")
        self.is_converting = False
        self.convert_btn.config(state=tk.NORMAL, bg="#27ae60")
        self.selected_files = []
        self.files_listbox.delete(0, tk.END)
        self.files_label.config(text="0 file dipilih")
        self.custom_name.set("")
        
        if self.merge_files.get():
            if converted_files:
                messagebox.showinfo(
                    "Success!", 
                    f"Semua foto berhasil digabung!\n\nFile: {os.path.basename(converted_files[0])}\nLokasi: {result_folder_with_date}"
                )
            else:
                # No output produced (e.g., all inputs failed to load). Inform the user gracefully.
                messagebox.showwarning(
                    "Warning",
                    "Tidak ada foto valid yang berhasil digabung. Pastikan file tidak rusak dan formatnya didukung (PNG/JPG/JPEG/GIF/BMP/TIFF/HEIC)."
                )
        else:
            messagebox.showinfo(
                "Success!", 
                f"Conversion completed!\n\n{len(converted_files)} PDF files created in:\n{result_folder_with_date}"
            )
        self.progress_bar['value'] = 0
        self.reset_after_conversion()


if __name__ == "__main__":
    # Prevent multiple instances (simple PID file lock)
    import tempfile, atexit, sys
    LOCK_PATH = os.path.join(tempfile.gettempdir(), "convert_img_pdf.lock")
    def _cleanup_lock():
        try:
            if os.path.exists(LOCK_PATH):
                os.remove(LOCK_PATH)
        except Exception:
            pass

    if os.path.exists(LOCK_PATH):
        try:
            with open(LOCK_PATH, "r") as f:
                pid_str = f.read().strip()
            pid = int(pid_str) if pid_str.isdigit() else None
        except Exception:
            pid = None

        still_running = False
        if pid:
            try:
                os.kill(pid, 0)
                still_running = True
            except Exception:
                still_running = False
        if still_running:
            # Show a small notice and exit
            tk.Tk().withdraw()
            messagebox.showinfo("Already Running", "Aplikasi sudah berjalan. Tutup aplikasi yang sedang berjalan sebelum membuka yang baru.")
            sys.exit(0)
        else:
            # Stale lock; remove
            try:
                os.remove(LOCK_PATH)
            except Exception:
                pass

    try:
        with open(LOCK_PATH, "w") as f:
            f.write(str(os.getpid()))
        atexit.register(_cleanup_lock)
    except Exception:
        pass

    root = tk.Tk()
    app = ImageToPDFConverter(root)
    root.mainloop()
