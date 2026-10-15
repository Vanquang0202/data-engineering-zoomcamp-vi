## Bài tập về nhà Tuần 2

Mục tiêu của bài tập về nhà này là giúp người dùng làm quen với cách sắp xếp và quan sát quy trình làm việc. 


## Câu hỏi 1. Tải dữ liệu tháng 1 năm 2020

Sử dụng luồng `etl_web_to_gcs.py` tải dữ liệu taxi vào GCS làm hướng dẫn, tạo luồng tải tập dữ liệu CSV taxi màu xanh lá cây cho tháng 1 năm 2020 vào GCS và chạy nó. Nhìn vào nhật ký để biết tập dữ liệu có bao nhiêu hàng.

Tập dữ liệu đó có bao nhiêu hàng?

* 447,770
* 766,792
* 299,234
* 822,132


## Câu hỏi 2. Lập lịch với Cron

Cron là một đặc tả lập lịch phổ biến cho các quy trình làm việc. 

Sử dụng quy trình trong `etl_web_to_gcs.py`, tạo một triển khai để chạy vào ngày đầu tiên hàng tháng lúc 5 giờ sáng UTC. Lịch trình cron cho việc đó là gì?

- `0 5 1 * *`
- `0 0 5 1 *`
- `5 * 1 0 *`
- `* * 5 1 0`


## Câu 3. Đang tải dữ liệu vào BigQuery 

Sử dụng `etl_gcs_to_bq.py` làm điểm bắt đầu, sửa đổi tập lệnh trích xuất dữ liệu từ GCS và tải nó vào BigQuery. Tập lệnh mới này không được điền hoặc xóa các hàng có giá trị bị thiếu. (Kịch bản thực ra chỉ làm phần E và L của ETL).

Luồng chính sẽ in tổng số hàng được tập lệnh xử lý. Đặt trình trang trí luồng để ghi lại câu lệnh in.

Tham số hóa luồng điểm nhập để chấp nhận danh sách tháng, năm và màu taxi. 

Thực hiện bất kỳ thay đổi cần thiết nào khác đối với mã để mã hoạt động theo yêu cầu.

Tạo một bản triển khai để luồng này chạy trong một quy trình con cục bộ với bộ lưu trữ mã luồng cục bộ (mặc định).

Đảm bảo bạn có tệp dữ liệu parquet cho dữ liệu taxi Vàng cho tháng 2 năm 2019 và tháng 3 năm 2019 được tải trong GCS. Chạy triển khai của bạn để nối dữ liệu này vào bảng BiqQuery của bạn. Mã quy trình của bạn đã xử lý bao nhiêu hàng?

- 14,851,920
- 12,282,990
- 27,235,753
- 11,338,483



## Câu hỏi 4. Khối lưu trữ Github

Sử dụng tập lệnh `web_to_gcs` từ video làm hướng dẫn, bạn muốn lưu trữ mã luồng của mình trong kho lưu trữ GitHub để cộng tác với nhóm của mình. Trưởng có thể xem trong kho lưu trữ GitHub để tìm mã quy trình của bạn và đọc nó. Tạo khối lưu trữ GitHub từ UI hoặc trong mã Python và sử dụng khối đó trong Triển khai của bạn thay vì lưu trữ cục bộ mã luồng của bạn hoặc nướng mã luồng của bạn thành hình ảnh Docker. 

Lưu ý là bạn sẽ phải đẩy mã của mình lên GitHub, Prefect sẽ không đẩy mã cho bạn.

Chạy hoạt động triển khai của bạn trong một quy trình con cục bộ (mặc định nếu bạn không chỉ định cơ sở hạ tầng). Sử dụng dữ liệu Xe taxi xanh cho tháng 11 năm 2020.

Tập lệnh đã xử lý bao nhiêu hàng?

- 88,019
- 192,297
- 88,605
- 190,225



## Câu 5. Thông báo qua email hoặc Slack

Q5. Thông thường, việc nhận được thông báo khi có điều gì đó trong luồng dữ liệu của bạn không hoạt động như kế hoạch thường rất hữu ích. Chọn một trong các tùy chọn bên dưới để tạo email hoặc thông báo chậm.

Prefect Cloud được lưu trữ cho phép bạn tránh phải chạy máy chủ của riêng mình và có tính năng Tự động hóa cho phép bạn nhận thông báo khi một số sự kiện nhất định xảy ra hoặc không xảy ra. 

Tạo tài khoản Prefect Cloud miễn phí vĩnh viễn tại app.prefect.cloud và kết nối không gian làm việc của bạn với tài khoản đó theo các bước trong UI khi bạn đăng ký. 

Thiết lập Tự động hóa sẽ tự gửi email cho chính bạn khi quá trình chạy quy trình hoàn tất. Chạy quá trình triển khai được sử dụng trong Q4 cho dữ liệu Taxi xanh vào tháng 4 năm 2019. Hãy kiểm tra email của bạn để xem thông báo.

Ngoài ra, hãy sử dụng Prefect Cloud Automation hoặc Thông báo máy chủ Orion tự lưu trữ để nhận thông báo trong không gian làm việc Slack thông qua webhook đến. 

Join không gian làm việc Slack tạm thời của tôi với [liên kết này](https://join.slack.com/t/temp-notify/shared_invite/zt-1odklt4wh-hH~b89HN8MjMrPGEaOlxIw). 400 người có thể sử dụng liên kết này và nó sẽ hết hạn sau 90 ngày. 

Trong Prefect Cloud UI, tạo [Tự động hóa](https://docs.prefect.io/ui/automations) hoặc trong Prefect Orion UI tạo [Thông báo](https://docs.prefect.io/ui/notifications/) để gửi tin nhắn Slack khi một luồng chạy chuyển sang trạng thái Đã hoàn thành. Đây là Webhook URL để sử dụng: https://hooks.slack.com/services/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

Kiểm tra chức năng.

Ngoài ra, bạn có thể lấy webhook URL từ không gian làm việc Slack của riêng bạn và Ứng dụng Slack mà bạn tạo. 


Tập lệnh đã xử lý bao nhiêu hàng?

- `125,268`
- `377,922`
- `728,390`
- `514,392`


## Câu hỏi 6. Bí mật

Các khối Bí mật hoàn hảo cung cấp khả năng lưu trữ được mã hóa, an toàn trong cơ sở dữ liệu và khả năng che giấu trong UI. Tạo một khối bí mật trong UI để lưu trữ mật khẩu giả gồm 10 chữ số để kết nối với dịch vụ của bên thứ ba. Khi bạn đã tạo khối của mình trong UI, có bao nhiêu ký tự được hiển thị dưới dạng dấu hoa thị (*) trên trang tiếp theo của UI?

- 5
- 6
- 8
- 10


## Nộp bài giải

* Hình thức nộp bài: https://forms.gle/PY8mBEGXJ1RvmTM97
* Có thể nộp bài tập về nhà nhiều lần. Trong trường hợp này, chỉ lần gửi cuối cùng sẽ được sử dụng. 

Hạn chót: 8 tháng 2 (Thứ Tư), 22:00 CET


## Giải pháp

* Video: https://youtu.be/L04lvYqNlc0
* Mã: https://github.com/discdiver/prefect-zoomcamp/tree/main/flows/04_homework
