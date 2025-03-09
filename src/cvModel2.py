import time
import subprocess
import json
import logging

# Configure logging
def process_image(capture_filename):
    logging.info("Processing image: %s", capture_filename)
    print(f"Processing image: {capture_filename}")

    # Build the curl command that uses base64 encoding on the image
    cmd = (
        f"base64 -i {capture_filename} | "
        f"curl -s -d @- \"https://detect.roboflow.com/mobile-phone-detection-mtsje/1?api_key=h2EXOUFyekrJwf9BZKoC\""
    )
    
    # Execute the command
    proc = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if proc.returncode != 0:
        logging.error("Error during curl call: %s", proc.stderr)
        print(f"Error during curl call: {proc.stderr}")
        return False, 0.0

    # Load the output JSON response
    try:
        result = json.loads(proc.stdout)
    except json.JSONDecodeError:
        logging.error("Failed to decode JSON from response.")
        print("Failed to decode JSON from response.")
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
    print(f"Phone detected: {phone_detected} | Confidence: {phone_confidence:.2f}")
    return phone_detected, phone_confidence

if __name__ == "__main__":
    phone_detected, confidence = process_image("captured_images/resized_Phone.jpeg")
    logging.info("Phone detected: %s | Confidence: %.2f", phone_detected, confidence)
    print(f"Phone detected: {phone_detected} | Confidence: {confidence:.2f}")