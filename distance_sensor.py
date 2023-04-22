#!/usr/bin/python
import RPi.GPIO as GPIO
import time
from ISStreamer.Streamer import Streamer

DISTANCE_SENSOR_A_LOCATION_NAME = "Filter Water Level"
BUCKET_NAME = ":partly_sunny: Room Temperatures"
BUCKET_KEY = "4WV9PEU4G6K4"
ACCESS_KEY = "ist_CsfUMjskTuo0o7UEoW-D7tjPb68ZwQru"
MINUTES_BETWEEN_READS = 10
METRIC_UNITS = False


# Live Data Stream - Initializer
streamer = Streamer(bucket_name=BUCKET_NAME, bucket_key=BUCKET_KEY, access_key=ACCESS_KEY)


try:
      GPIO.setmode(GPIO.BOARD)

      PIN_TRIGGER = 7
      PIN_ECHO = 11

      GPIO.setup(PIN_TRIGGER, GPIO.OUT)
      GPIO.setup(PIN_ECHO, GPIO.IN)

      GPIO.output(PIN_TRIGGER, GPIO.LOW)

      print("Waiting for sensor to settle")

      time.sleep(2)

      print("Calculating distance")

      GPIO.output(PIN_TRIGGER, GPIO.HIGH)

      time.sleep(0.00001)

      GPIO.output(PIN_TRIGGER, GPIO.LOW)

      while GPIO.input(PIN_ECHO)==0:
            pulse_start_time = time.time()
      while GPIO.input(PIN_ECHO)==1:
            pulse_end_time = time.time()

      pulse_duration = pulse_end_time - pulse_start_time
      distance = round(pulse_duration * 17150, 2)
      print("Distance:",distance,"cm")
      # convert distance from cm to inches
      distance_inches = format(distance * 0.393701, ".2f")
      streamer.log(DISTANCE_SENSOR_A_LOCATION_NAME + " Distance(inches)", distance_inches)
      streamer.flush()

finally:
      GPIO.cleanup()