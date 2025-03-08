import cv2
import os
import time
from datetime import datetime

# Set up the save directory
save_dir = "captured_images"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# Open the webcam (0 for built-in, 1 for external)
cap = cv2.VideoCapture(1)

# Set resolution to 1080p (Mac's webcam may not support exact resolution)
cap.set(3, 1920)  # Width
cap.set(4, 1080)  # Height

try:
    while True:
        # Read frame from webcam
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture image.")
            break

        # Generate a timestamped filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_path = os.path.join(save_dir, f"image_{timestamp}.jpg")

        # Save the image
        cv2.imwrite(image_path, frame)
        print(f"Captured: {image_path}")

        # Wait for 5 seconds
        time.sleep(5)

except KeyboardInterrupt:
    print("\nStopping the script.")

finally:
    cap.release()
    cv2.destroyAllWindows()
