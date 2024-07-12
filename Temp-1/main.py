import cv2
import numpy as np
import tensorflow as tf  # or keras, depending on your model

# Load the pre-trained model
model = tf.keras.models.load_model('model_defects.h5')

# Define a dictionary to map defect type indices to names
defect_type_mapping = {
    0: 'open-seam',
    1: 'high-low',
    2: 'Non-Defect',
    # 3: 'Run_Off'
    # Add other defect types as needed
}

# Define a function to process a single frame
def process_frame(frame):
    # Preprocess the frame as required by your model
    # Example: resizing, normalization, etc.
    processed_frame = cv2.resize(frame, (48, 48))  # Example size
    processed_frame = processed_frame / 255.0
    processed_frame = np.expand_dims(processed_frame, axis=0)
    
    # Predict the defect type
    prediction = model.predict(processed_frame)
    defect_type_index = np.argmax(prediction, axis=1)[0]
    
    # Get the defect type name from the mapping
    defect_type_name = defect_type_mapping[defect_type_index]
    
    return defect_type_name

# Function to draw the prediction on the frame
def draw_prediction(frame, defect_type_name):
    label = f"Defect Type: {defect_type_name}"
    cv2.putText(frame, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    return frame

# Open the video file
video_path = '2024_04_02_10_57_IMG_8641.MOV'
cap = cv2.VideoCapture(video_path)

# Check if the video capture opened successfully
if not cap.isOpened():
    print("Error opening video file")
    exit()

# Desired frame size
frame_width = 720
frame_height = 800

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Resize the frame to the desired size
    frame = cv2.resize(frame, (frame_width, frame_height))
    
    # Process the current frame
    defect_type_name = process_frame(frame)
    
    # Draw the prediction on the frame
    frame_with_prediction = draw_prediction(frame, defect_type_name)
    
    # Display the frame
    cv2.imshow('Defect Detection', frame_with_prediction)
    
    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
