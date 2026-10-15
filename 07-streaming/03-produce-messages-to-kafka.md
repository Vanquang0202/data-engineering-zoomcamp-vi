---
prev_url: 02-redpanda.md
next_url: 04-consume-messages-with-python.md
---
# Tạo tin nhắn tới Kafka

Khởi tạo dự án Python và thêm các phần phụ thuộc mà chúng tôi cần:

```bash
uv init -p 3.12
uv add kafka-python pandas pyarrow
```

> Nếu bạn sao chép kho lưu trữ, `pyproject.toml` đã tồn tại.
> Thay vào đó hãy chạy `uv sync`.

Chúng tôi sẽ gửi dữ liệu chuyến đi bằng taxi màu vàng của NYC tới Kafka. Bạn có thể chạy mã bên dưới
dưới dạng tập lệnh Python hoặc trong sổ ghi chép Jupyter (`uv add jupyter`,
rồi `uv run jupyter lab`).


*Đường dẫn của nhà sản xuất làm cho ranh giới lược đồ trở nên rõ ràng: đầu vào dạng bảng trở thành một sự kiện, sau đó là byte, sau đó là bản ghi chủ đề.*

Đầu tiên, tải xuống dữ liệu. Chúng tôi đọc tệp gỗ về các chuyến đi bằng taxi màu vàng và
lấy 1000 hàng đầu tiên:

```python
import pandas as pd

url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2025-11.parquet"
columns = ['PULocationID', 'DOLocationID', 'trip_distance', 'total_amount', 'tpep_pickup_datetime']
df = pd.read_parquet(url, columns=columns).head(1000)
df.head()
```

Chúng tôi chỉ đọc 5 cột để giữ mọi thứ tập trung. Tập dữ liệu đầy đủ có nhiều
hơn (phân tích giá vé, mã giá, loại thanh toán, v.v.).

Xác định một lớp dữ liệu cho tin nhắn của chúng tôi. Điều này cung cấp cho chúng ta một lược đồ rõ ràng cho mỗi chuyến taxi
:

```python
from dataclasses import dataclass

@dataclass
class Ride:
    PULocationID: int
    DOLocationID: int
    trip_distance: float
    total_amount: float
    tpep_pickup_datetime: int  # epoch milliseconds
```

Viết hàm chuyển đổi một hàng DataFrame thành `Ride`. Chúng tôi chuyển đổi Dấu thời gian của gấu trúc
thành kỷ nguyên mili giây - đó là định dạng mà Flink mong đợi
sau này:

```python
def ride_from_row(row):
    return Ride(
        PULocationID=int(row['PULocationID']),
        DOLocationID=int(row['DOLocationID']),
        trip_distance=float(row['trip_distance']),
        total_amount=float(row['total_amount']),
        tpep_pickup_datetime=int(row['tpep_pickup_datetime'].timestamp() * 1000),
    )
```

Kiểm tra nó:

```python
ride = ride_from_row(df.iloc[0])
ride
# Ride(PULocationID=186, DOLocationID=79, trip_distance=1.72,
# total_amount=17.31, tpep_pickup_datetime=1730429702000)
```

Tiếp theo, kết nối với Kafka. `bootstrap_servers` là nơi nhà môi giới chấp nhận các kết nối
- `localhost:9092` vì chúng tôi đang chạy tính năng này từ máy tính xách tay
(bên ngoài Docker). Trong quá trình sản xuất với nhiều nhà môi giới, bạn sẽ liệt kê một số
để dự phòng - nếu một nhà môi giới không hoạt động, máy khách sẽ kết nối thông qua một nhà môi giới khác.

Kafka hoạt động với các byte thô, vì vậy chúng tôi cần một bộ tuần tự hóa chuyển đổi các ký tự Python
thành JSON:

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
```

Hãy gửi một chuyến đi để thử nó. `dataclasses.asdict(ride)` chuyển đổi
lớp dữ liệu thành một lệnh đơn giản, mà trình tuần tự hóa biến thành các byte JSON.
Nhà môi giới tự động tạo chủ đề `rides` trong lần sử dụng đầu tiên:

```python
import dataclasses

topic_name = 'rides'

producer.send(topic_name, value=dataclasses.asdict(ride))
producer.flush()
```

Tính năng này hoạt động nhưng việc gọi `dataclasses.asdict()` mỗi lần thật tẻ nhạt.
của chúng tôi có thể tạo một bộ tuần tự hóa xử lý trực tiếp các lớp dữ liệu:

```python
def ride_serializer(ride):
    ride_dict = dataclasses.asdict(ride)
    json_str = json.dumps(ride_dict)
    return json_str.encode('utf-8')
```

Bây giờ, hãy tạo lại trình sản xuất bằng trình tuần tự hóa mới - chúng ta có thể chuyển trực tiếp các đối tượng `Ride`
mà không cần chuyển đổi chúng thành dict trước:

```python
producer = KafkaProducer(
    bootstrap_servers=[server],
    value_serializer=ride_serializer
)
```

Gửi một chuyến đi để xác minh:

```python
producer.send(topic_name, value=ride)
producer.flush()
```

Điều đó đã gửi một bản ghi. Bây giờ, hãy gửi tất cả 1000 chuyến đi trong một vòng lặp:

```python
import time

t0 = time.time()

for _, row in df.iterrows():
    ride = ride_from_row(row)
    producer.send(topic_name, value=ride)
    print(f"Sent: {ride}")
    time.sleep(0.01)

producer.flush()

t1 = time.time()
print(f'took {(t1 - t0):.2f} seconds')
```

Nếu bạn đang xây dựng từ đầu (không sử dụng tệp repo nhân bản), hãy tạo
cấu trúc thư mục nguồn và lưu mô hình dữ liệu được chia sẻ. Cả tập lệnh sản xuất và tiêu dùng
đều nhập từ tệp này:

```bash
mkdir -p src/producers src/consumers src/job
```

Tạo `src/models.py`:

```python
import json
from dataclasses import dataclass

@dataclass
class Ride:
    PULocationID: int
    DOLocationID: int
    trip_distance: float
    total_amount: float
    tpep_pickup_datetime: int  # epoch milliseconds

def ride_from_row(row):
    return Ride(
        PULocationID=int(row['PULocationID']),
        DOLocationID=int(row['DOLocationID']),
        trip_distance=float(row['trip_distance']),
        total_amount=float(row['total_amount']),
        tpep_pickup_datetime=int(row['tpep_pickup_datetime'].timestamp() * 1000),
    )

def ride_deserializer(data):
    json_str = data.decode('utf-8')
    ride_dict = json.loads(json_str)
    return Ride(**ride_dict)
```

`ride_deserializer` được giới thiệu trong bước tiếp theo - chúng tôi đưa nó vào đây để tệp
hoàn tất.

> Tập lệnh hoàn chỉnh có trong `src/producers/producer.py`.

Chạy nó:

```bash
uv run python src/producers/producer.py
```

Bạn sẽ thấy 1000 chuyến taxi được gửi trong ~10 giây:

```
Sent: Ride(PULocationID=..., DOLocationID=..., trip_distance=..., total_amount=..., tpep_pickup_datetime=...)
...
took 10.23 seconds
```
