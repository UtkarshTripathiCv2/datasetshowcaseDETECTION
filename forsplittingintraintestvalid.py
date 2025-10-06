import os
import random
import shutil

# --- Configuration ---
# Path to the main folder containing 'images' and 'labels' folders
SOURCE_DIR = "dataset" 
# Path to the folder where 'train', 'valid', and 'test' folders will be created
OUTPUT_DIR = "output" 

# Ratios for splitting the data
# The rest will be assigned to the test set
TRAIN_RATIO = 0.7  # 70% for training
VALID_RATIO = 0.15 # 15% for validation
# TEST_RATIO will be 15% (1.0 - 0.7 - 0.15)

# --- Get subdirectories ---
source_images_dir = os.path.join(SOURCE_DIR, "images")
source_labels_dir = os.path.join(SOURCE_DIR, "labels")

# --- Create destination directories ---
# Base directories
train_dir = os.path.join(OUTPUT_DIR, "train")
valid_dir = os.path.join(OUTPUT_DIR, "valid")
test_dir = os.path.join(OUTPUT_DIR, "test")

# Subdirectories for images and labels
# Train
train_images_dir = os.path.join(train_dir, "images")
train_labels_dir = os.path.join(train_dir, "labels")
# Validation
valid_images_dir = os.path.join(valid_dir, "images")
valid_labels_dir = os.path.join(valid_dir, "labels")
# Test
test_images_dir = os.path.join(test_dir, "images")
test_labels_dir = os.path.join(test_dir, "labels")

# Create all directories if they don't exist
for path in [train_images_dir, train_labels_dir, valid_images_dir, valid_labels_dir, test_images_dir, test_labels_dir]:
    os.makedirs(path, exist_ok=True)

print("Created output directory structure successfully! ✅")

# --- Splitting Logic ---
# Get list of all image files
image_files = [f for f in os.listdir(source_images_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
# Shuffle the list randomly
random.shuffle(image_files)

# Calculate split indices
total_files = len(image_files)
train_end = int(total_files * TRAIN_RATIO)
valid_end = train_end + int(total_files * VALID_RATIO)

# Split the file list
train_files = image_files[:train_end]
valid_files = image_files[train_end:valid_end]
test_files = image_files[valid_end:]

# --- Function to copy files ---
def copy_files(file_list, src_img_dir, src_lbl_dir, dest_img_dir, dest_lbl_dir):
    copied_count = 0
    for filename in file_list:
        basename = os.path.splitext(filename)[0]
        label_filename = basename + ".txt"

        # Source paths
        src_image_path = os.path.join(src_img_dir, filename)
        src_label_path = os.path.join(src_lbl_dir, label_filename)

        # Destination paths
        dest_image_path = os.path.join(dest_img_dir, filename)
        dest_label_path = os.path.join(dest_lbl_dir, label_filename)

        # Copy image file
        shutil.copy(src_image_path, dest_image_path)
        
        # Copy label file if it exists
        if os.path.exists(src_label_path):
            shutil.copy(src_label_path, dest_label_path)
        else:
            print(f"Warning: Label file not found for image {filename}")
        
        copied_count += 1
    return copied_count

# --- Copy files to their new directories ---
print("\nCopying training files...")
train_count = copy_files(train_files, source_images_dir, source_labels_dir, train_images_dir, train_labels_dir)
print(f"Copied {train_count} files to the training set.")

print("\nCopying validation files...")
valid_count = copy_files(valid_files, source_images_dir, source_labels_dir, valid_images_dir, valid_labels_dir)
print(f"Copied {valid_count} files to the validation set.")

print("\nCopying testing files...")
test_count = copy_files(test_files, source_images_dir, source_labels_dir, test_images_dir, test_labels_dir)
print(f"Copied {test_count} files to the testing set.")

print("\nDataset splitting complete! 🎉")
