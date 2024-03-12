import os
import json
import sys
import logging
import paho.mqtt.client as mqtt
from pymongo import MongoClient


logging.basicConfig(stream=sys.stdout, level=logging.INFO)

logging.info("Starting MQTT to MongoDB service")

# Load configuration from environment variables
mongo_host = os.getenv('MONGO_HOST')
mongo_port = int(os.getenv('MONGO_PORT'))  # Convert port to integer
mongo_username = os.getenv('MONGO_USERNAME')
mongo_password = os.getenv('MONGO_PASSWORD')
mongo_database_name = os.getenv('MONGO_DATABASE_NAME')
mongo_collection_name = os.getenv('MONGO_COLLECTION_NAME')

mqtt_user = os.getenv('MQTT_USER')
mqtt_password = os.getenv('MQTT_PASSWORD')
mqtt_host = os.getenv('MQTT_HOST')
mqtt_port = int(os.getenv('MQTT_PORT'))  # Convert port to integer
mqtt_topic = os.getenv('MQTT_TOPIC')


# MongoDB setup
mongo_client = MongoClient(host=mongo_host, port=mongo_port,
                           username=mongo_username, password=mongo_password)

# Check if the database exists
db_list = mongo_client.list_database_names()
if mongo_database_name not in db_list:
    # The database doesn't exist, so we attempt to create it by creating a collection
    db = mongo_client[mongo_database_name]
    try:
        db.create_collection(mongo_collection_name)
        logging.info(f"Database and collection '{mongo_collection_name}' created.")
    except:
        logging.warning(f"Collection '{mongo_collection_name}' already exists.")
else:
    logging.warning(f"Database '{mongo_database_name}' already exists.")


db = mongo_client[mongo_database_name]
collection = db[mongo_collection_name]

mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)  # Create a new MQTT client
mqtt_client.username_pw_set(mqtt_user, mqtt_password)  # Set MQTT credentials

# Configure TLS/SSL connection if necessary (uncomment if needed)
mqtt_client.tls_set()


# MQTT setup and event handlers
def on_connect(client, userdata, flags, rc):
    logging.info(f"Connected with result code {rc}")
    client.subscribe(mqtt_topic)  # Subscribe to the topic from the environment

def on_message(client, userdata, msg):
    try:
        # Convert message payload to string and then to JSON
        message_str = msg.payload.decode('utf-8')
        message_data = json.loads(message_str[:-1])
        # Insert the message into MongoDB
        logging.info(f"Inserting message into MongoDB: {message_data}")
        message_data['topic'] = msg.topic
        
        collection.insert_one(message_data)
    except Exception as e:
        logging.error(f"Error handling message: {e}")

mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

try:
    mqtt_client.connect(mqtt_host, mqtt_port, 60)  # Connect to the MQTT broker
    mqtt_client.loop_forever()  # Start processing MQTT messages
except Exception as e:
    logging.error(f"Error connecting to MQTT broker: {e}")
