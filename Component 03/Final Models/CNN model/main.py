import cv2
import numpy as np
import tensorflow as tf

# Load the pre-trained model
model = tf.keras.models.load_model('model_defects.h5')

# Define a dictionary to map defect type indices to names
defect_type_mapping = {
    0: 'open-seam',
    1: 'high-low',
    2: 'Non-Defect'
    
}

# Define a function to process a single frame
def process_frame(frame):
    # Convert the image from BGRA to BGR (removes alpha channel)
    if frame.shape[2] == 4:  # Check if the frame has an alpha channel
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
    
    # Preprocess the frame as required by your model
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

# Initialize the video capture with the HD USB camera (usually device 0)
cap = cv2.VideoCapture(1)

# Set the desired frame width and height
frame_width = 1920
frame_height = 1080
cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

if not cap.isOpened():
    print("Error: Could not open video stream from USB camera")
    exit()

try:
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        
        if not ret:
            print("Failed to grab frame")
            break
        
        # Process the current frame
        defect_type_name = process_frame(frame)
        
        # Draw the prediction on the frame
        frame_with_prediction = draw_prediction(frame, defect_type_name)
        
        # Display the resulting frame
        cv2.imshow('Defect Detection', frame_with_prediction)
        
        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("Camera feed stopped by user")

# When everything is done, release the capture and close windows
cap.release()
cv2.destroyAllWindows()