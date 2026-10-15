# Bài tập

Trong bài tập này, chúng ta sẽ học về Streaming với PyFlink.

Thay vì Kafka, chúng ta sẽ dùng Redpanda, một giải pháp có thể thay thế
Kafka trực tiếp. Redpanda cung cấp cùng giao diện, nên chúng ta có thể
dùng thư viện Kafka cho Python để giao tiếp với nó, cũng như dùng
Kafka connector trong PyFlink.

Bài tập sử dụng dữ liệu taxi:
- Dữ liệu taxi Green tháng 10/2019 [tại đây](https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-10.csv.gz)


## Chuẩn bị

Chúng ta cần:

- Red Panda
- Flink Job Manager
- Flink Task Manager
- Postgres

Môi trường giống với [module pyflink](../../../06-streaming/pyflink/). Hãy chuyển đến đó và khởi chạy docker-compose:

```bash
cd ../../../06-streaming/pyflink/
docker-compose up
```

(Thêm `-d` nếu muốn chạy ở chế độ nền)

Truy cập http://localhost:8081 để xem Flink Job Manager

Kết nối Postgres bằng pgcli, pg-admin, [DBeaver](https://dbeaver.io/) hoặc công cụ khác.

Thông tin kết nối:

- Tên người dùng `postgres`
- Mật khẩu `postgres`
- Cơ sở dữ liệu `postgres`
- Host `localhost`
- Cổng `5432`

Với pgcli, chạy lệnh sau để kết nối:

```bash
pgcli -h localhost -p 5432 -u postgres -d postgres
```

Chạy các truy vấn sau để tạo bảng tiếp nhận các event và window đầu tiên trong Postgres:

```sql 
CREATE TABLE processed_events (
    test_data INTEGER,
    event_timestamp TIMESTAMP
);

CREATE TABLE processed_events_aggregated (
    event_hour TIMESTAMP,
    test_data INTEGER,
    num_hits INTEGER 
);
```

## Câu hỏi 1: Phiên bản Redpanda

Trước tiên, hãy tìm phiên bản Redpanda. 

Hãy xem đầu ra của lệnh `rpk help` _bên trong container_. Tên container là `redpanda-1`.

Dựa vào phần `help`, tìm lệnh cần chạy.

Phiên bản hiển thị trong kết quả lệnh bạn vừa chạy là gì? (Sao chép đầy đủ chuỗi phiên bản.)


## Câu hỏi 2. Tạo topic

Trước khi gửi dữ liệu đến Redpanda server, chúng ta cần tạo một topic.
Việc này cũng thực hiện bằng lệnh `rpk` đã dùng để tìm phiên bản Redpanda.

Đọc đầu ra của `help`, rồi tạo topic tên `green-trips`. 

Đầu ra của lệnh tạo topic là gì? Hãy đưa toàn bộ đầu ra vào câu trả lời.


## Câu hỏi 3. Kết nối Kafka server

Chúng ta cần bảo đảm kết nối được đến server để sau đó gửi dữ liệu
vào các topic của nó.

Trước tiên, hãy cài Kafka connector (bạn có thể dùng virtual environment
riêng nếu muốn).

```bash
pip install kafka-python
```

Bạn có thể tạo Jupyter notebook trong thư mục lời giải hoặc viết một script.

Hãy thử kết nối đến server:

```python
import json

from kafka import KafkaProducer

def json_serializer(data):
    return json.dumps(data).encode('utf-8')

server = 'localhost:9092'

producer = KafkaProducer(
    bootstrap_servers=[server],
    value_serializer=json_serializer
)

producer.bootstrap_connected()
```

Nếu kết nối thành công, đầu ra của lệnh cuối cùng là gì?

## Câu hỏi 4: Gửi dữ liệu chuyến đi

Bây giờ hãy gửi dữ liệu vào topic `green-trips`.

Đọc dữ liệu và chỉ giữ các cột sau:

* `'lpep_pickup_datetime',`
* `'lpep_dropoff_datetime',`
* `'PULocationID',`
* `'DOLocationID',`
* `'passenger_count',`
* `'trip_distance',`
* `'tip_amount'`

Gửi toàn bộ dữ liệu bằng đoạn code sau:

```python
producer.send(topic_name, value=message)
```

Thực hiện cho từng dòng (`message`) trong bộ dữ liệu. Ở đây, `message`
là một dictionary.

Sau khi gửi hết các message, hãy flush dữ liệu:

```python
producer.flush()
```

Dùng `from time import time` để đo tổng thời gian. 

```python
from time import time

t0 = time()

# ... your code

t1 = time()
took = t1 - t0
```

Mất bao lâu để gửi toàn bộ dữ liệu và flush? 


## Câu hỏi 5: Xây dựng Session Window (2 điểm)

Dữ liệu đã có trong luồng Kafka. Bây giờ hãy xử lý dữ liệu đó.

* Sao chép `aggregation_job.py` và đổi tên bản sao thành `session_job.py`
* Cho job đọc dữ liệu từ `green-trips` và điều chỉnh schema cho phù hợp
* Dùng [session window](https://nightlies.apache.org/flink/flink-docs-master/docs/dev/datastream/operators/windows/) với khoảng ngắt 5 phút
* Dùng thời điểm `lpep_dropoff_datetime` làm Watermark với độ trễ cho phép 5 giây
* Cặp khu vực đón và trả khách nào có chuỗi chuyến taxi liên tiếp dài nhất?


## Nộp bài

- Biểu mẫu nộp bài: https://courses.datatalks.club/de-zoomcamp-2025/homework/hw6
- Hạn nộp: Xem trên trang web

