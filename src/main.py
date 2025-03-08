import cvModel2
import lcd
import threading
import time
import capturePhotos
import RPi.GPIO as GPIO
import logging

# Global boolean variables
nightModeEnabled = True 
timerEnabled = False
buzzerEnabled = False
phoneMissing = False
brightNess = 10
phoneDetected = False
confidence = 0
confidenceThreshold = 0.5

capture_filename = "resized_Phone.jpeg"

photo_lock = threading.Lock()

# Configure logging
logging.basicConfig(filename='main.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def triggerBuzzer():

    BuzzerPin = 26

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BuzzerPin, GPIO.OUT) 
    GPIO.setwarnings(False)

    global Buzz 

    while buzzerEnabled and not lcd.getNightMode():
        Buzz = GPIO.PWM(BuzzerPin, 440) 
        Buzz.start(50) 


def getPhoto():
    global capture_filename
    with photo_lock:
        capturePhotos.capture_photo(capture_filename)
    non_blocking_sleep(1)

def non_blocking_sleep(seconds):
    event = threading.Event()
    event.wait(seconds)

def process_image_thread(capture_filename):
    global phoneDetected, confidence
    while True:
        with photo_lock:
            phoneDetected, confidence = cvModel2.process_image(capture_filename)
        non_blocking_sleep(5)
def updateOutput():
    global nightModeEnabled, timerEnabled, buzzerEnabled, phoneMissing, brightNess, phoneDetected, confidence, capture_filename
    while True:
        non_blocking_sleep(5)
        if(lcd.timer_running):
            if (not phoneDetected) or (confidence < confidenceThreshold):
                phoneMissing = True
                lcd.setTimerRunning(False)
                logging.info("Phone not found; Phone Missing = True")
                print("Phone not found; Phone Missing = True")
                if not nightModeEnabled:
                    buzzerEnabled = True
                    logging.info("Buzzer Enabled = True")
                    print("Buzzer Enabled = True")
            else:
                phoneMissing = False
                lcd.setTimerRunning(True)
                buzzerEnabled = False
                logging.info("Phone Found; phoneMissing = False buzzerEnabled = False")
                print("Phone Found; phoneMissing = False buzzerEnabled = False") 

def main():
    cv_thread = threading.Thread(target=process_image_thread, args=(capture_filename,))
    cv_thread.daemon = True
    cv_thread.start()

    updateOutput_thread = threading.Thread(target=updateOutput)
    updateOutput_thread.daemon = True
    updateOutput_thread.start()

    updatePhoto_thread = threading.Thread(target=getPhoto)
    updatePhoto_thread.daemon = True
    updatePhoto_thread.start()

    triggerBuzzer_thread = threading.Thread(target=triggerBuzzer)
    triggerBuzzer_thread.daemon = True
    triggerBuzzer_thread.start()

    lcd.main()

if __name__ == "__main__":
    main()