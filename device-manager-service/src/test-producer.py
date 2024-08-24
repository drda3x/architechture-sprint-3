import time
import json
import argparse
from kafka import KafkaProducer


def main(kafka_server):
    produser = KafkaProducer()

    test_messages = [
        ('device-add', dict(device_id=1, device_type="light_device")),
        ('device-add', dict(device_id=2, device_type="gate_device")),
        ('device-state-set', dict(device_id=1, status='off')),
        ('device-state-set', dict(device_id=2, status='open'))
    ]

    for topic, message in test_messages:
        produser.send(topic, json.dumps(message).encode("utf-8"))
        print(f"send: {message}")
        time.sleep(1)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--kafka", help="Kafka server setting")

    args = parser.parse_args()

    if args.kafka:
        main(args.kafka)
