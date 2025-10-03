import os
import shutil
from pathlib import Path
import yaml

# ===================================================================
# SETUP: YOU ONLY NEED TO EDIT THESE THREE VARIABLES
# ===================================================================

# 1. Path to the single YOLO dataset you want to filter
source_dataset_path = Path(r"C:\Users\HP\Desktop\NOTMASTER")

# 2. Path where the new, filtered dataset will be created
output_path = Path(r"C:\Users\HP\Desktop\FilteredDataset")

# 3. List of class names you want to KEEP in the new dataset
#    (Names must exactly match the names in your source data.yaml file)
selected_classes = [
 'Ants',
    'Bees',
    'Beetles',
    'COW',
    'Caterpillars',
    'Corn leaf blight',
    'Early Blight',
    'Earthworms',
    'Earwigs',
    'Grasshoppers',
    'Healthy',
    'Healthy Wheat',
    'Late Blight',
    'Leaf Miner',
    'Leaf Mold',
    'Mosaic Virus',
    'Moths',
    'Potato leaf',
    'Potato leaf early blight',
    'Potato leaf late blight',
    'Septoria',
    'Slugs',
    'Snails',
    'Spider Mites',
    'Squash Powdery mildew leaf',
    'Tomato Early blight leaf',  
    'Tomato Septoria leaf spot', 
    'Tomato leaf',
    'Tomato leaf bacterial spot',
    'Tomato leaf late blight',   
    'Tomato leaf mosaic virus',  
    'Tomato leaf yellow virus',  
    'Tomato mold leaf',
    'Tomato two spotted spider mites leaf',
    'Wasps',
    'Weevils',
    'Yellow Leaf Curl Virus',    
    'fire',
    'horse',
    'pig',
    'sheep',
    'smoke',
]
# ===================================================================

def get_class_list_from_yaml(yaml_path):
    """Reads a YOLO data.yaml file and returns the list of class names."""
    try:
        with open(yaml_path, 'r') as f:
            data = yaml.safe_load(f)
            if 'names' in data:
                return [str(name).strip() for name in data['names']]
    except Exception as e:
        print(f"⚠ Error reading {yaml_path}: {e}")
    return []

def filter_and_copy_files(split, old_classes, new_class_map):
    """
    Reads label files, keeps only selected classes with new IDs,
    and copies the corresponding images and new labels to the output folder.
    """
    image_dir = source_dataset_path / split / 'images'
    label_dir = source_dataset_path / split / 'labels'

    if not label_dir.is_dir() or not image_dir.is_dir():
        print(f"   ⚠ Skipping '{split}' (missing images or labels directory).")
        return 0

    dest_img_dir = output_path / split / 'images'
    dest_lbl_dir = output_path / split / 'labels'
    dest_img_dir.mkdir(parents=True, exist_ok=True)
    dest_lbl_dir.mkdir(parents=True, exist_ok=True)

    images_copied_count = 0

    for label_file_name in os.listdir(label_dir):
        if not label_file_name.endswith('.txt'):
            continue

        new_labels = []
        with open(label_dir / label_file_name, 'r') as f:
            for line in f.readlines():
                parts = line.strip().split()
                if not parts:
                    continue

                old_cls_id = int(parts[0])

                if old_cls_id < len(old_classes):
                    class_name = old_classes[old_cls_id]
                    # Check if this class is one we want to keep
                    if class_name in new_class_map:
                        new_cls_id = new_class_map[class_name]
                        new_line = f"{new_cls_id} {' '.join(parts[1:])}"
                        new_labels.append(new_line)
                else:
                    print(f"     ⚠ Invalid class index {old_cls_id} in {label_file_name}")

        # If the file contains any of the selected classes, save the new label file and copy the image
        if new_labels:
            # Write the new label file
            with open(dest_lbl_dir / label_file_name, 'w') as f:
                f.write('\n'.join(new_labels))

            # Find and copy the corresponding image
            copied = False
            for ext in ['.jpg', '.jpeg', '.png', '.bmp', '.webp']:
                image_path = image_dir / f"{Path(label_file_name).stem}{ext}"
                if image_path.exists():
                    shutil.copy(image_path, dest_img_dir / f"{Path(label_file_name).stem}{ext}")
                    copied = True
                    images_copied_count += 1
                    break
            
            if not copied:
                print(f"     ⚠ Image not found for label: {label_file_name}")

    return images_copied_count

def create_output_yaml():
    """Creates the final data.yaml for the new filtered dataset."""
    yaml_path = output_path / "data.yaml"
    with open(yaml_path, "w") as f:
        f.write(f"train: ../{output_path.name}/train/images\n")
        f.write(f"val: ../{output_path.name}/valid/images\n")
        f.write(f"test: ../{output_path.name}/test/images\n\n")
        f.write("names:\n")
        for i, name in enumerate(selected_classes):
            f.write(f"  {i}: {name}\n")
    print(f"\n📄 New YAML created at: {yaml_path}")


if __name__ == '__main__':
    print("🚀 Starting dataset filtering process...")
    
    # Ensure the PyYAML package is installed
    try:
        import yaml
    except ImportError:
        print("❌ PyYAML is not installed. Please run: pip install PyYAML")
        exit()

    yaml_file = source_dataset_path / 'data.yaml'
    if not yaml_file.exists():
        print(f"❌ Critical Error: 'data.yaml' not found in {source_dataset_path}")
        exit()

    print(f"\n📂 Processing dataset: {source_dataset_path.name}")
    original_class_list = get_class_list_from_yaml(yaml_file)
    
    if not original_class_list:
        print(f"❌ Could not read classes from {yaml_file}. Aborting.")
        exit()

    print(f"  Found {len(original_class_list)} original classes.")
    print(f"  Filtering to keep {len(selected_classes)} selected classes.")

    # Create a mapping from the selected class name to its new ID (0, 1, 2...)
    new_class_mapping = {name: i for i, name in enumerate(selected_classes)}

    total_images = 0
    for split in ['train', 'valid', 'test']:
        print(f"  → Processing '{split}' split...")
        count = filter_and_copy_files(split, original_class_list, new_class_mapping)
        if count > 0:
            print(f"    ✅ Copied {count} images and their filtered labels.")
        total_images += count

    if total_images > 0:
        create_output_yaml()
        print("\n✅ All done! Your new filtered dataset is ready in:", output_path)
    else:
        print("\n⏹️ Process finished, but no images were copied. Check if `selected_classes` match names in `data.yaml`.")
