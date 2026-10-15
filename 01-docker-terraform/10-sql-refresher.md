---
video_url: https://www.youtube.com/watch?v=QEcps_iskgg
prev_url: 09-docker-compose.md
next_url: 11-cleanup.md
---
# Trình giới thiệu SQL

Điều kiện tiên quyết: Nếu bạn theo dõi khóa học theo thứ tự nhất định, Docker Compose sẽ chạy với pgdatabase và pgAdmin.

Sau khi hoàn tất, bạn có thể truy cập http://localhost:8085/browser/ để truy cập pgAdmin.
Đừng quên Nhấp chuột phải vào máy chủ hoặc cơ sở dữ liệu để làm mới nó trong trường hợp bạn không thấy bảng mới.

Bây giờ bắt đầu truy vấn!


## Nội tham gia

### INNER ngầm THAM GIA

Nối bảng Taxi màu vàng với bảng Tra cứu vùng (ngầm INNER THAM GIA):

```sql
SELECT
    tpep_pickup_datetime,
    tpep_dropoff_datetime,
    total_amount,
    CONCAT(zpu."Borough", ' | ', zpu."Zone") AS "pickup_loc",
    CONCAT(zdo."Borough", ' | ', zdo."Zone") AS "dropoff_loc"
FROM
    yellow_taxi_trips t,
    zones zpu,
    zones zdo
WHERE
    t."PULocationID" = zpu."LocationID"
    AND t."DOLocationID" = zdo."LocationID"
LIMIT 100;
```

### INNER rõ ràng THAM GIA

```sql
SELECT
    tpep_pickup_datetime,
    tpep_dropoff_datetime,
    total_amount,
    CONCAT(zpu."Borough", ' | ', zpu."Zone") AS "pickup_loc",
    CONCAT(zdo."Borough", ' | ', zdo."Zone") AS "dropoff_loc"
FROM
    yellow_taxi_trips t
JOIN
-- or INNER JOIN but it's less used, when writing JOIN, postgreSQL understands implicitly that we want to use an INNER JOIN
    zones zpu ON t."PULocationID" = zpu."LocationID"
JOIN
    zones zdo ON t."DOLocationID" = zdo."LocationID"
LIMIT 100;
```

## Kiểm tra chất lượng dữ liệu

### Đang kiểm tra ID vị trí NULL

```sql
SELECT
    tpep_pickup_datetime,
    tpep_dropoff_datetime,
    total_amount,
    "PULocationID",
    "DOLocationID"
FROM
    yellow_taxi_trips
WHERE
    "PULocationID" IS NULL
    OR "DOLocationID" IS NULL
LIMIT 100;
```

### Kiểm tra ID vị trí KHÔNG CÓ TRONG Bảng vùng

```sql
SELECT
    tpep_pickup_datetime,
    tpep_dropoff_datetime,
    total_amount,
    "PULocationID",
    "DOLocationID"
FROM
    yellow_taxi_trips
WHERE
    "DOLocationID" NOT IN (SELECT "LocationID" from zones)
    OR "PULocationID" NOT IN (SELECT "LocationID" from zones)
LIMIT 100;
```

## TRÁI, PHẢI và NGOÀI THAM GIA

Sử dụng LEFT, RIGHT và OUTER JOINS khi một số ID vị trí không có trong cả hai Bảng:

```sql
DELETE FROM zones WHERE "LocationID" = 142;

SELECT
    tpep_pickup_datetime,
    tpep_dropoff_datetime,
    total_amount,
    CONCAT(zpu."Borough", ' | ', zpu."Zone") AS "pickup_loc",
    CONCAT(zdo."Borough", ' | ', zdo."Zone") AS "dropoff_loc"
FROM
    yellow_taxi_trips t
LEFT JOIN
    zones zpu ON t."PULocationID" = zpu."LocationID"
JOIN
    zones zdo ON t."DOLocationID" = zdo."LocationID"
LIMIT 100;
```

```sql
SELECT
    tpep_pickup_datetime,
    tpep_dropoff_datetime,
    total_amount,
    CONCAT(zpu."Borough", ' | ', zpu."Zone") AS "pickup_loc",
    CONCAT(zdo."Borough", ' | ', zdo."Zone") AS "dropoff_loc"
FROM
    yellow_taxi_trips t
RIGHT JOIN
    zones zpu ON t."PULocationID" = zpu."LocationID"
JOIN
    zones zdo ON t."DOLocationID" = zdo."LocationID"
LIMIT 100;
```

```sql
SELECT
    tpep_pickup_datetime,
    tpep_dropoff_datetime,
    total_amount,
    CONCAT(zpu."Borough", ' | ', zpu."Zone") AS "pickup_loc",
    CONCAT(zdo."Borough", ' | ', zdo."Zone") AS "dropoff_loc"
FROM
    yellow_taxi_trips t
OUTER JOIN
    zones zpu ON t."PULocationID" = zpu."LocationID"
JOIN
    zones zdo ON t."DOLocationID" = zdo."LocationID"
LIMIT 100;
```

## NHÓM THEO

### Tính Số Chuyến Đi Mỗi Ngày

```sql
SELECT
    CAST(tpep_dropoff_datetime AS DATE) AS "day",
    COUNT(1)
FROM
    yellow_taxi_trips
GROUP BY
    CAST(tpep_dropoff_datetime AS DATE)
LIMIT 100;
```

## ĐẶT HÀNG BỞI

### Đặt hàng theo ngày

```sql
SELECT
    CAST(tpep_dropoff_datetime AS DATE) AS "day",
    COUNT(1)
FROM
    yellow_taxi_trips
GROUP BY
    CAST(tpep_dropoff_datetime AS DATE)
ORDER BY
    "day" ASC
LIMIT 100;
```

### Thứ tự theo số lượng

```sql
SELECT
    CAST(tpep_dropoff_datetime AS DATE) AS "day",
    COUNT(1) AS "count"
FROM
    yellow_taxi_trips
GROUP BY
    CAST(tpep_dropoff_datetime AS DATE)
ORDER BY
    "count" DESC
LIMIT 100;
```

## Các tập hợp khác

```sql
SELECT
    CAST(tpep_dropoff_datetime AS DATE) AS "day",
    COUNT(1) AS "count",
    MAX(total_amount) AS "total_amount",
    MAX(passenger_count) AS "passenger_count"
FROM
    yellow_taxi_trips
GROUP BY
    CAST(tpep_dropoff_datetime AS DATE)
ORDER BY
    "count" DESC
LIMIT 100;
```

## Nhóm theo nhiều trường

```sql
SELECT
    CAST(tpep_dropoff_datetime AS DATE) AS "day",
    "DOLocationID",
    COUNT(1) AS "count",
    MAX(total_amount) AS "total_amount",
    MAX(passenger_count) AS "passenger_count"
FROM
    yellow_taxi_trips
GROUP BY
    1, 2
ORDER BY
    "day" ASC,
    "DOLocationID" ASC
LIMIT 100;
```
