# Ví dụ phát trực tuyến bổ sung

Các ví dụ xử lý luồng bổ sung từ các năm học trước. Đây là
không phải là một phần của hội thảo chính nhưng có thể hữu ích làm tài liệu tham khảo.


## trăn/

Ví dụ Python Kafka của Irem Erturk, sử dụng nhiều thư viện khác nhau.

- [json_example/](python/json_example) - nhà sản xuất và người tiêu dùng sử dụng
`kafka-python` với tuần tự hóa JSON
- [avro_example/](python/avro_example) - nhà sản xuất và người tiêu dùng sử dụng
`confluent-kafka` với tính năng tuần tự hóa Avro và Sổ đăng ký lược đồ
- [redpanda_example/](python/redpanda_example) - giống như ví dụ JSON
nhưng chạy với Redpanda thay vì Kafka, với thiết lập soạn thảo docker
cục bộ
- [streams-example/faust/](python/streams-example/faust) - xử lý luồng
với [Faust](https://faust-streaming.github.io/faust/), thư viện Python
cho Luồng Kafka. Bao gồm các ví dụ về cửa sổ, phân nhánh và đếm.
- [streams-example/pyspark/](python/streams-example/pyspark) - Spark
Truyền phát có cấu trúc tiêu thụ từ Kafka, với sổ ghi chép Jupyter
- [streams-example/redpanda/](python/streams-example/redpanda) - giống như
the PySpark ví dụ nhưng sử dụng Redpanda làm nhà môi giới
- [docker/](python/docker) - Docker Soạn các tệp để chạy Kafka và
Cụm Spark cục bộ
- [resources/](python/resources) - dữ liệu mẫu (rides.csv) và lược đồ Avro


## pyflink/

Hội thảo PyFlink của Irem Erturk. Sử dụng Apache Flink 1.x với quy trình làm việc dựa trên
Makefile, phần chìm PostgreSQL và thiết lập Docker Compose.
[luồng 2025 với Zach Wilson](https://www.youtube.com/watch?v=P2loELMUUeI)
đã được Alexey viết lại thành [hội thảo 2026](../code/) hiện tại,
bằng cách sử dụng Flink 2.2, uv và README từng bước.


## ksqldb/

[commands.md](ksqldb/commands.md) - ví dụ về các truy vấn ksqlDB để tạo luồng
, lọc, nhóm và tổng hợp cửa sổ theo các chủ đề Kafka.
Đồng hành với [ksqlDB và kết nối video](../theory/#kafka-streams) trong phần lý thuyết của
.
