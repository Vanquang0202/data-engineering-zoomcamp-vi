### Xử lý luồng bằng Python

Trong tài liệu này, bạn sẽ tìm thấy thông tin về xử lý luồng
bằng các thư viện Python khác nhau (`kafka-python`,`confluent-kafka`,`pyspark`, `faust`).

Mô-đun Python này có thể được tách thành các mô-đun sau.

#### 1. Docker
Mô-đun Docker bao gồm các định nghĩa Dockerfiles và docker-compose
để chạy Kafka và Spark trong vùng chứa docker. Thiết lập các dịch vụ cần thiết là
là bước tiên quyết để chạy các mô-đun sau.

#### 2. Nhà sản xuất Kafka - Ví dụ về người tiêu dùng
- [Ví dụ về nhà sản xuất-người tiêu dùng Json](json_example) sử dụng thư viện `kafka-python`
- [Ví dụ về nhà sản xuất-người tiêu dùng Avro](avro_example) sử dụng thư viện `confluent-kafka`

Cả hai ví dụ này đều yêu cầu các dịch vụ Kafka thiết lập và chạy, do đó vui lòng đảm bảo
tuân theo các bước trong [docker-README](docker/README.md)

Để chạy các ví dụ nhà sản xuất-người tiêu dùng trong thư mục ví dụ tương ứng, hãy chạy các lệnh sau
```bash
# Start producer script
python3 producer.py
# Start consumer script
python3 consumer.py
```





