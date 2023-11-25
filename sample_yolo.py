import cv2
import os

# Define the class mapping
class_mapping = {
    0: 'koala',
}

image_width = 200
image_height = 200

def plot_bounding_boxes(image, annotation_list):
    annotations = annotation_list.strip().split('\n')
    
    for annotation in annotations:
        annotation_data = annotation.split()
        # print(annotation_data)
        class_index = int(annotation_data[0])
        x_center = float(annotation_data[1])
        y_center = float(annotation_data[2])
        bbox_width = float(annotation_data[3])
        bbox_height = float(annotation_data[4])

        x1 = int((x_center - bbox_width / 2) * image_width)
        y1 = int((y_center - bbox_height / 2) * image_height)
        x2 = int((x_center + bbox_width / 2) * image_width)
        y2 = int((y_center + bbox_height / 2) * image_height)

        color = (0, 0, 255)  # Red color for bounding boxes
        cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
        cv2.putText(image, class_mapping[class_index], (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    return image

ann_path = '/home/bapary/Videos/koala/aug_labels'
img_path = '/home/bapary/Videos/koala/aug_images'
output_path = '/home/bapary/Videos/koala/aug_annotation_sample'


annotations = [f for f in os.listdir(ann_path) if f.endswith('.txt')]


for annotation_file in annotations:
    with open(os.path.join(ann_path, annotation_file), "r") as file:
        annotation_list = file.read()

    image_file = os.path.join(img_path, annotation_file.replace("txt", "png"))


    image = cv2.imread(image_file)

    if image is not None:
        image_with_bboxes = plot_bounding_boxes(image.copy(), annotation_list)
        output_file = os.path.join(output_path, os.path.basename(image_file))
        cv2.imwrite(output_file, image_with_bboxes)
    else:
        print(f"Failed to load the image: {image_file}")
