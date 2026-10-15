---
prev_url: 07-pgadmin.md
next_url: 09-docker-compose.md
---
# Docker hóa tập lệnh nhập

Bây giờ, hãy chứa tập lệnh nhập để có thể chạy tập lệnh đó trong Docker.


## Tệp Docker

`pipeline/Dockerfile` cho biết cách chứa tập lệnh nhập:

```dockerfile
FROM python:3.13.11-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

WORKDIR /code
ENV PATH="/code/.venv/bin:$PATH"

COPY pyproject.toml .python-version uv.lock ./
RUN uv sync --locked

COPY ingest_data.py .

ENTRYPOINT ["uv", "run", "python", "ingest_data.py"]
```

### Giải thích

- `FROM python:3.13.11-slim`: Bắt đầu với slim Python 3.13 image cho kích thước nhỏ hơn
- `COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/`: Sao chép nhị phân uv từ image uv chính thức
- `WORKDIR /code`: Đặt thư mục làm việc bên trong container
- `ENV PATH="/code/.venv/bin:$PATH"`: Thêm môi trường ảo vào PATH
- `COPY pyproject.toml .python-version uv.lock ./`: Sao chép các tệp phụ thuộc trước (bộ nhớ đệm tốt hơn)
- `RUN uv sync --locked`: Cài đặt tất cả các phần phụ thuộc từ tệp khóa (đảm bảo các bản dựng có thể tái tạo)
- `COPY ingest_data.py .`: Sao chép tập lệnh truyền
- `ENTRYPOINT ["uv", "run", "python", "ingest_data.py"]`: Đặt điểm vào để chạy tập lệnh nhập

## Xây dựng hình ảnh Docker

```bash
cd pipeline
docker build -t taxi_ingest:v001 .
```

## Chạy quá trình nhập vào trong vùng chứa

```bash
docker run -it \
  --network=pg-network \
  taxi_ingest:v001 \
    --pg-user=root \
    --pg-pass=root \
    --pg-host=pgdatabase \
    --pg-port=5432 \
    --pg-db=ny_taxi \
    --target-table=yellow_taxi_trips
```

### Lưu ý quan trọng

* Chúng ta cần cung cấp network cho Docker để tìm Postgres container. Nó đi trước tên của hình ảnh.
* Vì Postgres đang chạy trên một vùng chứa riêng nên đối số máy chủ sẽ phải trỏ đến tên vùng chứa của Postgres (`pgdatabase`).
* Bạn có thể thả bảng vào pgAdmin trước nếu muốn, nhưng tập lệnh sẽ tự động thay thế bảng có sẵn.
