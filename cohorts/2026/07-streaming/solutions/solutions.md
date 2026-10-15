# Lời giải

## Câu hỏi 1. Phiên bản Redpanda

```bash
docker exec -it workshop-redpanda-1 rpk version
```

Đáp án: `v25.3.9` (khớp với image tag trong docker-compose.yml)


## Câu hỏi 2. Gửi dữ liệu vào Redpanda

Tạo topic:

```bash
docker exec -it workshop-redpanda-1 rpk topic create green-trips
```

Chạy producer:

```bash
python producer.py
```

Bộ dữ liệu có 49.416 dòng. Thời gian gửi khoảng 10 giây, tùy theo máy.

Đáp án: 10 giây


## Câu hỏi 3. Consumer - quãng đường chuyến đi

Chạy consumer:

```bash
python consumer.py
```

Đáp án: Có 8.506 chuyến đi với `trip_distance` > 5.0


## Câu hỏi 4. Tumbling window - địa điểm đón khách

Tạo bảng PostgreSQL:

```sql
CREATE TABLE tumbling_pickup_counts (
    window_start TIMESTAMP(3),
    PULocationID INT,
    num_trips BIGINT,
    PRIMARY KEY (window_start, PULocationID) NOT ENFORCED
);
```

Sao chép `tumbling_job.py` vào `07-streaming/workshop/src/job/` rồi chạy:

```bash
docker exec -it workshop-jobmanager-1 \
    flink run -py /opt/src/job/tumbling_job.py
```

Truy vấn kết quả:

```sql
SELECT PULocationID, num_trips
FROM tumbling_pickup_counts
ORDER BY num_trips DESC
LIMIT 3;
```

Đáp án: PULocationID 74 (có 15 chuyến trong cửa sổ 5 phút đông nhất)


## Câu hỏi 5. Session window - chuỗi chuyến dài nhất

Tạo bảng PostgreSQL:

```sql
CREATE TABLE session_pickup_counts (
    session_start TIMESTAMP(3),
    session_end TIMESTAMP(3),
    PULocationID INT,
    num_trips BIGINT,
    PRIMARY KEY (session_start, PULocationID) NOT ENFORCED
);
```

Sao chép `session_job.py` vào `07-streaming/workshop/src/job/` rồi chạy:

```bash
docker exec -it workshop-jobmanager-1 \
    flink run -py /opt/src/job/session_job.py
```

Truy vấn kết quả:

```sql
SELECT PULocationID, num_trips, session_start, session_end
FROM session_pickup_counts
ORDER BY num_trips DESC
LIMIT 3;
```

Đáp án: 81 chuyến (PULocationID 74, session vào sáng ngày 2025-10-08)

Lưu ý: job xử lý session phải dùng parallelism bằng 1 vì topic `green-trips`
chỉ có 1 partition. Nếu tăng parallelism, các subtask nhàn rỗi sẽ khiến
Watermark không tiến lên và session window không xuất kết quả.


## Câu hỏi 6. Tumbling window - tổng tiền tip lớn nhất

Tạo bảng PostgreSQL:

```sql
CREATE TABLE hourly_tips (
    window_start TIMESTAMP(3),
    total_tips DOUBLE,
    PRIMARY KEY (window_start) NOT ENFORCED
);
```

Sao chép `tip_job.py` vào `07-streaming/workshop/src/job/` rồi chạy:

```bash
docker exec -it workshop-jobmanager-1 \
    flink run -py /opt/src/job/tip_job.py
```

Truy vấn kết quả:

```sql
SELECT window_start, total_tips
FROM hourly_tips
ORDER BY total_tips DESC
LIMIT 3;
```

Đáp án: 2025-10-16 18:00:00 (tổng tiền tip: khoảng $524.96)
