# Bài tập [BẢN NHÁP]

> [!NOTE]
> Đây là bản nháp được chuyển từ khóa 2026. Câu hỏi, bộ dữ liệu và
> hạn nộp sẽ được cập nhật trước khi module bắt đầu.

Trong bài tập này, chúng ta sẽ thực hành Streaming với Kafka (Redpanda) và PyFlink.

Chúng ta dùng Redpanda, một giải pháp có thể thay thế Kafka trực tiếp.
Redpanda triển khai cùng giao thức nên các thư viện Kafka client có thể dùng mà không cần sửa.

Bài tập sử dụng dữ liệu chuyến đi taxi Green tháng 10/2025:

- [green_tripdata_2025-10.parquet](https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-10.parquet)


## Chuẩn bị

Chúng ta sẽ dùng hạ tầng giống [workshop](code/).

Làm theo hướng dẫn thiết lập: build Docker image rồi khởi chạy các service:

```bash
cd 07-streaming/workshop/
docker compose build
docker compose up -d
```

Sau đó chúng ta có:

- Redpanda (broker tương thích Kafka) tại `localhost:9092`
- Flink Job Manager tại http://localhost:8081
- Flink Task Manager
- PostgreSQL tại `localhost:5432` (người dùng: `postgres`, mật khẩu: `postgres`)

Nếu bạn đã chạy workshop và còn container/volume cũ,
hãy khởi động lại từ môi trường trống:

```bash
docker compose down -v
docker compose build
docker compose up -d
```

Lưu ý: tên container (như `workshop-redpanda-1`) giả định thư mục có tên
`workshop`. Nếu đã đổi tên thư mục, hãy điều chỉnh cho phù hợp.


## Câu hỏi 1. Phiên bản Redpanda

Chạy `rpk version` bên trong container Redpanda:

```bash
docker exec -it workshop-redpanda-1 rpk version
```

Bạn đang chạy phiên bản Redpanda nào?


## Câu hỏi 2. Gửi dữ liệu vào Redpanda

Tạo topic tên `green-trips`:

```bash
docker exec -it workshop-redpanda-1 rpk topic create green-trips
```

Bây giờ hãy viết producer để gửi dữ liệu taxi green vào topic này.

Đọc file Parquet và chỉ giữ các cột sau:

- `lpep_pickup_datetime`
- `lpep_dropoff_datetime`
- `PULocationID`
- `DOLocationID`
- `passenger_count`
- `trip_distance`
- `tip_amount`
- `total_amount`

Chuyển từng dòng thành dictionary rồi gửi vào topic `green-trips`.
Với các cột thời gian, hãy chuyển chúng thành chuỗi trước khi serialize sang JSON.

Đo thời gian gửi toàn bộ dữ liệu và flush:

```python
from time import time

t0 = time()

# send all rows ...

producer.flush()

t1 = time()
print(f'took {(t1 - t0):.2f} seconds')
```

Mất bao lâu để gửi dữ liệu?

- 10 giây
- 60 giây
- 120 giây
- 300 giây


## Câu hỏi 3. Consumer - quãng đường chuyến đi

Viết Kafka consumer đọc tất cả message từ topic `green-trips`
(đặt `auto_offset_reset='earliest'`).

Đếm số chuyến có `trip_distance` lớn hơn 5,0 km.

Có bao nhiêu chuyến có `trip_distance` > 5?

- 6506
- 7506
- 8506
- 9506


## Phần 2: PyFlink (Câu hỏi 4-6)

Với các câu hỏi PyFlink, bạn sẽ điều chỉnh code workshop để xử lý dữ liệu
taxi green. Những điểm khác biệt chính so với workshop:

- Tên topic: `green-trips` (thay vì `rides`)
- Các cột thời gian có tiền tố `lpep_` (thay vì `tpep_`)
- Cần xử lý timestamp dưới dạng chuỗi (không phải mili giây tính từ epoch)

Bạn có thể chuyển timestamp dạng chuỗi sang timestamp của Flink trong source DDL:

```sql
lpep_pickup_datetime VARCHAR,
event_timestamp AS TO_TIMESTAMP(lpep_pickup_datetime, 'yyyy-MM-dd HH:mm:ss'),
WATERMARK FOR event_timestamp AS event_timestamp - INTERVAL '5' SECOND
```

Trước khi chạy các Flink job, hãy tạo những bảng PostgreSQL cần thiết để lưu kết quả.

Lưu ý quan trọng cho các Flink job:

- Đặt các file job trong `workshop/src/job/` - thư mục này được mount
  vào container Flink tại `/opt/src/job/`
- Submit job bằng lệnh:
  `docker exec -it workshop-jobmanager-1 flink run -py /opt/src/job/your_job.py`
- Topic `green-trips` có 1 partition, nên đặt parallelism bằng 1 trong
  Flink job (`env.set_parallelism(1)`). Nếu parallelism cao hơn, các consumer
  subtask nhàn rỗi sẽ ngăn Watermark tiến lên.
- Flink Streaming job chạy liên tục. Hãy để job chạy một đến hai phút
  cho đến khi kết quả xuất hiện trong PostgreSQL, rồi truy vấn kết quả.
  Bạn có thể hủy job từ giao diện Flink tại http://localhost:8081
- Nếu đã gửi dữ liệu vào topic nhiều lần, hãy xóa và tạo lại topic
  để tránh bản ghi trùng:
  `docker exec -it workshop-redpanda-1 rpk topic delete green-trips`


## Câu hỏi 4. Tumbling window - địa điểm đón khách

Tạo Flink job đọc từ `green-trips` và dùng Tumbling window 5 phút
để đếm số chuyến theo `PULocationID`.

Ghi kết quả vào bảng PostgreSQL gồm các cột:
`window_start`, `PULocationID`, `num_trips`.

Sau khi job xử lý toàn bộ dữ liệu, hãy truy vấn kết quả:

```sql
SELECT PULocationID, num_trips
FROM <your_table>
ORDER BY num_trips DESC
LIMIT 3;
```

`PULocationID` nào có nhiều chuyến nhất trong một window 5 phút?

- 42
- 74
- 75
- 166


## Câu hỏi 5. Session window - chuỗi chuyến dài nhất

Tạo Flink job khác dùng Session window với khoảng ngắt 5 phút
theo `PULocationID`, lấy `lpep_pickup_datetime` làm event time
và đặt độ trễ cho phép của Watermark là 5 giây.

Session window nhóm các event cách nhau không quá 5 phút.
Khi khoảng cách vượt 5 phút, window sẽ đóng.

Ghi kết quả vào bảng PostgreSQL và tìm `PULocationID` có session dài nhất
(nhiều chuyến nhất trong một session).

Session dài nhất có bao nhiêu chuyến?

- 12
- 31
- 51
- 81


## Câu hỏi 6. Tumbling window - tổng tiền tip lớn nhất

Tạo Flink job dùng Tumbling window 1 giờ để tính tổng `tip_amount`
theo giờ (trên mọi địa điểm).

Giờ nào có tổng tiền tip cao nhất?

- 2025-10-01 18:00:00
- 2025-10-16 18:00:00
- 2025-10-22 08:00:00
- 2025-10-30 16:00:00


## Nộp bài

- Biểu mẫu nộp bài: https://courses.datatalks.club/de-zoomcamp-2026/homework/hw7


## Chia sẻ quá trình học công khai

Chúng tôi khuyến khích mọi người chia sẻ những gì mình đã học.
Đọc thêm về lợi ích [tại đây](https://aishippingblog.com/p/benefits-of-learning-in-public-and).

## Bài đăng mẫu trên LinkedIn

```
Week 7 of Data Engineering Zoomcamp by @DataTalksClub complete!

Just finished Module 7 - Streaming with PyFlink. Learned how to:

- Set up Redpanda as a Kafka replacement
- Build Kafka producers and consumers in Python
- Create tumbling and session windows in Flink
- Analyze real-time taxi trip data with stream processing

Here's my homework solution: <LINK>

You can sign up here: https://github.com/DataTalksClub/data-engineering-zoomcamp/
```

## Bài đăng mẫu trên Twitter/X

```
Module 7 of Data Engineering Zoomcamp done!

- Kafka producers and consumers
- PyFlink tumbling and session windows
- Real-time taxi data analysis
- Redpanda as Kafka replacement

My solution: <LINK>

Free course by @DataTalksClub: https://github.com/DataTalksClub/data-engineering-zoomcamp/
```
