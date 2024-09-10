from ultralytics import YOLO

# Load the pre-trained YOLOv8 model for classification
model = YOLO('yolov8m-cls.pt')

# Train the model with specified parameters
model.train(task='classify', data=r'C:/Users/cheha/OneDrive/Desktop/V8-OBJ/Dataset', epochs=50, imgsz=128)
