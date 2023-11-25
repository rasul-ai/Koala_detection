import os

import cv2
import albumentations as A
import random
from PIL import Image

image_dir = "/home/bapary/Videos/koala/albumentation_imgs_labels"
random.seed(50)

imgs = []
lbls = []


for images in os.listdir(image_dir):
    if (images.endswith(".png")):
        img_path = os.path.join(image_dir,images)
        imgs.append(img_path)
    if (images.endswith(".txt")):
            bb_path = os.path.join(image_dir,images)
            lbls.append(bb_path)

imgs.sort()
lbls.sort()
# print(imgs)
# print(lbls)

for i in range(len(imgs)):
    image = cv2.imread(imgs[i])
    filename_with_extension = os.path.basename(imgs[i])
    filename_without_extension = os.path.splitext(filename_with_extension)[0]
    print(filename_without_extension)
    d = 0

    labels = open(lbls[i], 'r')
    line = labels.readline()
    coors = line.split(' ')[0:]
    # print(coors)
    list = []
    for point in coors:
        point = float(point)
        list.append(point)
    # print(list)
    for j in range(0,5):
        transform = A.Compose([
            # A.HorizontalFlip(p=0.5),
                A.Rotate(limit=random.choice([5, 10, 15, 18, 7, 12, -5, -10, -15, -18, -7, -12])), # Works Fine
                A.ShiftScaleRotate(p=0.3, shift_limit=random.choice([.01, .02, .03, .04, 0.05, .06])), #Works Fine
                # A.BBoxSafeRandomCrop(erosion_rate=random.randint(1,6)/10.0, always_apply=False, p=1.0),
                A.GaussNoise(var_limit=500.0), #Works Fine
                A.Affine(keep_ratio=True, scale=1.3, fit_output=False),
                A.RGBShift(r_shift_limit=30, g_shift_limit=30, b_shift_limit=30, p=0.3),
                # A.GridDistortion(distort_limit=random.randint(1,3)/10.0), #Works fine. Default = 0.3
                A.OpticalDistortion(distort_limit=random.randint(1,3)/10.0, shift_limit=random.randint(1,3)/10.0), #works Fine
             ],
            bbox_params=A.BboxParams(format='yolo', label_fields=['class_labels']),
        )
        d = d+1


        transformed = transform(image=image, bboxes=[list[1:]], class_labels=[0])
        # print(transformed)

        my_list = []
        for i in transformed.values():
            my_list.append(i)
        # print(my_list)
        img = Image.fromarray(my_list[0])
        img.save("/home/bapary/Videos/koala/images/"+filename_without_extension+"-"+str(d)+".png")

        with open("/home/bapary/Videos/koala/labels/"+filename_without_extension+"-"+str(d)+".txt","w") as w:
            for t, class_label in zip(my_list[1], my_list[2]):
                w.write("{:d} {:.5f} {:.5f} {:.5f} {:.5f}\n".format(int(class_label), t[0], t[1], t[2], t[3]))
