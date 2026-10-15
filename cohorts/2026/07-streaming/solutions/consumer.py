import json
from collections import Counter

from kafka import KafkaConsumer


def json_deserializer(data):
    return json.loads(data.decode('utf-8'))


server = 'localhost:9092'
topic_name = 'green-trips'

consumer = KafkaConsumer(
    topic_name,
    bootstrap_servers=[server],
    auto_offset_reset='earliest',
    group_id='green-trips-homework',
    value_deserializer=json_deserializer,
    consumer_timeout_ms=10000,  # stop after 10s of no messages
)

count = 0
long_trips = 0

for message in consumer:
    trip = message.value
    count += 1
    if trip['trip_distance'] > 5.0:
        long_trips += 1

consumer.close()

print(f'Total messages: {count}')
print(f'Trips with distance > 5: {long_trips}')
