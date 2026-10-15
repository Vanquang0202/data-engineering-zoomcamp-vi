---
prev_url: 03-produce-messages-to-kafka.md
next_url: 05-save-events-to-postgresql.md
---
# Sử dụng tin nhắn bằng Python

Bây giờ chúng ta hãy đọc lại tin nhắn. Người tiêu dùng nhận được byte thô từ
Kafka. Thay vì giải tuần tự hóa thành một lệnh rồi xây dựng `Ride`
theo cách thủ công, hãy viết một hàm thực hiện cả hai điều đó trong một bước:


*Các nhóm người tiêu dùng theo dõi tiến trình thông qua chủ đề: phát lại sớm nhất các bản ghi có sẵn, trong khi bản ghi mới nhất bắt đầu ở bản ghi mới.*

```python
import json

def ride_deserializer(data):
    json_str = data.decode('utf-8')
    ride_dict = json.loads(json_str)
    return Ride(**ride_dict)
```

Kiểm tra nó bằng chuỗi nhị phân JSON mẫu (đây là những gì Kafka cung cấp):

```python
test_bytes = json.dumps({
    'PULocationID': 186,
    'DOLocationID': 79,
    'trip_distance': 1.72,
    'total_amount': 17.31,
    'tpep_pickup_datetime': 1730429702000
}).encode('utf-8')

ride_deserializer(test_bytes)
# Ride(PULocationID=186, DOLocationID=79, trip_distance=1.72,
# total_amount=17.31, tpep_pickup_datetime=1730429702000)
```

Bây giờ chúng ta có thể chuyển trực tiếp `ride_deserializer` dưới dạng `value_deserializer` -
Kafka gọi nó trên mọi tin nhắn, vì vậy `message.value` đã là `Ride`.

Kết nối với Kafka với tư cách là người tiêu dùng. `auto_offset_reset='earliest'` có nghĩa là chúng tôi
bắt đầu đọc từ đầu chủ đề (không có điều này, người tiêu dùng mới
mặc định là `latest` và chỉ xem tin nhắn mới). `group_id` xác định nhóm người tiêu dùng
này - Kafka theo dõi xem mỗi nhóm đã đọc được bao xa, vì vậy việc khởi động lại
với cùng một ID nhóm sẽ tiếp tục ở nơi nó đã dừng lại:

```python
from kafka import KafkaConsumer

server = 'localhost:9092'
topic_name = 'rides'

consumer = KafkaConsumer(
    topic_name,
    bootstrap_servers=[server],
    auto_offset_reset='earliest',
    group_id='rides-console',
    value_deserializer=ride_deserializer
)
```

Đọc tin nhắn và in chúng. Vì `value_deserializer` trả về `Ride`,
`message.value` đã là đối tượng `Ride` - không cần chuyển đổi thêm:

```python
from datetime import datetime

print(f"Listening to {topic_name}...")

count = 0
for message in consumer:
    ride = message.value
    pickup_dt = datetime.fromtimestamp(ride.tpep_pickup_datetime / 1000)
    print(f"Received: PU={ride.PULocationID}, DO={ride.DOLocationID}, "
          f"distance={ride.trip_distance}, amount=${ride.total_amount:.2f}, "
          f"pickup={pickup_dt}")
    count += 1
    if count >= 10:
        print(f"\n... received {count} messages so far (stopping after 10 for demo)")
        break

consumer.close()
```

> Tập lệnh hoàn chỉnh có trong `src/consumers/consumer.py`.

Chạy nó:

```bash
uv run python src/consumers/consumer.py
```

```
Listening to rides...
Received: PU=..., DO=..., distance=..., amount=$..., pickup=2025-...
...
... received 10 messages so far (stopping after 10 for demo)
```
