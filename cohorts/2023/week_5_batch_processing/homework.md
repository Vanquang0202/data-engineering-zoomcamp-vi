## Bài tập về nhà Tuần 5 

Trong bài tập về nhà này, chúng ta sẽ áp dụng những gì đã học về Spark vào thực tế.

Đối với bài tập về nhà này, chúng tôi sẽ sử dụng dữ liệu FHVHV 2021-06 có tại đây. [Dữ liệu FHVHV](https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhvhv/fhvhv_tripdata_2021-06.csv.gz )


### Câu hỏi 1: 

**Cài đặt Spark và PySpark** 

- Cài đặt Spark
- Chạy PySpark
- Tạo phiên spark cục bộ
- Thực thi spark.version.

Đầu ra là gì?
- 3.3.2
- 2.1.4
- 1.2.3
- 5.4
</br></br>


### Câu hỏi 2: 

**HVFHW Tháng 6 năm 2021**

Đọc nó với Spark bằng cách sử dụng cùng một lược đồ như chúng ta đã làm trong các bài học.</br> 
Chúng ta sẽ sử dụng tập dữ liệu này cho tất cả các câu hỏi còn lại.</br> Phân vùng lại thành 12 phân vùng và lưu vào parquet.</br> Kích thước trung bình của Parquet (kết thúc bằng phần mở rộng .parquet) Các tệp đã được tạo (trong MB) là bao nhiêu? Chọn câu trả lời phù hợp nhất.</br>


- 2MB
- 24MB
- 100MB
- 250MB
</br></br>


### Câu hỏi 3: 

**Đếm hồ sơ**  

Có bao nhiêu chuyến taxi vào ngày 15 tháng 6?</br></br> Chỉ xem xét các chuyến đi bắt đầu vào ngày 15 tháng 6.</br>

- 308,164
- 12,856
- 452,470
- 50,982
</br></br>


### Câu hỏi 4: 

**Chuyến đi dài nhất mỗi ngày**  

Bây giờ hãy tính thời lượng cho mỗi chuyến đi.</br> Chuyến đi dài nhất trong Giờ là bao lâu?</br>

- 66,87 giờ
- 243,44 giờ
- 7,68 giờ
- 3,32 giờ
</br></br>

### Câu hỏi 5: 

**Giao diện người dùng**

 Giao diện người dùng của Spark hiển thị bảng điều khiển của ứng dụng chạy trên cổng cục bộ nào?</br>

- 80
- 443
- 4040
- 8080
</br></br>


### Câu hỏi 6: 

**Vùng vị trí lấy hàng thường xuyên nhất**

Tải dữ liệu tra cứu vùng vào chế độ xem tạm thời trong Spark</br>
[Dữ liệu vùng](https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv)</br>

Sử dụng dữ liệu tra cứu vùng và fhvhv June Dữ liệu năm 2021, tên của khu vực địa điểm đón thường xuyên nhất là gì?</br>

- East Chelsea
- Astoria
- Union Sq
- Crown Heights North
</br></br>




## Nộp giải pháp

* Mẫu nộp: https://forms.gle/EcSvDs6vp64gcGuD8
* Bạn có thể nộp bài tập về nhà nhiều lần. Trong trường hợp này, chỉ lần gửi cuối cùng sẽ được sử dụng. 

Hạn chót: 06/03 (Thứ Hai), 22:00 CET


## Giải pháp

* Video: https://www.youtube.com/watch?v=ldoDIT32pJs
* Đáp án:
  * Câu 1: 3.3.2
  * Câu 2: 24MB
  * Câu 3: 452.470
  * Câu 4: 66,87 giờ
  * Câu 5: 4040
  * Câu 6: Crown Heights North
