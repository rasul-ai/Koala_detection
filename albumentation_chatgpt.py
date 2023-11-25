import os
import cv2
import numpy as np
from albumentations import (
    Compose,
    HorizontalFlip,
    VerticalFlip,
    Rotate,
    RandomBrightnessContrast,
    BboxParams,
)

def read_annotations(file_path):
    """Read bounding box annotations from a YOLO format text file."""
    with open(file_path, 'r') as file:
        lines = file.read().splitlines()
    boxes = []
    for line in lines:
        values = line.split()
        class_label = int(values[0])
        x_center, y_center, width, height = map(float, values[1:])
        boxes.append([x_center, y_center, width, height, class_label])
    return boxes

def save_annotations(file_path, boxes):
    """Save bounding box annotations to a YOLO format text file."""
    lines = [f"{box[4]} {box[0]} {box[1]} {box[2]} {box[3]}" for box in boxes]
    with open(file_path, 'w') as file:
        file.write('\n'.join(lines))

def augment_data(image_path, annotation_path, output_folder, num_augmentations=5):
    """Apply data augmentation and save augmented images and annotations."""
    image = cv2.imread(image_path)
    annotations = read_annotations(annotation_path)

    bbox_params = BboxParams(format='yolo', min_area=1, min_visibility=0.1, label_fields=['category_id'])

    for i in range(num_augmentations):
        augmented = aug(image=image, bboxes=annotations, category_id=[box[4] for box in annotations])
        augmented_image = augmented['image']
        augmented_annotations = augmented['bboxes']

        # Save augmented image
        image_name, image_extension = os.path.splitext(os.path.basename(image_path))
        output_image_path = os.path.join(output_folder+"/a/", f"{image_name}_aug_{i}{image_extension}")
        cv2.imwrite(output_image_path, augmented_image)

        # Save augmented annotations
        output_annotation_path = os.path.join(output_folder+"/b/", f"{image_name}_aug_{i}.txt")
        save_annotations(output_annotation_path, augmented_annotations)

# Define the augmentations you want to apply
aug = Compose([
    HorizontalFlip(p=0.5),
    VerticalFlip(p=0.5),
    Rotate(limit=30, p=0.5),
    RandomBrightnessContrast(p=0.5),
], bbox_params=BboxParams(format='yolo', min_area=1, min_visibility=0.1, label_fields=['category_id']))

# Set your data folder
data_folder = "/home/bapary/Videos/koala/albumentation_imgs_labels"

# Iterate through images and annotations
for image_name in os.listdir(data_folder):
    if image_name.endswith(".png"):
        image_path = os.path.join(data_folder, image_name)
        annotation_path = os.path.join(data_folder, f"{os.path.splitext(image_name)[0]}.txt")
        
        # Perform data augmentation
        augment_data(image_path, annotation_path, output_folder="/home/bapary/Videos/koala", num_augmentations=5)
