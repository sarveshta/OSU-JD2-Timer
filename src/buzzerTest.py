import RPi.GPIO as GPIO

def triggerBuzzer():
    while True:
        BuzzerPin = 26

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(BuzzerPin, GPIO.OUT) 
        GPIO.setwarnings(False)

        global Buzz 

        # while buzzerEnabled and not lcd.getNightMode():
        while True:
            Buzz = GPIO.PWM(BuzzerPin, 440) 
            Buzz.start(50) 
