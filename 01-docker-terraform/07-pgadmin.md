---
prev_url: 06-ingestion-script.md
next_url: 08-dockerizing-ingestion.md
---
#pgAdmin - Công cụ quản lý cơ sở dữ liệu

`pgcli` là một công cụ tiện dụng nhưng lại cồng kềnh khi sử dụng cho các truy vấn phức tạp và quản lý cơ sở dữ liệu. [`pgAdmin` là một công cụ dựa trên web](https://www.pgadmin.org/) giúp truy cập và quản lý cơ sở dữ liệu của chúng tôi thuận tiện hơn.

Có thể chạy pgAdmin dưới dạng vùng chứa cùng với vùng chứa Postgres, nhưng cả hai vùng chứa sẽ phải nằm trong cùng một _mạng ảo_ để chúng có thể tìm thấy nhau.


## Chạy pgAdmin Container

```bash
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -v pgadmin_data:/var/lib/pgadmin \
  -p 8085:80 \
  dpage/pgadmin4
```

Ánh xạ khối `-v pgadmin_data:/var/lib/pgadmin` lưu cài đặt pgAdmin (kết nối máy chủ, tùy chọn) để bạn không phải cấu hình lại nó mỗi khi khởi động lại vùng chứa.

### Giải thích các thông số

* Vùng chứa cần 2 biến môi trường: email đăng nhập và mật khẩu. Chúng tôi sử dụng `admin@admin.com` và `root` trong ví dụ này.
* pgAdmin là một ứng dụng web và cổng mặc định của nó là 80; chúng tôi ánh xạ nó tới 8085 trong máy chủ cục bộ của mình để tránh mọi xung đột có thể xảy ra.
* Tên hình ảnh thực tế là `dpage/pgadmin4`.

**Lưu ý:** Tính năng này vẫn chưa hoạt động vì pgAdmin không thể nhìn thấy vùng chứa PostgreSQL. Họ cần phải ở trên cùng một mạng Docker!

## Mạng Docker

Hãy tạo một mạng Docker ảo có tên `pg-network`:

```bash
docker network create pg-network
```

> Bạn có thể xóa mạng sau bằng lệnh `docker network rm pg-network`. Bạn có thể xem các mạng hiện có với `docker network ls`.

### Chạy các container trên cùng một mạng

Dừng cả hai vùng chứa và chạy lại chúng với cấu hình mạng:

```bash
# Run PostgreSQL on the network
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v ny_taxi_postgres_data:/var/lib/postgresql \
  -p 5432:5432 \
  --network=pg-network \
  --name pgdatabase \
  postgres:18

# In another terminal, run pgAdmin on the same network
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -v pgadmin_data:/var/lib/pgadmin \
  -p 8085:80 \
  --network=pg-network \
  --name pgadmin \
  dpage/pgadmin4
```

* Giống như vùng chứa Postgres, chúng tôi chỉ định mạng và tên cho pgAdmin.
* Tên vùng chứa (`pgdatabase` và `pgadmin`) cho phép các vùng chứa tìm thấy nhau trong mạng.

## Kết nối pgAdmin với PostgreSQL

Bây giờ bạn có thể tải pgAdmin trên trình duyệt web bằng cách duyệt tới `http://localhost:8085`. Sử dụng cùng email và mật khẩu bạn đã sử dụng để chạy vùng chứa để đăng nhập.

1. Mở trình duyệt và truy cập `http://localhost:8085`
2. Đăng nhập bằng email: `admin@admin.com`, mật khẩu: `root`
3. Nhấp chuột phải vào "Servers" → Register → Server
4. Cấu hình:
- **tab General**: Name: `Local Docker`
- **tab kết nối**:
- Máy chủ: `pgdatabase` (tên vùng chứa)
- Cổng: `5432`
- Tên người dùng: `root`
- Mật khẩu: `root`
5. Lưu

Bây giờ bạn có thể khám phá cơ sở dữ liệu bằng giao diện pgAdmin!
