---
prev_url: 04-consume-messages-with-python.md
next_url: 06-why-flink.md
---
# Lưu sự kiện vào PostgreSQL

In ra màn hình là cách tốt để gỡ lỗi, nhưng hãy lưu các sự kiện vào cơ sở dữ liệu
. Thêm dịch vụ PostgreSQL vào `docker-compose.yml`:


*Phần chìm cơ sở dữ liệu biến mỗi sự kiện được sử dụng thành một hàng lâu bền thay vì chỉ để nó trong thiết bị đầu cuối hoặc trong bộ nhớ.*

```yaml
  postgres:
    image: postgres:18
    restart: on-failure
    environment:
      - POSTGRES_DB=postgres
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
    ports:
      - "5432:5432"
```

Bắt đầu nó:

```bash
docker compose up postgres -d
```

Kết nối với PostgreSQL. Với `pgcli`:

```bash
uvx pgcli -h localhost -p 5432 -U postgres -d postgres
# password: postgres
```

Hoặc thông qua Docker:

```bash
docker compose exec postgres psql -U postgres -d postgres
```

Tạo bảng cho các sự kiện của chúng tôi:

```sql
CREATE TABLE processed_events (
    PULocationID INTEGER,
    DOLocationID INTEGER,
    trip_distance DOUBLE PRECISION,
    total_amount DOUBLE PRECISION,
    pickup_datetime TIMESTAMP
);
```

Cài đặt thư viện máy khách PostgreSQL:

```bash
uv add psycopg2-binary
```

Tạo `src/consumers/consumer_postgres.py`.

Thiết lập người tiêu dùng Kafka. Chúng tôi sử dụng lại `ride_deserializer` tương tự từ bước
trước đó. `group_id` khác nhau - mỗi nhóm người tiêu dùng theo dõi độ lệch
của mình một cách độc lập, do đó, người tiêu dùng bảng điều khiển và người tiêu dùng PostgreSQL
đều đọc tất cả thông báo:

```python
from kafka import KafkaConsumer

server = 'localhost:9092'
topic_name = 'rides'

consumer = KafkaConsumer(
    topic_name,
    bootstrap_servers=[server],
    auto_offset_reset='earliest',
    group_id='rides-to-postgres',
    value_deserializer=ride_deserializer
)
```

Kết nối với PostgreSQL:

```python
import psycopg2

conn = psycopg2.connect(
    host='localhost',
    port=5432,
    database='postgres',
    user='postgres',
    password='postgres'
)
conn.autocommit = True
cur = conn.cursor()
```

`autocommit = True` có nghĩa là mỗi INSERT được cam kết ngay lập tức - không cần
gọi `conn.commit()` sau mỗi hàng.

Đọc tin nhắn và chèn vào PostgreSQL:

```python
from datetime import datetime

print(f"Listening to {topic_name} and writing to PostgreSQL...")

count = 0
for message in consumer:
    ride = message.value
    pickup_dt = datetime.fromtimestamp(ride.tpep_pickup_datetime / 1000)
    cur.execute(
        """INSERT INTO processed_events
           (PULocationID, DOLocationID, trip_distance, total_amount, pickup_datetime)
           VALUES (%s, %s, %s, %s, %s)""",
        (ride.PULocationID, ride.DOLocationID,
         ride.trip_distance, ride.total_amount, pickup_dt)
    )
    count += 1
    if count % 100 == 0:
        print(f"Inserted {count} rows...")

consumer.close()
cur.close()
conn.close()
```

Chạy nó (nhấn Ctrl+C sau khi xử lý dữ liệu):

```bash
uv run python src/consumers/consumer_postgres.py
```

Kiểm tra PostgreSQL:

```sql
SELECT count(*) FROM processed_events;
```

```
 count
-------
  1000
```

Điều này có hiệu quả, nhưng hãy nghĩ đến những gì còn thiếu:

- Nếu muốn tổng hợp theo cửa sổ thời gian thì sao? Chúng ta cần tự mình triển khai logic
cửa sổ.
- Điều gì sẽ xảy ra nếu người tiêu dùng gặp sự cố? Chúng tôi cần phải tự theo dõi các khoản chênh lệch để tránh việc
xử lý lại hoặc thiếu dữ liệu.
- Còn tính song song thì sao? Chúng tôi cần quản lý nhiều phiên bản tiêu dùng và phân công phân vùng
.
- Còn việc ghi vào các ổ ghi khác nhau thì sao? Chúng tôi cần viết mã kết nối cho
mỗi đích.

Đây là lúc Flink xuất hiện. Xóa bảng trước khi tiếp tục:

```sql
TRUNCATE processed_events;
```
