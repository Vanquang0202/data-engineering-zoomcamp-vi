# Bài tập Module 2 [BẢN NHÁP]

> [!NOTE]
> Đây là bản nháp được chuyển từ khóa 2026. Câu hỏi, bộ dữ liệu và
> hạn nộp sẽ được cập nhật trước khi module bắt đầu.

LƯU Ý: Ở cuối biểu mẫu nộp bài, bạn cần cung cấp link đến repository GitHub hoặc trang lưu trữ code công khai khác. Repository này phải chứa code giải bài tập của bạn. Nếu một phần lời giải không nằm trong file code, hãy đưa phần đó trực tiếp vào file README của repository.

> Nếu kết quả không khớp hoàn toàn với các lựa chọn, hãy chọn đáp án gần nhất. 

Trong bài tập này, chúng ta sẽ dùng bộ dữ liệu taxi _green_ tại đây:

`https://github.com/DataTalksClub/nyc-tlc-data/releases/tag/green/download`

Để tạo link có thể tải bằng `wget`, hãy dùng tiền tố sau (lưu ý bản thân link này trả về 404):

`https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/`

### Yêu cầu bài tập

Đến đây, khóa học đã xử lý dữ liệu năm 2019 và 2020. Nhiệm vụ của bạn là mở rộng các flow hiện có để xử lý thêm dữ liệu năm 2021.

Bài tập này gồm bảy file dữ liệu theo tháng cho mỗi loại taxi:

| Dịch vụ | Các file cần nạp |
| --- | --- |
| Taxi Yellow | `yellow_tripdata_2021-01.csv.gz` đến `yellow_tripdata_2021-07.csv.gz` |
| Taxi Green | `green_tripdata_2021-01.csv.gz` đến `green_tripdata_2021-07.csv.gz` |

Gợi ý: Kestra giúp việc này khá đơn giản:
1. Bạn có thể dùng chức năng Backfill trong [scheduled flow](flows/09_gcp_taxi_scheduled.yaml) để nạp bù dữ liệu năm 2021. Hãy chọn đúng khoảng thời gian có dữ liệu, từ `2021-01-01` đến `2021-07-31`. Thực hiện cho cả taxi `yellow` và `green` (chọn đúng loại ở input `taxi`).
2. Hoặc chạy flow thủ công cho từng tháng trong bảy tháng của năm 2021, với cả taxi `yellow` và `green`. Thử thách: tìm cách lặp qua từng tổ hợp Năm-Tháng và loại `taxi` bằng task `ForEach`, rồi kích hoạt flow cho mỗi tổ hợp bằng task `Subflow`.

### Câu hỏi trắc nghiệm

Hãy trả lời 6 câu hỏi trắc nghiệm dưới đây để kiểm tra hiểu biết về điều phối workflow, Kestra và pipeline ETL.

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

* Biểu mẫu nộp bài: https://courses.datatalks.club/de-zoomcamp-2026/homework/hw2
* Xem hạn nộp tại link trên

## Lời giải

Sẽ được bổ sung sau hạn nộp bài


## Chia sẻ quá trình học công khai

Chúng tôi khuyến khích mọi người chia sẻ những gì mình đã học. Cách học này gọi là "learning in public".

Đọc thêm về lợi ích [tại đây](https://aishippingblog.com/p/benefits-of-learning-in-public-and).

### Bài đăng mẫu trên LinkedIn

```
🚀 Week 2 of Data Engineering Zoomcamp by @DataTalksClub and @Will Russell complete!

Just finished Module 2 - Workflow Orchestration with @Kestra. Learned how to:

✅ Orchestrate data pipelines with Kestra flows
✅ Use variables and expressions for dynamic workflows
✅ Implement backfill for historical data
✅ Schedule workflows with timezone support
✅ Process NYC taxi data (Yellow & Green) for 2019-2021

Built ETL pipelines that extract, transform, and load taxi trip data automatically!

Thanks to the @Kestra team for the great orchestration tool!

Here's my homework solution: <LINK>

Following along with this amazing free course - who else is learning data engineering?

You can sign up here: https://github.com/DataTalksClub/data-engineering-zoomcamp/
```

### Bài đăng mẫu trên Twitter/X

```
Module 2 of DE Zoomcamp by @DataTalksClub @wrussell1999 done!

- @kestra_io workflow orchestration
- ETL pipelines for taxi data
- Backfill & scheduling
- Variables & dynamic flows

My solution: <LINK>

Join me here: https://github.com/DataTalksClub/data-engineering-zoomcamp/
```
