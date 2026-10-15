---
video_url: https://www.youtube.com/watch?v=b-6KhfWfk2M
prev_url: 11-load-taxi-data-to-bigquery.md
next_url: 13-why-ai-for-workflows.md
---
# Quy trình làm việc của GCP: Lên lịch và chèn lấp toàn bộ bộ dữ liệu

Giờ đây, chúng tôi có thể lên lịch cho quy trình tương tự được hiển thị ở trên để chạy hàng ngày lúc 9 giờ sáng UTC cho tập dữ liệu màu xanh lá cây và lúc 10 giờ sáng UTC cho tập dữ liệu màu vàng. Bạn có thể chèn lấp dữ liệu lịch sử trực tiếp từ giao diện người dùng Kestra.

Vì hiện tại chúng tôi xử lý dữ liệu trong môi trường đám mây với khả năng lưu trữ và điện toán có khả năng mở rộng vô hạn nên chúng tôi có thể chèn lấp toàn bộ tập dữ liệu cho cả dữ liệu taxi màu vàng và màu xanh lá cây mà không gặp nguy cơ hết tài nguyên trên máy cục bộ.


Mã luồng: [`09_gcp_taxi_scheduled.yaml`](flows/09_gcp_taxi_scheduled.yaml).
