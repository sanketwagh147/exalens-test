import paho.mqtt.client as mqtt
import json
import time
import random
from datetime import datetime
import os

sensor_id = os.getenv("SENSOR_ID", default=None)
sensor_type = os.getenv("SENSOR_TYPE", default=None)

if not sensor_id:
    raise ValueError("Sensor Id must be present as environment variables")
if not sensor_type:
    raise ValueError("Sensor Type must be present as environment variables")


mqtt_broker_host = "my-mosquitto"  
mqtt_port = 1883
mqtt_topic = sensor_type


def publish_temperature(client, value):
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
    publish_temperature(client, "25.5")

client = mqtt.Client()
client.on_connect = on_connect

client.connect(mqtt_broker_host, mqtt_port, 60)

client.loop_start()

try:
    while True:
        temperature_reading = random.randint(10, 40)

        publish_temperature(client, temperature_reading)
        time.sleep(5)  
except KeyboardInterrupt:
    print("Exit")
    client.loop_stop()
    client.disconnect()
