
# Chạy truyền phát PySpark với Redpanda

### 1. Điều kiện tiên quyết

Điều quan trọng là tạo mạng và khối lượng như được mô tả trong tài liệu. Vì vậy, hãy đảm bảo rằng khối lượng và mạng của bạn được tạo chính xác.

```bash
docker volume ls # should list hadoop-distributed-file-system
docker network ls # should list kafka-spark-network 
```

### 2. Tạo Docker Network & Volume

Nếu bạn chưa làm theo bất kỳ ví dụ nào khác và các bước `ls` ở trên không hiển thị kết quả, hãy tạo chúng ngay bây giờ.

```bash
# Create Network
docker network create kafka-spark-network

# Create Volume
docker volume create --name=hadoop-distributed-file-system
```

### Đang chạy Nhà sản xuất và Người tiêu dùng
```bash
# Run producer
python producer.py

# Run consumer with default settings
python consumer.py
# Run consumer for specific topic
python consumer.py --topic <topic-name>
```

### Chạy tập lệnh phát trực tuyến

tập lệnh spark-submit đảm bảo cài đặt các lọ cần thiết trước khi chạy streaming.py

```bash
./spark-submit.sh streaming.py 
```

### Tài nguyên bổ sung
- [Hướng dẫn lập trình phát trực tuyến có cấu trúc](https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html#structured-streaming-programming-guide)
- [Truyền phát có cấu trúc + Tích hợp Kafka](https://spark.apache.org/docs/latest/structured-streaming-kafka-integration.html#structured-streaming-kafka-integration-guide-kafka-broker-versio)
