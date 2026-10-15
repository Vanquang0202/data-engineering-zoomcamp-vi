import json
from time import time

import pandas as pd
from kafka import KafkaProducer


url = "https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-10.parquet"

columns = [
    'lpep_pickup_datetime',
    'lpep_dropoff_datetime',
    'PULocationID',
    'DOLocationID',
    'passenger_count',
    'trip_distance',
    'tip_amount',
    'total_amount',
]

df = pd.read_parquet(url, columns=columns)

# Convert datetime columns to strings for JSON serialization
df['lpep_pickup_datetime'] = df['lpep_pickup_datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')
df['lpep_dropoff_datetime'] = df['lpep_dropoff_datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')

# Fill NaN values in passenger_count
df['passenger_count'] = df['passenger_count'].fillna(0).astype(int)


def json_serializer(data):
    return json.dumps(data).encode('utf-8')


server = 'localhost:9092'
topic_name = 'green-trips'

producer = KafkaProducer(
    bootstrap_servers=[server],
    value_serializer=json_serializer
)

t0 = time()

for _, row in df.iterrows():
    message = row.to_dict()
    producer.send(topic_name, value=message)

producer.flush()

t1 = time()
print(f'Sent {len(df)} messages')
print(f'Took {(t1 - t0):.2f} seconds')
