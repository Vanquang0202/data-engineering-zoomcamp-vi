---
video_url: https://www.youtube.com/watch?v=1pu_C_oOAMA
prev_url: 07-load-taxi-data-to-postgres.md
next_url: 09-etl-vs-elt.md
---
# DB cục bộ: Tìm hiểu cách lập kế hoạch và chèn lấp

Bây giờ chúng tôi có thể lên lịch cho quy trình tương tự được hiển thị ở trên để chạy hàng ngày lúc 9 giờ sáng theo giờ UTC. Chúng tôi cũng sẽ trình bày cách chèn lấp đường dẫn dữ liệu để chạy trên dữ liệu lịch sử.

Lưu ý: với tập dữ liệu lớn, chúng tôi sẽ chỉ chèn lấp dữ liệu cho tập dữ liệu taxi xanh cho năm 2019.


Mã luồng: [`05_postgres_taxi_scheduled.yaml`](flows/05_postgres_taxi_scheduled.yaml).
