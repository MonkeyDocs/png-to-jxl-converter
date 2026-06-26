import os
import sys
import piexif
import piexif.helper
from PIL import Image, ImageChops

# === THE FIX: Force Pillow to register and accept the JXL format ===
try:
    import pillow_jxl
except ImportError:
    print("[-] CRITICAL ERROR: 'pillow_jxl' module could not be found.")
    print("    Make sure you are running this script using the WebUI's venv python executable!")
    sys.exit(1)
# ===================================================================

# ==================== CONFIGURATION ====================
USE_MULTIPROCESSING = True  # TRUE = Use all CPU cores (Fast!) | FALSE = Single thread
NUM_WORKERS = None          # None uses all cores (12 threads on 5600x). Or set an integer.
EFFORT = 9                  # Max compression efficiency
DELETE_ON_SUCCESS = False   # Set to True ONLY after testing!
# =======================================================

def convert_png_to_jxl_with_webui_metadata(png_path):
    base, _ = os.path.splitext(png_path)
    jxl_path = base + ".jxl"
    
    try:
        with Image.open(png_path) as img:
            # Extract the WebUI parameters text chunk
            metadata_text = img.info.get("parameters", "")
            orig_rgb = img.convert("RGB")
            
            save_args = {"lossless": True, "effort": EFFORT}
            
            # Convert text chunk into binary EXIF UserComment block
            if metadata_text:
                exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}
                exif_dict["Exif"][piexif.ExifIFD.UserComment] = piexif.helper.UserComment.dump(
                    metadata_text, encoding="unicode"
                )
                save_args["exif"] = piexif.dump(exif_dict)
            
            # This will now succeed because pillow_jxl is imported above
            img.save(jxl_path, **save_args)

        # Strict Pixel Verification
        with Image.open(jxl_path) as jxl_img:
            jxl_rgb = jxl_img.convert("RGB")
            if orig_rgb.size != jxl_rgb.size or ImageChops.difference(orig_rgb, jxl_rgb).getbbox() is not None:
                raise ValueError("Pixel data validation failed.")
                
        print(f"[✓] Converted: {os.path.basename(png_path)}")
        if DELETE_ON_SUCCESS:
            os.remove(png_path)
        return True

    except Exception as e:
        print(f"[X] Failed {os.path.basename(png_path)}: {e}")
        if os.path.exists(jxl_path):
            os.remove(jxl_path)
        return False

def main():
    # Safely resolve target directory inside the main process loop
    if len(sys.argv) > 1:
        target_dir = sys.argv[1]
    else:
        target_dir = os.getcwd()

    if not os.path.isdir(target_dir):
        print(f"Error: '{target_dir}' is not a valid directory.")
        return

    png_files = [os.path.join(target_dir, f) for f in os.listdir(target_dir) if f.lower().endswith('.png')]
    total = len(png_files)
    
    print(f"Target Folder: {target_dir}")
    success = 0
    
    if USE_MULTIPROCESSING and total > 0:
        from multiprocessing import Pool
        print(f"Starting parallel batch conversion of {total} PNGs using multiprocessing...")
        
        with Pool(processes=NUM_WORKERS) as pool:
            # imap_unordered lets us process images across all 12 threads concurrently
            for result in pool.imap_unordered(convert_png_to_jxl_with_webui_metadata, png_files):
                if result:
                    success += 1
    else:
        print(f"Starting sequential batch conversion of {total} PNGs (Single-threaded)...")
        for idx, png_path in enumerate(png_files, 1):
            print(f"[{idx}/{total}] ", end="")
            if convert_png_to_jxl_with_webui_metadata(png_path):
                success += 1
            
    print(f"\n🏁 Finished! Successfully converted {success}/{total} images.")

if __name__ == "__main__":
    main()