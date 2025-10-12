import os
import shutil
import yaml

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
            # Store the original index
            selected_class_indices_original.append(i)
            # Map original index to new index
            index_map[i] = len(new_names)
            # Add the name to our new list of names
            new_names.append(name)

    if not new_names:
        print("Error: None of the selected classes were found in the original dataset.")
        return

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
        # Use 'val' for directory but handle 'valid' from YAML if it exists
        yaml_split_key = 'valid' if split == 'val' and 'valid' in original_data_yaml else split
        
        if yaml_split_key not in original_data_yaml:
            print(f"Warning: Split '{yaml_split_key}' not found in YAML. Skipping.")
            continue

        original_image_dir = original_data_yaml[yaml_split_key]
        # Assume labels are in a parallel directory structure
        original_label_dir = original_image_dir.replace('images', 'labels')

        # FIX: Ensure the output directory name is 'valid' to match the created folder
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
                if not parts:
                    continue
                
                original_class_index = int(parts[0])
                
                # Check if this class is one we want to keep
                if original_class_index in selected_class_indices_original:
                    contains_selected_class = True
                    # Remap to the new index
                    new_class_index = index_map[original_class_index]
                    new_annotations.append(f"{new_class_index} {' '.join(parts[1:])}")

            # If the file had at least one of our selected classes, save the new label file and copy the image
            if contains_selected_class:
                # Write the new label file
                new_label_path = os.path.join(new_label_dir, label_filename)
                with open(new_label_path, 'w') as f:
                    f.write('\n'.join(new_annotations))

                # Copy the corresponding image
                image_name = os.path.splitext(label_filename)[0]
                
                # Find the correct image extension (e.g., .jpg, .png)
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
    
    # Correcting the paths for the new YAML file to be relative
    new_data_yaml = {
        'path': os.path.abspath(new_dataset_dir),
        'train': 'train/images',
        'val': 'valid/images', # Using 'valid' for consistency in new dataset
        'test': 'test/images',
        'names': new_names
    }

    with open(new_yaml_path, 'w') as f:
        yaml.dump(new_data_yaml, f, sort_keys=False, default_flow_style=False)

    print(f"\nSuccessfully created new dataset at '{new_dataset_dir}'")
    print(f"New configuration file saved at '{new_yaml_path}'")


if __name__ == '__main__':
    # --- Configuration ---
    
    # 1. Define the classes you want to keep in your new dataset
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
    
    # 2. Define the structure of your original dataset (paste your YAML content here)
    #    IMPORTANT: Make sure the paths are correct. 
    #    Using forward slashes '/' is recommended for cross-platform compatibility.
    #    You might need to adjust these paths if the script is not in the same parent folder.
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
    
    # 3. Specify the name for the new directory where the filtered dataset will be saved
    NEW_DATASET_DIRECTORY = 'filtered_farm_safety_dataset'
    
    # --- Run the script ---
    filter_dataset(ORIGINAL_DATA_YAML_CONTENT, SELECTED_CLASSES, NEW_DATASET_DIRECTORY)

