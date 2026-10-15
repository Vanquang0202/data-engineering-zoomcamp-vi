---
prev_url: 04-postgres-docker.md
next_url: 06-ingestion-script.md
---
# Bộ dữ liệu taxi NY và nhập dữ liệu

Bây giờ chúng tôi sẽ tạo tệp Jupyter Notebook `notebook.ipynb` mà chúng tôi sẽ sử dụng để đọc tệp CSV và xuất tệp đó sang Postgres.


## Thiết lập Jupyter

Cài đặt Jupyter:

```bash
uv add --dev jupyter
```

Hãy tạo sổ ghi chép Jupyter để khám phá dữ liệu:

```bash
uv run jupyter notebook
```

## Bộ dữ liệu taxi NYC

Chúng ta sẽ sử dụng dữ liệu từ [trang dữ liệu chuyến đi của NYC TLC](https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page).

Cụ thể, chúng tôi sẽ sử dụng [Tệp CSV hồ sơ chuyến đi taxi màu vàng cho tháng 1 năm 2021](https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz).

Dữ liệu này trước đây là csv, nhưng sau đó họ chuyển sang parquet. Chúng tôi muốn tiếp tục sử dụng CSV vì chúng tôi cần thực hiện thêm một chút quá trình xử lý trước (với mục đích tìm hiểu về nó).

Từ điển để hiểu từng trường có sẵn [tại đây](https://www1.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf).

> Lưu ý: Dữ liệu CSV được lưu trữ dưới dạng tệp được nén. Gấu trúc có thể đọc chúng trực tiếp.

## Khám phá dữ liệu

Tạo một sổ ghi chép mới và chạy:

```python
import pandas as pd

# Read a sample of the data
prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
df = pd.read_csv(prefix + 'yellow_tripdata_2021-01.csv.gz', nrows=100)

# Display first rows
df.head()

# Check data types
df.dtypes

# Check data shape
df.shape
```
### Lưu ý
- Khi sử dụng `nrows=100` để lấy mẫu 100 hàng đầu tiên, tất cả các cột đều có kiểu dữ liệu nhất quán trong tập hợp con này, vì vậy **`DtypeWarning` bên dưới sẽ KHÔNG xuất hiện**.
- Để tái tạo cảnh báo loại hiển thị bên dưới, hãy xóa tham số `nrows=100` và đọc toàn bộ tập dữ liệu.

### Xử lý kiểu dữ liệu

Chúng tôi có một cảnh báo: (Lưu ý rằng cảnh báo này có thể xuất hiện sau này đối với một số người dùng, vì vậy tốt nhất bạn nên làm theo hướng dẫn bên dưới)

```
/tmp/ipykernel_25483/2933316018.py:1: DtypeWarning: Columns (6) have mixed types. Specify dtype option on import or set low_memory=False.
```

Vì vậy chúng ta cần chỉ định các loại:

```python
dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]

df = pd.read_csv(
    prefix + 'yellow_tripdata_2021-01.csv.gz',
    nrows=100,
    dtype=dtype,
    parse_dates=parse_dates
)
```

## Nhập dữ liệu vào Postgres

Trong sổ ghi chép Jupyter, chúng tôi tạo mã thành:

1. Tải xuống tệp CSV
2. Đọc nó theo từng đoạn với gấu trúc
3. Chuyển đổi các cột ngày giờ
4. Chèn dữ liệu vào PostgreSQL bằng SQLAlchemy

### Cài đặt SQLAlchemy

```bash
uv add sqlalchemy "psycopg[binary,pool]"
```

### Tạo kết nối cơ sở dữ liệu

```python
from sqlalchemy import create_engine
engine = create_engine('postgresql+psycopg://root:root@localhost:5432/ny_taxi')
```

### Nhận lược đồ DDL

```python
print(pd.io.sql.get_schema(df, name='yellow_taxi_data', con=engine))
```

Đầu ra:

```sql
CREATE TABLE yellow_taxi_data (
    "VendorID" BIGINT,
    tpep_pickup_datetime TIMESTAMP WITHOUT TIME ZONE,
    tpep_dropoff_datetime TIMESTAMP WITHOUT TIME ZONE,
    passenger_count BIGINT,
    trip_distance FLOAT(53),
    "RatecodeID" BIGINT,
    store_and_fwd_flag TEXT,
    "PULocationID" BIGINT,
    "DOLocationID" BIGINT,
    payment_type BIGINT,
    fare_amount FLOAT(53),
    extra FLOAT(53),
    mta_tax FLOAT(53),
    tip_amount FLOAT(53),
    tolls_amount FLOAT(53),
    improvement_surcharge FLOAT(53),
    total_amount FLOAT(53),
    congestion_surcharge FLOAT(53)
)
```

### Tạo bảng

```python
df.head(n=0).to_sql(name='yellow_taxi_data', con=engine, if_exists='replace')
```

`head(n=0)` đảm bảo chúng ta chỉ tạo bảng, chưa thêm bất kỳ dữ liệu nào.

## Nhập dữ liệu theo khối

Chúng tôi không muốn chèn tất cả dữ liệu cùng một lúc. Hãy thực hiện theo đợt và sử dụng trình vòng lặp cho việc đó:

```python
df_iter = pd.read_csv(
    prefix + 'yellow_tripdata_2021-01.csv.gz',
    dtype=dtype,
    parse_dates=parse_dates,
    iterator=True,
    chunksize=100000
)
```

### Lặp lại các đoạn

```python
for df_chunk in df_iter:
    print(len(df_chunk))
```

### Chèn dữ liệu

```python
df_chunk.to_sql(name='yellow_taxi_data', con=engine, if_exists='append')
```

### Hoàn thành vòng nhập

```python
first = True

for df_chunk in df_iter:

    if first:
        # Create table schema (no data)
        df_chunk.head(0).to_sql(
            name="yellow_taxi_data",
            con=engine,
            if_exists="replace"
        )
        first = False
        print("Table created")

    # Insert chunk
    df_chunk.to_sql(
        name="yellow_taxi_data",
        con=engine,
        if_exists="append"
    )

    print("Inserted:", len(df_chunk))
```

### Phương pháp thay thế (Không có cờ đầu tiên)

```python
first_chunk = next(df_iter)

first_chunk.head(0).to_sql(
    name="yellow_taxi_data",
    con=engine,
    if_exists="replace"
)

print("Table created")

first_chunk.to_sql(
    name="yellow_taxi_data",
    con=engine,
    if_exists="append"
)

print("Inserted first chunk:", len(first_chunk))

for df_chunk in df_iter:
    df_chunk.to_sql(
        name="yellow_taxi_data",
        con=engine,
        if_exists="append"
    )
    print("Inserted chunk:", len(df_chunk))
```

## Thêm thanh tiến trình

Thêm `tqdm` để xem tiến độ:

```bash
uv add tqdm
```

Đặt nó xung quanh iterable:

```python
from tqdm.auto import tqdm

for df_chunk in tqdm(df_iter):
    ...
```
Để xem tiến trình về tổng số khối, bạn sẽ phải thêm đối số `total` vào `tqdm(df_iter)`. Trong kịch bản của chúng tôi, cách thực dụng là
để mã hóa cứng một giá trị dựa trên số lượng mục trong bảng.

## Xác minh dữ liệu

Kết nối với nó bằng pgcli:

```bash
uv run pgcli -h localhost -p 5432 -u root -d ny_taxi
```

Và khám phá dữ liệu.
