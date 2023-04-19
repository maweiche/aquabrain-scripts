# Air Temp Sensor - DHT22
import adafruit_dht
import board
# Constants
from ISStreamer.Streamer import Streamer
import time


# --------- User Settings ---------
AIR_SENSOR_LOCATION_NAME = "Air"
WATER_SENSOR_LOCATION_NAME = "Water"
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
dhtSensor = adafruit_dht.DHT22(board.D4)

while True:
        try:
                # Air Sensor
                humidity = dhtSensor.humidity
                temp_c = dhtSensor.temperature

        except RuntimeError:
                print("RuntimeError, trying again...")
                continue
                
        if METRIC_UNITS:
                streamer.log(AIR_SENSOR_LOCATION_NAME + " Temperature(C)", temp_c)
        else:
                temp_f = format(temp_c * 9.0 / 5.0 + 32.0, ".2f")
                streamer.log(AIR_SENSOR_LOCATION_NAME + " Temperature(F)", temp_f)
        humidity = format(humidity,".2f")
        streamer.log(AIR_SENSOR_LOCATION_NAME + " Humidity(%)", humidity)
        streamer.flush()
        time.sleep(60*MINUTES_BETWEEN_READS)