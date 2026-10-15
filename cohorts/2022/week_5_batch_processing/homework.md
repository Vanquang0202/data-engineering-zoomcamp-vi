## Bài tập về nhà Tuần 5

Trong bài tập về nhà này, chúng ta sẽ áp dụng những gì đã học về Spark vào thực tế.

Chúng ta sẽ sử dụng tập dữ liệu về xe cho thuê số lượng lớn (HVFHV) cho việc đó.

## Câu hỏi 1. Cài đặt Spark và PySpark

* Cài đặt Spark
* Chạy PySpark
* Tạo Spark session cục bộ
* Chạy `spark.version`

Đầu ra là gì?


## Câu hỏi 2. HVFHW Tháng 2 năm 2021

Tải xuống dữ liệu HVFHV cho tháng 2 năm 2021:

```bash
wget https://nyc-tlc.s3.amazonaws.com/trip+data/fhvhv_tripdata_2021-02.csv
```

Đọc nó với Spark bằng cách sử dụng cùng một lược đồ như chúng ta đã làm 
trong các bài học. Chúng tôi sẽ sử dụng tập dữ liệu này cho tất cả các câu hỏi còn lại.

Phân vùng lại thành 24 phân vùng và lưu nó vào
Parquet.

Kích thước của thư mục chứa kết quả (trong MB) là bao nhiêu?


## Câu 3. Đếm số liệu 

Ngày 15 tháng 2 có bao nhiêu chuyến taxi?

Chỉ xét các chuyến đi bắt đầu vào ngày 15 tháng 2.


## Câu 4. Chuyến đi dài nhất mỗi ngày

Bây giờ hãy tính thời gian cho mỗi chuyến đi.

Chuyến đi bắt đầu vào ngày nào dài nhất? 


## Câu hỏi 5. `dispatching_base_num` thường xuyên nhất

Bây giờ hãy tìm `dispatching_base_num` xảy ra thường xuyên nhất 
trong tập dữ liệu này.

Công việc spark này có bao nhiêu giai đoạn?

> Lưu ý: câu trả lời có thể phụ thuộc vào cách bạn viết truy vấn,
> vì vậy có nhiều câu trả lời đúng. 
> Chọn cái bạn có.


## Câu 6. Cặp địa điểm thường gặp nhất

Tìm cặp đón - trả khách phổ biến nhất. 

Ví dụ:

"Vịnh Jamaica / Clinton East"

Nhập hai tên khu vực cách nhau bằng dấu gạch chéo

Nếu bất kỳ tên khu vực nào không xác định (thiếu), hãy sử dụng "Không xác định". Ví dụ: "Không xác định / Clinton East". 


## Câu hỏi bổ sung. Loại tham gia

(không được chấm điểm) 

Để tìm câu trả lời cho Q6, bạn cần thực hiện phép nối.

Đó là kiểu join nào?

Và công việc spark của bạn có bao nhiêu giai đoạn?


## Nộp bài giải

* Hình thức nộp bài: https://forms.gle/dBkVK9yT8cSMDwuw7
* Có thể nộp bài tập về nhà nhiều lần. Trong trường hợp này, chỉ lần gửi cuối cùng sẽ được sử dụng. 

Hạn chót: 07/03 (Thứ Hai), 22:00 CET
