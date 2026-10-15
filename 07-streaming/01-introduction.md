---
video_url: https://www.youtube.com/watch?v=YDUgFeHQzJU
prev_url: ../06-batch/16-connecting-spark-to-bigquery.md
next_url: 02-redpanda.md
---
# PyFlink: Xưởng xử lý luồng

Hội thảo này dựa trên
[luồng phát sóng năm 2025 với Zach Wilson](https://www.youtube.com/watch?v=P2loELMUUeI).

Trong hội thảo này, chúng tôi từng bước xây dựng quy trình phát trực tuyến theo thời gian thực.
Chúng tôi bắt đầu với những điều cơ bản - nhà môi giới tin nhắn, nhà sản xuất và người tiêu dùng -
, sau đó thêm cơ sở dữ liệu và cuối cùng là khung xử lý luồng.

Chúng tôi sẽ sử dụng dữ liệu chuyến đi bằng taxi màu vàng của NYC làm nguồn dữ liệu.

Những gì chúng tôi sẽ xây dựng vào cuối:

```
Producer (Python) -> Kafka (Redpanda) -> Flink -> PostgreSQL
```


*Hội thảo phát triển lộ trình sự kiện trực tiếp từ sản xuất thông qua môi giới và xử lý luồng đến lưu trữ quan hệ bền vững.*

Điều kiện tiên quyết:

- Docker và Docker Compose
- [uv](https://docs.astral.sh/uv/)
- Máy khách SQL - [pgcli](https://www.pgcli.com/) (`uvx pgcli`), DBeaver, pgAdmin hoặc DataGrip

Mã số:

- [Mã tham chiếu](code/) trong thư mục `code/` của mô-đun này
- [Mã được tạo trong hội thảo](code/live/) của Alexey

Các đơn vị theo dõi sẽ xây dựng mọi thứ từ đầu - bạn có thể
làm theo từng bước hoặc nghiên cứu các tệp hiện có và chạy lệnh.
