# Bài tập Module 6

Trong bài tập này, chúng ta sẽ thực hành những kiến thức đã học về Spark.

Chúng ta sẽ dùng dữ liệu taxi Yellow tháng 11/2025 từ trang web chính thức:

```bash
wget https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2025-11.parquet
```


## Câu hỏi 1: Cài đặt Spark và PySpark

- Cài đặt Spark
- Chạy PySpark
- Tạo một Spark session cục bộ
- Chạy `spark.version`.

Kết quả hiển thị là gì?

> [!NOTE]
> Để cài đặt PySpark, hãy làm theo [hướng dẫn này](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/06-batch/setup/)


## Câu hỏi 2: Dữ liệu taxi Yellow tháng 11/2025

Đọc dữ liệu taxi Yellow tháng 11/2025 vào Spark DataFrame.

Chia lại DataFrame thành 4 Partition rồi lưu dưới định dạng Parquet.

Kích thước trung bình của các file Parquet vừa tạo (đuôi `.parquet`) là bao nhiêu MB? Chọn đáp án gần đúng nhất.

- 6MB
- 25MB
- 75MB
- 100MB


## Câu hỏi 3: Đếm số bản ghi

Có bao nhiêu chuyến taxi vào ngày 15 tháng 11?

Chỉ tính những chuyến bắt đầu trong ngày 15 tháng 11.

- 62,610
- 102,340
- 162,604
- 225,768


## Câu hỏi 4: Chuyến đi dài nhất

Chuyến đi dài nhất trong bộ dữ liệu kéo dài bao nhiêu giờ?

- 22.7
- 58.2
- 90.6
- 134.5


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

Dựa vào dữ liệu tra cứu khu vực và dữ liệu taxi Yellow tháng 11/2025, khu vực đón khách nào xuất hiện ÍT nhất?

- Governor's Island/Ellis Island/Liberty Island
- Arden Heights
- Rikers Island
- Jamaica Bay

Nếu có nhiều đáp án đúng, bạn có thể chọn bất kỳ đáp án nào.

## Nộp bài

- Biểu mẫu nộp bài: https://courses.datatalks.club/de-zoomcamp-2026/homework/hw6
- Hạn nộp: Xem trên trang web


## Chia sẻ quá trình học công khai

Chúng tôi khuyến khích mọi người chia sẻ những gì mình đã học. Cách học này gọi là "learning in public".

Đọc thêm về lợi ích [tại đây](https://aishippingblog.com/p/benefits-of-learning-in-public-and).

### Bài đăng mẫu trên LinkedIn

```
🚀 Week 6 of Data Engineering Zoomcamp by @DataTalksClub complete!

Just finished Module 6 - Batch Processing with Spark. Learned how to:

✅ Set up PySpark and create Spark sessions
✅ Read and process Parquet files at scale
✅ Repartition data for optimal performance
✅ Analyze millions of taxi trips with DataFrames
✅ Use Spark UI for monitoring jobs

Processing 4M+ taxi trips with Spark - distributed computing is powerful! 💪

Here's my homework solution: <LINK>

Following along with this amazing free course - who else is learning data engineering?

You can sign up here: https://github.com/DataTalksClub/data-engineering-zoomcamp/
```

### Bài đăng mẫu trên Twitter/X

```
⚡ Module 6 of Data Engineering Zoomcamp done!

- Batch processing with Spark 🔥
- PySpark & DataFrames
- Parquet file optimization
- Spark UI on port 4040

My solution: <LINK>

Free course by @DataTalksClub: https://github.com/DataTalksClub/data-engineering-zoomcamp/
```
