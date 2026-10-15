# Bài tập về nhà

Đối với bài tập về nhà này, chúng ta sẽ sử dụng dữ liệu Taxi:
- Dữ liệu xanh 2019-10 từ [tại đây](https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-10.csv.gz)


## Khởi động Red Panda, Trình quản lý công việc Flink, Trình quản lý tác vụ Flink và Postgres

Có tệp `docker-compose.yml` trong thư mục bài tập về nhà (lấy từ [tại đây](https://github.com/redpanda-data-blog/2023-python-gsg/blob/main/docker-compose.yml))

Sao chép tệp này vào thư mục bài tập về nhà của bạn và chạy

```bash
docker-compose up
```

(Thêm `-d` nếu bạn muốn chạy ở chế độ tách rời)

Truy cập `localhost:8081` để xem Trình quản lý công việc Flink

Kết nối với Postgres bằng [DBeaver](https://dbeaver.io/).

Thông tin đăng nhập kết nối là:
- Tên người dùng `postgres`
- Mật khẩu `postgres`
- Cơ sở dữ liệu `postgres`
- Máy chủ `localhost`
- Cổng `5432`


Trong DBeaver, hãy chạy truy vấn này để tạo vùng hạ cánh Postgres cho các sự kiện đầu tiên:
```sql 
CREATE TABLE processed_events (
    test_data INTEGER,
    event_timestamp TIMESTAMP
)
```


## Câu hỏi 1. Kết nối với máy chủ Kafka

Chúng tôi cần đảm bảo rằng chúng tôi có thể kết nối với máy chủ, để
sau này chúng tôi có thể gửi một số dữ liệu đến các chủ đề của nó

Trước tiên, hãy cài đặt trình kết nối kafka (tùy thuộc vào bạn nếu
muốn có một môi trường ảo riêng cho điều đó)

```bash
pip install kafka-python
```

Bạn có thể khởi động sổ ghi chép jupyter trong thư mục giải pháp của mình hoặc
tạo tập lệnh

Hãy thử kết nối với máy chủ của chúng tôi:

```python
import json
import time 

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

## Câu hỏi 3: Gửi dữ liệu chuyến đi

* Đọc tệp csv.gz màu xanh lá cây
* Chúng tôi sẽ chỉ cần các cột sau:
* `'lpep_pickup_datetime',`
* `'lpep_dropoff_datetime',`
* `'PULocationID',`
* `'DOLocationID',`
* `'passenger_count',`
* `'trip_distance',`
* `'tip_amount'`

* Tạo một chủ đề `green-trips` và gửi dữ liệu đến đó với `load_taxi_data.py`
* Mất bao nhiêu thời gian tính bằng giây? (Bạn có thể làm tròn nó thành số nguyên)
* Đảm bảo bạn không bao gồm các chế độ ngủ trong mã của mình

## Câu 4: Xây dựng cửa sổ Sessionization

* Sao chép `aggregation_job.py` và đổi tên thành `session_job.py`
* Đọc nó từ `green-trips` sửa lược đồ
* Sử dụng [cửa sổ phiên](https://nightlies.apache.org/flink/flink-docs-master/docs/dev/datastream/operators/windows/) với khoảng cách 5 phút
* Sử dụng thời gian `lpep_dropoff_datetime` làm thời gian của bạn hình mờ có dung sai 5 giây
* Địa điểm đón và trả khách nào có chuỗi chuyến đi taxi dài nhất không gián đoạn?




