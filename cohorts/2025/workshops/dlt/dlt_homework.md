File gốc nằm tại
    https://colab.research.google.com/drive/1plqdl33K_HkVx0E0nGJrrkEUssStQsW7

# **Workshop "Data Ingestion với dlt": Bài tập**

---

## **Bộ dữ liệu và API**

Chúng ta sẽ dùng **dữ liệu taxi NYC** thông qua API riêng đã sử dụng trong workshop:

🔹 **URL gốc của API:**  
```
https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api
```
🔹 **Định dạng dữ liệu:** JSON được phân trang (1.000 bản ghi mỗi trang).  
🔹 **Phân trang API:** Dừng khi API trả về trang rỗng.

## **Câu hỏi 1: Phiên bản dlt**

1. **Cài đặt dlt**:

```
!pip install dlt[duckdb]
```

> Bạn cũng có thể chọn cấu hình khác như `bigquery`, `redshift`, v.v. nếu muốn dùng destination khác. Trong bài tập này, chúng ta vẫn kiểm tra nhanh với DuckDB.

2. **Kiểm tra** phiên bản:

```
!dlt --version
```

hoặc:

```py
import dlt
print("dlt version:", dlt.__version__)
```

Hãy ghi lại **phiên bản** xuất hiện trong kết quả.

## **Câu hỏi 2: Định nghĩa và chạy pipeline (API taxi NYC)**

Dùng dlt để trích xuất dữ liệu từ tất cả các trang của API.

Các bước:

1️⃣ Dùng decorator `@dlt.resource` để định nghĩa nguồn dữ liệu API.

2️⃣ Triển khai phân trang tự động bằng REST client tích hợp của dlt.

3️⃣ Nạp dữ liệu đã trích xuất vào DuckDB để truy vấn.

```py
import dlt
from dlt.sources.helpers.rest_client import RESTClient
from dlt.sources.helpers.rest_client.paginators import PageNumberPaginator


# your code is here


pipeline = dlt.pipeline(
    pipeline_name="ny_taxi_pipeline",
    destination="duckdb",
    dataset_name="ny_taxi_data"
)
```

Nạp dữ liệu vào DuckDB để kiểm tra:
```py
load_info = pipeline.run(ny_taxi)
print(load_info)
```
Kết nối cơ sở dữ liệu bằng `duckdb` và xem các bảng đã được tạo:"""

```py
import duckdb
from google.colab import data_table
data_table.enable_dataframe_formatter()

# A database '<pipeline_name>.duckdb' was created in working directory so just connect to it

# Connect to the DuckDB database
conn = duckdb.connect(f"{pipeline.pipeline_name}.duckdb")

# Set search path to the dataset
conn.sql(f"SET search_path = '{pipeline.dataset_name}'")

# Describe the dataset
conn.sql("DESCRIBE").df()

```

Có bao nhiêu bảng được tạo?

* 2
* 4
* 6
* 8

## **Câu hỏi 3: Khám phá dữ liệu đã nạp**

Kiểm tra bảng `ride`:

```py
df = pipeline.dataset(dataset_type="default").rides.df()
df
```

Tổng số bản ghi đã trích xuất là bao nhiêu?

* 2500
* 5000
* 7500
* 10000

## **Câu hỏi 4: Phân tích thời lượng chuyến đi**

Chạy truy vấn SQL dưới đây để:

* Tính thời lượng chuyến đi trung bình theo phút.

```py
with pipeline.sql_client() as client:
    res = client.execute_sql(
            """
            SELECT
            AVG(date_diff('minute', trip_pickup_date_time, trip_dropoff_date_time))
            FROM rides;
            """
        )
    # Prints column values of the first row
    print(res)
```

Thời lượng chuyến đi trung bình là bao nhiêu?

* 12.3049
* 22.3049
* 32.3049
* 42.3049

## **Nộp bài**

* Biểu mẫu nộp bài: https://courses.datatalks.club/de-zoomcamp-2025/homework/workshop1

## **Lời giải**

Lời giải sẽ được đăng tại đây sau hạn nộp bài.
