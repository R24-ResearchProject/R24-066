import cv2
import numpy as np
import tensorflow as tf

# Load the pre-trained model
model = tf.keras.models.load_model('model_defects.h5', compile=False)

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
    # Increase fontScale for larger text
    cv2.putText(frame, label, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3, cv2.LINE_AA)
    return frame

# Input and output video paths
input_video_path = 'Test2.MOV'  # Replace with your input video path
output_video_path = 'predicted_Test2.MOV'  # Replace with your desired output path

# Initialize video capture for the input video
cap = cv2.VideoCapture(input_video_path)

# Check if the video capture is initialized properly
if not cap.isOpened():
    print("Error: Could not open input video file")
    exit()

# Get video properties
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

# Initialize video writer for the output video
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Use 'mp4v' codec for .mp4 file
out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

try:
    while True:
        # Read frame-by-frame from the input video
        ret, frame = cap.read()
        
        if not ret:
            print("End of video file or failed to grab frame")
            break
        
        # Process the current frame
        defect_type_name = process_frame(frame)
        
        # Draw the prediction on the frame
        frame_with_prediction = draw_prediction(frame, defect_type_name)
        
        # Write the frame with prediction to the output video
        out.write(frame_with_prediction)
        
        # Display the frame for debugging (optional)
        cv2.imshow('Defect Detection', frame_with_prediction)
        
        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("Processing interrupted by user")

# Release resources
cap.release()
out.release()
cv2.destroyAllWindows()
