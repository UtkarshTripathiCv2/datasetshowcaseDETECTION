import os

# --- Configuration ---
# The class names for your dataset.
CLASS_NAMES = [
    "person", 
    "hi-vis"
]

# The main directory where your split 'train', 'valid', 'test' folders are.
DATASET_DIR = "output"

# --- YAML File Generation ---

# Get the absolute path to make the YAML file work from anywhere.
absolute_path = os.path.abspath(DATASET_DIR)

# Define paths to the image folders. 'val' is the standard name for validation.
train_path = os.path.join(absolute_path, "train", "images")
valid_path = os.path.join(absolute_path, "valid", "images")
test_path = os.path.join(absolute_path, "test", "images")

# Automatically get the number of classes.
num_classes = len(CLASS_NAMES)

# Create the YAML content as a string.
yaml_content = f"""
# YOLO dataset configuration file

train: {train_path}
val: {valid_path}
test: {test_path}

# Number of classes
nc: {num_classes}

# Class names
names: {CLASS_NAMES}
"""

# Write the content to 'data.yaml'.
file_name = "data.yaml"
with open(file_name, "w") as f:
    f.write(yaml_content)

print(f"Successfully created '{file_name}' with {num_classes} classes! 🎉")
