
# Chạy PySpark Truyền phát

#### Điều kiện tiên quyết

Đảm bảo các dịch vụ Kafka và Spark của bạn luôn hoạt động bằng cách làm theo [readme setup docker](./../../docker/README.md).
Điều quan trọng là tạo mạng và âm lượng như được mô tả trong tài liệu. Vì vậy, hãy đảm bảo rằng ổ đĩa và mạng của bạn được tạo chính xác

```bash
docker volume ls # should list hadoop-distributed-file-system
docker network ls # should list kafka-spark-network 
```


### Đang chạy Nhà sản xuất và Người tiêu dùng
```bash
# Run producer
python3 producer.py

# Run consumer with default settings
python3 consumer.py
# Run consumer for specific topic
python3 consumer.py --topic <topic-name>
```

### Chạy tập lệnh phát trực tuyến

tập lệnh spark-submit đảm bảo cài đặt các lọ cần thiết trước khi chạy streaming.py

```bash
./spark-submit.sh streaming.py 
```

### Tài nguyên bổ sung
- [Hướng dẫn lập trình phát trực tuyến có cấu trúc](https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html#structured-streaming-programming-guide)
- [Truyền phát có cấu trúc + Tích hợp Kafka](https://spark.apache.org/docs/latest/structured-streaming-kafka-integration.html#structured-streaming-kafka-integration-guide-kafka-broker-versio)
