# this script should be run on the raspberry pi
# it will turn on a servo motor at pin 24
# the servo motor will rotate 180 degrees then back to 0 degrees

import RPi.GPIO as GPIO
import time

servoPIN = 24
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50) # GPIO 24 for PWM with 50Hz
p.start(2.5) # Initialization
try:
        while True:
                p.ChangeDutyCycle(5)
                time.sleep(0.5)
                p.ChangeDutyCycle(7.5)
                time.sleep(0.5)
                p.ChangeDutyCycle(10)
                time.sleep(0.5)
                p.ChangeDutyCycle(12.5)
                time.sleep(0.5)
                p.ChangeDutyCycle(10)
                time.sleep(0.5)
                p.ChangeDutyCycle(7.5)
                time.sleep(0.5)
                p.ChangeDutyCycle(5)
                time.sleep(0.5)
                p.ChangeDutyCycle(2.5)
                time.sleep(0.5)
except KeyboardInterrupt:
        p.stop()
        GPIO.cleanup()

