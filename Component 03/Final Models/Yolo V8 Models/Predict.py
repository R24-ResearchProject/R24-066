import cv2
from ultralytics import YOLO

# Load the trained YOLO model
model = YOLO(r'C:\Users\cheha\OneDrive\Desktop\V8-OBJ\runs\classify\train\weights\best.pt')

# Define the path to the video
video_path = r'C:\Users\cheha\OneDrive\Desktop\V8-OBJ\Test1.mov'

# Open the video file
cap = cv2.VideoCapture(video_path)

# Set the frame-skipping interval (e.g., every 10th frame)
frame_skip = 10

# Initialize frame counter
frame_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    
    if not ret:
        break
    
    # Process every nth frame
    if frame_count % frame_skip == 0:
        # Run prediction on the frame
        results = model.predict(source=frame, conf=0.5, save=False)
        
        # Draw the results on the frame
        for result in results:
            # Use result.plot() to draw the predictions on the frame
            annotated_frame = result.plot()
            
            # Display the annotated frame
            cv2.imshow('Predicted Video', annotated_frame)
        
        # Wait for a short period to mimic real-time playback
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    frame_count += 1

# Release the video capture object
cap.release()
cv2.destroyAllWindows()


