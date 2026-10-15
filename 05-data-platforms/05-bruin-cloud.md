---
video_url: https://www.youtube.com/watch?v=uBqjLEwF8rc
prev_url: 04-bruin-mcp.md
next_url: 06-core-concepts-projects.md
---
# Triển khai lên Bruin Cloud

## Đám mây Bruin là gì?

Bruin Cloud là cơ sở hạ tầng được quản lý hoàn toàn cho đường dẫn dữ liệu của bạn. Nó được hỗ trợ bởi cùng một công cụ CLI nguồn mở mà bạn sử dụng cục bộ để phát triển. Mọi thứ đều ở cùng một nơi:

- Nhập và chuyển đổi
- Kiểm tra và giám sát chất lượng
- Dòng dõi và siêu dữ liệu
- Quản trị dữ liệu
- Các tính năng hỗ trợ AI (tạo siêu dữ liệu tự động, phân tích dữ liệu hội thoại)


*Triển khai trên đám mây giúp kết nối mã kho lưu trữ, kết nối trong phạm vi, chạy theo lịch và giám sát vận hành.*

## Đăng ký

1. Đi tới [Bruin Cloud](https://getbruin.com/) và đăng ký
2. Điền tên, email của bạn và đặt mật khẩu
3. Xác minh email của bạn bằng cách nhấp vào liên kết trong email xác minh
4. Chọn tham gia nhóm hiện có hoặc tạo tổ chức mới
5. Đặt tên cho tổ chức của bạn

## Kết nối kho lưu trữ GitHub của bạn

Bạn có hai lựa chọn:

1. **Kết nối GitHub trực tiếp** (được khuyến nghị) — kết nối trực tiếp tài khoản GitHub của bạn và chọn kho lưu trữ của bạn từ danh sách thả xuống
2. **Mã thông báo truy cập cá nhân** — cung cấp mã thông báo truy cập cá nhân GitHub và liên kết kho lưu trữ của bạn theo cách thủ công

## Thiết lập kết nối

Sau khi kết nối kho lưu trữ của bạn, hãy thiết lập kết nối kho dữ liệu của bạn. Đây là những kết nối bạn định cấu hình cục bộ trong `.bruin.yml` nhưng được lưu trữ an toàn trên đám mây.

1. Đi tới trang kết nối
2. Chọn loại kết nối của bạn (MotherDuck, BigQuery, Redshift, v.v.)
3. Đặt cho nó cùng tên kết nối mà bạn sử dụng cục bộ
4. Cung cấp thông tin xác thực cần thiết (ví dụ: mã thông báo dịch vụ, tên cơ sở dữ liệu)
5. Kết nối sẽ được xác thực và kiểm tra tự động

Đọc tài liệu Bruin để biết chi tiết về cách lưu trữ bí mật một cách an toàn.

## Triển khai đường ống

1. Điều hướng đến trang **Pipelines** để xem danh sách các quy trình từ kho lưu trữ
của bạn 2. Bruin sẽ xác thực mọi nội dung và đảm bảo dòng và kết nối hoạt động (việc này mất một chút thời gian)
3. Khi đã sẵn sàng, **bật** quy trình

Khi bạn kích hoạt một quy trình có lịch trình, Bruin sẽ tự động tạo một lần chạy cho khoảng thời gian cuối cùng. Ví dụ: quy trình hàng tháng sẽ xử lý ngay dữ liệu của tháng trước.

## Giám sát

Sau khi một đường ống chạy:

- Kiểm tra trạng thái của từng nội dung (thành công/thất bại)
- Xem lại kết quả kiểm tra chất lượng
- Xem dòng trên tất cả nội dung
- Sử dụng các tính năng hỗ trợ AI để phân tích dữ liệu hoặc đặt câu hỏi về quy trình của bạn

## Nhận trợ giúp

- Tham gia [cộng đồng Bruin Slack](https://getbruin.com/) để biết các câu hỏi và yêu cầu tính năng
- Gửi các vấn đề trên [GitHub](https://github.com/bruin-data/bruin)
