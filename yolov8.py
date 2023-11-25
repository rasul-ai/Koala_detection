from ultralytics import YOLO

model = YOLO("yolov8n.pt")  # load a pretrained model (recommended for training)

# Use the model
model.train(data="./custom.yaml", epochs=100, imgsz=200)  # train the model
# metrics = model.val()  # evaluate model performance on the validation set
# results = model.predict(source="/home/bapary/Videos/koala/Cartoon", save=True)  # predict on an image
# success = model.export(format="")  # export the model to ONNX format
