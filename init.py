import os
from PIL import Image
import imageio.v2 as imageio
import sys
import shutil
from datetime import datetime


def get_directory_input(prompt, default_path=None):
    """Get directory input from user with optional default"""
    if default_path:
        user_input = input(f"{prompt} (default: {default_path}): ").strip()
        return user_input if user_input else default_path
    else:
        while True:
            user_input = input(f"{prompt}: ").strip()
            if user_input:
                return user_input
            print("Path tidak boleh kosong!")


def count_items(folder_path, supported_formats):
    """Count images in root folder and subfolders (first level only)"""
    total_images = 0
    total_subfolders = 0
    
    # Count images in root folder
    try:
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path) and any(file_name.lower().endswith(ext) for ext in supported_formats):
                total_images += 1
            elif os.path.isdir(file_path):
                # Count this subfolder
                total_subfolders += 1
    except Exception as e:
        print(f"Error membaca folder: {e}")
    
    return total_images, total_subfolders


def update_progress(processed_items, total_items, current_file=""):
    """Update progress bar"""
    progress = (processed_items / total_items) * 100 if total_items > 0 else 0
    bar_length = 40
    filled = int(bar_length * processed_items / total_items) if total_items > 0 else 0
    bar = '█' * filled + '░' * (bar_length - filled)
    
    sys.stdout.write(f"\r[{bar}] {processed_items}/{total_items} ({progress:.1f}%) - {current_file}")
    sys.stdout.flush()


def get_unique_name(parent_folder, base_name, extension=""):
    """Generate unique name for file or folder"""
    counter = 1
    new_name = base_name + extension
    while os.path.exists(os.path.join(parent_folder, new_name)):
        new_name = f"{base_name}({counter}){extension}"
        counter += 1
    return new_name


def process_folders(folder_path, result_folder):
    """Main function to process images and convert to PDF"""
    # Supported image formats
    supported_formats = [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".heic"]

    # Create RESULT folder with date
    date_str = datetime.now().strftime("%Y-%m-%d")
    result_folder_with_date = os.path.join(result_folder, date_str)
    os.makedirs(result_folder_with_date, exist_ok=True)

    # Count total items
    total_images, total_subfolders = count_items(folder_path, supported_formats)
    total_items = total_images + total_subfolders
    
    if total_images == 0 and total_subfolders == 0:
        print("Tidak ada gambar untuk dikonversi.")
        return

    print(f"\n{'='*60}")
    print(f"MEMULAI KONVERSI GAMBAR KE PDF")
    print(f"{'='*60}")
    print(f"Folder input : {folder_path}")
    print(f"Folder output: {result_folder_with_date}")
    print(f"\nTotal gambar di root: {total_images}")
    print(f"Total subfolder      : {total_subfolders}")
    print(f"{'='*60}\n")

    processed_items = 0
    converted_files = []
    skipped_files = []

    # Process individual image files in root folder
    try:
        items = sorted(os.listdir(folder_path))
    except Exception as e:
        print(f"Error membaca folder: {e}")
        return

    for item_name in items:
        item_path = os.path.join(folder_path, item_name)
        
        # Process individual image files
        if os.path.isfile(item_path) and any(item_name.lower().endswith(ext) for ext in supported_formats):
            try:
                base_name = os.path.splitext(item_name)[0]
                output_pdf_name = get_unique_name(result_folder_with_date, base_name, ".pdf")
                output_pdf_path = os.path.join(result_folder_with_date, output_pdf_name)
                
                update_progress(processed_items, total_items, f"Converting: {item_name}")
                
                # Read and convert image to RGB
                if item_name.lower().endswith(".heic"):
                    img = imageio.imread(item_path)
                    img = Image.fromarray(img).convert("RGB")
                else:
                    img = Image.open(item_path).convert("RGB")

                # Save as PDF
                img.save(output_pdf_path)
                converted_files.append(output_pdf_path)
                
                processed_items += 1
                update_progress(processed_items, total_items, f"✓ {item_name}")

            except Exception as e:
                print(f"\n✗ Error memproses '{item_name}': {e}")
                processed_items += 1

    # Process subfolders (first level only)
    for item_name in items:
        item_path = os.path.join(folder_path, item_name)
        
        if os.path.isdir(item_path):
            try:
                update_progress(processed_items, total_items, f"Processing folder: {item_name}")
                
                # Collect images from subfolder
                image_list = []
                subfolder_files = []
                
                try:
                    subfolder_items = sorted(os.listdir(item_path))
                except Exception as e:
                    print(f"\n✗ Error membaca subfolder '{item_name}': {e}")
                    processed_items += 1
                    continue
                
                for file_name in subfolder_items:
                    file_path = os.path.join(item_path, file_name)
                    
                    if os.path.isfile(file_path) and any(file_name.lower().endswith(ext) for ext in supported_formats):
                        try:
                            # Read and convert image
                            if file_name.lower().endswith(".heic"):
                                img = imageio.imread(file_path)
                                img = Image.fromarray(img).convert("RGB")
                            else:
                                img = Image.open(file_path).convert("RGB")
                            
                            image_list.append(img)
                            subfolder_files.append(file_path)
                        except Exception as e:
                            print(f"\n✗ Error memproses '{file_name}' dalam folder '{item_name}': {e}")

                # Save as single PDF if images found
                if image_list:
                    output_pdf_name = get_unique_name(result_folder_with_date, item_name, ".pdf")
                    output_pdf_path = os.path.join(result_folder_with_date, output_pdf_name)
                    
                    image_list[0].save(
                        output_pdf_path,
                        save_all=True,
                        append_images=image_list[1:] if len(image_list) > 1 else []
                    )
                    converted_files.append(output_pdf_path)
                    
                    processed_items += 1
                    update_progress(processed_items, total_items, f"✓ {item_name} ({len(image_list)} images)")
                else:
                    processed_items += 1
                    update_progress(processed_items, total_items, f"⊘ {item_name} (no images)")
                    
            except Exception as e:
                print(f"\n✗ Error memproses subfolder '{item_name}': {e}")
                processed_items += 1

    # Final summary
    print(f"\n\n{'='*60}")
    print(f"KONVERSI SELESAI!")
    print(f"{'='*60}")
    print(f"Total PDF berhasil dibuat: {len(converted_files)}")
    
    if converted_files:
        print(f"\nDaftar file PDF yang berhasil dibuat:")
        for file in converted_files:
            print(f"  ✓ {os.path.basename(file)}")
    
    if skipped_files:
        print(f"\nDaftar file yang dilewati:")
        for file in skipped_files:
            print(f"  ⊘ {os.path.basename(file)}")
    
    print(f"\nLokasi output: {result_folder_with_date}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    print(f"\n{'='*60}")
    print("IMAGE TO PDF CONVERTER")
    print(f"{'='*60}\n")
    
    # Check if arguments provided via command line
    if len(sys.argv) >= 3:
        # Use command line arguments
        folder_path = sys.argv[1]
        result_folder = sys.argv[2]
        
        print("Mode: Command Line Arguments")
        
    else:
        # Interactive mode - ask user for paths
        print("Mode: Interactive Input")
        print("\nMasukkan path untuk folder-folder berikut:")
        print("(Tekan Enter untuk menggunakan default jika tersedia)\n")
        
        # Get script directory for default paths
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Input folder (BAHAN)
        default_input = os.path.join(script_dir, "BAHAN")
        folder_path = get_directory_input(
            "Folder input (gambar yang akan dikonversi)",
            default_input
        )
        
        # Result folder
        default_result = os.path.join(script_dir, "HASIL")
        result_folder = get_directory_input(
            "Folder output (hasil PDF)",
            default_result
        )
    
    # Create folders if they don't exist
    os.makedirs(folder_path, exist_ok=True)
    os.makedirs(result_folder, exist_ok=True)
    
    print(f"\n✓ Folder input : {folder_path}")
    print(f"✓ Folder output: {result_folder}")
    
    # Start processing
    try:
        process_folders(folder_path, result_folder)
    except KeyboardInterrupt:
        print("\n\n✗ Proses dibatalkan oleh user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n✗ Error: {e}")
        sys.exit(1)
