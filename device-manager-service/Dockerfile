from python

run pip install kafka-python-ng
copy ./src /app
workdir /app

env KAFKA_SERVER="localhost:9092"

cmd python main.py --kafka $KAFKA_SERVER
