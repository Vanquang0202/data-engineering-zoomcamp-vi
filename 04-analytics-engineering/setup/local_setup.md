# Hướng dẫn cài đặt cục bộ

Hướng dẫn này hướng dẫn bạn cách thiết lập môi trường kỹ thuật phân tích cục bộ bằng DuckDB và dbt.

<div align="center">

[![dbt Core](https://img.shields.io/badge/dbt-FF694B?style=for-the-badge&logo=dbt&logoColor=white)](https://www.getdbt.com/)
[![DuckDB](https://img.shields.io/badge/DuckDB-FFF000?style=for-the-badge&logo=duckdb&logoColor=black)](https://duckdb.org/)

</div>

>[!NOTE]
>*Hướng dẫn này sẽ giải thích cách thiết lập thủ công. Nếu bạn muốn thử thách thêm, hãy thử chạy thiết lập này bằng Docker Compose hoặc môi trường ảo Python.*

**Quan trọng**: Tất cả các lệnh dbt phải được chạy từ bên trong thư mục `taxi_rides_ny/`. Các bước thiết lập bên dưới sẽ hướng dẫn bạn:

1. Cài đặt các công cụ cần thiết
2. Định cấu hình kết nối của bạn với DuckDB
3. Đang tải dữ liệu taxi NYC
4. Xác minh mọi thứ đều hoạt động

## Bước 1: Cài đặt DuckDB

DuckDB là cơ sở dữ liệu SQL nhanh, phù hợp với các tác vụ phân tích cục bộ. Để cài đặt DuckDB, hãy làm theo hướng dẫn trên [trang web chính thức](https://duckdb.org/docs/installation) cho hệ điều hành của bạn.

> [!TIP]
> *Bạn có thể cài đặt DuckDB theo hai cách. Bạn có thể cài đặt CLI hoặc cài đặt API máy khách cho ngôn ngữ lập trình yêu thích của mình (trong trường hợp Python, bạn có thể sử dụng `pip install duckdb`). Cá nhân tôi thích cài đặt CLI hơn, nhưng cách nào cũng được.*

## Bước 2: Cài đặt dbt

```bash
pip install dbt-duckdb
```

Cài đặt này:

* `dbt-core`: Khung dbt cốt lõi
* `dbt-duckdb`: Bộ điều hợp DuckDB cho dbt

## Bước 3: Cấu hình Profile dbt

Vì kho lưu trữ này đã chứa dự án dbt (`taxi_rides_ny/`), nên bạn không cần chạy `dbt init`. Thay vào đó, bạn cần định cấu hình hồ sơ dbt của mình để kết nối với DuckDB.

### Tạo hoặc cập nhật `~/.dbt/profiles.yml`

Cấu hình dbt cho dbt biết cách kết nối với cơ sở dữ liệu của bạn. Tạo hoặc cập nhật file `~/.dbt/profiles.yml` với nội dung sau:

```yaml
taxi_rides_ny:
  target: dev
  outputs:
    # DuckDB Development profile
    dev:
      type: duckdb
      path: taxi_rides_ny.duckdb
      schema: dev
      threads: 1
      extensions:
        - parquet
      settings:
        memory_limit: '2GB'
        preserve_insertion_order: false

    # DuckDB Production profile
    prod:
      type: duckdb
      path: taxi_rides_ny.duckdb
      schema: prod
      threads: 1
      extensions:
        - parquet
      settings:
        memory_limit: '2GB'
        preserve_insertion_order: false

# Troubleshooting:
# - If you have less than 4GB RAM, try setting memory_limit to '1GB'
# - If you have 16GB+ RAM, you can increase to '4GB' for faster builds
# - Expected build time: 5-10 minutes on most systems
```

## Bước 4: Tải xuống và nhập dữ liệu

Bây giờ hồ sơ dbt của bạn đã được định cấu hình, hãy tải dữ liệu taxi vào DuckDB. Điều hướng đến thư mục dự án dbt và chạy tập lệnh nhập

```python
import duckdb
import requests
from pathlib import Path

BASE_URL = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download"

def download_and_convert_files(taxi_type):
    data_dir = Path("data") / taxi_type
    data_dir.mkdir(exist_ok=True, parents=True)

    for year in [2019, 2020]:
        for month in range(1, 13):
            parquet_filename = f"{taxi_type}_tripdata_{year}-{month:02d}.parquet"
            parquet_filepath = data_dir / parquet_filename

            if parquet_filepath.exists():
                print(f"Skipping {parquet_filename} (already exists)")
                continue

            # Download CSV.gz file
            csv_gz_filename = f"{taxi_type}_tripdata_{year}-{month:02d}.csv.gz"
            csv_gz_filepath = data_dir / csv_gz_filename

            response = requests.get(f"{BASE_URL}/{taxi_type}/{csv_gz_filename}", stream=True)
            response.raise_for_status()

            with open(csv_gz_filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            print(f"Converting {csv_gz_filename} to Parquet...")
            con = duckdb.connect()
            con.execute(f"""
                COPY (SELECT * FROM read_csv_auto('{csv_gz_filepath}'))
                TO '{parquet_filepath}' (FORMAT PARQUET)
            """)
            con.close()

            # Remove the CSV.gz file to save space
            csv_gz_filepath.unlink()
            print(f"Completed {parquet_filename}")

def update_gitignore():
    gitignore_path = Path(".gitignore")

    # Read existing content or start with empty string
    content = gitignore_path.read_text() if gitignore_path.exists() else ""

    # Add data/ if not already present
    if 'data/' not in content:
        with open(gitignore_path, 'a') as f:
            f.write('\n# Data directory\ndata/\n' if content else '# Data directory\ndata/\n')

if __name__ == "__main__":
    # Update .gitignore to exclude data directory
    update_gitignore()

    for taxi_type in ["yellow", "green"]:
        download_and_convert_files(taxi_type)

    con = duckdb.connect("taxi_rides_ny.duckdb")
    con.execute("CREATE SCHEMA IF NOT EXISTS prod")

    for taxi_type in ["yellow", "green"]:
        con.execute(f"""
            CREATE OR REPLACE TABLE prod.{taxi_type}_tripdata AS
            SELECT * FROM read_parquet('data/{taxi_type}/*.parquet', union_by_name=true)
        """)

    con.close()
```

Tập lệnh này tải xuống dữ liệu taxi màu vàng và xanh lục từ năm 2019-2020, tạo lược đồ `prod` và tải dữ liệu thô vào DuckDB. Quá trình tải xuống có thể mất vài phút tùy thuộc vào kết nối internet của bạn.

## Bước 5: Test kết nối dbt

Xác minh dbt có thể kết nối với cơ sở dữ liệu DuckDB của bạn:

```bash
dbt debug
```

## Bước 6: Cài đặt dbt Power User Extension (VS Code Users)

Nếu bạn đang sử dụng Visual Studio Code, hãy cài đặt tiện ích mở rộng **dbt Power User** để nâng cao trải nghiệm phát triển dbt của bạn.

### Người dùng dbt Power là gì?

dbt Power User là tiện ích mở rộng Mã VS cung cấp:

* Làm nổi bật và định dạng cú pháp SQL cho các mô hình dbt
* Trực quan hóa dòng cấp độ cột nội tuyến
* Tự động hoàn thành cho các mô hình, nguồn và macro dbt
* Xem trước tài liệu tương tác
* Biên dịch và thực thi mô hình trực tiếp từ trình chỉnh sửa

### Tại sao không sử dụng tiện ích mở rộng dbt chính thức?

dbt Labs đã phát hành tiện ích mở rộng VS Code chính thức có tên [dbt Extension](https://marketplace.visualstudio.com/items?itemName=dbtLabsInc.dbt) được hỗ trợ bởi công cụ dbt Fusion mới. Tuy nhiên, tiện ích mở rộng này **yêu cầu dbt Fusion** và không hỗ trợ dbt Core.

Vì chúng tôi đang sử dụng **dbt Core** với DuckDB để phát triển cục bộ nên thay vào đó, chúng tôi cần tiện ích mở rộng **dbt Power User by AltimateAI** do cộng đồng duy trì. Tiện ích mở rộng này:

* Hoạt động trơn tru với dbt Core (không chỉ dbt Cloud)
* Hỗ trợ tất cả các bộ điều hợp dbt, bao gồm DuckDB
* Được duy trì tích cực và mã nguồn mở
* Cung cấp bộ tính năng phong phú để phát triển cục bộ

### Cài đặt

1. Mở Mã VS
2. Đi tới Tiện ích mở rộng (Ctrl+Shift+X / Cmd+Shift+X)
3. Tìm kiếm "dbt Power User"
4. Cài đặt **dbt Power User của AltimateAI** (không phải phiên bản dbt Labs)

Ngoài ra, hãy cài đặt nó từ [VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=innoverio.vscode-dbt-power-user).

> [!NOTE]
> Tại thời điểm này, môi trường dbt cục bộ của bạn đã được cấu hình đầy đủ và sẵn sàng để sử dụng. Các bước tiếp theo (chạy mô hình, kiểm tra và xây dựng tài liệu) sẽ được đề cập trong các video hướng dẫn.

## Tài nguyên bổ sung

* [Tài liệu DuckDB](https://duckdb.org/docs/)
* [Tài liệu dbt](https://docs.getdbt.com/)
* [Bộ chuyển đổi dbt-duckdb](https://github.com/duckdb/dbt-duckdb)
* [Từ điển dữ liệu taxi NYC](https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf)
