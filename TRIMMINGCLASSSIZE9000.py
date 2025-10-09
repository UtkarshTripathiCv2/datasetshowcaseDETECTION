import os
import shutil
import random
from collections import defaultdict
import yaml

# --- CONFIGURATION ---
# Set the limit for images per class
IMAGE_LIMIT = 9000

# Set up the paths. This script assumes both folders are on your Desktop.
# os.path.expanduser('~') gets the path to your home directory (e.g., C:/Users/Utkarsh)
desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
source_dataset_path = os.path.join(desktop_path, 'ALLmaster_dataset')
output_dataset_path = os.path.join(desktop_path, 'folder9000')
source_yaml_name = 'master.yaml' # The name of your yaml file in the source folder

# --- SCRIPT LOGIC (No need to edit below this line) ---

def find_image_file(label_path, image_dir):
    """Finds the corresponding image file for a given label file."""
    base_name = os.path.splitext(os.path.basename(label_path))[0]
    for ext in ['.jpg', '.jpeg', '.png', '.bmp', '.webp']:
        image_path = os.path.join(image_dir, base_name + ext)
        if os.path.exists(image_path):
            return image_path
    return None

def main():
    print("🚀 Starting dataset balancing process...")
    
    if not os.path.exists(source_dataset_path):
        print(f"❌ Error: Source dataset folder not found at '{source_dataset_path}'")
        return

    # --- 1. Scan the dataset and build an index of images per class ---
    print("\n🔍 Step 1: Scanning dataset and indexing images by class...")
    class_to_images = defaultdict(list)
    image_to_split = {} # To remember if an image is in train, valid, or test

    for split in ['train', 'valid', 'test']:
        label_dir = os.path.join(source_dataset_path, split, 'labels')
        image_dir = os.path.join(source_dataset_path, split, 'images')
        
        if not os.path.exists(label_dir):
            print(f"   - Warning: No '{split}/labels' directory found. Skipping.")
            continue
        
        print(f"   - Processing '{split}' split...")
        label_files = [f for f in os.listdir(label_dir) if f.endswith('.txt')]
        
        for label_file in label_files:
            label_path = os.path.join(label_dir, label_file)
            image_path = find_image_file(label_path, image_dir)
            
            if image_path is None:
                continue

            image_name = os.path.basename(image_path)
            image_to_split[image_name] = split
            
            with open(label_path, 'r') as f:
                # Use a set to only count an image once per class it contains
                classes_in_image = set()
                for line in f:
                    try:
                        class_id = int(line.strip().split()[0])
                        classes_in_image.add(class_id)
                    except (ValueError, IndexError):
                        continue # Ignore empty or malformed lines
                
                for class_id in classes_in_image:
                    class_to_images[class_id].append(image_name)

    print("✅ Indexing complete.")
    for class_id, images in class_to_images.items():
        print(f"   - Class {class_id}: Found {len(images)} images.")

    # --- 2. Trim the lists for classes exceeding the limit ---
    print(f"\n✂️ Step 2: Trimming classes with more than {IMAGE_LIMIT} images...")
    images_to_keep = set()

    for class_id, images in class_to_images.items():
        if len(images) > IMAGE_LIMIT:
            print(f"   - Class {class_id} has {len(images)} images. Reducing to {IMAGE_LIMIT}.")
            trimmed_list = random.sample(images, IMAGE_LIMIT)
            images_to_keep.update(trimmed_list)
        else:
            # If the class is within the limit, keep all its images
            images_to_keep.update(images)
    
    print(f"✅ Trimming complete. Total unique images to keep: {len(images_to_keep)}")

    # --- 3. Create the new dataset structure and copy files ---
    print("\n📁 Step 3: Creating new dataset and copying files...")
    
    # Remove old output directory if it exists for a clean start
    if os.path.exists(output_dataset_path):
        print(f"   - Found existing '{os.path.basename(output_dataset_path)}' folder. Removing it.")
        shutil.rmtree(output_dataset_path)

    # Create new directory structure
    for split in ['train', 'valid', 'test']:
        os.makedirs(os.path.join(output_dataset_path, split, 'images'), exist_ok=True)
        os.makedirs(os.path.join(output_dataset_path, split, 'labels'), exist_ok=True)
    
    # Copy the selected files
    copied_count = 0
    for image_name in images_to_keep:
        split = image_to_split[image_name]
        
        # Source paths
        source_img_path = os.path.join(source_dataset_path, split, 'images', image_name)
        label_name = os.path.splitext(image_name)[0] + '.txt'
        source_lbl_path = os.path.join(source_dataset_path, split, 'labels', label_name)
        
        # Destination paths
        dest_img_path = os.path.join(output_dataset_path, split, 'images', image_name)
        dest_lbl_path = os.path.join(output_dataset_path, split, 'labels', label_name)
        
        if os.path.exists(source_img_path) and os.path.exists(source_lbl_path):
            shutil.copy2(source_img_path, dest_img_path)
            shutil.copy2(source_lbl_path, dest_lbl_path)
            copied_count += 1

    print(f"   - Successfully copied {copied_count} image/label pairs.")

    # --- 4. Copy the YAML file ---
    print("\n📝 Step 4: Copying YAML file...")
    source_yaml_path = os.path.join(source_dataset_path, source_yaml_name)
    dest_yaml_path = os.path.join(output_dataset_path, 'dataset.yaml') # Standard name

    if os.path.exists(source_yaml_path):
        # We need to update the path in the YAML to be relative
        with open(source_yaml_path, 'r') as f:
            data = yaml.safe_load(f)
        
        data['path'] = '../' + os.path.basename(output_dataset_path)
        data['train'] = './train/images'
        data['val'] = './valid/images' # YAML standard is often 'val'
        data['test'] = './test/images'

        with open(dest_yaml_path, 'w') as f:
            yaml.dump(data, f, sort_keys=False)

        print(f"   - Copied and updated '{source_yaml_name}' to '{os.path.basename(dest_yaml_path)}'.")
    else:
        print(f"   - Warning: YAML file '{source_yaml_name}' not found in source directory.")

    print("\n\n🎉 All done! Your new balanced dataset is ready in 'folder9000' on your Desktop.")


# Run the main function
if __name__ == '__main__':
    main()
