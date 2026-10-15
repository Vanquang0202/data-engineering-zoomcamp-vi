---
prev_url: 05-data-ingestion.md
next_url: 07-pgadmin.md
---
# Tạo tập lệnh nhập dữ liệu

Bây giờ hãy chuyển đổi sổ ghi chép thành tập lệnh Python.


## Chuyển Notebook thành Script

```bash
uv run jupyter nbconvert --to=script notebook.ipynb
mv notebook.py ingest_data.py
```

## Tập lệnh nhập hoàn chỉnh

Xem thư mục `pipeline/` để biết tập lệnh hoàn chỉnh có tích hợp nhấp chuột. Đây là cấu trúc cốt lõi:

```python
import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm

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
```

## Nhấp vào Tích hợp

Tập lệnh sử dụng `click` để phân tích đối số dòng lệnh:

```python
import click

@click.command()
@click.option('--pg-user', default='root', help='PostgreSQL user')
@click.option('--pg-pass', default='root', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default=5432, type=int, help='PostgreSQL port')
@click.option('--pg-db', default='ny_taxi', help='PostgreSQL database name')
@click.option('--target-table', default='yellow_taxi_data', help='Target table name')
def run(pg_user, pg_pass, pg_host, pg_port, pg_db, target_table):
    # Ingestion logic here
    pass
```

## Chạy tập lệnh

Tập lệnh đọc dữ liệu theo khối (100.000 hàng cùng lúc) để xử lý các tệp lớn một cách hiệu quả mà không hết bộ nhớ.

Ví dụ sử dụng:

```bash
uv run python ingest_data.py \
  --pg-user=root \
  --pg-pass=root \
  --pg-host=localhost \
  --pg-port=5432 \
  --pg-db=ny_taxi \
  --target-table=yellow_taxi_trips
```
