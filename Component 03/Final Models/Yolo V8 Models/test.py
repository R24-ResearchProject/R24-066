import cv2
from ultralytics import YOLO

# Load the trained model
model = YOLO(r'C:\Users\cheha\OneDrive\Desktop\V8-OBJ\runs\classify\train\weights\best.pt')

# Define the path to the input and output video files
input_video_path = r'C:\Users\cheha\OneDrive\Desktop\V8-OBJ\Test3.MOV'
output_video_path = r'C:\Users\cheha\OneDrive\Desktop\V8-OBJ\Test3_predicted.MOV'

# Open the input video file
cap = cv2.VideoCapture(input_video_path)

# Get video properties
fps = int(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Define the codec and create a VideoWriter object for the output video
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for MOV or MP4 format
out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

while cap.isOpened():
    ret, frame = cap.read()
    
    if not ret:
        break

    # Run prediction on the frame
    results = model.predict(source=frame, conf=0.5, save=False)

    # Draw the results on the frame
    for result in results:
        annotated_frame = result.plot()

        # Display the frame with predictions
        cv2.imshow('Predicted Video', annotated_frame)

        # Save the frame to the output video file
        out.write(annotated_frame)
        
        # Exit if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release the video capture and writer objects
cap.release()
out.release()
cv2.destroyAllWindows()




