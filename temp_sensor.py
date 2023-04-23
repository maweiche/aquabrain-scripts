# Air Temp Sensor - DHT22
import adafruit_dht
import board
# Water Temp Sensor - DS18B20
import os
import glob
# Distance Sensor - HC-SR04
import RPi.GPIO as GPIO
# Water Pump - Relay
from classes import Hardware
from classes import TimeKeeper as TK
import schedule
import smtplib
import ssl

# Constants
from ISStreamer.Streamer import Streamer
import time

# --------- User Settings ---------
AIR_SENSOR_LOCATION_NAME = "Tank A - Air"
WATER_SENSOR_LOCATION_NAME = "Tank A - Water"
DISTANCE_SENSOR_A_LOCATION_NAME = "Filter Water Level"
SERVO_MOTOR_A_LOCATION_NAME = "Tank A - Fish"
WATER_PUMP_NAME = "Tank A - Filter"
BUCKET_NAME = "Tank_A"
BUCKET_KEY = "WQD6H7XVNKXE"
ACCESS_KEY = "ist_6e6lvyD--6Gm7Z6FJri4PZ4q-_pC7t4V"
MINUTES_BETWEEN_READS = 10
METRIC_UNITS = False
# ---------------------------------

# Live Data Stream - Initializer
streamer = Streamer(bucket_name=BUCKET_NAME, bucket_key=BUCKET_KEY, access_key=ACCESS_KEY)

# Air Temp Sensor - DHT22

# Initialize the DHT device, with data pin connected to:
# dhtSensor = adafruit_dht.DHT22(7, use_pulseio=False)
dhtSensor = adafruit_dht.DHT22(board.D4, use_pulseio=False)

# Water Temp Sensor - DS18B20 ----------------
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

# Water Pump - Relay -------------------------
# WATERING_TIME must be in "00:00:00 PM" format
WATERING_TIME = '11:59:50 AM'
SECONDS_TO_WATER = 5
RELAY = Hardware.Relay(18, False)
EMAIL_MESSAGES = {
    'last_watered': {
        'subject': 'Raspberry Pi: Plant Watering Time',
        'message': 'Your plant was last watered at'
    },
    'check_water_level': {
        'subject': 'Raspberry Pi: Check Water Level',
        'message': 'Check your water level!',
    }
}

def send_email(time_last_watered, subject, message):
    port = 465
    smtp_server = "smtp.gmail.com"
    FROM = TO = "YOUR_EMAIL@gmail.com"
    password = "YOUR_PASSWORD"

    complete_message = ''
    if time_last_watered == False:
        complete_message = "Subject: {}\n\n{}".format(subject, message)
    else:
        complete_message = "Subject: {}\n\n{} {}".format(subject, message, time_last_watered)
    
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(FROM, password)
        server.sendmail(FROM, TO, complete_message)

def send_last_watered_email(time_last_watered):
    message = EMAIL_MESSAGES['last_watered']['message']
    subject = EMAIL_MESSAGES['last_watered']['subject']
    send_email(time_last_watered, subject, message)

def send_check_water_level_email():
    message = EMAIL_MESSAGES['check_water_level']['message']
    subject = EMAIL_MESSAGES['check_water_level']['subject']
    send_email(False, subject, message)

def water_plant(relay, seconds):
    relay.on()
    # check to see if relay is on
    
    print("Plant is being watered!")
    time.sleep(seconds)
    print("Watering is finished!")
    relay.off()

def water_pump_actions():
    time_keeper = TK.TimeKeeper(TK.TimeKeeper.get_current_time())
    water_plant(RELAY, SECONDS_TO_WATER)
    print("\nPlant was last watered at {}".format(time_keeper.time_last_watered))
#     if(time_keeper.current_time == WATERING_TIME):
#         water_plant(RELAY, SECONDS_TO_WATER)
#         time_keeper.set_time_last_watered(TK.TimeKeeper.get_current_time())
#         print("\nPlant was last watered at {}".format(time_keeper.time_last_watered))
        # send_last_watered_email(time_keeper.time_last_watered)
        

# schedule.every().friday.at("12:00").do(send_check_water_level_email)



base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw():
        f = open(device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines

def read_temp():
        print("Reading temp")
        lines = read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
                time.sleep(0.2)
                lines = read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
                temp_string = lines[1][equals_pos+2:]
                temp_d = float(temp_string) / 1000.0
                print("Temp: " + str(temp_d))
                return temp_d
        
def run_servo():
        print("Running servo")
        servoPIN = 24
        GPIO.setup(servoPIN, GPIO.OUT)
        servo = GPIO.PWM(servoPIN, 50) # GPIO 24 for PWM with 50Hz
        servo.start(2.5) # Initialization
        # rotate 180 degrees then back to 0 degrees
        servo.ChangeDutyCycle(12.5) # 180 degrees
        time.sleep(1)
        servo.ChangeDutyCycle(2.5) # 0 degrees
        time.sleep(1)
        servo.stop()
        print("Servo stopped")
        return 

def measure_distance():
        # Distance Sensor
        GPIO.setmode(GPIO.BCM)

        PIN_TRIGGER = 11
        PIN_ECHO = 12

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
        return distance

# --------------------------------------------

while True:
        try:
                # Air Sensor
                humidity = dhtSensor.humidity
                temp_c = dhtSensor.temperature

                # Water Sensor
                temp_d = read_temp()
                temp_e = temp_d * 9.0 / 5.0 + 32.0
                
                # Distance Sensor
                measure_distance()

                # print("Running Water Pump Actions")
                # water_pump_actions()
                print("Running Servo")
                run_servo()
                GPIO.cleanup()
        except RuntimeError:
                GPIO.cleanup()
                print("RuntimeError, trying again...")
                continue
        except KeyboardInterrupt:
                servo.stop()
                GPIO.cleanup()
                
        if METRIC_UNITS:
                streamer.log(AIR_SENSOR_LOCATION_NAME + " Temperature(C)", temp_c)
                streamer.log(WATER_SENSOR_LOCATION_NAME + " Temperature(C)", temp_d)
                
        else:
                temp_f = format(temp_c * 9.0 / 5.0 + 32.0, ".2f")
                humidity = format(humidity,".2f")
                streamer.log(AIR_SENSOR_LOCATION_NAME + ": Humidity(%)", humidity)
                streamer.log(AIR_SENSOR_LOCATION_NAME + ": Temperature(F)", temp_f)
                streamer.log(WATER_SENSOR_LOCATION_NAME + ": Temperature(F)", temp_e)
                streamer.log(DISTANCE_SENSOR_A_LOCATION_NAME + ": Distance(cm)", distance)
                streamer.log(WATER_PUMP_NAME + ": Run Time (seconds)", SECONDS_TO_WATER)
                streamer.log(SERVO_MOTOR_A_LOCATION_NAME + ": Fed at", time.strftime("%H:%M:%S"))
        streamer.flush()
        time.sleep(1*MINUTES_BETWEEN_READS)

