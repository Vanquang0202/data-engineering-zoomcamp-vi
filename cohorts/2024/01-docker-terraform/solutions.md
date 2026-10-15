## Câu 1. Biết thẻ docker
```
❯ docker run --help | grep "Automatically remove"
--rm                               Automatically remove
```

- Toán tử pipe `|` chuyển hướng đầu ra lệnh trước đó làm đầu vào cho lệnh sau toán tử
- `docker run --help` -----> xuất ra `|` ----------> đầu vào thành `grep "Automatically remove"`
- `grep` cho phép tìm kiếm qua văn bản
  
Trả lời: `--rm`


## Câu hỏi 2. Tìm hiểu về docker lần chạy đầu tiên

- Chạy hình ảnh python:3.9 với `docker run -it python:3.9 bash`
- Vì bạn đã mở bằng thẻ `it` nên vùng chứa sẽ tương tác`
- Vì lệnh docker kết thúc bằng `bash` nên điểm vào vào thùng chứa sẽ là `bash`

```shell
root@root: docker run -it python:3.9 bash
root@b67c6949422a:/# pip list
Package    Version
---------- -------
pip        23.0.1
setuptools 58.1.0
wheel      0.45.1
```

Vì đã lâu rồi kể từ đoàn hệ 2024 nên phiên bản bánh xe của bạn có thể khác và có thể không nằm trong các tùy chọn được cung cấp.

Trả lời: Đối với tôi đó là `0.45.1`


## Câu hỏi 3. Đếm các bản ghi

- Các chuyến đi bắt đầu và kết thúc vào ngày 18-09-2019
- Định dạng dấu thời gian (ngày và giờ+phút+giây) cho đến ngày.

```sql
SELECT COUNT(*) FROM "csv_green_tripdata_2019_09"
WHERE DATE("lpep_pickup_datetime") = '2019-09-18' AND
      DATE("lpep_dropoff_datetime") = '2019-09-18';
```
```
+-------+
| count |
|-------|
| 15612 |
+-------+
```

Trả lời: `15612`


## Câu 4. Chuyến đi dài nhất mỗi ngày
```sql
SELECT
    DATE("lpep_pickup_datetime") AS "pickup_date",
    MAX("trip_distance") AS "longest_trip"
FROM
    "csv_green_tripdata_2019_09"
GROUP BY
    DATE("lpep_pickup_datetime")
ORDER BY
    "longest_trip" DESC
LIMIT 1;
```
```
+-------------+--------------+
| pickup_date | longest_trip |
|-------------+--------------|
| 2019-09-26  | 341.64       |
+-------------+--------------+
```

Trả lời: `2019-09-26`


## Câu 5. Ba khu vực đón khách lớn nhất
```sql
SELECT
    "zone"."Zone",
    ROUND(SUM(("total_amount")::NUMERIC), 3) AS "total_amount"
FROM
    "csv_green_tripdata_2019_09"
INNER JOIN
    "zone" ON "csv_green_tripdata_2019_09"."PULocationID" = "zone"."LocationID"
WHERE
    DATE("lpep_pickup_datetime") = '2019-09-18'
GROUP BY
    "zone"."Zone"
ORDER BY
    "total_amount" DESC
LIMIT 3;
```
```
+---------------------+--------------+
| Zone                | total_amount |
|---------------------+--------------|
| East Harlem North   | 17893.060    |
| East Harlem South   | 17152.160    |
| Morningside Heights | 11259.680    |
+---------------------+--------------+
```

Trả lời: `East Harlem North, East Harlem South, Morningside Heights`


## Câu 6. Mẹo lớn nhất
```sql
SELECT
    puz."Zone" AS pickup_zone,
    doz."Zone" AS dropoff_zone,
    g."tip_amount"
FROM
    "csv_green_tripdata_2019_09" g
INNER JOIN
    "zone" puz ON g."PULocationID" = puz."LocationID"
INNER JOIN
    "zone" doz ON g."DOLocationID" = doz."LocationID"
WHERE
    puz."Zone" = 'Astoria'
ORDER BY
    g."tip_amount" DESC
LIMIT 1;
```

```
+-------------+--------------+------------+
| pickup_zone | dropoff_zone | tip_amount |
|-------------+--------------+------------|
| Astoria     | JFK Airport  | 62.31      |
+-------------+--------------+------------+
```

Trả lời: `JFK Airport`


## Câu 7. Quy trình làm việc Terraform

> tự giải thích
