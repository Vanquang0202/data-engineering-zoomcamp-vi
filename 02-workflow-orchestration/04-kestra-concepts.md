---
video_url: https://www.youtube.com/watch?v=MNOKVx8780E
prev_url: 03-installing-kestra.md
next_url: 05-orchestrate-python-code.md
---
# Khái niệm Kestra

Để bắt đầu xây dựng quy trình công việc trong Kestra, chúng ta cần hiểu một số khái niệm.
- [Flow](https://go.kestra.io/de-zoomcamp/flow) - nơi chứa các nhiệm vụ và logic điều phối của chúng.
- [Nhiệm vụ](https://go.kestra.io/de-zoomcamp/tasks) - các bước trong một quy trình.
- [Đầu vào](https://go.kestra.io/de-zoomcamp/inputs) - các giá trị động được truyền vào luồng trong thời gian chạy.
- [Đầu ra](https://go.kestra.io/de-zoomcamp/outputs) - truyền dữ liệu giữa các tác vụ và luồng.
- [Trình kích hoạt](https://go.kestra.io/de-zoomcamp/triggers) - cơ chế tự động bắt đầu thực hiện một luồng.
- [Thực thi](https://go.kestra.io/de-zoomcamp/execution) - một lần chạy luồng với trạng thái cụ thể.
- [Biến](https://go.kestra.io/de-zoomcamp/variables) - cặp khóa-giá trị cho phép bạn sử dụng lại các giá trị trong các tác vụ.
- [Mặc định plugin](https://go.kestra.io/de-zoomcamp/plugin-defaults) - các giá trị mặc định được áp dụng cho mọi tác vụ thuộc một loại nhất định trong một hoặc nhiều luồng.
- [Đồng thời](https://go.kestra.io/de-zoomcamp/concurrency) - kiểm soát số lần thực thi của một luồng có thể chạy cùng lúc.

Mặc dù có nhiều khái niệm hơn được sử dụng để xây dựng quy trình công việc mạnh mẽ nhưng đây là những khái niệm chúng tôi sẽ sử dụng để xây dựng quy trình dữ liệu của mình.


Quy trình [`01_hello_world.yaml`](flows/01_hello_world.yaml) hiển thị tất cả các khái niệm này trong một quy trình làm việc:
- Quy trình có 5 nhiệm vụ: 3 nhiệm vụ ghi nhật ký và một nhiệm vụ ngủ
- Luồng này nhận đầu vào có tên là `name`.
- Có một biến lấy đầu vào `name` để tạo thông báo chào mừng đầy đủ.
- Đầu ra được tạo từ tác vụ trả về và được ghi vào tác vụ nhật ký sau này.
- Có một trình kích hoạt để thực thi luồng này vào lúc 10 giờ sáng hàng ngày.
- Mặc định của plugin được sử dụng để khiến cả hai tác vụ nhật ký gửi thông báo của chúng ở cấp độ `ERROR`.
- Chúng tôi có giới hạn đồng thời là 2 lần thực thi. Bất kỳ cái nào khác được thực hiện trong khi 2 đang chạy sẽ thất bại.

## Tài nguyên
- [Hướng dẫn](https://go.kestra.io/de-zoomcamp/tutorial)
- [Tài liệu về thành phần quy trình công việc](https://go.kestra.io/de-zoomcamp/workflow-components)
