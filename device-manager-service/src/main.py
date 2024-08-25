import time
import json
import argparse

from kafka import KafkaConsumer
from device_database import DeviceDatabase


STATE_SET_TOPIC  = 'device-state-set'
DEVICE_ADD_TOPIC = 'device-add'

TOPICS = [
    STATE_SET_TOPIC,
    DEVICE_ADD_TOPIC
]


def process_message(db, topic, message_data):
    if topic == DEVICE_ADD_TOPIC:
        db.add(message_data)

    elif topic == STATE_SET_TOPIC:
        device = db.get(message_data)
        if device:
            device.set_state(message_data)


def main(kafka_server):
    consumer = KafkaConsumer(*TOPICS, bootstrap_servers=kafka_server)
    db = DeviceDatabase()
    rate = 0.1

    while True:
        try:
            polled = consumer.poll()
            for topic, messages in polled.items():
                messages = list(messages)
                messages.sort(key=lambda x: (x.timestamp, x.offset))
                for message in messages:
                    process_message(db, topic.topic, json.loads(message.value))
            time.sleep(rate)
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--kafka", help="Kafka server setting")

    args = parser.parse_args()

    if args.kafka:
        main(args.kafka)
    else:
        pass
