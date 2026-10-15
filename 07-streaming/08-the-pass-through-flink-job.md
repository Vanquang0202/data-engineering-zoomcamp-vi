---
prev_url: 07-the-flink-image-and-services.md
next_url: 09-offsets-earliest-vs-latest.md
---
# Công việc Flink chuyển tiếp

Bây giờ, hãy làm điều tương tự mà người tiêu dùng Python của chúng ta đã làm, nhưng với Flink.

Không giống như tập lệnh của nhà sản xuất và người tiêu dùng, công việc Flink không thể chạy từ sổ ghi chép Jupyter
. Chúng được gửi tới cụm Flink dưới dạng tệp .py
bằng `docker compose exec`. Chúng tôi đề cập đến cách thức hoạt động của việc gửi công việc trong quá trình sản xuất
trong phần "Flink in production" ở cuối.


*Công việc chuyển tiếp tiếp tục chạy: nó di chuyển các sự kiện đến vào phần lưu trữ và định kỳ chụp nhanh trạng thái và tiến trình nguồn để khôi phục.*

Tạo `src/job/pass_through_job.py`.

Bảng nguồn Kafka:

```python
def create_events_source_kafka(t_env):
    table_name = "events"
    source_ddl = f"""
        CREATE TABLE {table_name} (
            PULocationID INTEGER,
            DOLocationID INTEGER,
            trip_distance DOUBLE,
            total_amount DOUBLE,
            tpep_pickup_datetime BIGINT
        ) WITH (
            'connector' = 'kafka',
            'properties.bootstrap.servers' = 'redpanda:29092',
            'topic' = 'rides',
            'scan.startup.mode' = 'latest-offset',
            'properties.auto.offset.reset' = 'latest',
            'format' = 'json'
        );
        """
    t_env.execute_sql(source_ddl)
    return table_name
```

Đây là câu lệnh DDL Flink SQL. Phân tích nó:

- `PULocationID`, `DOLocationID`, `trip_distance`, `total_amount`,
`tpep_pickup_datetime` - các trường JSON từ nhà sản xuất
của chúng tôi - `'properties.bootstrap.servers' = 'redpanda:29092'` - địa chỉ mạng Docker nội bộ
(không phải `localhost` - Flink chạy bên trong Docker)
- `'scan.startup.mode' = 'latest-offset'` - chỉ đọc các tin nhắn mới đến
sau khi công việc bắt đầu
- `'format' = 'json'` - Flink tự động giải tuần tự hóa JSON

Bảng chìm PostgreSQL:

```python
def create_processed_events_sink_postgres(t_env):
    table_name = 'processed_events'
    sink_ddl = f"""
        CREATE TABLE {table_name} (
            PULocationID INTEGER,
            DOLocationID INTEGER,
            trip_distance DOUBLE,
            total_amount DOUBLE,
            pickup_datetime TIMESTAMP
        ) WITH (
            'connector' = 'jdbc',
            'url' = 'jdbc:postgresql://postgres:5432/postgres',
            'table-name' = '{table_name}',
            'username' = 'postgres',
            'password' = 'postgres',
            'driver' = 'org.postgresql.Driver'
        );
        """
    t_env.execute_sql(sink_ddl)
    return table_name
```

Không có câu lệnh psycopg2, không có câu lệnh INSERT - chỉ cần khai báo bảng và Flink xử lý
phần còn lại.

Việc thực thi:

```python
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import EnvironmentSettings, StreamTableEnvironment

def log_processing():
    env = StreamExecutionEnvironment.get_execution_environment()
    env.enable_checkpointing(10 * 1000)  # checkpoint every 10 seconds

    settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
    t_env = StreamTableEnvironment.create(env, environment_settings=settings)

    source_table = create_events_source_kafka(t_env)
    postgres_sink = create_processed_events_sink_postgres(t_env)

    t_env.execute_sql(
        f"""
        INSERT INTO {postgres_sink}
        SELECT
            PULocationID,
            DOLocationID,
            trip_distance,
            total_amount,
            TO_TIMESTAMP_LTZ(tpep_pickup_datetime, 3) as pickup_datetime
        FROM {source_table}
        """
    ).wait()

if __name__ == '__main__':
    log_processing()
```

- Chế độ truyền phát - công việc chạy liên tục, chờ dữ liệu mới
- `INSERT INTO ... SELECT` là đường dẫn - đọc từ Kafka, chuyển đổi dấu thời gian
, ghi vào PostgreSQL

`enable_checkpointing(10 * 1000)` yêu cầu Flink chụp ảnh nhanh trạng thái công việc
cứ sau 10 giây. Một điểm kiểm tra ghi lại các giá trị chênh lệch Kafka (cách
đọc được đến nay) và mọi dữ liệu trên chuyến bay. Nếu công việc gặp sự cố, nó sẽ tiếp tục
từ điểm kiểm tra cuối cùng thay vì bắt đầu lại từ đầu.

Việc kiểm tra điểm đặc biệt quan trọng với windows. Nếu bạn có cửa sổ
5 phút và công việc không thành công sau 2 phút, Flink không chỉ theo dõi phần bù
- nó cũng tuần tự hóa các cửa sổ đang mở vào đĩa. Khi
khởi động lại, nó sẽ tiếp tục ngay tại nơi nó đã dừng lại, với cửa sổ
được lấp đầy một phần vẫn nguyên vẹn.

Sự đánh đổi là khả năng phục hồi so với hiệu quả. Việc kiểm tra
cứ sau 1 giây rất tốn kém - Flink phải tuần tự hóa và duy trì toàn bộ trạng thái mà
thường xuyên. Việc kiểm tra cứ sau 10 phút có nghĩa là bạn có thể mất tới 10 phút tiến trình
nếu thất bại. 10 giây là mặc định hợp lý cho hầu hết các công việc.

Gửi công việc:

```bash
docker compose exec jobmanager ./bin/flink run \
    -py /opt/src/job/pass_through_job.py \
    --pyFiles /opt/src -d
```

```
Job has been submitted with JobID 663cff6811b65e97fc1e068d641401f4
```

Kiểm tra giao diện Flink tại [http://localhost:8081](http://localhost:8081) - bạn sẽ thấy
thấy một công việc đang chạy.

Vì công việc sử dụng `latest-offset` nên nó đang chờ tin nhắn mới. Gửi dữ liệu:

```bash
uv run python src/producers/producer.py
```

Truy vấn PostgreSQL:

```sql
SELECT count(*) FROM processed_events;
```

So sánh điều này với cách tiếp cận người tiêu dùng Python của chúng tôi - kết quả tương tự, nhưng Flink xử lý điểm kiểm tra
, quản lý bù đắp và ghi PostgreSQL tự động.
