---
prev_url: 03-dockerizing-pipeline.md
next_url: 05-data-ingestion.md
---
# Chạy PostgreSQL với Docker

Bây giờ chúng tôi muốn thực hiện kỹ thuật dữ liệu thực sự. Hãy sử dụng cơ sở dữ liệu Postgres cho việc đó.

Bạn có thể chạy phiên bản Postgres được đóng gói mà không yêu cầu bất kỳ bước cài đặt nào. Bạn chỉ cần cung cấp một vài _biến môi trường_ cho nó cũng như _volume_ để lưu trữ dữ liệu.


## Chạy PostgreSQL trong Vùng chứa

Tạo một thư mục ở bất cứ đâu bạn muốn để Postgres lưu trữ dữ liệu. Chúng tôi sẽ sử dụng thư mục mẫu `ny_taxi_postgres_data`. Đây là cách chạy container:

```bash
docker run -it --rm \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v ny_taxi_postgres_data:/var/lib/postgresql \
  -p 5432:5432 \
  postgres:18
```

### Giải thích thông số

* `-e` đặt các biến môi trường (người dùng, mật khẩu, tên cơ sở dữ liệu)
* `-v ny_taxi_postgres_data:/var/lib/postgresql` tạo một **khối lượng được đặt tên**
* Docker tự động quản lý ổ đĩa này
* Dữ liệu vẫn tồn tại ngay cả sau khi xóa vùng chứa
* Ổ đĩa được lưu trữ trong bộ nhớ trong của Docker
* `-p 5432:5432` ánh xạ cổng 5432 từ vùng chứa đến máy chủ
* `postgres:18` sử dụng PostgreSQL phiên bản 18 (mới nhất tính đến tháng 12 năm 2025)

### Phương pháp thay thế - Gắn kết

Đầu tiên tạo thư mục, sau đó ánh xạ nó:

```bash
mkdir ny_taxi_postgres_data

docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql \
  -p 5432:5432 \
  postgres:18
```

### Ổ đĩa được đặt tên so với Bind Mount

* **Khối lượng được đặt tên** (`name:/path`): Được quản lý bởi Docker,
dễ dàng hơn * **Liên kết gắn kết** (`/host/path:/container/path`): Ánh xạ trực tiếp tới hệ thống tệp máy chủ, kiểm soát nhiều hơn

## Đang kết nối với PostgreSQL

Khi vùng chứa đang chạy, chúng tôi có thể đăng nhập vào cơ sở dữ liệu của mình bằng [pgcli](https://www.pgcli.com/).

Cài đặt pgcli:

```bash
uv add --dev pgcli
```

Cờ `--dev` đánh dấu đây là phần phụ thuộc phát triển (không cần thiết trong sản xuất). Nó sẽ được thêm vào phần `[dependency-groups]` của `pyproject.toml` thay vì phần `dependencies` chính.

Bây giờ hãy sử dụng nó để kết nối với Postgres:

```bash
uv run pgcli -h localhost -p 5432 -u root -d ny_taxi
```

* `uv run` thực thi lệnh trong bối cảnh môi trường ảo
* `-h` là máy chủ. Vì chúng tôi đang chạy cục bộ nên chúng tôi có thể sử dụng `localhost`.
* `-p` là cổng.
* `-u` là tên người dùng.
* `-d` là tên cơ sở dữ liệu.
* Mật khẩu không được cung cấp; nó sẽ được yêu cầu sau khi chạy lệnh.

Khi được nhắc, hãy nhập mật khẩu: `root`

## Các lệnh SQL cơ bản

Hãy thử một số lệnh SQL:

```sql
-- List tables
\dt

-- Create a test table
CREATE TABLE test (id INTEGER, name VARCHAR(50));

-- Insert data
INSERT INTO test VALUES (1, 'Hello Docker');

-- Query data
SELECT * FROM test;

-- Exit
\q
```
