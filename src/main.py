import cvModel2
import lcd
import threading
import time
import capturePhotos
import RPi.GPIO as GPIO
import os
import logging

# Global boolean variables
nightModeEnabled = False 
timerEnabled = False
buzzerEnabled = False
phoneMissing = False
brightNess = 10
phoneDetected = False
confidence = 0
confidenceThreshold = 0.2


target_dir = "/home/pi/projects/OSU-JD2-Timer/src/captured_images"
capture_filename = os.path.join(target_dir, "captured_image.jpeg")

photo_lock = threading.Lock()

# Configure logging
logging.basicConfig(filename='/home/pi/projects/OSU-JD2-Timer/main.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def triggerBuzzer():
    logging.info("Buzzer trigger thread started")
    
    BuzzerPin = 19  # Use GPIO 19

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BuzzerPin, GPIO.OUT)
    GPIO.setwarnings(False)

    global Buzz
    Buzz = GPIO.PWM(BuzzerPin, 440)
    Buzz.start(0)
    
    while True:
        while buzzerEnabled and not lcd.getNightMode():
            logging.info("Buzzer is enabled and night mode is off")
        if buzzerEnabled and not lcd.getNightMode():
            for _ in range(3):
                logging.info("Buzzer on for 1 second at 440 Hz")
                Buzz.ChangeDutyCycle(50)
                non_blocking_sleep(1)
                logging.info("Buzzer off for 1 second")
                Buzz.ChangeDutyCycle(0)
                non_blocking_sleep(1)
        else:
            Buzz.ChangeDutyCycle(0)  
    non_blocking_sleep(0.5)  

def getPhoto():
    while True:
        logging.info("Capturing photo")
        global capture_filename
        with photo_lock:
            capturePhotos.capture_photo(capture_filename)
        non_blocking_sleep(4)
        logging.info("Photo captured and saved as %s", capture_filename)

def non_blocking_sleep(seconds):
    logging.info("Sleeping for %d seconds", seconds)
    event = threading.Event()
    event.wait(seconds)

def process_image_thread(capture_filename):
    logging.info("Image processing thread started")
    global phoneDetected, confidence
    while True:
        with photo_lock:
            phoneDetected, confidence = cvModel2.process_image(capture_filename)
            logging.info("Image processed: phoneDetected=%s, confidence=%.2f", phoneDetected, confidence)
        non_blocking_sleep(5)

def updateOutput():
    logging.info("Update output thread started")
    global phoneMissing, phoneDetected, confidence, confidenceThreshold

    while True:
        non_blocking_sleep(5)

        if lcd.timer_running:
            logging.info("Timer is running")
            if not phoneDetected or confidence < confidenceThreshold:
                phoneMissing = True
                lcd.setTimerRunning(False)
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
                    phoneMissing = False
                    lcd.start_timer() 
                    buzzerEnabled = False
                    logging.info("Buzzer Disabled")
                    print("Buzzer Disabled")

def main():
    logging.info("Main function started")
    cv_thread = threading.Thread(target=process_image_thread, args=(capture_filename,))
    cv_thread.daemon = True
    cv_thread.start()
    logging.info("Started image processing thread")

    updateOutput_thread = threading.Thread(target=updateOutput)
    updateOutput_thread.daemon = True
    updateOutput_thread.start()
    logging.info("Started update output thread")

    updatePhoto_thread = threading.Thread(target=getPhoto)
    updatePhoto_thread.daemon = True
    updatePhoto_thread.start()
    logging.info("Started photo capture thread")

    triggerBuzzer_thread = threading.Thread(target=triggerBuzzer)
    triggerBuzzer_thread.daemon = True
    triggerBuzzer_thread.start()
    logging.info("Started buzzer trigger thread")

    lcd.main()
    logging.info("LCD main function started")

if __name__ == "__main__":
    main()
    logging.info("Program started")