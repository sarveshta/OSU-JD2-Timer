import time
import os
from datetime import datetime
from picamera import PiCamera  # Use picamera2 for newer Raspberry Pi OS

# Directory to store images
save_dir = "/home/pi/captured_images"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# Initialize the camera
camera = PiCamera()

# Set resolution to 1080p
camera.resolution = (1920, 1080)

try:
    while True:
        # Generate a timestamped filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_path = os.path.join(save_dir, f"image_{timestamp}.jpg")

        # Capture the image
        camera.capture(image_path)
        print(f"Captured: {image_path}")

        # Wait for 5 seconds
        time.sleep(5)

except KeyboardInterrupt:
    print("\nStopping the camera script.")
    camera.close()
