import json
import os

class_mapping = {
    "Coala": 0,
}

def labelme_to_yolo(json_path, output_path):
    with open(json_path, 'r') as json_file:
        data = json.load(json_file)

    yolo_annotations = []

    image_width = data.get("imageWidth", 0)
    image_height = data.get("imageHeight", 0)

    for shape in data['shapes']:
        label = shape['label']
        if label in class_mapping:
            class_index = class_mapping[label]
            points = shape['points']

            x1, y1 = points[0]
            x2, y2 = points[1]

            center_x = (x1 + x2) / (2.0 * image_width)
            center_y = (y1 + y2) / (2.0 * image_height)
            bbox_width = abs(x2 - x1) / image_width
            bbox_height = abs(y2 - y1) / image_height

            yolo_annotations.append(f"{class_index} {center_x:.6f} {center_y:.6f} {bbox_width:.6f} {bbox_height:.6f}")

    output_file_path = os.path.join(output_path, os.path.splitext(os.path.basename(json_path))[0] + ".txt")
    with open(output_file_path, 'w') as output_file:
        output_file.write("\n".join(yolo_annotations))

# Path to the directory containing LabelMe JSON annotations
labelme_annotations_dir = '/home/bapary/Videos/koala/realistic'

# Output directory for YOLO annotations
output_dir = '/home/bapary/Videos/koala/labels'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Process each JSON file in the LabelMe directory
for filename in os.listdir(labelme_annotations_dir):
    if filename.endswith('.json'):
        json_path = os.path.join(labelme_annotations_dir, filename)
        labelme_to_yolo(json_path, output_dir)
