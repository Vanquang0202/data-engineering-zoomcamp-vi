# Bài tập Module 5

Trong bài tập này, chúng ta sẽ thực hành những kiến thức đã học về Spark.

Chúng ta sẽ sử dụng dữ liệu taxi Yellow tháng 10/2024 từ trang web chính thức: 

```bash
wget https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-10.parquet
```


## Câu hỏi 1: Cài đặt Spark và PySpark

- Cài đặt Spark
- Chạy PySpark
- Tạo một Spark session cục bộ
- Chạy `spark.version`.

Kết quả hiển thị là gì?

> [!NOTE]
> Để cài đặt PySpark, hãy làm theo [hướng dẫn này](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/05-batch/setup/pyspark.md)


## Câu hỏi 2: Dữ liệu taxi Yellow tháng 10/2024

Đọc dữ liệu taxi Yellow tháng 10/2024 vào Spark DataFrame.

Chia lại DataFrame thành 4 Partition rồi lưu dưới định dạng Parquet.

Kích thước trung bình của các file Parquet vừa tạo (đuôi `.parquet`) là bao nhiêu MB? Chọn đáp án gần đúng nhất.

- 6MB
- 25MB
- 75MB
- 100MB


## Câu hỏi 3: Đếm số bản ghi 

Có bao nhiêu chuyến taxi vào ngày 15 tháng 10?

Chỉ tính những chuyến bắt đầu trong ngày 15 tháng 10.

- 85,567
- 105,567
- 125,567
- 145,567


## Câu hỏi 4: Chuyến đi dài nhất

Chuyến đi dài nhất trong bộ dữ liệu kéo dài bao nhiêu giờ?

- 122
- 142
- 162
- 182


## Câu hỏi 5: Giao diện người dùng

Giao diện Spark hiển thị dashboard của ứng dụng chạy trên cổng cục bộ nào?

- 80
- 443
- 4040
- 8080



## Câu hỏi 6: Khu vực đón khách ít xuất hiện nhất

Nạp dữ liệu tra cứu khu vực vào một temp view trong Spark:

```bash
wget https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv
```

Dựa vào dữ liệu tra cứu khu vực và dữ liệu taxi Yellow tháng 10/2024, khu vực đón khách nào xuất hiện ÍT nhất?

- Governor's Island/Ellis Island/Liberty Island
- Arden Heights
- Rikers Island
- Jamaica Bay


## Nộp bài

- Biểu mẫu nộp bài: https://courses.datatalks.club/de-zoomcamp-2025/homework/hw5
- Hạn nộp: Xem trên trang web
