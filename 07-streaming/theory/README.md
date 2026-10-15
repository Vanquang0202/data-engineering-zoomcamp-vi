# Lý thuyết Kafka (tùy chọn)

Các bài giảng video bao gồm các khái niệm Kafka, kèm theo các ví dụ về mã bằng Java.

Mã: [java/kafka_examples](java/kafka_examples)


## Xử lý luồng

- [7.0.1 Giới thiệu](https://youtu.be/hfvju3iOIP0&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=67)
- [7.0.2 Xử lý luồng là gì](https://youtu.be/WxTxKGcfA-k&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=68)

![Hai luồng nguồn đi qua các chủ đề Kafka và Spark riêng biệt trước khi đến tay người tiêu dùng theo thời gian thực.](images/07-stream-processing-two-topic-flow.png)

- [7.3 Kafka là gì?](https://youtu.be/zPLZUDPi4AY&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=69)

![Một điểm dữ liệu phân chia thành nhiều vùng sự kiện trong một chủ đề Kafka.](images/07-kafka-event-fanout-to-partitions.png)

![Bảng thông báo do Kafka hỗ trợ định tuyến các thông điệp của nhà sản xuất thông qua các chủ đề riêng biệt tới người tiêu dùng.](images/07-kafka-notice-board-topics.png)

- [7.4 Đám mây hợp lưu](https://youtu.be/ZnEZFEYKppw&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=70)
- [7.5 Người tiêu dùng của nhà sản xuất Kafka](https://youtu.be/aegTuyxX7Yg&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=71)
- [Cấu hình 7.6 Kafka](https://youtu.be/SXQtWyRpMKs&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=72)

![Một chủ đề Kafka có bản sao của người dẫn đầu và người theo dõi, trong đó người tiêu dùng đọc từ người dẫn đầu.](images/07-kafka-replication.png)

![Việc lưu giữ Kafka giữ các bản ghi gần đây bên trong một cửa sổ lưu giữ và làm hết hạn các bản ghi cũ hơn.](images/07-kafka-retention-window.png)

![Chủ đề Rides được chia thành các phân vùng được phân bổ trên các nút Kafka riêng biệt.](images/07-kafka-partitions-to-nodes.png)

![Một nhóm người tiêu dùng chỉ định các làn phân vùng Kafka song song trên các người tiêu dùng của mình.](images/07-kafka-consumer-group-partition-assignment.png)

Liên kết:

- [Trang trình bày](https://docs.google.com/presentation/d/1bCtdCba8v1HxJ_uMm9pwjRUC-NAMeB-6nOG2ng3KujA/edit?usp=sharing)
- [Tham khảo cấu hình Kafka](https://docs.confluent.io/platform/current/installation/configuration/)
- [Bản dùng thử Confluent Cloud](https://www.confluent.io/confluent-cloud/tryfree/)


## Kafka phát trực tiếp

- [7.7 Thông tin cơ bản về luồng Kafka](https://youtu.be/dUyA_63eRb0&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=73)

![Kafka Streams nhóm các bản ghi theo khóa, đếm từng nhóm và đưa ra đầu ra có khóa.](images/07-kafka-key-count-flow.png)

- [7.8 Tham gia luồng Kafka](https://youtu.be/NcpKlujh34Y&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=74)
- [7.9 Thử nghiệm luồng Kafka](https://youtu.be/TNx5rmLY8Pk&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=75)

![Cấu trúc liên kết kiểm tra Luồng Kafka kết hợp hai chủ đề đầu vào và ghi vào một chủ đề đầu ra.](images/07-kafka-testing-topology.png)

- [Cửa sổ luồng Kafka 7.10](https://youtu.be/r1OuLdwxbRc&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=76)

![KTable toàn cầu sao chép dữ liệu tham chiếu được phân vùng thành các bản sao cục bộ hoàn chỉnh.](images/07-kafka-global-ktable-replication.png)

![Hai luồng sự kiện tạo ra kết quả liên kết bên trong một cửa sổ liên kết giới hạn.](images/07-kafka-stream-join-window.png)

![Cửa sổ lộn xộn chia thời gian truyền phát thành các khoảng thời gian liền kề bằng nhau, không chồng chéo.](images/07-kafka-tumbling-window-timeline.png)

- [7.11 Kafka ksqlDB và Connect](https://youtu.be/DziQ4a4tn9Y&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=77)
- [7.12 Kafka Schema register](https://youtu.be/tBY_hBuyzwI&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=78)

![ Sổ đăng ký lược đồ làm trung gian cho các lược đồ giữa nhà sản xuất, chủ đề và người tiêu dùng.](images/07-kafka-schema-registry-flow.png)

![Khả năng tương thích về phía trước cho phép kỳ vọng mới hơn của người tiêu dùng hoạt động với lược đồ cũ hơn thông qua Sổ đăng ký lược đồ.](images/07-kafka-schema-forward-compatibility.png)

Liên kết:

- [Trang trình bày](https://docs.google.com/presentation/d/1fVi9sFa7fL2ZW3ynS5MAZm0bRSZ4jO10fymPmrfTUjE/edit?usp=sharing)
- [Khái niệm về luồng](https://docs.confluent.io/platform/current/streams/concepts.html)
