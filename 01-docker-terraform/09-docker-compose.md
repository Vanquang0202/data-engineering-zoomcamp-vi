---
prev_url: 08-dockerizing-ingestion.md
next_url: 10-sql-refresher.md
---
# Docker Soạn

`docker-compose` cho phép chúng tôi khởi chạy nhiều vùng chứa bằng một tệp cấu hình duy nhất, do đó chúng tôi không phải chạy riêng nhiều lệnh `docker run` phức tạp.


Docker soạn thảo sử dụng các tệp YAML. Đây là tệp `docker-compose.yaml`:

```yaml
services:
  pgdatabase:
    image: postgres:18
    environment:
      POSTGRES_USER: "root"
      POSTGRES_PASSWORD: "root"
      POSTGRES_DB: "ny_taxi"
    volumes:
      - "ny_taxi_postgres_data:/var/lib/postgresql"
    ports:
      - "5432:5432"

  pgadmin:
    image: dpage/pgadmin4
    environment:
      PGADMIN_DEFAULT_EMAIL: "admin@admin.com"
      PGADMIN_DEFAULT_PASSWORD: "root"
    volumes:
      - "pgadmin_data:/var/lib/pgadmin"
    ports:
      - "8085:80"

volumes:
  ny_taxi_postgres_data:
  pgadmin_data:
```

### Giải thích

* Chúng tôi không phải chỉ định mạng vì `docker compose` sẽ xử lý mạng đó: mọi vùng chứa (hoặc "dịch vụ", như trạng thái của tệp) sẽ chạy trong cùng một mạng và có thể tìm thấy nhau theo tên của chúng (`pgdatabase` và `pgadmin` trong ví dụ này).
* Tất cả các chi tiết khác từ lệnh `docker run` (biến môi trường, ổ đĩa và cổng) đều được đề cập tương ứng trong tệp theo cú pháp YAML.

## Khởi động dịch vụ với Docker Compose

Bây giờ chúng ta có thể chạy Docker soạn bằng cách chạy lệnh sau từ cùng thư mục nơi tìm thấy `docker-compose.yaml`. Đảm bảo rằng tất cả các vùng chứa trước đó không chạy nữa:

```bash
docker-compose up
```

### Chế độ tách rời

Nếu bạn muốn chạy lại các vùng chứa ở chế độ nền thay vì ở nền trước (do đó giải phóng thiết bị đầu cuối của bạn), bạn có thể chạy chúng ở chế độ tách rời:

```bash
docker-compose up -d
```

## Dừng dịch vụ

Bạn sẽ phải nhấn `Ctrl+C` để tắt các thùng chứa khi chạy ở chế độ nền trước. Cách tắt chúng thích hợp là bằng lệnh này:

```bash
docker-compose down
```

## Các lệnh hữu ích khác

```bash
# View logs
docker-compose logs

# Stop and remove volumes
docker-compose down -v
```

## Lợi ích của Docker Compose

- Lệnh duy nhất để khởi động tất cả các dịch vụ
- Tạo mạng tự động
- Quản lý cấu hình dễ dàng
- Cơ sở hạ tầng khai báo

## Chạy tập lệnh nhập bằng Docker Compose

Nếu muốn chạy lại tập lệnh nhập vào dockerized khi chạy Postgres và pgAdmin với `docker compose`, bạn sẽ phải tìm tên của mạng ảo mà Docker soạn đã tạo cho các vùng chứa.

```bash
# check the network link:
docker network ls

# it's pipeline_default (or similar based on directory name)
# now run the script:
docker run -it --rm\
  --network=pipeline_default \
  taxi_ingest:v001 \
    --pg-user=root \
    --pg-pass=root \
    --pg-host=pgdatabase \
    --pg-port=5432 \
    --pg-db=ny_taxi \
    --target-table=yellow_taxi_trips
```
