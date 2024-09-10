import threading
import cv2
import numpy as np
import matplotlib.pyplot as plt

def identify_seam_photos(image, dynamic_threshold_factor=0.9):
    # Convert the image to grayscale
    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Compute the dynamic threshold based on image characteristics
    dynamic_threshold = np.mean(grayscale_image) * dynamic_threshold_factor
    
    # Apply thresholding to identify seam photos
    _, binary_image = cv2.threshold(grayscale_image, dynamic_threshold, 255, cv2.THRESH_BINARY)
    
    return binary_image

def crop_image(image):
    crop_start_y = int(image.shape[0] * 0.2)
    crop_end_y = int(image.shape[0] * 0.8)
    cropped_image = image[crop_start_y:crop_end_y, :]
    return cropped_image

def process_image(image_path, result):
    # Load the uploaded image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Error: Image not loaded properly")

    # Crop the original image
    cropped_image = crop_image(image)

    # Identify seam photos using dynamic thresholding on the cropped image
    seam_photos = identify_seam_photos(cropped_image)
    
    result.append(seam_photos)

# Path to the uploaded image
image_path = "D:\\SLIIT\\test\\15f15690-6428-4452-b05c-26798e94c6fb.jpeg"

# List to store the result
result = []

# Create and start the thread
thread = threading.Thread(target=process_image, args=(image_path, result))
thread.start()

# Wait for the thread to complete
thread.join()

# Display the seam identification result
if result:
    plt.imshow(result[0], cmap='gray')
    plt.title('Seam Photos')
    plt.axis('off')
    plt.show()
else:
    print("Error: No result to display")
