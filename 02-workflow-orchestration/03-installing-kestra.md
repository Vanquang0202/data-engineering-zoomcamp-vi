---
video_url: https://www.youtube.com/watch?v=wgPxC4UjoLM
prev_url: 02-what-is-kestra.md
next_url: 04-kestra-concepts.md
---
# Cài đặt Kestra

Để cài đặt Kestra, chúng tôi sẽ sử dụng Docker Compose. Chúng tôi đã thiết lập cơ sở dữ liệu Postgres, cùng với pgAdmin từ Mô-đun 1. Chúng tôi có thể tiếp tục sử dụng những cơ sở dữ liệu này với Kestra nhưng chúng tôi sẽ cần thực hiện một số sửa đổi đối với tệp Docker Compose của mình.

Sử dụng [ví dụ này Docker Compose file](docker-compose.yml) để thêm chính xác 2 dịch vụ mới và thiết lập ổ đĩa chính xác.

Thêm thông tin về việc đặt tên người dùng và mật khẩu.

Chúng tôi sẽ thiết lập Kestra bằng Docker Compose chứa một vùng chứa cho máy chủ Kestra và một vùng chứa khác cho cơ sở dữ liệu Postgres:


```bash
cd 02-workflow-orchestration
docker compose up -d
```

**Lưu ý:** Kiểm tra để đảm bảo `pgAdmin` không chạy trên cùng cổng với Kestra. Nếu vậy, hãy xem [FAQ](#troubleshooting-tips) ở cuối README.

Sau khi container khởi động, bạn có thể truy cập giao diện Kestra tại [http://localhost:8080](http://localhost:8080).

Để tắt Kestra, hãy chuyển đến cùng thư mục và chạy lệnh sau:

```bash
docker compose down
```
## Thêm luồng vào Kestra
Có thể thêm luồng vào Kestra bằng cách sao chép và dán YAML trực tiếp vào trình chỉnh sửa hoặc bằng cách thêm qua API của Kestra. Xem bên dưới để thêm theo chương trình.

<details>
<summary>Thêm luồng vào Kestra theo lập trình</summary>

Nếu bạn muốn thêm các luồng theo chương trình bằng API của Kestra, hãy chạy các lệnh sau:

```bash
# Import all flows: assuming username admin@kestra.io and password Admin1234! (adjust to match your username and password)
curl -X POST -u 'admin@kestra.io:Admin1234!' http://localhost:8080/api/v1/flows/import -F fileUpload=@flows/01_hello_world.yaml
curl -X POST -u 'admin@kestra.io:Admin1234!' http://localhost:8080/api/v1/flows/import -F fileUpload=@flows/02_python.yaml
curl -X POST -u 'admin@kestra.io:Admin1234!' http://localhost:8080/api/v1/flows/import -F fileUpload=@flows/03_getting_started_data_pipeline.yaml
curl -X POST -u 'admin@kestra.io:Admin1234!' http://localhost:8080/api/v1/flows/import -F fileUpload=@flows/04_postgres_taxi.yaml
curl -X POST -u 'admin@kestra.io:Admin1234!' http://localhost:8080/api/v1/flows/import -F fileUpload=@flows/05_postgres_taxi_scheduled.yaml
curl -X POST -u 'admin@kestra.io:Admin1234!' http://localhost:8080/api/v1/flows/import -F fileUpload=@flows/06_gcp_kv.yaml
curl -X POST -u 'admin@kestra.io:Admin1234!' http://localhost:8080/api/v1/flows/import -F fileUpload=@flows/07_gcp_setup.yaml
curl -X POST -u 'admin@kestra.io:Admin1234!' http://localhost:8080/api/v1/flows/import -F fileUpload=@flows/08_gcp_taxi.yaml
curl -X POST -u 'admin@kestra.io:Admin1234!' http://localhost:8080/api/v1/flows/import -F fileUpload=@flows/09_gcp_taxi_scheduled.yaml
curl -X POST -u 'admin@kestra.io:Admin1234!' http://localhost:8080/api/v1/flows/import -F fileUpload=@flows/10_chat_without_rag.yaml
curl -X POST -u 'admin@kestra.io:Admin1234!' http://localhost:8080/api/v1/flows/import -F fileUpload=@flows/11_chat_with_rag.yaml
```
</details>

## Tài nguyên
- [Cài đặt Kestra với Docker Compose](https://go.kestra.io/de-zoomcamp/docker-compose)
