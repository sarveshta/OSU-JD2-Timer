import os
import subprocess

def capture_photo(capture_filename):
    target_dir = "/home/pi/projects/OSU-JD2-Timer/captured_images"
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    filepath = os.path.join(target_dir, capture_filename)
    cmd = ["libcamera-still", "-t", "0", "-o", filepath]
    subprocess.run(cmd, check=True)
    return filepath

if __name__ == "__main__":
    filename = capture_photo("captured_image.jpg")
    print("Photo captured and saved as:", filename)
