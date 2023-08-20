import paho.mqtt.client as mqtt
import json
from pymongo import MongoClient
from datetime import datetime

mqtt_broker_host = "my-mosquitto"  
mqtt_port = 1883
mqtt_topic = "temperature"

mongodb_host = "my-mongodb"  
mongodb_port = 27017
mongodb_db = "sensor_data"
mongodb_collection = "readings"

def on_message(client, userdata, message):
    payload = message.payload.decode("utf-8")
    data = json.loads(payload)
    store_in_mongodb(data)

def store_in_mongodb(data):
    client = MongoClient(mongodb_host, mongodb_port)
    db = client[mongodb_db]
    collection = db[mongodb_collection]
    data["timestamp"] = datetime.utcnow()
    collection.insert_one(data)
    print("Stored data in MongoDB:", data)

client = mqtt.Client()
client.on_message = on_message

client.connect(mqtt_broker_host, mqtt_port, 60)
client.subscribe(mqtt_topic)

client.loop_forever()
