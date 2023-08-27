import paho.mqtt.client as mqtt
import json
import time
import random
from datetime import datetime
import os

sensor_id = os.getenv("SENSOR_ID", default=None)
sensor_type = os.getenv("SENSOR_TYPE", default=None)
frequency = os.getenv("FREQUENCY", default=None)
range_ = os.getenv("RANGE",default=None)


if not range_:
    print("Sensor range must be present in the env vars")
    exit()

if not sensor_id:
    print("Sensor Id must be present as environment variables")
    exit()
if not sensor_type:
    print("Sensor Type must be present as environment variables")
    exit()
if not frequency:
    print("Frequency must be present as environment variables for the publisher device")
    exit()


mqtt_broker_host = "my-mosquitto"  
mqtt_port = 1883
mqtt_topic = sensor_type


def publish_sensor_reading(client, value):
    timestamp = datetime.utcnow().isoformat()
    payload = {
        "sensor_id": sensor_id,
        "value": value,
        "timestamp": timestamp
    }
    client.publish(mqtt_topic, json.dumps(payload))

#TODO: more on this later
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    publish_sensor_reading(client, "25.5")

client = mqtt.Client()
client.on_connect = on_connect

client.connect(mqtt_broker_host, mqtt_port, 60)

client.loop_start()

try:
    while True:
        sensor_reading = random.randint(*[int(i) for i in range_.split(",")])

        publish_sensor_reading(client, sensor_reading)
        time.sleep(int(frequency))  
except KeyboardInterrupt:
    print("Exit")
    client.loop_stop()
    client.disconnect()
