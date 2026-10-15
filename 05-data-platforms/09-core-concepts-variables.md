---
video_url: https://www.youtube.com/watch?v=XCx0nDmhhxA
prev_url: 08-core-concepts-assets.md
next_url: 10-core-concepts-commands.md
---
# Khái niệm cốt lõi: Biến

## Biến là gì?

**Các biến** được khởi tạo động mỗi khi tạo quy trình chạy quy trình. Chúng cho phép bạn tham số hóa quy trình của mình và chuyển các giá trị động khi chạy.


*Các biến thời gian chạy cho phép cùng một quy trình chọn khoảng thời gian và tham số tùy chỉnh cho mỗi lần chạy mà không cần ghi lại logic nội dung.*

## Các loại biến

### 1. Biến tích hợp

Luôn được Bruin cung cấp tự động:

| Biến | Mô tả |
|----------|-------------|
| `start_date` | Bắt đầu khoảng thời gian theo lịch trình |
| `end_date` | Kết thúc khoảng thời gian dự kiến ​​|

Những ngày này được xác định theo lịch trình của đường ống:

| Lịch trình | Ngày bắt đầu | Ngày kết thúc |
|----------|------------|----------|
| **Hàng tháng** | Ngày đầu tháng | Ngày cuối cùng của tháng |
| **Hàng ngày** | Bắt đầu ngày | Cuối ngày |
| **Hàng giờ** | Bắt đầu giờ | Cuối giờ |

#### Nội dung SQL - Định dạng Jinja

Trong SQL, các biến được chèn bằng cách sử dụng khuôn mẫu Jinja:

```sql
@bruin.asset(name="staging.monthly_trips", type="sql")
SELECT *
FROM raw.trips
WHERE pickup_date >= '{{ start_date }}'
  AND pickup_date < '{{ end_date }}'
```

Sử dụng **Bảng kết xuất Bruin** trong Mã VS để xem truy vấn đã biên dịch với các giá trị thực tế.

#### Tài sản Python - Biến môi trường

Trong Python, các biến được truy cập thông qua các biến môi trường:

```python
import os
from datetime import datetime

@bruin.asset(name="raw.monthly_data", type="python")
def ingest_monthly_data():
    start_date = os.environ['BRUIN_VAR_START_DATE']
    end_date = os.environ['BRUIN_VAR_END_DATE']

    # Parse and use dates to fetch data for specific period
    start = datetime.fromisoformat(start_date)
    end = datetime.fromisoformat(end_date)

    # Loop through months in range
    # ...
```

### 2. Biến tùy chỉnh

Các biến do người dùng xác định được đặt ở cấp quy trình.

#### Định nghĩa trong `pipeline.yml`

```yaml
variables:
  - name: taxi_types
    type: array
    default:
      - "yellow"
```

#### Ghi đè khi chạy

Thay đổi giá trị mặc định khi tạo đường chạy:

```bash
bruin run ./pipeline.yml --var taxi_types=["green","fhv"]
```

#### Truy cập các biến tùy chỉnh trong Python

```python
import os
import json

@bruin.asset(name="example.asset", type="python")
def example_asset():
    # Custom variables are prefixed with BRUIN_VAR_
    taxi_types_json = os.environ['BRUIN_VAR_TAXI_TYPES']
    taxi_types = json.loads(taxi_types_json)

    # Use the variable in your code
    for taxi_type in taxi_types:
        # Process each taxi type
        pass
```

## Bảng mở rộng mã VS

Từ bảng Bruin trong Mã/Con trỏ VS:

1. **Ghi đè biến** - Đặt giá trị biến tùy chỉnh trước khi chạy
2. **Bruin Render** - Xem cách các mẫu Jinja được biên dịch với các giá trị thực tế
3. **Chạy cấu hình** - Đặt ngày, môi trường và biến

## Các trường hợp sử dụng thực tế

| Trường hợp sử dụng | Mô tả |
|----------|-------------|
| **Phân vùng dựa trên ngày** | Trích xuất dữ liệu trong khoảng thời gian cụ thể |
| **Xử lý nhiều người thuê** | Chạy cùng một quy trình cho các khách hàng khác nhau |
| **Biến đổi tham số** | Thay đổi logic dựa trên các biến |
| **Thử nghiệm A/B** | Kiểm tra các cấu hình khác nhau mà không thay đổi mã |

## Tham khảo nhanh

```bash
# Run with custom dates
bruin run ./pipeline.yml --start-date 2020-01-01 --end-date 2020-01-31

# Run with variable override (array)
bruin run ./pipeline.yml --var taxi_types=["green","fhv"]

# Run with variable override (string)
bruin run ./pipeline.yml --var customer_id=12345

# Run with full refresh (affects materialization)
bruin run ./pipeline.yml --full-refresh

# Set end date as exclusive
bruin run ./pipeline.yml --exclusive-end-date
```

## Đọc thêm

- [Tài liệu về Bruin - Biến](https://getbruin.com/docs/bruin/core-concepts/variables.html)
- [Tùy chọn thời gian chạy đường ống](https://getbruin.com/docs/bruin/commands/run.html)
