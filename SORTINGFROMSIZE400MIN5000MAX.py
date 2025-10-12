import os
import shutil
import yaml
import random

def filter_dataset(original_data_yaml, selected_classes, new_dataset_dir):
    """
    Filters a YOLO dataset to include only selected classes.

    Args:
        original_data_yaml (dict): The loaded content of the original data.yaml file.
        selected_classes (list): A list of class names to keep.
        new_dataset_dir (str): The path to save the new filtered dataset.
    """
    # --- 1. Setup and Configuration ---
    print("Starting dataset filtering process...")

    original_names = original_data_yaml['names']
    
    # Create a mapping from old class index to new class index
    # and a list of the original indices we want to keep.
    selected_class_indices_original = []
    index_map = {}
    new_names = []
    
    for i, name in enumerate(original_names):
        if name in selected_classes:
            selected_class_indices_original.append(i)
            index_map[i] = len(new_names)
            new_names.append(name)

    if not new_names:
        print("Error: None of the selected classes were found in the original dataset.")
        return None

    print(f"Selected classes to keep: {new_names}")
    print(f"Original indices: {selected_class_indices_original}")
    print(f"New index mapping (old_index -> new_index): {index_map}")

    # --- 2. Create New Directory Structure ---
    print(f"\nCreating new dataset directory at: {new_dataset_dir}")
    for split in ['train', 'valid', 'test']:
        os.makedirs(os.path.join(new_dataset_dir, split, 'images'), exist_ok=True)
        os.makedirs(os.path.join(new_dataset_dir, split, 'labels'), exist_ok=True)

    # --- 3. Process Each Data Split (train, valid, test) ---
    for split in ['train', 'val', 'test']:
        yaml_split_key = 'valid' if split == 'val' and 'valid' in original_data_yaml else split
        
        if yaml_split_key not in original_data_yaml:
            print(f"Warning: Split '{yaml_split_key}' not found in YAML. Skipping.")
            continue

        original_image_dir = original_data_yaml[yaml_split_key]
        original_label_dir = original_image_dir.replace('images', 'labels')

        output_split_name = 'valid' if split == 'val' else split
        new_image_dir = os.path.join(new_dataset_dir, output_split_name, 'images')
        new_label_dir = os.path.join(new_dataset_dir, output_split_name, 'labels')
        
        print(f"\nProcessing '{yaml_split_key}' split...")
        print(f"Original labels directory: {original_label_dir}")

        if not os.path.isdir(original_label_dir):
            print(f"Warning: Label directory not found for '{split}' split. Skipping.")
            continue

        image_copy_count = 0
        for label_filename in os.listdir(original_label_dir):
            if not label_filename.endswith('.txt'):
                continue

            original_label_path = os.path.join(original_label_dir, label_filename)
            
            with open(original_label_path, 'r') as f:
                lines = f.readlines()
            
            new_annotations = []
            contains_selected_class = False
            for line in lines:
                parts = line.strip().split()
                if not parts: continue
                
                original_class_index = int(parts[0])
                
                if original_class_index in selected_class_indices_original:
                    contains_selected_class = True
                    new_class_index = index_map[original_class_index]
                    new_annotations.append(f"{new_class_index} {' '.join(parts[1:])}")

            if contains_selected_class:
                new_label_path = os.path.join(new_label_dir, label_filename)
                with open(new_label_path, 'w') as f:
                    f.write('\n'.join(new_annotations))

                image_name = os.path.splitext(label_filename)[0]
                
                found_image = False
                for ext in ['.jpg', '.jpeg', '.png']:
                    original_image_path = os.path.join(original_image_dir, image_name + ext)
                    if os.path.exists(original_image_path):
                        new_image_path = os.path.join(new_image_dir, image_name + ext)
                        shutil.copy2(original_image_path, new_image_path)
                        image_copy_count += 1
                        found_image = True
                        break
                
                if not found_image:
                    print(f"Warning: Image for label '{label_filename}' not found.")

        print(f"Finished processing '{split}'. Copied {image_copy_count} images and their labels.")

    # --- 4. Generate New data.yaml File ---
    new_yaml_path = os.path.join(new_dataset_dir, 'data.yaml')
    new_data_yaml = {
        'path': os.path.abspath(new_dataset_dir),
        'train': 'train/images', 'val': 'valid/images', 'test': 'test/images',
        'names': new_names
    }
    with open(new_yaml_path, 'w') as f:
        yaml.dump(new_data_yaml, f, sort_keys=False, default_flow_style=False)

    print(f"\nSuccessfully created new dataset at '{new_dataset_dir}'")
    print(f"New configuration file saved at '{new_yaml_path}'")
    return new_names

# --- Balancing Helper Functions ---

def find_image_path(image_name_no_ext, image_dir):
    """Finds the full path of an image given its name without extension."""
    for ext in ['.jpg', '.jpeg', '.png']:
        path = os.path.join(image_dir, f"{image_name_no_ext}{ext}")
        if os.path.exists(path):
            return path
    return None

def delete_image_and_label(image_name_no_ext, image_dir, label_dir):
    """Deletes an image and its corresponding label file."""
    try:
        label_path = os.path.join(label_dir, f"{image_name_no_ext}.txt")
        if os.path.exists(label_path):
            os.remove(label_path)
        
        image_path = find_image_path(image_name_no_ext, image_dir)
        if image_path:
            os.remove(image_path)
    except OSError as e:
        print(f"Error deleting file {image_name_no_ext}: {e}")


def copy_image_and_label(original_name_no_ext, new_name_no_ext, image_dir, label_dir):
    """Copies an image and its label file to new names."""
    try:
        # Copy label
        original_label_path = os.path.join(label_dir, f"{original_name_no_ext}.txt")
        new_label_path = os.path.join(label_dir, f"{new_name_no_ext}.txt")
        if os.path.exists(original_label_path):
            shutil.copy2(original_label_path, new_label_path)
            
        # Copy image
        original_image_path = find_image_path(original_name_no_ext, image_dir)
        if original_image_path:
            ext = os.path.splitext(original_image_path)[1]
            new_image_path = os.path.join(image_dir, f"{new_name_no_ext}{ext}")
            shutil.copy2(original_image_path, new_image_path)
    except OSError as e:
        print(f"Error copying file {original_name_no_ext}: {e}")

def balance_dataset_split(dataset_dir, split, names, min_images, max_images):
    """Balances the number of images per class in a specific dataset split."""
    image_dir = os.path.join(dataset_dir, split, 'images')
    label_dir = os.path.join(dataset_dir, split, 'labels')

    def scan_and_get_counts():
        class_counts = {i: 0 for i in range(len(names))}
        class_image_map = {i: [] for i in range(len(names))}
        
        for label_file in os.listdir(label_dir):
            image_name = os.path.splitext(label_file)[0]
            with open(os.path.join(label_dir, label_file), 'r') as f:
                unique_classes_in_image = set(int(line.split()[0]) for line in f if line.strip())
            
            for class_idx in unique_classes_in_image:
                if class_idx in class_counts:
                    class_counts[class_idx] += 1
                    class_image_map[class_idx].append(image_name)
        return class_counts, class_image_map

    # --- 1. Initial Scan ---
    class_counts, class_image_map = scan_and_get_counts()
    print("Initial class distribution (image count):")
    for i, name in enumerate(names):
        print(f"  - {name}: {class_counts.get(i, 0)} images")

    # --- 2. Undersampling ---
    print("\n--- Starting Undersampling ---")
    for class_idx, count in class_counts.items():
        if count > max_images:
            num_to_remove = count - max_images
            print(f"Undersampling class '{names[class_idx]}': removing {num_to_remove} of {count} images.")
            images_to_remove = random.sample(class_image_map[class_idx], num_to_remove)
            for image_name in images_to_remove:
                delete_image_and_label(image_name, image_dir, label_dir)

    # --- 3. Rescan after Undersampling ---
    print("\nRescanning dataset after undersampling...")
    class_counts, class_image_map = scan_and_get_counts()
    print("Class distribution after undersampling:")
    for i, name in enumerate(names):
        print(f"  - {name}: {class_counts.get(i, 0)} images")

    # --- 4. Oversampling ---
    print("\n--- Starting Oversampling (by duplication) ---")
    for class_idx, count in class_counts.items():
        if 0 < count < min_images:
            num_to_add = min_images - count
            print(f"Oversampling class '{names[class_idx]}': adding {num_to_add} images to reach {min_images}.")
            images_to_duplicate = random.choices(class_image_map[class_idx], k=num_to_add)
            for i, image_name in enumerate(images_to_duplicate):
                new_name = f"{image_name}_aug_{i}"
                copy_image_and_label(image_name, new_name, image_dir, label_dir)

    # --- 5. Final Report ---
    print("\n--- Balancing Complete ---")
    final_counts, _ = scan_and_get_counts()
    print(f"Final class distribution in '{split}' set:")
    for i, name in enumerate(names):
        print(f"  - {name}: {final_counts.get(i, 0)} images")


if __name__ == '__main__':
    # --- Configuration ---
    SELECTED_CLASSES = [
        'fire', 
        'smoke', 
        'person', 
        'COW',  # Note: Case sensitive, should match your YAML
        'horse', 
        'sheep',
        'pig',
        'Ants',
        'Bees',
        'Beetles',
        'Caterpillars',
        'Earthworms',
        'Grasshoppers',
        'Healthy',
        'Healthy Wheat',
        'Potato leaf',
        'Potato leaf early blight',
        'Potato leaf late blight',
        'Tomato Early blight leaf',
        'Tomato Septoria leaf spot',
        'Tomato leaf',
        'Tomato leaf bacterial spot',
        'Tomato leaf late blight',
        'Tomato leaf mosaic virus',
        'Tomato leaf yellow virus',
        'Tomato mold leaf',
        'Tomato two spotted spider mites leaf',
        'Black Rust',
        'Brown Rust',
        'Early Blight'
    ]
    ORIGINAL_DATA_YAML_CONTENT = {
        'train': 'C:/Users/HP/Desktop/ALLmaster_dataset/train/images',
        'val': 'C:/Users/HP/Desktop/ALLmaster_dataset/valid/images',
        'test': 'C:/Users/HP/Desktop/ALLmaster_dataset/test/images',
        'names': [
            'Ants', 'Bees', 'Beetles', 'Black Rust', 'Brown Rust', 'COW', 
            'Caterpillars', 'Corn Gray leaf spot', 'Corn leaf blight', 'Corn rust leaf',
            'Early Blight', 'Earthworms', 'Earwigs', 'Grasshoppers', 'Healthy', 
            'Healthy Wheat', 'Late Blight', 'Leaf Miner', 'Leaf Mold', 'Mosaic Virus',
            'Moths', 'Potato leaf', 'Potato leaf early blight', 'Potato leaf late blight',
            'Septoria', 'Slugs', 'Snails', 'Spider Mites', 'Squash Powdery mildew leaf',
            'Tomato Early blight leaf', 'Tomato Septoria leaf spot', 'Tomato leaf',
            'Tomato leaf bacterial spot', 'Tomato leaf late blight', 'Tomato leaf mosaic virus',
            'Tomato leaf yellow virus', 'Tomato mold leaf', 'Tomato two spotted spider mites leaf',
            'Wasps', 'Weevils', 'Yellow Leaf Curl Virus', 'Yellow Rust', 'fire', 
            'hi-vis', 'horse', 'person', 'pig', 'sheep', 'smoke'
        ]
    }
    NEW_DATASET_DIRECTORY = 'filtered_farm_safety_dataset5400'
    
    # --- Balancing Configuration ---
    MIN_IMAGES_PER_CLASS = 400
    MAX_IMAGES_PER_CLASS = 5000
    
    # --- Run the script ---
    new_class_names = filter_dataset(ORIGINAL_DATA_YAML_CONTENT, SELECTED_CLASSES, NEW_DATASET_DIRECTORY)

    # After filtering, balance the training set
    if new_class_names:
        print("\n--- Starting Dataset Balancing for Training Set ---")
        balance_dataset_split(
            NEW_DATASET_DIRECTORY,
            'train',
            new_class_names,
            MIN_IMAGES_PER_CLASS,
            MAX_IMAGES_PER_CLASS
        )

