import time
import subprocess
import json
from PIL import Image
import logging

# Configure logging
def process_image(capture_filename):
    logging.info("Processing image: %s", capture_filename)
    # Open and possibly resize the image
    img = Image.open(capture_filename)
    width, height = img.size
    max_dimension = max(width, height)

    if max_dimension > 1080:
        scale = 1080 / max_dimension
        new_width = int(width * scale)
        new_height = int(height * scale)
        img = img.resize((new_width, new_height), resample=Image.LANCZOS)
        img.save(capture_filename)
        logging.info("Image resized to: %dx%d", new_width, new_height)

    # Build the curl command that uses base64 encoding on the image
    cmd = (
        f"base64 -i {capture_filename} | "
        f"curl -s -d @- \"https://detect.roboflow.com/mobile-phone-detection-mtsje/1?api_key=h2EXOUFyekrJwf9BZKoC\""
    )
    
    # Execute the command
    proc = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if proc.returncode != 0:
        logging.error("Error during curl call: %s", proc.stderr)
        return False, 0.0

    # Load the output JSON response
    try:
        result = json.loads(proc.stdout)
    except json.JSONDecodeError:
        logging.error("Failed to decode JSON from response.")
        return False, 0.0

    # Check predictions for a cell phone
    phone_detected = False
    phone_confidence = 0.0
    for prediction in result.get("predictions", []):
        if prediction.get("class") == "mobilephone screen":
            phone_detected = True
            phone_confidence = max(phone_confidence, prediction.get("confidence", 0))
        if prediction.get("class") == "cell-phone":
            phone_detected = True
            phone_confidence = max(phone_confidence, prediction.get("confidence", 0))
        if prediction.get("class") == "phone":
            phone_detected = True
            phone_confidence = max(phone_confidence, prediction.get("confidence", 0))


    logging.info("Phone detected: %s | Confidence: %.2f", phone_detected, phone_confidence)
    return phone_detected, phone_confidence

if __name__ == "__main__":
    phone_detected, confidence = process_image("captured_images/resized_Phone.jpeg")
    logging.info("Phone detected: %s | Confidence: %.2f", phone_detected, confidence)