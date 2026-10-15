## Bài tập về nhà của Mô-đun 2

ATTENTION: Ở cuối biểu mẫu gửi, bạn sẽ được yêu cầu đính kèm liên kết đến kho lưu trữ GitHub của bạn hoặc trang web lưu trữ mã công khai khác. Kho lưu trữ này sẽ chứa mã của bạn để giải bài tập về nhà. Nếu giải pháp của bạn bao gồm mã không ở định dạng tệp, vui lòng đưa chúng trực tiếp vào tệp README trong kho lưu trữ của bạn.

> Trong trường hợp bạn không có chính xác một tùy chọn, hãy chọn tùy chọn gần nhất 

Đối với bài tập về nhà, chúng ta sẽ làm việc với tập dữ liệu taxi _green_ có tại đây:

`https://github.com/DataTalksClub/nyc-tlc-data/releases/tag/green/download`

Để có được liên kết có thể sử dụng `wget`, hãy sử dụng tiền tố này (lưu ý rằng chính liên kết đó cung cấp 404):

`https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/`

### Bài tập

Mục tiêu sẽ là xây dựng một đường dẫn ETL tải dữ liệu, thực hiện một số chuyển đổi và ghi dữ liệu vào cơ sở dữ liệu (và Google Cloud!).

- Tạo một đường dẫn mới, gọi là `green_taxi_etl`
- Thêm khối tải dữ liệu và sử dụng Pandas để đọc dữ liệu cho quý cuối cùng của năm 2020 (các tháng `10`, `11`, `12`).
  - Bạn có thể sử dụng các kiểu dữ liệu và phương pháp phân tích ngày giống như trong khóa học.
  - `BONUS`: tải ba tháng cuối cùng bằng vòng lặp for và `pd.concat`
- Thêm khối biến áp và thực hiện như sau:
  - Xóa các hàng có số lượng hành khách bằng 0 _and_ khoảng cách chuyến đi bằng 0.
  - Tạo cột mới `lpep_pickup_date` bằng cách chuyển đổi `lpep_pickup_datetime` thành một ngày.
  - Đổi tên các cột trong Trường hợp Lạc đà thành Trường hợp Rắn, ví dụ: `VendorID` đến `vendor_id`.
  - Thêm ba xác nhận:
    - `vendor_id` is one of the existing values in the column (currently)
    - `passenger_count` is greater than 0
    - `trip_distance` is greater than 0
- Sử dụng trình xuất dữ liệu Postgres (SQL hoặc Python), ghi tập dữ liệu vào bảng có tên `green_taxi` trong lược đồ `mage`. Thay thế bảng nếu nó đã tồn tại.
- Ghi dữ liệu của bạn dưới dạng tệp Parquet vào một nhóm trong GCP, được phân chia bởi `lpep_pickup_date`. Sử dụng thư viện `pyarrow`!
- Lên lịch chạy quy trình của bạn hàng ngày lúc 5 giờ sáng UTC.

### Câu hỏi

## Câu hỏi 1. Đang tải dữ liệu

Sau khi tải tập dữ liệu, hình dạng của dữ liệu sẽ như thế nào?

* 266.855 hàng x 20 cột
* 544.898 hàng x 18 cột
* 544.898 hàng x 20 cột
* 133.744 hàng x 20 cột

## Câu 2. Chuyển đổi dữ liệu

Khi lọc tập dữ liệu trong đó số lượng hành khách lớn hơn 0 _and_ khoảng cách chuyến đi lớn hơn 0, còn lại bao nhiêu hàng?

* 544.897 hàng
* 266.855 hàng
* 139.370 hàng
* 266.856 hàng

## Câu hỏi 3. Chuyển đổi dữ liệu

Điều nào sau đây tạo cột mới `lpep_pickup_date` bằng cách chuyển đổi `lpep_pickup_datetime` thành một ngày?

* `data = data['lpep_pickup_datetime'].date`
* `data('lpep_pickup_date') = data['lpep_pickup_datetime'].date`
* `data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date`
* `data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt().date()`

## Câu hỏi 4. Chuyển đổi dữ liệu

Các giá trị hiện có của `VendorID` trong tập dữ liệu là gì?

* 1, 2, or 3
* 1 or 2
* 1, 2, 3, 4
* 1

## Câu 5. Chuyển đổi dữ liệu

Cần đổi tên bao nhiêu cột thành dạng rắn?

* 3
* 6
* 2
* 4

## Câu hỏi 6. Xuất dữ liệu

Sau khi xuất, có bao nhiêu phân vùng (thư mục) trong Google Cloud?

* 96
* 56
* 67
* 108

## Gửi giải pháp

* Hình thức gửi: https://courses.datatalks.club/de-zoomcamp-2024/homework/hw2
* Kiểm tra liên kết ở trên để xem ngày đến hạn
  
## Giải pháp

Sẽ được bổ sung sau ngày đến hạn
