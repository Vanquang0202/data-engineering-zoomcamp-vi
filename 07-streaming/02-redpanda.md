---
prev_url: 01-introduction.md
next_url: 03-produce-messages-to-kafka.md
---
# Redpanda - nhà môi giới tương thích Kafka

Trước khi có thể tạo hoặc tiêu thụ tin nhắn, chúng tôi cần một nhà môi giới tin nhắn -
, một dịch vụ nhận tin nhắn từ nhà sản xuất, lưu trữ và gửi
đến người tiêu dùng.

Chúng tôi sử dụng [Redpanda](https://redpanda.com/), một giải pháp thay thế sẵn có cho
Apache Kafka. Redpanda triển khai cùng một giao thức, do đó, mọi thư viện
của máy khách Kafka đều hoạt động với nó không thay đổi. Thư viện `kafka-python` mà chúng tôi sẽ sử dụng
không biết hoặc quan tâm rằng Redpanda đang chạy thay vì Kafka.

Tại sao Redpanda thay vì Kafka?

- Không có JVM - Kafka chạy trên Java và cần bộ nhớ đáng kể cho JVM.
Redpanda được viết bằng C++ và bắt đầu sau vài giây với chi phí sử dụng ít hơn nhiều.
- Không có ZooKeeper - Kafka theo truyền thống yêu cầu một cụm ZooKeeper
riêng biệt để phối hợp (siêu dữ liệu, bầu chọn người lãnh đạo). Redpanda xử lý nội bộ
này bằng giao thức đồng thuận Raft - bớt đi một dịch vụ để chạy.
- Nhị phân đơn - chỉ một vùng chứa, không cần cấu hình gì khác.

Đối với hội thảo này, mỗi khi chúng tôi nói "Kafka", chúng tôi muốn nói đến giao thức Kafka
và các khái niệm. Redpanda là nhà môi giới thực sự đang hoạt động bên dưới.


*Sự khác biệt chính về cấu trúc liên kết là nơi máy khách chạy: cả hai đường dẫn đều sử dụng máy khách Kafka, nhưng dịch vụ Docker và máy tính xách tay cần các tuyến mạng khác nhau.*

Tạo `docker-compose.yml` với dịch vụ Redpanda:

```yaml
services:
  redpanda:
    image: redpandadata/redpanda:v25.3.9
    command:
      - redpanda
      - start
      - --smp
      - '1'
      - --reserve-memory
      - 0M
      - --overprovisioned
      - --node-id
      - '1'
      - --kafka-addr
      - PLAINTEXT://0.0.0.0:29092,OUTSIDE://0.0.0.0:9092
      - --advertise-kafka-addr
      - PLAINTEXT://redpanda:29092,OUTSIDE://localhost:9092
      - --pandaproxy-addr
      - PLAINTEXT://0.0.0.0:28082,OUTSIDE://0.0.0.0:8082
      - --advertise-pandaproxy-addr
      - PLAINTEXT://redpanda:28082,OUTSIDE://localhost:8082
      - --rpc-addr
      - 0.0.0.0:33145
      - --advertise-rpc-addr
      - redpanda:33145
    ports:
      - 8082:8082
      - 9092:9092
      - 28082:28082
      - 29092:29092
```

Lệnh có nhiều tham số. Chúng ta hãy đi qua chúng.

Thông số tài nguyên:

| Tham số | Nó làm gì |
|---|---|
| `--smp 1` | Sử dụng 1 lõi CPU. Redpanda được xây dựng trên [Seastar](http://seastar.io/), một khung ghim các luồng vào lõi để có hiệu suất cao. Để phát triển, 1 lõi là đủ. |
| `--reserve-memory 0M` | Đừng dành thêm bộ nhớ cho bộ đệm trong của Redpanda. Trong quá trình sản xuất, Redpanda dành bộ nhớ cho bộ đệm trang của riêng mình; chúng tôi bỏ qua điều này trong quá trình phát triển. |
| `--overprovisioned` | Không ghim luồng vào các lõi CPU cụ thể. Trên một máy phát triển dùng chung, điều này tránh được sự xung đột với các quy trình khác. |
| `--node-id 1` | Mã định danh duy nhất cho nhà môi giới này trong cụm. Với một nhà môi giới duy nhất thì điều đó không thành vấn đề, nhưng tham số là bắt buộc. |

Thông số mạng:

Redpanda hiển thị hai trình nghe riêng biệt cho giao thức Kafka - một cho các kết nối
từ bên trong Docker (các vùng chứa khác) và một cho các kết nối
từ Docker bên ngoài (máy tính xách tay của bạn):

| Tham số | Nội bộ (Docker) | Bên ngoài (máy tính xách tay của bạn) |
|---|---|---|
| `--kafka-addr` | `PLAINTEXT://0.0.0.0:29092` | `OUTSIDE://0.0.0.0:9092` |
| `--advertise-kafka-addr` | `PLAINTEXT://redpanda:29092` | `OUTSIDE://localhost:9092` |

Tại sao lại có hai địa chỉ? Máy khách Kafka sử dụng quy trình kết nối hai bước:

1. Máy khách kết nối với máy chủ bootstrap và yêu cầu siêu dữ liệu cụm
2. Nhà môi giới phản hồi bằng các địa chỉ được quảng cáo - trong đó máy khách nên kết nối
để truyền dữ liệu thực tế

Bên trong Docker, các container tìm nhau theo tên dịch vụ nên địa chỉ được quảng cáo
nội bộ là `redpanda:29092`. Từ máy tính xách tay của bạn, bạn kết nối qua
cổng được xuất bản tại `localhost:9092`. Nếu chúng tôi chỉ sử dụng một địa chỉ, thì bộ chứa Docker
hoặc máy tính xách tay của bạn sẽ không thể kết nối.

`--pandaproxy-addr` / `--advertise-pandaproxy-addr` tuân theo mẫu
tương tự cho HTTP REST API của Redpanda (không được sử dụng trong hội thảo này).
`--rpc-addr` / `--advertise-rpc-addr` dành cho giao tiếp
của cụm nội bộ giữa các nút Redpanda (không liên quan đến một nút duy nhất).

Cổng đã xuất bản:

| Cảng | Nó dùng để làm gì |
|---|---|
| `9092` | Giao thức Kafka (bên ngoài) - nhà sản xuất/người tiêu dùng Python của bạn kết nối tại đây |
| `29092` | Giao thức Kafka (nội bộ) - Vùng chứa Flink sẽ kết nối ở đây sau |
| `8082` / `28082` | Proxy HTTP - Truy cập API REST (không được sử dụng trong hội thảo này) |

Bắt đầu Redpanda:

```bash
docker compose up redpanda -d
```

Xác minh nó đang chạy:

```bash
docker compose ps
```

```
NAME                IMAGE                           SERVICE    STATUS
workshop-redpanda   redpandadata/redpanda:v25.3.9   redpanda   Up
```
