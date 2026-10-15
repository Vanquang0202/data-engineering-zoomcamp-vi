## Bài tập về nhà tuần 3
<b><u>Lưu ý quan trọng:</b></u> <p>Bạn có thể tải dữ liệu theo cách bạn muốn nhưng giữ các tệp ở định dạng .GZĐịnh dạng. 
Nếu bạn đang sử dụng tính năng điều phối như Airflow hoặc Prefect thì không tải dữ liệu vào Big Query bằng bộ điều phối.</br> 
Dừng việc tải tệp vào một nhóm. </br></br>
<u>NOTE:</u> Bạn có thể sử dụng tùy chọn CSV cho các tệp GZ khi tạo Bảng bên ngoài</br>

<b>SETUP:</b></br>
Tạo bảng bên ngoài bằng cách sử dụng dữ liệu fhv 2019. </br> Tạo bảng trong BQ bằng cách sử dụng dữ liệu fhv 2019 (không partition hoặc phân cụm bảng này). </br> Dữ liệu có thể tìm thấy tại đây: https://github.com/DataTalksClub/nyc-tlc-data/releases/tag/fhv </p>

## Câu hỏi 1:
Hồ sơ xe fhv trong năm 2019 là bao nhiêu?
- 65,623,481
- 43,244,696
- 22,978,333
- 13,942,414

## Câu hỏi 2:
Viết truy vấn để đếm số lượng affiliated_base_number riêng biệt cho toàn bộ tập dữ liệu trên cả hai bảng.</br> 
Lượng dữ liệu ước tính sẽ được đọc khi truy vấn này được thực thi trên Bảng ngoài và Bảng là bao nhiêu?

- 25,2 MB cho Bảng ngoài và 100,87 MB cho Bảng BQ
- 225,82 MB cho Bảng ngoài và 47,60 MB cho Bảng BQ
- 0 MB cho Bảng ngoài và 0 MB cho Bảng ngoài Bảng BQ
- 0 MB cho Bảng bên ngoài và 317,94 MB cho Bảng BQ 


## Câu hỏi 3:
Có bao nhiêu bản ghi có cả PUlocationID và DOlocationID trống (null) trong toàn bộ tập dữ liệu?
- 717,748
- 1,215,687
- 5
- 20,332

## Câu hỏi 4:
Đâu là chiến lược tốt nhất để tối ưu hóa bảng nếu truy vấn luôn lọc theo pickup_datetime và sắp xếp theo affiliated_base_number?
- Cụm trên pickup_datetime Cụm trên affiliated_base_number
- Partition của pickup_datetime Cụm trên affiliated_base_number
- Partition của pickup_datetime Partition của affiliated_base_number
- Partition by affiliated_base_number Cluster trên pickup_datetime

## Câu hỏi 5:
Thực hiện giải pháp tối ưu hóa mà bạn đã chọn cho câu hỏi 4. Viết truy vấn để truy xuất affiliated_base_number riêng biệt giữa pickup_datetime 2019/03/01 và 2019/03/31 (đã bao gồm).</br> 
Sử dụng bảng BQ mà bạn đã tạo trước đó trong mệnh đề from và ghi lại số byte ước tính. Bây giờ hãy thay đổi bảng trong mệnh đề from sang bảng được phân vùng mà bạn đã tạo cho câu hỏi 4 và ghi lại số byte ước tính được xử lý. Những giá trị này là gì? Chọn câu trả lời phù hợp nhất.
- 12,82 MB cho bảng không được phân vùng và 647,87 MB cho bảng được phân vùng
- 647,87 MB cho bảng không được phân vùng và 23,06 MB cho bảng được phân vùng
- 582,63 MB cho bảng không được phân vùng và 0 MB cho bảng được phân vùng
- 646,25 MB cho bảng không được phân vùng và 646,25 MB cho bảng được phân vùng


## Câu 6: 
Dữ liệu được lưu trong Bảng ngoài bạn đã tạo ở đâu?

- Truy vấn lớn
- Nhóm GCP
- Đăng ký vùng chứa
- Bảng lớn


## Câu hỏi 7:
Cách tốt nhất trong Big Query là luôn phân cụm dữ liệu của bạn:
- Đúng
- Sai


## (Không bắt buộc) Câu hỏi 8:
Định dạng tốt hơn để lưu trữ các tệp này có thể là parquet. Tạo một đường dẫn dữ liệu để tải xuống các tệp gzip và chuyển đổi chúng thành parquet. Tải các tệp lên Nhóm GCP của bạn và tạo Bảng bên ngoài và Bảng BQ. 


Lưu ý: Các loại cột của tất cả các tệp được sử dụng trong Bảng ngoài phải có cùng kiểu dữ liệu. Mặc dù Bảng bên ngoài có thể được tạo và hiển thị trong bảng điều khiển bên trong Big Query, nhưng bảng này sẽ cần được xác thực bằng cách chạy truy vấn đếm trên Bảng bên ngoài để kiểm tra xem có lỗi nào xảy ra không. 
 
## Nộp bài giải

* Hình thức nộp bài: https://forms.gle/rLdvQW2igsAT73HTA
* Có thể nộp bài tập về nhà nhiều lần. Trong trường hợp này, chỉ lần gửi cuối cùng sẽ được sử dụng. 

Hạn chót: 13 tháng 2 (Thứ Hai), 22:00 CET


## Giải pháp

Giải pháp: https://www.youtube.com/watch?v=j8r2OigKBWE
