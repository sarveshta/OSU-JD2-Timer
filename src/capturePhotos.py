from picamzero import Camera
import os
import random
import string

def capture_photo(capture_filename):
    target_dir = os.path.join(os.getcwd(), "captured_images")
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    cam = Camera()
    cam.start_preview()
    cam.take_photo(os.path.join(target_dir, capture_filename))
    cam.stop_preview()

if __name__ == "__main__":
    filename = capture_photo()
    print("Photo captured and saved as:", filename)
