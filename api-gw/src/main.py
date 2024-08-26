
import os
import json
import time
import requests
from threading import Thread, Event
from flask import Flask, request
from flask_json import json_response, FlaskJSON
from kafka import KafkaProducer, KafkaConsumer


app = Flask(__name__)
FlaskJSON(app)

DEVICE_ADD_TOPIC = 'device-add'
DEVICE_SET_STATE = 'device-state-set'
DEVICE_GET_STATE = 'device-telemetry'


print(os.environ["KAFKA_SERVER"])
java_monolith_addr = os.environ["JAVA_MONOLITH_ADDR"]
kafka_producer = KafkaProducer(bootstrap_servers=os.environ["KAFKA_SERVER"])
kafka_consumer = KafkaConsumer(DEVICE_GET_STATE, bootstrap_servers=os.environ["KAFKA_SERVER"])


STATE_CACHE = {}
TERMINATE = Event()


def read_kafka_messages():
    while not TERMINATE.is_set():
        for topic, messages in kafka_consumer.poll().items():
            for message in messages:
                device_data = json.loads(message.value)
                device_id = device_data.get("device_id")

                if device_id:
                    STATE_CACHE[device_id] = device_data

        time.sleep(0.001)


@app.route("/")
def index():
    return "OK", 200


@app.route("/device/add", methods=("POST",))
def add_device():
    data = request.get_json()
    kafka_producer.send(DEVICE_ADD_TOPIC, json.dumps(data).encode('utf-8'))
    return 'OK', 200


@app.route("/device/state", methods=("POST", ))
def set_device_state():
    data = request.get_json()

    if data["device_type"] == "hit_device":
        if data["status"] == "off":
            data = requests.post(java_monolith_addr + "/" + data["device_id"] + "/turn-on")
            data = requests.post(java_monolith_addr + "/" + data["device_id"] + "/set-temperature")
            return "OK", 200
    else:
        kafka_producer.send(DEVICE_SET_STATE, json.dumps(data).encode('utf-8'))
        return 'OK', 200


@app.route("/device/state", methods=("GET",))
def get_device_state():
    data = request.get_json()

    # java monolith behaviour
    if data["device_type"] == "hit_device":
        data = requests.get(java_monolith_addr + '/' + device["id"])
        return json_response(**data)

    else:
        response = STATE_CACHE.get(data["device_id"])
        return json_response(**response)


read_proc = Thread(target=read_kafka_messages)
read_proc.start()
app.run(host='0.0.0.0')

TERMINATE.set()
print("wait for proc termination")
read_proc.join()
