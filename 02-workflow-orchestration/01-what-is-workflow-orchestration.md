---
video_url: https://www.youtube.com/watch?v=-JLnp-iLins
prev_url: ../01-docker-terraform/13-gcp-overview.md
next_url: 02-what-is-kestra.md
---
# Điều phối quy trình công việc là gì?

Hãy nghĩ về một dàn nhạc. Có nhiều loại nhạc cụ khác nhau. Một số nhiều hơn những cái khác, tất cả đều có vai trò khác nhau khi chơi nhạc. Để đảm bảo tất cả họ đến cùng nhau vào đúng thời điểm, họ đi theo một nhạc trưởng giúp dàn nhạc chơi cùng nhau.

Bây giờ thay thế các nhạc cụ bằng các công cụ và thay thế người chỉ huy bằng một người điều phối âm nhạc. Chúng ta thường có nhiều công cụ và nền tảng cần để làm việc cùng nhau. Đôi khi theo lịch trình thường lệ, những lúc khác dựa trên các sự kiện xảy ra. Đó là lúc người điều phối xuất hiện để giúp tất cả các công cụ này hoạt động cùng nhau.

Người điều phối quy trình công việc có thể thực hiện các tác vụ sau:
- Chạy quy trình công việc có chứa một số bước được xác định trước
- Giám sát và ghi nhật ký lỗi cũng như thực hiện một số bước bổ sung khi chúng xảy ra
- Tự động chạy quy trình công việc dựa trên lịch trình và sự kiện

Trong kỹ thuật dữ liệu, bạn thường cần di chuyển dữ liệu từ nơi này sang nơi khác, đôi khi thực hiện một số sửa đổi đối với dữ liệu ở giữa. Đây là lúc người điều phối quy trình làm việc có thể trợ giúp bằng cách quản lý các bước này, đồng thời cung cấp cho chúng tôi khả năng hiển thị về nó cùng một lúc.


Trong mô-đun này, chúng ta sẽ xây dựng đường dẫn dữ liệu của riêng mình bằng cách sử dụng ETL (Trích xuất, Tải chuyển đổi) với Kestra là cốt lõi của hoạt động, nhưng trước tiên chúng ta cần hiểu thêm một chút về cách Kestra hoạt động trước khi chúng ta có thể bắt đầu xây dựng!
