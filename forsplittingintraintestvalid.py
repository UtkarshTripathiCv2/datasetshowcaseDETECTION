import os
import random
import shutil

# --- Configuration ---
# Set to "." because the script is in the same folder as 'images' and 'labels'
SOURCE_DIR = "." 
OUTPUT_DIR = "output" 
TRAIN_RATIO = 0.7
VALID_RATIO = 0.15

# --- Get subdirectories ---
source_images_dir = os.path.join(SOURCE_DIR, "images")
source_labels_dir = os.path.join(SOURCE_DIR, "labels")

print("--- Initial Setup ---")
print(f"[*] Reading from: {os.path.abspath(source_images_dir)}")
if not os.path.isdir(source_images_dir):
    print("\n[FATAL ERROR] 'images' directory not found! ❌")
    exit()
print("[SUCCESS] Image directory found! ✅")

# --- Find Files ---
image_files = [f for f in os.listdir(source_images_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
print(f"[*] Found {len(image_files)} total images.")
if len(image_files) == 0:
    print("\n[FATAL ERROR] No images found in the 'images' directory. ❌")
    exit()
print("--- Setup Complete ---\n")

# --- Create destination directories ---
os.makedirs(os.path.join(OUTPUT_DIR, "train", "images"), exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "train", "labels"), exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "valid", "images"), exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "valid", "labels"), exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "test", "images"), exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "test", "labels"), exist_ok=True)
print("Created output directory structure successfully!\n")

# --- Splitting Logic ---
random.shuffle(image_files)
total_files = len(image_files)
train_end = int(total_files * TRAIN_RATIO)
valid_end = train_end + int(total_files * VALID_RATIO)

train_files = image_files[:train_end]
valid_files = image_files[train_end:valid_end]
test_files = image_files[valid_end:]

print("--- Data Split Calculation ---")
print(f"[*] Total images to split: {total_files}")
print(f"[*] Training files count: {len(train_files)}")
print(f"[*] Validation files count: {len(valid_files)}")
print(f"[*] Testing files count: {len(test_files)}\n")

# --- File Copying Process ---
def copy_files(file_list, source_img_dir, source_lbl_dir, dest_folder_name):
    for filename in file_list:
        basename = os.path.splitext(filename)[0]
        label_filename = basename + ".txt"
        
        src_image_path = os.path.join(source_img_dir, filename)
        src_label_path = os.path.join(source_lbl_dir, label_filename)

        dest_image_path = os.path.join(OUTPUT_DIR, dest_folder_name, "images", filename)
        dest_label_path = os.path.join(OUTPUT_DIR, dest_folder_name, "labels", label_filename)

        shutil.copy(src_image_path, dest_image_path)
        if os.path.exists(src_label_path):
            shutil.copy(src_label_path, dest_label_path)

print("--- Starting File Copy ---")

# Copy Train Files
print(f"[*] Copying {len(train_files)} training files...")
copy_files(train_files, source_images_dir, source_labels_dir, "train")
print("[SUCCESS] Training files copied.\n")

# Copy Validation Files
print(f"[*] Copying {len(valid_files)} validation files...")
copy_files(valid_files, source_images_dir, source_labels_dir, "valid")
print("[SUCCESS] Validation files copied.\n")

# Copy Test Files
print(f"[*] Copying {len(test_files)} testing files...")
copy_files(test_files, source_images_dir, source_labels_dir, "test")
print("[SUCCESS] Testing files copied.\n")

print("--- All tasks complete! 🎉 ---")
