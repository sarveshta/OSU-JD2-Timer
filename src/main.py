import cvModel2
import lcd
import threading
import time
import capturePhotos
import pigpio
import os
import logging

# Global boolean variables
nightModeEnabled = False 
timerEnabled = False
buzzerEnabled = False
phoneMissing = False
brightNess = 10
phoneDetected = True
confidence = 0
confidenceThreshold = 0.2
alertFlag = True


target_dir = "/home/pi/projects/OSU-JD2-Timer/src/captured_images"
capture_filename = os.path.join(target_dir, "captured_image.jpeg")

photo_lock = threading.Lock()

# Configure logging
logging.basicConfig(filename='/home/pi/projects/OSU-JD2-Timer/main.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def triggerBuzzer():
    global buzzerEnabled, nightModeEnabled, alertFlag
    logging.info("Buzzer trigger thread started")
    print("Buzzer trigger thread started")
    
    BuzzerPin = 19  # Use GPIO 19
    pi = pigpio.pi()  # Connect to pigpio daemon

    if not pi.connected:
        logging.error("pigpio daemon is not running. Exiting buzzer thread.")
        print("pigpio daemon is not running. Exiting buzzer thread.")
        return
    
    pi.set_mode(BuzzerPin, pigpio.OUTPUT)

    try:
        while True:
            if buzzerEnabled and not lcd.getNightMode() and alertFlag:
                for _ in range(3):
                    logging.info("Buzzer on for 1 second at 440 Hz")
                    print("Buzzer on for 1 second at 440 Hz")
                    pi.hardware_PWM(BuzzerPin, 440, 500000)  # 440Hz, 50% duty cycle
                    non_blocking_sleep(1)

                    logging.info("Buzzer off for 1 second")
                    print("Buzzer off for 1 second")
                    pi.hardware_PWM(BuzzerPin, 0, 0)  # Stop PWM
                    non_blocking_sleep(1)
                    alertFlag = False
            else:
                pi.hardware_PWM(BuzzerPin, 0, 0)  # Ensure the buzzer is off
            if lcd.getNightMode:
                alertFlag = False
            if not buzzerEnabled:
                alertFlag = True
            non_blocking_sleep(0.5)  
            print(confidenceThreshold)

    except Exception as e:
        logging.error(f"Error in buzzer thread: {e}")
        print(f"Error in buzzer thread: {e}")

    finally:
        pi.hardware_PWM(BuzzerPin, 0, 0)  # Stop PWM before exiting
        pi.stop()  # Disconnect from pigpio
        logging.info("Buzzer thread stopped")
        print("Buzzer thread stopped")

def getPhoto():
    global capture_filename
    while True:
        logging.info("Capturing photo")
        print("Capturing photo")
        with photo_lock:
            capturePhotos.capture_photo(capture_filename)
        non_blocking_sleep(4)
        logging.info("Photo captured and saved as %s", capture_filename)
        print(f"Photo captured and saved as {capture_filename}")

def non_blocking_sleep(seconds):
    logging.info("Sleeping for %d seconds", seconds)
    print(f"Sleeping for {seconds} seconds")
    event = threading.Event()
    event.wait(seconds)

def process_image_thread(capture_filename):
    global phoneDetected, confidence
    logging.info("Image processing thread started")
    print("Image processing thread started")
    while True:
        with photo_lock:
            phoneDetected, confidence = cvModel2.process_image(capture_filename)
            logging.info("Image processed: phoneDetected=%s, confidence=%.2f", phoneDetected, confidence)
            print(f"Image processed: phoneDetected={phoneDetected}, confidence={confidence:.2f}")
        non_blocking_sleep(5)

def updateOutput():
    global phoneMissing, phoneDetected, confidence, confidenceThreshold, buzzerEnabled, nightModeEnabled
    logging.info("Update output thread started")
    print("Update output thread started")
    while True:
        non_blocking_sleep(5)
        confidenceThreshold = (lcd.getConfidenceThreshold() / 100)
        if lcd.timer_running:
            logging.info("Timer is running")
            print("Timer is running")
            if not phoneDetected or confidence < confidenceThreshold:
                phoneMissing = True
                lcd.stop_timer()
                lcd.increaseTimeBy(13) #Make up for time lost due to scheduling
                logging.info("Phone not found; Timer Stopped")
                print("Phone not found; Timer Stopped")
                
                if not nightModeEnabled:
                    buzzerEnabled = True
                    logging.info("Buzzer Enabled")
                    print("Buzzer Enabled")
            else:
                if phoneMissing: 
                    logging.info("Phone detected again. Restarting timer.")
                    print("Phone detected again. Restarting timer.")
                    phoneMissing = False
                    alertFlag = True
                    lcd.start_timer() 
                    buzzerEnabled = False
                    logging.info("Buzzer Disabled")
                    print("Buzzer Disabled")

def main():
    global capture_filename
    logging.info("Main function started")
    print("Main function started")
    cv_thread = threading.Thread(target=process_image_thread, args=(capture_filename,))
    cv_thread.daemon = True
    cv_thread.start()
    logging.info("Started image processing thread")
    print("Started image processing thread")

    updateOutput_thread = threading.Thread(target=updateOutput)
    updateOutput_thread.daemon = True
    updateOutput_thread.start()
    logging.info("Started update output thread")
    print("Started update output thread")

    updatePhoto_thread = threading.Thread(target=getPhoto)
    updatePhoto_thread.daemon = True
    updatePhoto_thread.start()
    logging.info("Started photo capture thread")
    print("Started photo capture thread")

    triggerBuzzer_thread = threading.Thread(target=triggerBuzzer)
    triggerBuzzer_thread.daemon = True
    triggerBuzzer_thread.start()
    logging.info("Started buzzer trigger thread")
    print("Started buzzer trigger thread")

    lcd.main()
    logging.info("LCD main function started")
    print("LCD main function started")

if __name__ == "__main__":
    main()
    logging.info("Program started")
    print("Program started")