# Air Temp Sensor - DHT22
import adafruit_dht
import board
# Water Temp Sensor - DS18B20
import os
import glob
# Constants
from ISStreamer.Streamer import Streamer
import time


# --------- User Settings ---------
AIR_SENSOR_LOCATION_NAME = "Air"
WATER_SENSOR_LOCATION_NAME = "Water"
DISTANCE_SENSOR_A_LOCATION_NAME = "Filter Water Level"
BUCKET_NAME = ":partly_sunny: Room Temperatures"
BUCKET_KEY = "4WV9PEU4G6K4"
ACCESS_KEY = "ist_CsfUMjskTuo0o7UEoW-D7tjPb68ZwQru"
MINUTES_BETWEEN_READS = 10
METRIC_UNITS = False
# ---------------------------------

# Live Data Stream - Initializer
streamer = Streamer(bucket_name=BUCKET_NAME, bucket_key=BUCKET_KEY, access_key=ACCESS_KEY)

# Air Temp Sensor - DHT22
# Initialize the DHT device, with data pin connected to:
dhtSensor = adafruit_dht.DHT22(board.D4, use_pulseio=False)

# Water Temp Sensor - DS18B20 ----------------
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

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
# --------------------------------------------

while True:
        try:
                # Air Sensor
                humidity = dhtSensor.humidity
                temp_c = dhtSensor.temperature

                # Water Sensor
                temp_d = read_temp()
                temp_e = temp_d * 9.0 / 5.0 + 32.0

        except RuntimeError:
                print("RuntimeError, trying again...")
                continue
                
        if METRIC_UNITS:
                streamer.log(AIR_SENSOR_LOCATION_NAME + " Temperature(C)", temp_c)
                streamer.log(WATER_SENSOR_LOCATION_NAME + " Temperature(C)", temp_d)
        else:
                temp_f = format(temp_c * 9.0 / 5.0 + 32.0, ".2f")
                streamer.log(AIR_SENSOR_LOCATION_NAME + " Temperature(F)", temp_f)
                streamer.log(WATER_SENSOR_LOCATION_NAME + " Temperature(F)", temp_e)
        humidity = format(humidity,".2f")
        streamer.log(AIR_SENSOR_LOCATION_NAME + " Humidity(%)", humidity)
        streamer.flush()
        time.sleep(60*MINUTES_BETWEEN_READS)