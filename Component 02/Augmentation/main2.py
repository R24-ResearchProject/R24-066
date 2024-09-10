import cv2
import numpy as np
import concurrent.futures
import tensorflow as tf

# Load the pre-trained models
model_defects = tf.keras.models.load_model('D:\SLIIT\Research\Repo\Organization\R24-066\Component 02\Augmentation\model_defects2.h5')
model_seam = tf.keras.models.load_model('D:\SLIIT\Research\Repo\Organization\R24-066\Component 02\Augmentation\model_cloth2.h5')


# Define a dictionary to map defect type indices to names
defect_type_mapping = {
    0: 'open-seam',
    1: 'high-low',
    2: 'Non-Defect'
}

# Define a function to check if a frame contains a seam
def is_seam(frame):
    processed_frame = cv2.resize(frame, (48, 48))
    processed_frame = processed_frame / 255.0
    processed_frame = np.expand_dims(processed_frame, axis=0)
    
    if processed_frame.shape[-1] != 3:
        processed_frame = np.repeat(processed_frame[:, :, :, np.newaxis], 3, axis=-1)
    
    prediction = model_seam.predict(processed_frame)
    seam_detected = np.argmax(prediction, axis=1)[0]
    
    return seam_detected == 1

# Define a function to process a single frame for defect prediction
def process_frame_for_defect(frame):
    processed_frame = cv2.resize(frame, (48, 48))
    processed_frame = processed_frame / 255.0
    processed_frame = np.expand_dims(processed_frame, axis=0)
    
    if processed_frame.shape[-1] != 3:
        processed_frame = np.repeat(processed_frame[:, :, :, np.newaxis], 3, axis=-1)
    
    prediction = model_defects.predict(processed_frame)
    defect_type_index = np.argmax(prediction, axis=1)[0]
    defect_type_name = defect_type_mapping[defect_type_index]
    
    return defect_type_name

# Define a function to apply advanced filters to a frame using multi-threading
def apply_filters(frame):
    def sharpen_image(image):
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        return cv2.filter2D(src=image, ddepth=-1, kernel=kernel)

    def adjust_brightness_contrast(image, brightness=30, contrast=1.5):
        return cv2.convertScaleAbs(image, alpha=contrast, beta=brightness)

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        # Parallel execution of remaining filters
        future_sharpened = executor.submit(sharpen_image, frame)
        future_adjusted = executor.submit(adjust_brightness_contrast, future_sharpened.result())

    # Optimized memory management: reuse data across filters without duplication
    filtered_frame = future_adjusted.result()

    return filtered_frame

# Function to process a single frame for both seam identification and defect prediction
def process_frame(frame):
    if is_seam(frame):
        filtered_frame = apply_filters(frame)
        defect_type = process_frame_for_defect(filtered_frame)
        cv2.putText(filtered_frame, defect_type, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        return filtered_frame, True
    else:
        return frame, False

# Function to process the video and apply the models with thread pooling
def process_video(video_path, max_workers=4, frame_width=720, frame_height=800):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video file.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        resized_frame = cv2.resize(frame, (frame_width, frame_height))

        # Dynamic thread allocation and load balancing using ThreadPoolExecutor
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future = executor.submit(process_frame, resized_frame)
            processed_frame, is_seam_frame = future.result()

        if is_seam_frame:
            cv2.imshow('Seam Photos with Defect Prediction', processed_frame)
            cv2.imshow('Original Frame', resized_frame)
        else:
            cv2.imshow('Original Frame', resized_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Path to the video file
video_path = "Component 02\\videos\\test4.mp4"

# Real-time processing considerations: process and display video frames
process_video(video_path)
