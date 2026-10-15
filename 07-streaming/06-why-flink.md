---
prev_url: 05-save-events-to-postgresql.md
next_url: 07-the-flink-image-and-services.md
---
# Tại sao lại nhấp nháy?

Flink là một khung xử lý luồng xử lý tất cả các phần cứng:

- Cửa sổ - cửa sổ xoay, trượt và phiên tích hợp
- Điểm kiểm tra - khôi phục trạng thái tự động sau lỗi (không theo dõi bù thủ công)
- Tính song song - xử lý phân phối trên nhiều trình chạy
- Trình kết nối - JDBC, Kafka, hệ thống tệp chìm tích hợp (không có mã psycopg2)
- Giao diện SQL - xử lý luồng tốc hành với Truy vấn SQL

Flink cũng có thể kết nối với các nguồn ngoài Kafka - API REST, ổ cắm web, hệ thống tệp
, v.v. Nhưng Kafka là nguồn phổ biến nhất trong xử lý luồng.

Sự đánh đổi là sự phức tạp của cơ sở hạ tầng - chúng tôi cần các bộ chứa Trình quản lý tác vụ JobManager và
. Công việc phát trực tuyến giống như sở hữu một máy chủ hơn là
chạy một quy trình hàng loạt - nó chạy 24/7 và cần được giám sát. Nhưng đối với bất kỳ thứ gì
ngoài việc sử dụng và ghi đơn giản, Flink sẽ tự trả tiền.
