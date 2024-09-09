import cv2
import numpy as np
import tensorflow as tf
import concurrent.futures

# Load the pre-trained defect detection model
model_defects = tf.keras.models.load_model('model_defects.h5')

# Define a dictionary to map defect type indices to names
defect_type_mapping = {
    0: 'open-seam',
    1: 'high-low',
    2: 'Non-Defect'
    # Add other defect types as needed
}

# Define a function to identify seam photos using dynamic thresholding
def identify_seam_photos(image, dynamic_threshold_factor=1):
    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    dynamic_threshold = np.mean(grayscale_image) * dynamic_threshold_factor
    _, binary_image = cv2.threshold(grayscale_image, dynamic_threshold, 255, cv2.THRESH_BINARY)
    return binary_image

# Define a function to process a single frame for defect prediction
def process_frame_for_defect(frame):
    processed_frame = cv2.resize(frame, (48, 48))
    processed_frame = processed_frame / 255.0
    processed_frame = np.expand_dims(processed_frame, axis=0)
    
    # Ensure the frame has 3 channels
    if processed_frame.shape[-1] != 3:  # (1, 48, 48)
        processed_frame = np.repeat(processed_frame[:, :, :, np.newaxis], 3, axis=-1)  # (1, 48, 48, 3)
    
    prediction = model_defects.predict(processed_frame)
    defect_type_index = np.argmax(prediction, axis=1)[0]
    defect_type_name = defect_type_mapping[defect_type_index]
    
    return defect_type_name

# Function to draw the prediction on the frame
def draw_prediction(frame, defect_type_name):
    label = f"Defect Type: {defect_type_name}"
    cv2.putText(frame, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    return frame

def resize_frame(frame, frame_width=720, frame_height=800):
    return cv2.resize(frame, (frame_width, frame_height))

def process_frame(frame, dynamic_threshold_factor=0.2):
    if frame is None:
        return None, None

    seam_photos = identify_seam_photos(frame, dynamic_threshold_factor)
    defect_type_name = process_frame_for_defect(frame)
    
    # Only draw prediction if it's a defect (not 'Non-Defect')
    if defect_type_name != 'Non-Defect':
        frame_with_prediction = draw_prediction(frame, defect_type_name)
        return frame_with_prediction, seam_photos
    else:
        return None, seam_photos  # Skip non-defect frames

def process_video(video_path, output_path='output_video.mp4', max_workers=4, frame_width=720, frame_height=800):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video file.")
        return

    # Get the video writer initialized to save the output video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for .mp4 file
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    output_size = (frame_width, frame_height)
    out = cv2.VideoWriter(output_path, fourcc, fps, output_size)

    futures = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            resized_frame = resize_frame(frame, frame_width, frame_height)
            
            future = executor.submit(process_frame, resized_frame)
            futures.append(future)

        # Wait for all submitted tasks to complete
        for future in concurrent.futures.as_completed(futures):
            try:
                result, filtered_frame = future.result()
                if result is not None:
                    cv2.imshow('Defect Detection', result)
                    out.write(result)  # Write only defect frames to the output video
                
            except Exception as e:
                print(f"Error processing frame: {e}")

    cap.release()
    out.release()
    cv2.destroyAllWindows()

# Path to the video file
video_path = "Test2.MOV"

# Process and display video frames and save the output
process_video(video_path, output_path='Test2_output_video.mp4')
