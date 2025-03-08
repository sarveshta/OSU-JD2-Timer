import os
import subprocess

def capture_photo(capture_filename):
    target_dir = "/home/pi/projects/OSU-JD2-Timer/src/captured_images"
    
    # Ensure directory exists
    os.makedirs(target_dir, exist_ok=True)

    filepath = os.path.join(target_dir, capture_filename)

    # Kill any existing libcamera processes to free up the camera
    subprocess.run(["sudo", "killall", "libcamera-still"], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

    # Camera capture command (added a short delay)
    cmd = ["libcamera-still", "-t", "1000", "-o", filepath]

    try:
        subprocess.run(cmd, check=True)
        print(f"Photo captured and saved as: {filepath}")
        return filepath
    except subprocess.CalledProcessError as e:
        print(f"Error capturing photo: {e}")
        return None

if __name__ == "__main__":
    filename = capture_photo("captured_image.jpeg")
    if filename:
        print("Photo successfully saved!")
    else:
        print("Photo capture failed. Check camera connection or try restarting.")
