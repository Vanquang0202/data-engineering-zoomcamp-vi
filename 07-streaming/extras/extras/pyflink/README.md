# Đào tạo Apache Flink
Đường ống truyền phát Apache Flink

## : đinh ghim: Bắt đầu

### :whale: Cài đặt

Để chạy repo này, các thành phần sau sẽ cần được cài đặt:

1. [Docker](https://docs.docker.com/get-docker/) (bắt buộc)
2. [Docker soạn](https://docs.docker.com/compose/install/#installation-scenarios) (bắt buộc)
3. Tạo (được khuyến nghị) -- xem bên dưới
- Trên hầu hết các bản phân phối Linux và macOS, `make` thường được cài đặt sẵn theo mặc định. Để kiểm tra xem `make` đã được cài đặt trên hệ thống của bạn chưa, bạn có thể chạy lệnh `make --version` trong terminal hoặc dấu nhắc lệnh. Nếu được cài đặt, nó sẽ hiển thị thông tin phiên bản.
- Nếu không, bạn có thể thử làm theo hướng dẫn bên dưới hoặc bạn chỉ cần sao chép+dán các lệnh từ `Makefile` vào thiết bị đầu cuối hoặc dấu nhắc lệnh và chạy thủ công.

        ```bash
        # On Ubuntu or Debian:
        sudo apt-get update
        sudo apt-get install build-essential

        # On CentOS or Fedora:
        sudo dnf install make

        # On macOS:
        xcode-select --install

        # On windows:
        choco install make # uses Chocolatey, https://chocolatey.org/install
        ```

### :máy tính: Thiết lập cục bộ

Đảm bảo bạn đang ở trong thư mục `pyflick`:

```bash
cd 07-streaming/pyflink
```

## :boom: Chạy đường ống

1. Xây dựng hình ảnh Docker và triển khai các dịch vụ trong tệp `docker-compose.yml`, bao gồm cơ sở dữ liệu PostgreSQL và cụm Flink. Điều này cũng sẽ (nên) tạo bảng chìm, `processed_events`, nơi Flink sẽ ghi các thông điệp Kafka vào.

    ```bash
    make up

    #// if you dont have make, you can run:
    # docker compose up --build --remove-orphans  -d
    ```

**:star: Hãy đợi Flink UI hoạt động tại [http://localhost:8081/](http://localhost:8081/) trước khi chuyển sang bước tiếp theo.** _Lưu ý: lần đầu build Docker image có thể mất 5 đến 30 phút. Những lần build sau chỉ mất vài giây nếu bạn chưa xóa image._

:information_source: Sau khi image được xây dựng, Docker sẽ tự động khởi động dịch vụ quản lý công việc và quản lý tác vụ. Việc này sẽ mất một phút hoặc lâu hơn. Kiểm tra nhật ký vùng chứa trong máy tính để bàn Docker và khi bạn nhìn thấy dòng bên dưới, bạn biết rằng mình đã sẵn sàng chuyển sang bước tiếp theo.

    ```
    taskmanager Successful registration at resource manager akka.tcp://flink@jobmanager:6123/user/rpc/resourcemanager_* under registration id <id_number>
    ```

2. Bây giờ cụm Flink đã hoạt động, cuối cùng đã đến lúc chạy công việc PyFlink! :cười:

    ```bash
    make job

    #// if you dont have make, you can run:
    # docker-compose exec jobmanager ./bin/flink run -py /opt/job/start_job.py -d
    ```

Sau khoảng một phút, bạn sẽ thấy lời nhắc cho biết công việc đã được gửi (ví dụ: `Job has been submitted with JobID <job_id_number>`). Bây giờ hãy quay lại [Flink UI](http://localhost:8081/#/job/running) để xem công việc đang chạy! :tada:


3. Khi hoàn tất, bạn có thể dừng và/hoặc dọn sạch tài nguyên Docker bằng cách chạy các lệnh bên dưới.

    ```bash
    make stop # to stop running services in docker compose
    make down # to stop and remove docker compose services
    make clean # to remove the docker container and dangling images
    ```

:grey_exclaim: Lưu ý thư mục `/var/lib/postgresql/data` bên trong vùng chứa PostgreSQL được gắn vào thư mục `./postgres-data` trên máy cục bộ của bạn. Điều này có nghĩa là dữ liệu sẽ vẫn tồn tại sau khi khởi động lại hoặc xóa vùng chứa, vì vậy ngay cả khi bạn dừng/xóa vùng chứa, bạn sẽ không mất bất kỳ dữ liệu nào được ghi trong vùng chứa.

------

:information_source: Để xem tất cả các lệnh make có sẵn và chức năng của chúng, hãy chạy:

```bash
make help
```

Tính đến thời điểm viết bài này, các lệnh có sẵn là:

```bash

Usage:
  make <target>

Targets:
  help                 Show help with `make help`
  db-init              Builds and runs the PostgreSQL database service
  build                Builds the Flink base image with pyFlink and connectors installed
  up                   Builds the base Docker image and starts Flink cluster
  down                 Shuts down the Flink cluster
  job                  Submit the Flink job
  stop                 Stops all services in Docker compose
  start                Starts all services in Docker compose
  clean                Stops and removes the Docker container as well as images with tag `<none>`
  psql                 Runs psql to query containerized postgreSQL database in CLI
  postgres-die-mac     Removes mounted postgres data dir on local machine (mac users) and in Docker
  postgres-die-pc      Removes mounted postgres data dir on local machine (PC users) and in Docker
```
