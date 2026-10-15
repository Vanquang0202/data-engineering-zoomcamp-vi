---
prev_url: 06-why-flink.md
next_url: 08-the-pass-through-flink-job.md
---
# Hình ảnh và dịch vụ Flink

Flink không hỗ trợ Python ngay lập tức. Chúng tôi cần hình ảnh Docker
tùy chỉnh với Python, PyFlink và JAR trình kết nối.


*Hình ảnh đóng gói các phần phụ thuộc của hội thảo; tọa độ Trình quản lý công việc hoạt động trong khi các khe Trình quản lý tác vụ thực thi nó song song.*

Tải xuống tệp bản dựng Flink:

```bash
PREFIX="https://raw.githubusercontent.com/DataTalksClub/data-engineering-zoomcamp/main/07-streaming/workshop"

wget ${PREFIX}/Dockerfile.flink
wget ${PREFIX}/pyproject.flink.toml
wget ${PREFIX}/flink-config.yaml
```

> Nếu bạn sao chép kho lưu trữ, các tệp này đã có trong thư mục
> `cohorts/2027/07-streaming/code/`.

Bạn có thể xem
[`Dockerfile.flink`](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/cohorts/2027/07-streaming/code/Dockerfile.flink)
để biết chức năng của nó:

- Bắt đầu từ hình ảnh Flink chính thức (`flink:2.2.0-scala_2.12-java17`)
- Cài đặt Python 3.12 và PyFlink qua uv
- Tải xuống các JAR trình kết nối (Kafka, JDBC, PostgreSQL)
- Áp dụng cấu hình Flink tùy chỉnh để tăng siêu không gian JVM cho PyFlink

Bây giờ hãy thêm dịch vụ Flink vào `docker-compose.yml`. Cụm Flink có
hai loại quy trình - hãy thêm từng loại quy trình một.

JobManager là người điều phối. Nó tiếp nhận công việc, quản lý các điểm kiểm tra,
và phân công công việc cho người quản lý tác vụ. Bạn tương tác với nó thông qua giao diện người dùng web
(cổng `8081`) và gửi công việc qua cổng RPC của nó (`6123`):

```yaml
  jobmanager:
    build:
      context: .
      dockerfile: ./Dockerfile.flink
    image: pyflink-workshop
    pull_policy: never
    expose:
      - "6123"
    ports:
      - "8081:8081"
    volumes:
      - ./:/opt/flink/usrlib
      - ./src/:/opt/src
    command: jobmanager
    environment:
      - |
        FLINK_PROPERTIES=
        jobmanager.rpc.address: jobmanager
        jobmanager.memory.process.size: 1600m
```

- `build` + `image: pyflink-workshop` - xây dựng hình ảnh Docker tùy chỉnh của chúng tôi và
gắn thẻ nó là `pyflink-workshop`. Trình quản lý tác vụ sẽ sử dụng lại hình ảnh
này mà không cần xây dựng lại.
- `pull_policy: never` - đừng cố kéo `pyflink-workshop` từ Docker Hub
(nó không tồn tại ở đó - chúng tôi đã xây dựng nó cục bộ).
- `volumes` - gắn mã nguồn vào thùng chứa để chúng tôi có thể gửi công việc
mà không cần xây dựng lại hình ảnh.
- `FLINK_PROPERTIES` - Cấu hình Flink được chuyển dưới dạng biến môi trường.
`jobmanager.rpc.address: jobmanager` cho Flink biết nơi điều phối viên
sống (`jobmanager` là tên dịch vụ Docker).

Trình quản lý tác vụ là công nhân. Nó thực hiện xử lý dữ liệu thực tế:

```yaml
  taskmanager:
    image: pyflink-workshop
    pull_policy: never
    expose:
      - "6121"
      - "6122"
    volumes:
      - ./:/opt/flink/usrlib
      - ./src/:/opt/src
    depends_on:
      - jobmanager
    command: taskmanager --taskmanager.registration.timeout 5 min
    environment:
      - |
        FLINK_PROPERTIES=
        jobmanager.rpc.address: jobmanager
        taskmanager.memory.process.size: 1728m
        taskmanager.numberOfTaskSlots: 15
        parallelism.default: 3
```

- `image: pyflink-workshop` - sử dụng lại hình ảnh được xây dựng bởi dịch vụ
của trình quản lý công việc, không cần `build`.
- `depends_on: jobmanager` - bắt đầu sau trình quản lý công việc.
- `--taskmanager.registration.timeout 5 min` - cho trình quản lý tác vụ
5 phút để tìm trình quản lý công việc khi khởi động (hữu ích khi các dịch vụ khởi động
song song).
- `taskmanager.numberOfTaskSlots: 15` - trình quản lý tác vụ này có 15 vị trí.
- `parallelism.default: 3` - theo mặc định, mỗi giai đoạn đường ống chạy 3 bản
xử lý dữ liệu song song.

Khe tác vụ là một đơn vị tài nguyên (bộ nhớ, CPU) có thể chạy một phiên bản
song song của giai đoạn đường ống. Hãy nghĩ về các khe giống như làn đường trên đường cao tốc - nhiều làn
hơn nghĩa là nhiều dữ liệu có thể lưu chuyển cùng một lúc. Nếu bạn gửi một công việc với
song song 3, công việc đó sẽ sử dụng 3 vị trí. Với 15 vị trí có sẵn, bạn có thể chạy đồng thời
5 công việc như vậy trên trình quản lý tác vụ duy nhất này. Trong quá trình sản xuất,
có nhiều trình quản lý tác vụ trên các máy khác nhau, mỗi máy đóng góp các vị trí
cho cụm. Người quản lý công việc quyết định vị trí nào chạy phần nào
trong số đó công việc nào.

Đảm bảo `src/` tồn tại trước khi khởi động Docker - ổ đĩa
`./src/:/opt/src` sẽ tạo nó dưới dạng root nếu nó không tồn tại, gây ra sự cố về quyền
sau này khi bạn cố gắng tạo tệp bên trong nó:

```bash
mkdir -p src/job
```

Xây dựng hình ảnh Flink và bắt đầu tất cả các dịch vụ:

```bash
docker compose up --build -d
```

Quá trình xây dựng đầu tiên mất vài phút - nó cài đặt Python, PyFlink và tải xuống
các JAR trình kết nối.

Xác minh tất cả bốn dịch vụ đang chạy:

```bash
docker compose ps
```

```
NAME                  IMAGE                           SERVICE        STATUS
workshop-jobmanager   pyflink-workshop                jobmanager     Up
workshop-taskmanager  pyflink-workshop                taskmanager    Up
workshop-postgres     postgres:18                     postgres       Up
workshop-redpanda     redpandadata/redpanda:v25.3.9   redpanda       Up
```

Kiểm tra bảng điều khiển Flink tại [http://localhost:8081](http://localhost:8081) -
bạn sẽ thấy 1 trình quản lý tác vụ với 15 ô tác vụ có sẵn.
