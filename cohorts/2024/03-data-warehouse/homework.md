## Bài tập về nhà của Mô-đun 3

Giải pháp: https://www.youtube.com/watch?v=8g_lRKaC9ro

ATTENTION: Ở cuối biểu mẫu gửi, bạn sẽ được yêu cầu đính kèm liên kết tới kho lưu trữ GitHub của bạn hoặc trang web lưu trữ mã công khai khác. Kho lưu trữ này sẽ chứa mã của bạn để giải bài tập về nhà. Nếu giải pháp của bạn bao gồm mã không ở định dạng tệp (chẳng hạn như truy vấn SQL hoặc lệnh shell), vui lòng đưa chúng trực tiếp vào tệp README trong kho lưu trữ của bạn.

<b><u>Lưu ý quan trọng:</b></u> <p> Đối với bài tập về nhà này, chúng tôi sẽ sử dụng Hồ sơ chuyến đi taxi xanh năm 2022 Các tệp Parquet từ New York
Dữ liệu taxi thành phố được tìm thấy tại đây: </br> https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page </br>
Nếu bạn đang sử dụng điều phối như Mage, Airflow hoặc Prefect thì không tải dữ liệu vào Big Query bằng bộ điều phối.</br> 
Dừng việc tải các tệp vào một nhóm. </br></br>
<u>NOTE:</u> Bạn sẽ cần sử dụng các tệp tùy chọn PARQUET khi tạo Bảng bên ngoài</br>

<b>SETUP:</b></br>
Tạo một bảng bên ngoài bằng cách sử dụng Dữ liệu Bản ghi chuyến đi Taxi Xanh cho năm 2022. </br> Tạo một bảng trong BQ bằng cách sử dụng Bản ghi Chuyến đi Taxi Xanh cho năm 2022 (không partition hoặc gộp bảng này). </br>
</p>

## Câu hỏi 1:
Câu hỏi 1: Số lượng bản ghi cho Dữ liệu Taxi Xanh 2022 là gì??
- 65,623,481
- 840,402
- 1,936,423
- 253,647

## Câu hỏi 2:
Viết truy vấn để đếm số lượng PULocationIDs riêng biệt cho toàn bộ tập dữ liệu trên cả hai bảng.</br> 
Lượng dữ liệu ước tính sẽ được đọc khi truy vấn này được thực thi trên Bảng ngoài và Bảng là bao nhiêu?

- 0 MB cho Bảng bên ngoài và 6,41MB cho Bảng vật chất hóa
- 18,82 MB cho Bảng bên ngoài và 47,60 MB cho Bảng vật chất hóa
- 0 MB cho Bảng bên ngoài và 0MB cho Bảng vật chất hóa
- 2.14 MB cho Bảng bên ngoài và 0MB cho Bảng vật chất hóa


## Câu hỏi 3:
Có bao nhiêu bản ghi có fare_amount bằng 0?
- 12,488
- 128,219
- 112
- 1,622

## Câu hỏi 4:
Chiến lược tốt nhất để tạo bảng được tối ưu hóa trong Big Query là gì nếu truy vấn của bạn luôn sắp xếp kết quả theo PUlocationID và lọc dựa trên lpep_pickup_datetime? (Tạo một bảng mới với chiến lược này)
- Cụm trên lpep_pickup_datetime Partition của PUlocationID
- Partition của lpep_pickup_datetime Cụm trên PUlocationID
- Partition của lpep_pickup_datetime và Partition của PUlocationID
- Phân cụm trên lpep_pickup_datetime và Cụm trên PUlocationID

## Câu hỏi 5:
Viết truy vấn để truy xuất PULocationID khác biệt giữa lpep_pickup_datetime 06/01/2022 và 06/30/2022 (bao gồm)</br>

Sử dụng bảng cụ thể hóa mà bạn đã tạo trước đó trong mệnh đề from của mình và lưu ý các byte ước tính. Bây giờ hãy thay đổi bảng trong mệnh đề from sang bảng được phân vùng mà bạn đã tạo cho câu hỏi 4 và ghi lại số byte ước tính được xử lý. Những giá trị này là gì? </br>

Chọn câu trả lời phù hợp nhất.</br> 

- 22,82 MB cho bảng không được phân vùng và 647,87 MB cho bảng được phân vùng
- 12,82 MB cho bảng không được phân vùng và 1,12 MB cho bảng được phân vùng
- 5,63 MB cho bảng không được phân vùng và 0 MB cho bảng được phân vùng
- 10,31 MB cho bảng không được phân vùng và 10,31 MB cho bảng được phân vùng


## Câu hỏi 6: 
Dữ liệu được lưu trữ trong Bảng ngoài bạn đã tạo ở đâu?

- Truy vấn lớn
- Nhóm GCP
- Bảng lớn
- Cơ quan đăng ký vùng chứa


## Câu hỏi 7:
Cách tốt nhất trong Big Query là luôn phân cụm dữ liệu của bạn:
- Đúng
- Sai


## (Phần thưởng: Không có giá trị điểm) Câu hỏi 8:
Không có điểm: Viết truy vấn `SELECT count(*)` FROM bảng cụ thể hóa mà bạn đã tạo. Nó ước tính bao nhiêu byte sẽ được đọc? Tại sao?

 
## Nộp giải pháp

* Hình thức nộp hồ sơ: https://courses.datatalks.club/de-zoomcamp-2024/homework/hw3


