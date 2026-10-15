---
video_url: https://www.youtube.com/watch?v=VAHm0R_XjqI
prev_url: 04-kestra-concepts.md
next_url: 06-getting-started-pipeline.md
---
# Sắp xếp mã Python

Bây giờ chúng ta đã xây dựng được quy trình làm việc đầu tiên của mình, chúng ta có thể tiến thêm một bước nữa bằng cách thêm mã Python vào quy trình của mình. Trong Kestra, chúng tôi có thể chạy mã Python từ một tệp chuyên dụng hoặc viết mã trực tiếp bên trong quy trình làm việc của mình.

Mặc dù Kestra có sẵn rất nhiều plugin để xây dựng quy trình làm việc của bạn, nhưng bạn cũng có tùy chọn viết mã của riêng mình và yêu cầu Kestra thực thi mã đó dựa trên lịch trình hoặc sự kiện. Điều này có nghĩa là bạn có thể chọn công cụ phù hợp cho quy trình của mình thay vì những công cụ mà bạn bị giới hạn.

Trong ví dụ về quy trình làm việc Python của chúng tôi, [`02_python.yaml`](flows/02_python.yaml), mã của chúng tôi tìm nạp số lần kéo hình ảnh Docker từ DockerHub và trả về dưới dạng đầu ra cho Kestra. Điều này rất hữu ích vì chúng ta có thể truy cập đầu ra này bằng các tác vụ khác, mặc dù nó được tạo bên trong tập lệnh Python của chúng ta.


## Tài nguyên
- [Hướng dẫn cách thực hiện: Python](https://go.kestra.io/de-zoomcamp/python)
