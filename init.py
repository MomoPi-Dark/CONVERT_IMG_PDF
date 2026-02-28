import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
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
        self.root.geometry("900x750")
        self.root.resizable(True, True)
        
        # Modern color palette
        self.colors = {
            'primary': '#4F46E5',      # Indigo
            'primary_hover': '#4338CA',
            'success': '#10B981',       # Green
            'success_hover': '#059669',
            'danger': '#EF4444',        # Red
            'danger_hover': '#DC2626',
            'secondary': '#6B7280',     # Gray
            'secondary_hover': '#4B5563',
            'dark': '#1F2937',          # Dark gray
            'light': '#F9FAFB',         # Light gray
            'border': '#E5E7EB',
            'text': '#374151',
            'text_light': '#6B7280',
            'warning': '#F59E0B',       # Amber
            'info': '#3B82F6'           # Blue
        }
        
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
        self.setup_button_hover_effects()
        
    def setup_ui(self):
        # Modern gradient-style header
        header_frame = tk.Frame(self.root, bg=self.colors['primary'], height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # Add icon and title
        title_container = tk.Frame(header_frame, bg=self.colors['primary'])
        title_container.pack(expand=True)
        
        tk.Label(
            title_container,
            text="📄",
            font=("Arial", 24),
            bg=self.colors['primary'],
            fg="white"
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Label(
            title_container,
            text="IMAGE TO PDF CONVERTER",
            font=("Segoe UI", 22, "bold"),
            bg=self.colors['primary'],
            fg="white"
        ).pack(side=tk.LEFT)
        
        tk.Label(
            title_container,
            text="Convert your images easily",
            font=("Segoe UI", 9),
            bg=self.colors['primary'],
            fg="#E0E7FF"
        ).pack(side=tk.LEFT, padx=(15, 0))
        
        # Main content (scrollable)
        # Container holds a canvas + vertical scrollbar. Inside the canvas we place a real content frame.
        content_container = tk.Frame(self.root, bg=self.colors['light'])
        content_container.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(content_container, highlightthickness=0, bg=self.colors['light'])
        vscroll = tk.Scrollbar(content_container, orient=tk.VERTICAL, command=canvas.yview)
        canvas.configure(yscrollcommand=vscroll.set)

        vscroll.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # The actual content frame that will hold all widgets
        content_frame = tk.Frame(canvas, padx=30, pady=25, bg=self.colors['light'])
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
        
        # Mode Selection with modern card style
        mode_frame = tk.LabelFrame(
            content_frame, 
            text="  🔄 Mode Konversi  ", 
            font=("Segoe UI", 11, "bold"),
            fg=self.colors['dark'],
            bg="white",
            padx=20,
            pady=18,
            relief=tk.FLAT,
            bd=2,
            highlightbackground=self.colors['border'],
            highlightthickness=1
        )
        mode_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        tk.Radiobutton(
            mode_frame,
            text="📁 Convert dari Folder",
            variable=self.mode,
            value="folder",
            command=self.on_mode_change,
            font=("Segoe UI", 10),
            bg="white",
            fg=self.colors['text'],
            selectcolor=self.colors['light'],
            activebackground="white",
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=(0, 35))
        
        tk.Radiobutton(
            mode_frame,
            text="📷 Pilih File Foto Individual",
            variable=self.mode,
            value="files",
            command=self.on_mode_change,
            font=("Segoe UI", 10),
            bg="white",
            fg=self.colors['text'],
            selectcolor=self.colors['light'],
            activebackground="white",
            cursor="hand2"
        ).pack(side=tk.LEFT)
        
        # Folder Mode Frame with card style
        self.folder_frame = tk.Frame(content_frame, bg=self.colors['light'])
        self.folder_frame.grid(row=1, column=0, sticky="ew")
        
        # Folder selection button
        tk.Label(
            self.folder_frame, 
            text="📁 Pilih Folder yang Berisi Gambar:", 
            font=("Segoe UI", 11, "bold"),
            bg=self.colors['light'],
            fg=self.colors['dark']
        ).grid(row=0, column=0, sticky="w", pady=(0, 12))
        
        self.folder_select_btn = tk.Button(
            self.folder_frame, 
            text="🔍  Pilih Folder", 
            command=self.select_folder_to_convert,
            bg=self.colors['primary'],
            fg="white",
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
            padx=35,
            pady=12,
            relief=tk.FLAT,
            bd=0,
            activebackground=self.colors['primary_hover'],
            activeforeground="white"
        )
        self.folder_select_btn.grid(row=1, column=0, pady=(0, 12))
        
        self.folder_status_label = tk.Label(
            self.folder_frame,
            text="Belum ada folder dipilih",
            font=("Segoe UI", 9),
            fg=self.colors['text_light'],
            bg=self.colors['light'],
            wraplength=700
        )
        self.folder_status_label.grid(row=2, column=0, sticky="w", pady=(0, 18))
        
        # Merge folder PDFs option
        self.folder_merge_check = tk.Checkbutton(
            self.folder_frame,
            text="🔗 Gabungkan foto menjadi 1 PDF",
            variable=self.merge_folder_pdfs,
            command=self.on_folder_merge_change,
            font=("Segoe UI", 10, "bold"),
            fg=self.colors['dark'],
            bg=self.colors['light'],
            selectcolor=self.colors['light'],
            activebackground=self.colors['light'],
            cursor="hand2"
        )
        self.folder_merge_check.grid(row=3, column=0, sticky="w", pady=(0, 12))
        
        # Folder custom name field (for merged PDF)
        self.folder_custom_name_frame = tk.Frame(self.folder_frame, bg=self.colors['light'])
        self.folder_custom_name_frame.grid(row=4, column=0, sticky="ew", pady=(0, 20))
        
        tk.Label(
            self.folder_custom_name_frame,
            text="📝 Nama PDF (opsional):",
            font=("Segoe UI", 10),
            bg=self.colors['light'],
            fg=self.colors['text']
        ).pack(side=tk.LEFT, padx=(25, 12))
        
        self.folder_custom_name_entry = tk.Entry(
            self.folder_custom_name_frame,
            textvariable=self.folder_custom_name,
            font=("Segoe UI", 10),
            width=32,
            relief=tk.FLAT,
            bd=1,
            highlightthickness=2,
            highlightbackground=self.colors['border'],
            highlightcolor=self.colors['primary']
        )
        self.folder_custom_name_entry.pack(side=tk.LEFT, ipady=6)
        
        tk.Label(
            self.folder_custom_name_frame,
            text=".pdf",
            font=("Segoe UI", 10, "bold"),
            fg=self.colors['text_light'],
            bg=self.colors['light']
        ).pack(side=tk.LEFT, padx=(4, 0))
        
        self.folder_custom_name_frame.grid_remove()  # Hide initially
        
        self.folder_frame.columnconfigure(0, weight=1)
        
        # Files Mode Frame
        self.files_frame = tk.Frame(content_frame, bg=self.colors['light'])
        self.files_frame.grid(row=1, column=0, sticky="ew")
        
        tk.Label(
            self.files_frame, 
            text="📷 Pilih File Foto:", 
            font=("Segoe UI", 11, "bold"),
            bg=self.colors['light'],
            fg=self.colors['dark']
        ).grid(row=0, column=0, sticky="w", pady=(0, 8))
        
        files_btn_frame = tk.Frame(self.files_frame, bg=self.colors['light'])
        files_btn_frame.grid(row=1, column=0, sticky="ew", pady=(0, 12))
        
        self.browse_files_btn = tk.Button(
            files_btn_frame, 
            text="+  Pilih File Foto", 
            command=self.browse_files,
            bg=self.colors['primary'],
            fg="white",
            font=("Segoe UI", 9, "bold"),
            cursor="hand2",
            padx=25,
            pady=8,
            relief=tk.FLAT,
            bd=0,
            activebackground=self.colors['primary_hover'],
            activeforeground="white"
        )
        self.browse_files_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.clear_files_btn = tk.Button(
            files_btn_frame, 
            text="🗑  Clear All", 
            command=self.clear_files,
            bg=self.colors['danger'],
            fg="white",
            font=("Segoe UI", 9),
            cursor="hand2",
            padx=20,
            pady=8,
            relief=tk.FLAT,
            bd=0,
            activebackground=self.colors['danger_hover'],
            activeforeground="white"
        )
        self.clear_files_btn.pack(side=tk.LEFT)
        
        self.files_label = tk.Label(
            files_btn_frame,
            text="0 file dipilih",
            font=("Segoe UI", 9),
            fg=self.colors['text_light'],
            bg=self.colors['light']
        )
        self.files_label.pack(side=tk.LEFT, padx=(18, 0))
        
        # Files list frame with scrollbar
        files_list_frame = tk.LabelFrame(
            self.files_frame,
            text="  📋 Daftar Foto  ",
            font=("Segoe UI", 10, "bold"),
            fg=self.colors['dark'],
            bg="white",
            padx=12,
            pady=12,
            relief=tk.FLAT,
            bd=2,
            highlightbackground=self.colors['border'],
            highlightthickness=1
        )
        files_list_frame.grid(row=2, column=0, sticky="ew", pady=(0, 18))
        
        # Create main container with two columns: listbox + preview
        main_list_container = tk.Frame(files_list_frame, bg="white")
        main_list_container.pack(fill=tk.BOTH, expand=True)
        
        # Left side: Listbox with scrollbar
        list_container = tk.Frame(main_list_container, bg="white")
        list_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(list_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Listbox for files
        self.files_listbox = tk.Listbox(
            list_container,
            font=("Segoe UI", 9),
            height=6,
            yscrollcommand=scrollbar.set,
            selectmode=tk.SINGLE,
            relief=tk.FLAT,
            bd=1,
            highlightthickness=1,
            highlightbackground=self.colors['border'],
            highlightcolor=self.colors['primary'],
            selectbackground=self.colors['primary'],
            selectforeground="white"
        )
        self.files_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.files_listbox.yview)
        
        # Bind selection event for preview
        self.files_listbox.bind('<<ListboxSelect>>', self.on_file_select)
        
        # Right side: Preview panel
        preview_container = tk.Frame(main_list_container, bg=self.colors['light'], width=200)
        preview_container.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))
        preview_container.pack_propagate(False)
        
        tk.Label(
            preview_container,
            text="📷 Preview",
            font=("Segoe UI", 9, "bold"),
            bg=self.colors['light'],
            fg=self.colors['dark']
        ).pack(pady=(5, 8))
        
        # Preview image label
        self.preview_label = tk.Label(
            preview_container,
            text="Pilih foto untuk\nlihat preview",
            font=("Segoe UI", 9),
            fg=self.colors['text_light'],
            bg=self.colors['light'],
            justify=tk.CENTER,
            relief=tk.FLAT,
            bd=1,
            highlightthickness=1,
            highlightbackground=self.colors['border']
        )
        self.preview_label.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
        
        # Store current preview image reference to prevent garbage collection
        self.current_preview_image = None
        
        # Button frame for list actions
        list_actions = tk.Frame(files_list_frame, bg="white")
        list_actions.pack(fill=tk.X, pady=(10, 0))
        
        self.remove_file_btn = tk.Button(
            list_actions,
            text="🗑  Hapus Foto Dipilih",
            command=self.remove_selected_file,
            bg=self.colors['danger'],
            fg="white",
            font=("Segoe UI", 8, "bold"),
            cursor="hand2",
            padx=18,
            pady=6,
            relief=tk.FLAT,
            bd=0,
            activebackground=self.colors['danger_hover'],
            activeforeground="white"
        )
        self.remove_file_btn.pack(side=tk.LEFT)
        
        tk.Label(
            list_actions,
            text="Klik foto untuk pilih, lalu klik tombol hapus",
            font=("Segoe UI", 8),
            fg=self.colors['text_light'],
            bg="white"
        ).pack(side=tk.LEFT, padx=(18, 0))
                # Merge option
        merge_check = tk.Checkbutton(
            self.files_frame,
            text="🔗 Gabung semua foto jadi 1 PDF",
            variable=self.merge_files,
            command=self.on_merge_change,
            font=("Segoe UI", 10, "bold"),
            fg=self.colors['dark'],
            bg=self.colors['light'],
            selectcolor=self.colors['light'],
            activebackground=self.colors['light'],
            cursor="hand2"
        )
        merge_check.grid(row=3, column=0, sticky="w", pady=(0, 12))
        
        # Custom name field (for merged PDF)
        self.custom_name_frame = tk.Frame(self.files_frame, bg=self.colors['light'])
        self.custom_name_frame.grid(row=4, column=0, sticky="ew", pady=(0, 20))
        
        tk.Label(
            self.custom_name_frame,
            text="📝 Nama PDF (opsional):",
            font=("Segoe UI", 10),
            bg=self.colors['light'],
            fg=self.colors['text']
        ).pack(side=tk.LEFT, padx=(25, 12))
        
        self.custom_name_entry = tk.Entry(
            self.custom_name_frame,
            textvariable=self.custom_name,
            font=("Segoe UI", 10),
            width=32,
            relief=tk.FLAT,
            bd=1,
            highlightthickness=2,
            highlightbackground=self.colors['border'],
            highlightcolor=self.colors['primary']
        )
        self.custom_name_entry.pack(side=tk.LEFT, ipady=6)
        
        tk.Label(
            self.custom_name_frame,
            text=".pdf",
            font=("Segoe UI", 10, "bold"),
            fg=self.colors['text_light'],
            bg=self.colors['light']
        ).pack(side=tk.LEFT, padx=(4, 0))
        
        self.custom_name_frame.grid_remove()  # Hide initially
        
        self.files_frame.columnconfigure(0, weight=1)
        self.files_frame.grid_remove()  # Hide initially
        
        # Output Folder
        output_info_frame = tk.LabelFrame(
            content_frame,
            text="  💾 Lokasi Hasil PDF  ",
            font=("Segoe UI", 11, "bold"),
            fg=self.colors['dark'],
            bg="white",
            padx=18,
            pady=15,
            relief=tk.FLAT,
            bd=2,
            highlightbackground=self.colors['border'],
            highlightthickness=1
        )
        output_info_frame.grid(row=3, column=0, sticky="ew", pady=(0, 25))
        
        output_path_frame = tk.Frame(output_info_frame, bg="white")
        output_path_frame.pack(fill=tk.X)
        
        # Create a StringVar for the display path (avoid backslash issues on Windows)
        output_path = self.output_folder.get()
        date_str = datetime.now().strftime("%Y-%m-%d")
        self.display_output_path = tk.StringVar(
            value=os.path.join(output_path, date_str)
        )
        
        output_entry = tk.Entry(
            output_path_frame, 
            textvariable=self.display_output_path, 
            font=("Segoe UI", 10),
            state="readonly",
            relief=tk.FLAT,
            bd=1,
            readonlybackground=self.colors['light'],
            fg=self.colors['text']
        )
        output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8)
        
        self.change_output_btn = tk.Button(
            output_path_frame, 
            text="📂 Ubah", 
            command=self.browse_output,
            bg=self.colors['secondary'],
            fg="white",
            font=("Segoe UI", 9, "bold"),
            cursor="hand2",
            padx=20,
            pady=8,
            relief=tk.FLAT,
            bd=0,
            activebackground=self.colors['secondary_hover'],
            activeforeground="white"
        )
        self.change_output_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        content_frame.columnconfigure(0, weight=1)
        
        # Progress section
        progress_frame = tk.LabelFrame(
            content_frame, 
            text="  ⏳ Progress  ", 
            font=("Segoe UI", 11, "bold"),
            fg=self.colors['dark'],
            bg="white",
            padx=18,
            pady=15,
            relief=tk.FLAT,
            bd=2,
            highlightbackground=self.colors['border'],
            highlightthickness=1
        )
        progress_frame.grid(row=4, column=0, sticky="ew", pady=(0, 22))
        
        # Configure ttk.Progressbar style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure(
            "Modern.Horizontal.TProgressbar",
            troughcolor=self.colors['light'],
            bordercolor=self.colors['border'],
            background=self.colors['success'],
            lightcolor=self.colors['success'],
            darkcolor=self.colors['success'],
            thickness=20
        )
        
        self.progress_bar = ttk.Progressbar(
            progress_frame, 
            mode='determinate',
            length=600,
            style="Modern.Horizontal.TProgressbar"
        )
        self.progress_bar.pack(fill=tk.X, pady=(0, 10))
        
        self.status_label = tk.Label(
            progress_frame, 
            text="Ready to convert...",
            font=("Segoe UI", 10),
            fg=self.colors['text_light'],
            bg="white"
        )
        self.status_label.pack()
        
        # Buttons
        button_frame = tk.Frame(content_frame, bg=self.colors['light'])
        button_frame.grid(row=5, column=0, pady=(0, 18))
        
        self.convert_btn = tk.Button(
            button_frame,
            text="🚀  START CONVERSION",
            command=self.start_conversion,
            bg=self.colors['success'],
            fg="white",
            font=("Segoe UI", 13, "bold"),
            cursor="hand2",
            padx=50,
            pady=15,
            relief=tk.FLAT,
            bd=0,
            activebackground=self.colors['success_hover'],
            activeforeground="white"
        )
        self.convert_btn.pack(side=tk.LEFT, padx=10)
        
        # Footer info with card style
        footer_frame = tk.Frame(
            content_frame,
            bg=self.colors['primary'],
            relief=tk.FLAT,
            bd=0
        )
        footer_frame.grid(row=6, column=0, pady=(15, 0), sticky="ew")
        
        info_label = tk.Label(
            footer_frame,
            text="ℹ️  Format didukung: PNG, JPG, JPEG, GIF, BMP, TIFF, HEIC  •  File asli tidak akan dihapus",
            font=("Segoe UI", 9),
            fg="white",
            bg=self.colors['primary'],
            pady=12
        )
        info_label.pack()
        
    def select_folder_to_convert(self):
        folder = filedialog.askdirectory(title="Pilih Folder yang Berisi Gambar")
        if folder:
            self.input_folder.set(folder)
            self.folder_status_label.config(
                text=f"✓ Folder dipilih: {folder}",
                fg=self.colors['success']
            )
    
    def browse_output(self):
        folder = filedialog.askdirectory(
            title="Pilih Lokasi Penyimpanan PDF",
            initialdir=self.output_folder.get()
        )
        if folder:
            self.output_folder.set(folder)
            # Update display path with new folder and current date
            self.display_output_path.set(os.path.join(folder, datetime.now().strftime("%Y-%m-%d")))
    
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
            self.status_label.config(text="Ready to convert...", fg=self.colors['text_light'])
        else:
            # Switch to file mode
            self.folder_frame.grid_remove()
            self.files_frame.grid()
            # Reset folder mode selection
            self.input_folder.set("")
            self.folder_status_label.config(
                text="Belum ada folder dipilih",
                fg=self.colors['text_light']
            )
            # Reset folder merge options
            self.merge_folder_pdfs.set(False)
            self.folder_custom_name.set("")
            self.folder_custom_name_frame.grid_remove()
            self.status_label.config(text="Ready to convert...", fg=self.colors['text_light'])
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
    
    def on_file_select(self, event):
        """Show preview when a file is selected from the listbox"""
        selection = self.files_listbox.curselection()
        if not selection:
            return
        
        index = selection[0]
        if index >= len(self.selected_files):
            return
        
        file_path = self.selected_files[index]
        
        try:
            # Load image
            if file_path.lower().endswith(".heic"):
                if HEIF_SUPPORTED:
                    img = Image.open(file_path)
                else:
                    img_array = imageio.imread(file_path)
                    img = Image.fromarray(img_array)
            else:
                img = Image.open(file_path)
            
            # Get preview container size (approximately)
            preview_width = 180
            preview_height = 180
            
            # Calculate resize ratio to fit in preview area
            img_width, img_height = img.size
            ratio = min(preview_width / img_width, preview_height / img_height)
            new_width = int(img_width * ratio)
            new_height = int(img_height * ratio)
            
            # Resize image
            img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(img_resized)
            
            # Update preview label
            self.preview_label.config(image=photo, text="")
            self.current_preview_image = photo  # Keep reference to prevent garbage collection
            
        except Exception as e:
            # If error loading image, show error message
            self.preview_label.config(
                image="",
                text=f"Error loading\npreview:\n{str(e)[:30]}...",
                fg=self.colors['danger']
            )
            self.current_preview_image = None
    
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
            self.status_label.config(text="Foto dihapus dari list", fg=self.colors['warning'])
            
            # Clear preview
            self.preview_label.config(
                image="",
                text="Pilih foto untuk\nlihat preview",
                fg=self.colors['text_light']
            )
            self.current_preview_image = None
        else:
            messagebox.showinfo("Info", "Pilih foto yang ingin dihapus dari list terlebih dahulu")
    
    def clear_files(self):
        self.selected_files = []
        self.files_listbox.delete(0, tk.END)
        self.files_label.config(text="0 file dipilih")
        self.custom_name.set("")
        self.status_label.config(text="Files cleared", fg=self.colors['warning'])
        
        # Clear preview
        self.preview_label.config(
            image="",
            text="Pilih foto untuk\nlihat preview",
            fg=self.colors['text_light']
        )
        self.current_preview_image = None
    
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
        self.convert_btn.config(state=tk.DISABLED, bg=self.colors['secondary'])
        
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
            self.update_status("Error: Folder tidak valid!", self.colors['danger'])
            self.is_converting = False
            self.convert_btn.config(state=tk.NORMAL, bg=self.colors['success'])
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
                self.update_status("Mengumpulkan semua gambar...", self.colors['info'])
                
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
                                self.update_status(f"Loading: {item_name}", self.colors['info'])
                            except Exception as e:
                                self.update_status(f"⚠️ Gagal load: {item_name}", self.colors['warning'])
                        
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
                                            self.update_status(f"Loading: {file_name}", self.colors['info'])
                                        except:
                                            pass
                            except:
                                pass
                except Exception as e:
                    self.update_status(f"Error: {e}", self.colors['danger'])
                    self.is_converting = False
                    self.convert_btn.config(state=tk.NORMAL, bg=self.colors['success'])
                    return
                
                # SIMPAN SEMUA JADI 1 PDF
                if all_images:
                    self.update_status("Menggabungkan semua gambar jadi 1 PDF...", self.colors['info'])
                    
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
                    self.update_status("Menyimpan PDF gabungan...", self.colors['info'])
                    all_images[0].save(
                        merged_pdf_path,
                        save_all=True,
                        append_images=all_images[1:] if len(all_images) > 1 else []
                    )
                    
                    self.update_progress(100)
                    self.update_status(f"✓ Semua gambar berhasil digabung jadi 1 PDF!", self.colors['success'])
                    messagebox.showinfo(
                        "Success!",
                        f"Semua gambar berhasil digabung!\n\nFile: {merged_pdf_name}\nJumlah halaman: {len(all_images)}\nLokasi: {result_folder_with_date}"
                    )
                else:
                    self.update_status("⚠️ Tidak ada gambar ditemukan!", self.colors['warning'])
                    messagebox.showwarning("Warning", "Tidak ada gambar ditemukan di folder")
                
                # Reset after merge
                self.is_converting = False
                self.convert_btn.config(state=tk.NORMAL, bg=self.colors['success'])
                self.progress_bar['value'] = 0
                self.reset_after_conversion()
            
            # JIKA MERGE TIDAK DICENTANG - PER FILE INDIVIDUAL
            else:
                self.update_status("Mengonversi gambar...", self.colors['info'])
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
                    self.update_status(f"Error: {e}", self.colors['danger'])
                    self.is_converting = False
                    self.convert_btn.config(state=tk.NORMAL, bg=self.colors['success'])
                    return
                
                if total_items == 0:
                    self.update_status("⚠️ Tidak ada gambar di folder ini!", self.colors['warning'])
                    self.is_converting = False
                    self.convert_btn.config(state=tk.NORMAL, bg=self.colors['success'])
                    messagebox.showwarning("Warning", "Folder tidak berisi gambar atau subfolder dengan gambar")
                    return
                
                # Process individual files
                for item_type, item_name, item_path in items_list:
                    
                    if item_type == "file":
                        try:
                            self.update_status(f"Converting: {item_name}", self.colors['info'])
                            
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
                            self.update_status(f"Error: {item_name} - {str(e)}", self.colors['danger'])
                            processed_items += 1
                    
                    elif item_type == "folder":
                        try:
                            self.update_status(f"Processing folder: {item_name}", self.colors['info'])
                            
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
                            self.update_status(f"Error: {item_name} - {str(e)}", self.colors['danger'])
                            processed_items += 1
                
                # Regular completion message (no merge)
                self.update_progress(100)
                self.update_status(f"✓ Conversion complete! {len(converted_files)} PDFs created", self.colors['success'])
                self.is_converting = False
                self.convert_btn.config(state=tk.NORMAL, bg=self.colors['success'])
                
                messagebox.showinfo(
                    "Success!", 
                    f"Conversion completed!\n\n{len(converted_files)} PDF files created in:\n{result_folder_with_date}"
                )
                self.progress_bar['value'] = 0
                self.reset_after_conversion()
            
        except Exception as e:
            self.update_status(f"Error: {str(e)}", self.colors['danger'])
            self.is_converting = False
            self.convert_btn.config(state=tk.NORMAL, bg=self.colors['success'])
    
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
            fg=self.colors['text_light']
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
        self.status_label.config(text="Ready to convert...", fg=self.colors['text_light'])
        
        # Reset button
        self.is_converting = False
        self.convert_btn.config(state=tk.NORMAL, bg=self.colors['success'])
    
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
            self.update_status("Menggabungkan semua foto jadi 1 PDF...", self.colors['info'])
            
            image_list = []
            for i, file_path in enumerate(self.selected_files):
                try:
                    file_name = os.path.basename(file_path)
                    self.update_status(f"Loading: {file_name}", self.colors['info'])
                    
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
                    self.update_status(f"Error: {file_name} - {e}", self.colors['danger'])
            
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
                    self.update_status(f"⚠️ File sudah ada, disimpan sebagai: {output_pdf_name}", self.colors['warning'])
                
                self.update_status("Menyimpan PDF...", self.colors['info'])
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
                    
                    self.update_status(f"Converting: {file_name}", self.colors['info'])
                    
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
                    self.update_status(f"Error: {file_name} - {e}", self.colors['danger'])
        
        # Done
        self.update_progress(100)
        self.update_status(f"✓ Conversion complete! {len(converted_files)} PDF created", self.colors['success'])
        self.is_converting = False
        self.convert_btn.config(state=tk.NORMAL, bg=self.colors['success'])
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
    
    def setup_button_hover_effects(self):
        """Setup hover effects for buttons"""
        buttons = [
            (self.convert_btn, self.colors['success'], self.colors['success_hover']),
        ]
        
        # Only add buttons that exist at initialization
        if hasattr(self, 'folder_select_btn'):
            buttons.append((self.folder_select_btn, self.colors['primary'], self.colors['primary_hover']))
        if hasattr(self, 'browse_files_btn'):
            buttons.append((self.browse_files_btn, self.colors['primary'], self.colors['primary_hover']))
        if hasattr(self, 'clear_files_btn'):
            buttons.append((self.clear_files_btn, self.colors['danger'], self.colors['danger_hover']))
        if hasattr(self, 'remove_file_btn'):
            buttons.append((self.remove_file_btn, self.colors['danger'], self.colors['danger_hover']))
        if hasattr(self, 'change_output_btn'):
            buttons.append((self.change_output_btn, self.colors['secondary'], self.colors['secondary_hover']))
        
        for btn, normal_color, hover_color in buttons:
            btn.bind('<Enter>', lambda e, b=btn, hc=hover_color: b.config(bg=hc) if b['state'] != 'disabled' else None)
            btn.bind('<Leave>', lambda e, b=btn, nc=normal_color: b.config(bg=nc) if b['state'] != 'disabled' else None)


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
