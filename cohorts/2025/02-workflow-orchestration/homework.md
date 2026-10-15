## Bài tập Module 2

LƯU Ý: Ở cuối biểu mẫu nộp bài, bạn cần cung cấp link đến repository GitHub hoặc trang lưu trữ code công khai khác. Repository này phải chứa code giải bài tập của bạn. Nếu một phần lời giải không nằm trong file code, hãy đưa phần đó trực tiếp vào file README của repository.

> Nếu kết quả không khớp hoàn toàn với các lựa chọn, hãy chọn đáp án gần nhất. 

Trong bài tập này, chúng ta sẽ dùng bộ dữ liệu taxi _green_ tại đây:

`https://github.com/DataTalksClub/nyc-tlc-data/releases/tag/green/download`

Để tạo link có thể tải bằng `wget`, hãy dùng tiền tố sau (lưu ý bản thân link này trả về 404):

`https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/`

### Yêu cầu bài tập

Đến đây, khóa học đã xử lý dữ liệu năm 2019 và 2020. Nhiệm vụ của bạn là mở rộng các flow hiện có để xử lý thêm dữ liệu năm 2021.

![Bộ dữ liệu cho bài tập](../../../02-workflow-orchestration/images/homework-cropped.png)

Gợi ý: Kestra giúp việc này khá đơn giản:
1. Bạn có thể dùng chức năng Backfill trong [scheduled flow](../../../02-workflow-orchestration/flows/06_gcp_taxi_scheduled.yaml) để nạp bù dữ liệu năm 2021. Hãy chọn đúng khoảng thời gian có dữ liệu, từ `2021-01-01` đến `2021-07-31`. Thực hiện cho cả taxi `yellow` và `green` (chọn đúng loại ở input `taxi`).
2. Hoặc chạy flow thủ công cho từng tháng trong bảy tháng của năm 2021, với cả taxi `yellow` và `green`. Thử thách: tìm cách lặp qua từng tổ hợp Năm-Tháng và loại `taxi` bằng task `ForEach`, rồi kích hoạt flow cho mỗi tổ hợp bằng task `Subflow`.

### Câu hỏi trắc nghiệm

Hãy trả lời 6 câu hỏi trắc nghiệm dưới đây để kiểm tra hiểu biết về điều phối workflow, Kestra và pipeline ETL cho Data Lake và Data Warehouse.

1) Khi chạy xử lý dữ liệu taxi `Yellow` cho năm `2020`, tháng `12`, kích thước file chưa nén là bao nhiêu (tức file đầu ra `yellow_tripdata_2020-12.csv` của task `extract`)?
- 128.3 MiB
- 134.5 MiB
- 364.7 MiB
- 692.6 MiB

2) Khi chạy với input `taxi` là `green`, `year` là `2020` và `month` là `04`, biến `file` được render thành giá trị nào?
- `{{inputs.taxi}}_tripdata_{{inputs.year}}-{{inputs.month}}.csv` 
- `green_tripdata_2020-04.csv`
- `green_tripdata_04_2020.csv`
- `green_tripdata_2020.csv`

3) Tổng số dòng trong tất cả file CSV của dữ liệu taxi `Yellow` năm 2020 là bao nhiêu?
- 13,537.299
- 24,648,499
- 18,324,219
- 29,430,127

4) Tổng số dòng trong tất cả file CSV của dữ liệu taxi `Green` năm 2020 là bao nhiêu?
- 5,327,301
- 936,199
- 1,734,051
- 1,342,034

5) File CSV dữ liệu taxi `Yellow` tháng 3/2021 có bao nhiêu dòng?
- 1,428,092
- 706,911
- 1,925,152
- 2,561,031

6) Bạn sẽ cấu hình múi giờ New York trong Schedule trigger như thế nào?
- Thêm thuộc tính `timezone` với giá trị `EST` vào cấu hình trigger `Schedule`  
- Thêm thuộc tính `timezone` với giá trị `America/New_York` vào cấu hình trigger `Schedule`
- Thêm thuộc tính `timezone` với giá trị `UTC-5` vào cấu hình trigger `Schedule`
- Thêm thuộc tính `location` với giá trị `New_York` vào cấu hình trigger `Schedule`  


## Nộp bài

* Biểu mẫu nộp bài: https://courses.datatalks.club/de-zoomcamp-2025/homework/hw2
* Xem hạn nộp tại link trên

## Lời giải

Sẽ được bổ sung sau hạn nộp bài
