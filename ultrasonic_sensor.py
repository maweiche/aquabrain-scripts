import RPi.GPIO as GPIO
import time
GPIO.setmode (GPIO.BCM)

TRIG_PIN=23
ECHO_PIN=32

GPIO.setup(TRIG_PIN,GPIO.OUT)
GPIO.setup(ECHO_PIN,GPIO.IN)
GPIO.OUTPUT(TRIG_PIN,GPIO.LOW)

print("Waiting for sensor to settle")

time.sleep(2)

print("Calculating distance")

GPIO.output(TRIG_PIN,GPIO.HIGH)

time.sleep(0.00001)


GPIO.output(TRIG_PIN,GPIO.LOW)

while GPIO.input(ECHO_PIN)==0:
    pulse_start=time.time()

while GPIO.input(ECHO_PIN)==1:
    pulse_end=time.time()

pulse_duration=pulse_end-pulse_start

pulse_duration=round(pulse_duration,2,2)

distance=3400*pulse_duration

print("Object is",distance,"cm away from the sensor")

GPIO.cleanup()

