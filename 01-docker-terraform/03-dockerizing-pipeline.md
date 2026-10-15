---
prev_url: 02-virtual-environment.md
next_url: 04-postgres-docker.md
---
# Docker hóa đường ống

Bây giờ hãy chứa tập lệnh. Tạo tệp `Dockerfile` sau:


## Dockerfile đơn giản với pip

```dockerfile
# base Docker image that we will build on
FROM python:3.13.11-slim

# set up our image by installing prerequisites; pandas in this case
RUN pip install pandas pyarrow

# set up the working directory inside the container
WORKDIR /app
# copy the script to the container. 1st name is source file, 2nd is destination
COPY pipeline.py pipeline.py

# define what to do first when the container runs
# in this example, we will just run the script
ENTRYPOINT ["python", "pipeline.py"]
```

**Giải thích:**

- `FROM`: Base image (Python 3.13)
- `RUN`: Thực thi các lệnh trong quá trình build
- `WORKDIR`: Đặt thư mục làm việc
- `COPY`: Sao chép file vào image
- `ENTRYPOINT`: Lệnh mặc định để chạy

### Xây dựng và chạy

Hãy xây dựng hình ảnh:

```bash
docker build -t test:pandas .
```

* Tên hình ảnh sẽ là `test` và thẻ của nó sẽ là `pandas`. Nếu thẻ không được chỉ định, thẻ sẽ mặc định là `latest`.

Bây giờ chúng ta có thể chạy vùng chứa và chuyển một đối số cho nó để đường dẫn của chúng ta sẽ nhận được nó:

```bash
docker run -it test:pandas some_number
```

Bạn sẽ nhận được kết quả tương tự như khi bạn chạy tập lệnh quy trình.

> Lưu ý: các hướng dẫn này giả định rằng `pipeline.py` và `Dockerfile` nằm trong cùng một thư mục. Các lệnh Docker cũng phải được chạy từ cùng thư mục với các tệp này.

## Dockerfile với uv

Còn tia cực tím thì sao? Hãy sử dụng nó thay vì sử dụng pip:

```dockerfile
# Start with slim Python 3.13 image
FROM python:3.13.10-slim

# Copy uv binary from official uv image (multi-stage build pattern)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

# Set working directory
WORKDIR /app

# Add virtual environment to PATH so we can use installed packages
ENV PATH="/app/.venv/bin:$PATH"

# Copy dependency files first (better layer caching)
COPY "pyproject.toml" "uv.lock" ".python-version" ./
# Install dependencies from lock file (ensures reproducible builds)
RUN uv sync --locked

# Copy application code
COPY pipeline.py pipeline.py

# Set entry point
ENTRYPOINT ["uv", "run", "python", "pipeline.py"]
```
