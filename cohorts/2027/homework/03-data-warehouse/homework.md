# Bài tập Module 3: Data Warehousing và BigQuery [BẢN NHÁP]

> [!NOTE]
> Đây là bản nháp được chuyển từ khóa 2026. Câu hỏi, bộ dữ liệu và
> hạn nộp sẽ được cập nhật trước khi module bắt đầu.

Trong bài tập này, chúng ta sẽ thực hành với BigQuery và Google Cloud Storage.

Khi nộp bài, bạn cần cung cấp link đến repository GitHub
hoặc một trang lưu trữ code công khai khác.

Repository này phải chứa code giải bài tập của bạn.

Nếu lời giải gồm câu lệnh SQL hoặc shell nhưng không được lưu
thành file code (ví dụ file Python), hãy ghi chúng trực tiếp vào
file README của repository.

## Dữ liệu

Bài tập sử dụng dữ liệu chuyến đi taxi Yellow từ tháng 1 đến tháng 6/2024 (không phải dữ liệu cả năm).

Các file Parquet có tại trang dữ liệu taxi Thành phố New York:

https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page

## Nạp dữ liệu

Bạn có thể dùng các script sau để nạp dữ liệu vào GCS bucket:

- Script Python: [load_yellow_taxi_data.py](./load_yellow_taxi_data.py)
- Notebook Jupyter với DLT: [DLT_upload_to_GCP.ipynb](./DLT_upload_to_GCP.ipynb)

Bạn cần tạo Service Account có quyền GCS Admin hoặc xác thực bằng Google SDK, rồi cập nhật tên bucket trong script.

Nếu dùng công cụ điều phối như Kestra, Mage, Airflow hoặc Prefect, đừng dùng orchestrator để nạp dữ liệu vào BigQuery.

Trước khi bắt đầu, hãy bảo đảm cả 6 file đã xuất hiện trong GCS bucket.

Lưu ý: Khi tạo external table, bạn cần chọn định dạng PARQUET.


## Thiết lập BigQuery

Tạo một external table từ dữ liệu chuyến đi taxi Yellow. 

Tạo một bảng thông thường (materialized) trong BQ từ dữ liệu này (không Partition hoặc Cluster bảng). 



## Câu hỏi 1. Đếm số bản ghi

Dữ liệu taxi Yellow năm 2024 có bao nhiêu bản ghi?
- 65,623
- 840,402
- 20,332,093
- 85,431,289


## Câu hỏi 2. Ước lượng dữ liệu được đọc

Viết truy vấn đếm số giá trị PULocationID khác nhau trên toàn bộ dữ liệu ở cả hai bảng.
 
Khi chạy truy vấn trên External Table và bảng thông thường, **dung lượng dữ liệu ước tính** được đọc là bao nhiêu?

- 18.82 MB cho External Table và 47.60 MB cho Materialized Table
- 0 MB cho External Table và 155.12 MB cho Materialized Table
- 2.14 GB cho External Table và 0MB cho Materialized Table
- 0 MB cho External Table và 0MB cho Materialized Table

## Câu hỏi 3. Tìm hiểu lưu trữ dạng cột

Viết truy vấn lấy PULocationID từ bảng trong BigQuery (không phải external table). Sau đó viết truy vấn lấy cả PULocationID và DOLocationID từ cùng bảng.

Vì sao số byte ước tính lại khác nhau?
- BigQuery là cơ sở dữ liệu dạng cột và chỉ quét những cột được yêu cầu trong truy vấn. Truy vấn hai cột (PULocationID, DOLocationID) cần đọc nhiều dữ liệu hơn một cột (PULocationID), nên số byte ước tính xử lý cao hơn.
- BigQuery sao chép dữ liệu trên nhiều storage partition, nên chọn hai cột thay vì một cột khiến bảng bị quét hai lần, làm số byte ước tính tăng gấp đôi.
- BigQuery tự động cache cột được truy vấn đầu tiên, nên thêm cột thứ hai làm tăng thời gian xử lý nhưng không ảnh hưởng đến số byte ước tính được quét.
- Khi chọn nhiều cột, BigQuery thực hiện phép join ngầm giữa chúng, làm tăng số byte ước tính được xử lý.

## Câu hỏi 4. Đếm chuyến đi có giá vé bằng 0

Có bao nhiêu bản ghi có fare_amount bằng 0?
- 128,210
- 546,578
- 20,188,016
- 8,333

## Câu hỏi 5. Partition và Clustering

Chiến lược nào tốt nhất để tối ưu bảng BigQuery nếu truy vấn luôn lọc theo tpep_dropoff_datetime và sắp xếp kết quả theo VendorID? Hãy tạo bảng mới theo chiến lược đó.

- Partition theo tpep_dropoff_datetime và Cluster theo VendorID
- Cluster theo tpep_dropoff_datetime và Cluster theo VendorID
- Cluster theo tpep_dropoff_datetime, Partition theo VendorID
- Partition theo tpep_dropoff_datetime và Partition theo VendorID


## Câu hỏi 6. Lợi ích của Partition

Viết truy vấn lấy các VendorID khác nhau khi tpep_dropoff_datetime nằm trong khoảng
từ 2024-03-01 đến hết 2024-03-15.


Trước tiên dùng Materialized Table đã tạo trong mệnh đề FROM và ghi lại số byte ước tính. Sau đó đổi sang bảng có Partition đã tạo ở câu 5 và ghi lại số byte ước tính được xử lý. Các giá trị này là bao nhiêu? 


Chọn đáp án gần đúng nhất.
 

- 12.47 MB cho bảng không Partition và 326.42 MB cho bảng có Partition
- 310.24 MB cho bảng không Partition và 26.84 MB cho bảng có Partition
- 5.87 MB cho bảng không Partition và 0 MB cho bảng có Partition
- 310.31 MB cho bảng không Partition và 285.64 MB cho bảng có Partition


## Câu hỏi 7. Nơi lưu dữ liệu của external table

Dữ liệu của External Table bạn vừa tạo được lưu ở đâu?

- Big Query
- Container Registry
- GCP Bucket
- Big Table

## Câu hỏi 8. Cách dùng Clustering hiệu quả

Trong BigQuery, có phải lúc nào cũng nên Cluster dữ liệu không?
- Đúng
- Sai


## Câu hỏi 9. Tìm hiểu việc quét bảng

Không tính điểm: Viết truy vấn `SELECT count(*)` FROM Materialized Table bạn đã tạo. Ước tính có bao nhiêu byte được đọc? Vì sao?


## Nộp bài

Biểu mẫu nộp bài: https://courses.datatalks.club/de-zoomcamp-2026/homework/hw3


## Chia sẻ quá trình học công khai

Chúng tôi khuyến khích mọi người chia sẻ những gì mình đã học. Cách học này gọi là "learning in public".

Đọc thêm về lợi ích [tại đây](https://aishippingblog.com/p/benefits-of-learning-in-public-and).

### Bài đăng mẫu trên LinkedIn

```
🚀 Week 3 of Data Engineering Zoomcamp by @DataTalksClub complete!

Just finished Module 3 - Data Warehousing with BigQuery. Learned how to:

✅ Create external tables from GCS bucket data
✅ Build materialized tables in BigQuery
✅ Partition and cluster tables for performance
✅ Understand columnar storage and query optimization
✅ Analyze NYC taxi data at scale

Working with 20M+ records and learning how partitioning reduces query costs!

Here's my homework solution: <LINK>

Following along with this amazing free course - who else is learning data engineering?

You can sign up here: https://github.com/DataTalksClub/data-engineering-zoomcamp/
```

### Bài đăng mẫu trên Twitter/X

```
📊 Module 3 of Data Engineering Zoomcamp done!

- BigQuery & GCS
- External vs materialized tables
- Partitioning & clustering
- Query optimization

My solution: <LINK>

Free course by @DataTalksClub: https://github.com/DataTalksClub/data-engineering-zoomcamp/
```
