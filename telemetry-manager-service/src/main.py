import json
import argparse
import time

from device_database import DeviceDatabase
from kafka import KafkaProducer, KafkaConsumer

DEVICE_ADD_TOPIC = 'device-add'
TELEMETRY_TOPIC = 'device-telemetry'


def process_message(db, topic, message_data):
    if topic == DEVICE_ADD_TOPIC:
        db.add(message_data)


def main(kafka_server):
    db = DeviceDatabase()
    produser = KafkaProducer(bootstrap_servers=kafka_server)
    consumer = KafkaConsumer(DEVICE_ADD_TOPIC, bootstrap_servers=kafka_server)
    rate = 0.1

    while True:
        try:
            polled = consumer.poll()
            for topic, messages in polled.items():
                messages = list(messages)
                messages.sort(key=lambda x: (x.timestamp, x.offset))
                for message in messages:
                    process_message(db, topic.topic, json.loads(message.value))

            for device in db.get_all():
                produser.send(TELEMETRY_TOPIC, json.dumps(device.get_data()).encode("utf-8"))

            time.sleep(rate)

        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--kafka", help="Kafka server setting")

    args = parser.parse_args()

    if args.kafka:
        main(args.kafka)
