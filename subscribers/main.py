import paho.mqtt.client as mqtt
import json
from pymongo import MongoClient
from datetime import datetime
import os
import sys

topics = os.getenv("SENSOR_TYPES", "")
if not topics:
    print("Sensor TYPES must be present as environment variables")
    exit()

mqtt_broker_host = "my-mosquitto"  
mqtt_port = 1883

mongodb_host = "my-mongodb"  
mongodb_port = 27017
mongodb_db = "sensor_data"
mongodb_collection = "readings"

def on_message(client, userdata, message):
    payload = message.payload.decode("utf-8")
    data = json.loads(payload)
    store_in_mongodb(data, sensor_type=message.topic)

def store_in_mongodb(data, sensor_type):
    client = MongoClient(mongodb_host, mongodb_port)
    db = client[mongodb_db]
    collection = db[mongodb_collection]
    data["timestamp"] = datetime.utcnow()
    data["sensor_type"] = sensor_type
    collection.insert_one(data)
    print("Stored data in MongoDB:", data)

client = mqtt.Client()
client.on_message = on_message

client.connect(mqtt_broker_host, mqtt_port, 60)

for each in topics.split(","):
    client.subscribe(each)

client.loop_forever()
