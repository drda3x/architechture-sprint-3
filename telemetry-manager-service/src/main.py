import json
import argparse
import time
import logging

from device_database import DeviceDatabase
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import NoBrokersAvailable

DEVICE_ADD_TOPIC = 'device-add'
TELEMETRY_TOPIC = 'device-telemetry'

logger = logging.getLogger("TelemetryManager")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)


def process_message(db, topic, message_data):
    logger.info(f"Received {message_data} from {topic}")
    if topic == DEVICE_ADD_TOPIC:
        db.add(message_data)


def wait_kafka(kafka_server):
    broker_found = False
    consumer, produser = None, None
    while not broker_found:
        try:
            produser = KafkaProducer(bootstrap_servers=kafka_server)
            consumer = KafkaConsumer(DEVICE_ADD_TOPIC, bootstrap_servers=kafka_server)
            broker_found = True

        except NoBrokersAvailable:
            pass

        finally:
            time.sleep(2)

    return consumer, produser


def main(kafka_server):
    db = DeviceDatabase(logger)

    logger.info("Wait for kafka")
    consumer, produser = wait_kafka(kafka_server)
    logger.info("kafka ok")

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
