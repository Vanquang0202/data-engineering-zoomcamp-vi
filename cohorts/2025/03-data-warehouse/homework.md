## Bài tập Module 3

LƯU Ý: Ở cuối biểu mẫu nộp bài, bạn cần cung cấp link đến repository GitHub hoặc trang lưu trữ code công khai khác. 
Repository này phải chứa code giải bài tập. Nếu một phần lời giải là câu lệnh SQL hoặc shell mà không nằm trong file code,
hãy ghi chúng trực tiếp vào file README của repository.

<b><u>Lưu ý quan trọng:</b></u> <p> Bài tập sử dụng dữ liệu chuyến đi taxi Yellow từ **tháng 1 đến tháng 6/2024, KHÔNG phải dữ liệu cả năm**. 
Các file Parquet có tại trang dữ liệu taxi Thành phố New York:</br> https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page </br>
Nếu dùng công cụ điều phối như Kestra, Mage, Airflow hoặc Prefect, đừng dùng orchestrator để nạp dữ liệu vào BigQuery.</br> 
Chỉ nạp các file vào bucket rồi dừng ở đó. </br></br>

**Script nạp dữ liệu:** Bạn có thể tải các file Parquet và đưa vào GCS Bucket thủ công, hoặc dùng script [tại đây](./load_yellow_taxi_data.py):<br>
Bạn cần tạo Service Account có quyền GCS Admin hoặc xác thực bằng Google SDK, rồi cập nhật tên bucket trong script cho đúng với bucket của mình.<br>
Trước khi bắt đầu, hãy kiểm tra để chắc chắn cả 6 file đều đã xuất hiện trong GCS Bucket.</br><br>

<u>LƯU Ý:</u> Khi tạo External Table, bạn cần chọn định dạng PARQUET.</br>

<b>THIẾT LẬP BIGQUERY:</b></br>
Tạo External Table từ dữ liệu chuyến đi taxi Yellow. </br>
Tạo một bảng thông thường (materialized) trong BQ từ dữ liệu này (không Partition hoặc Cluster bảng). </br>
</p>

## Câu hỏi 1:
Dữ liệu taxi Yellow năm 2024 có bao nhiêu bản ghi?
- 65,623
- 840,402
- 20,332,093
- 85,431,289


## Câu hỏi 2:
Viết truy vấn đếm số giá trị PULocationID khác nhau trên toàn bộ dữ liệu ở cả hai bảng.</br> 
Khi chạy truy vấn trên External Table và bảng thông thường, **dung lượng dữ liệu ước tính** được đọc là bao nhiêu?

- 18.82 MB cho External Table và 47.60 MB cho Materialized Table
- 0 MB cho External Table và 155.12 MB cho Materialized Table
- 2.14 GB cho External Table và 0MB cho Materialized Table
- 0 MB cho External Table và 0MB cho Materialized Table

## Câu hỏi 3:
Viết truy vấn lấy PULocationID từ bảng trong BigQuery (không phải external table), rồi viết truy vấn lấy cả PULocationID và DOLocationID từ cùng bảng. Vì sao số byte ước tính lại khác nhau?
- BigQuery là cơ sở dữ liệu dạng cột và chỉ quét những cột được yêu cầu trong truy vấn. Truy vấn hai cột (PULocationID, DOLocationID) cần đọc nhiều dữ liệu hơn một cột (PULocationID), nên số byte ước tính xử lý cao hơn.
- BigQuery sao chép dữ liệu trên nhiều storage partition, nên chọn hai cột thay vì một cột khiến bảng bị quét hai lần, làm số byte ước tính tăng gấp đôi.
- BigQuery tự động cache cột được truy vấn đầu tiên, nên thêm cột thứ hai làm tăng thời gian xử lý nhưng không ảnh hưởng đến số byte ước tính được quét.
- Khi chọn nhiều cột, BigQuery thực hiện phép join ngầm giữa chúng, làm tăng số byte ước tính được xử lý.

## Câu hỏi 4:
Có bao nhiêu bản ghi có fare_amount bằng 0?
- 128,210
- 546,578
- 20,188,016
- 8,333

## Câu hỏi 5:
Chiến lược nào tốt nhất để tối ưu bảng BigQuery nếu truy vấn luôn lọc theo tpep_dropoff_datetime và sắp xếp kết quả theo VendorID? Hãy tạo bảng mới theo chiến lược đó.
- Partition theo tpep_dropoff_datetime và Cluster theo VendorID
- Cluster theo tpep_dropoff_datetime và Cluster theo VendorID
- Cluster theo tpep_dropoff_datetime, Partition theo VendorID
- Partition theo tpep_dropoff_datetime và Partition theo VendorID


## Câu hỏi 6:
Viết truy vấn lấy các VendorID khác nhau khi tpep_dropoff_datetime nằm trong khoảng
từ 2024-03-01 đến hết 2024-03-15.</br>

Trước tiên dùng Materialized Table đã tạo trong mệnh đề FROM và ghi lại số byte ước tính. Sau đó đổi sang bảng có Partition đã tạo ở câu 5 và ghi lại số byte ước tính được xử lý. Các giá trị này là bao nhiêu? </br>

Chọn đáp án gần đúng nhất.</br> 

- 12.47 MB cho bảng không Partition và 326.42 MB cho bảng có Partition
- 310.24 MB cho bảng không Partition và 26.84 MB cho bảng có Partition
- 5.87 MB cho bảng không Partition và 0 MB cho bảng có Partition
- 310.31 MB cho bảng không Partition và 285.64 MB cho bảng có Partition


## Câu hỏi 7: 
Dữ liệu của External Table bạn vừa tạo được lưu ở đâu?

- Big Query
- Container Registry
- GCP Bucket
- Big Table

## Câu hỏi 8:
Trong BigQuery, có phải lúc nào cũng nên Cluster dữ liệu không?
- Đúng
- Sai


## Câu hỏi 9 (không tính điểm):
Viết truy vấn `SELECT count(*)` FROM Materialized Table bạn đã tạo. Ước tính có bao nhiêu byte được đọc? Vì sao?


## Nộp bài

Biểu mẫu nộp bài: https://courses.datatalks.club/de-zoomcamp-2025/homework/hw3

## Lời giải

Lời giải: https://www.youtube.com/watch?v=wpLmImIUlPg
