## Mô-đun 5 Bài tập về nhà 

Giải: https://www.youtube.com/watch?v=YtddC7vJOgQ

Trong bài tập về nhà này, chúng ta sẽ áp dụng những gì đã học về Spark vào thực tế.

Đối với bài tập về nhà này, chúng tôi sẽ sử dụng dữ liệu FHV 2019-10 có tại đây. [Dữ liệu FHV](https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/fhv_tripdata_2019-10.csv.gz)

### Câu hỏi 1: 

**Cài đặt Spark và PySpark** 

- Cài đặt Spark
- Chạy PySpark
- Tạo phiên spark cục bộ
- Thực thi spark.version.

Đầu ra là gì?

> [!NOTE]
> Để cài đặt PySpark, hãy làm theo [hướng dẫn](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/05-batch/setup/pyspark.md)

### Câu hỏi 2: 

**FHV tháng 10 năm 2019**

Đọc FHV tháng 10 năm 2019 thành Spark Dataframe với lược đồ như chúng ta đã làm trong bài học.

Phân vùng lại Dataframe thành 6 phân vùng và lưu vào parquet.

Kích thước trung bình của các tệp Parquet (kết thúc bằng phần mở rộng .parquet) đã được tạo (trong MB) là bao nhiêu? Chọn câu trả lời phù hợp nhất.

- 1MB
- 6MB
- 25MB
- 87MB



### Câu hỏi 3: 

**Đếm hồ sơ** 

Có bao nhiêu chuyến taxi vào ngày 15 tháng 10?

Chỉ xem xét các chuyến đi bắt đầu vào ngày 15 tháng 10.

- 108,164
- 12,856
- 452,470
- 62,610

> [!IMPORTANT]
> Lưu ý về thứ tự các cột khi xác định lược đồ

### Câu hỏi 4: 

**Chuyến đi dài nhất mỗi ngày** 

Độ dài của chuyến đi dài nhất trong tập dữ liệu tính bằng giờ là bao nhiêu?

- 631.152,50 giờ
- 243,44 giờ
- 7,68 giờ
- 3,32 giờ



### Câu hỏi 5: 

**Giao diện người dùng**

Giao diện người dùng của Spark hiển thị bảng điều khiển của ứng dụng chạy trên cổng cục bộ nào?

- 80
- 443
- 4040
- 8080



### Câu hỏi 6: 

**Khu vực địa điểm lấy hàng ít thường xuyên nhất**

Tải dữ liệu tra cứu khu vực vào chế độ xem tạm thời trong Spark</br>
[Dữ liệu vùng](https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv)

Sử dụng dữ liệu tra cứu khu vực và dữ liệu FHV tháng 10 năm 2019, tên của địa điểm lấy hàng thường xuyên LEAST là gì Zone?</br>

- Đông Chelsea
- Vịnh Jamaica
- Union Sq
- Crown Heights North


## Nộp giải pháp

- Hình thức nộp hồ sơ: https://courses.datatalks.club/de-zoomcamp-2024/homework/hw5
- Hạn chót: Xem trên website
