import time
import json
import argparse
import logging

from kafka import KafkaConsumer
from device_database import DeviceDatabase
from kafka.errors import NoBrokersAvailable


STATE_SET_TOPIC  = 'device-state-set'
DEVICE_ADD_TOPIC = 'device-add'

TOPICS = [
    STATE_SET_TOPIC,
    DEVICE_ADD_TOPIC
]

logger = logging.getLogger("DeviceManager")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)


def process_message(db, topic, message_data):
    logger.info(f"Received {message_data} from {topic}")
    if topic == DEVICE_ADD_TOPIC:
        db.add(message_data)

    elif topic == STATE_SET_TOPIC:
        device = db.get(message_data)
        if device:
            device.set_state(message_data)


def wait_consumer(kafka_server):
    broker_found = False
    consumer = None
    while not broker_found:
        try:
            consumer = KafkaConsumer(*TOPICS, bootstrap_servers=kafka_server)
            broker_found = True

        except NoBrokersAvailable:
            pass

        finally:
            time.sleep(2)
    return consumer


def main(kafka_server):
    logger.info("Waiting for kafka server")
    consumer = wait_consumer(kafka_server)
    logger.info("Kafka server OK")
    db = DeviceDatabase(logger)
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
