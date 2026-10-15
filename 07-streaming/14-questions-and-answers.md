---
prev_url: 13-cleanup.md
---
#Hỏi đáp

Câu hỏi và câu trả lời từ
[luồng phát sóng năm 2025 với Zach Wilson](https://www.youtube.com/watch?v=P2loELMUUeI).


*Phần Hỏi & Đáp xem xét lại các quyết định về hoạt động và kiến ​​trúc xung quanh việc khôi phục, xử lý trạng thái, độ trễ, độ trễ và phân phối sản phẩm.*

## Điều gì xảy ra khi công việc Flink chết và khởi động lại? Nó có xử lý lại mọi thứ không?
Cài đặt offset `earliest` chỉ dành cho lần khởi động đầu tiên. Nếu công việc
khởi động lại (không được gửi lại dưới dạng công việc mới), thì công việc đó sẽ sử dụng điểm kiểm tra để tiếp tục
từ ảnh chụp nhanh cuối cùng. Nếu không có điểm kiểm tra, bạn sẽ xử lý lại mọi thứ
(với `earliest`) hoặc bỏ qua dữ liệu (với `latest`).

Điểm bắt: các điểm kiểm tra nằm trong phạm vi một trường hợp công việc cụ thể. Nếu bạn
loại bỏ hoàn toàn một công việc và gửi một công việc mới, thì công việc mới đó không có kiến ​​thức về
các điểm kiểm tra trước đó. Để duy trì trạng thái trong quá trình triển khai lại, hãy khởi động lại
công việc hiện có thay vì tạo một công việc mới.

## Tại sao chúng ta không thể chỉ sử dụng người tiêu dùng Kafka? Flink thực sự thêm gì?
Để chuyển qua đơn giản (đọc tin nhắn, viết tin nhắn ở đâu đó), người tiêu dùng Kafka
vẫn ổn. Đối với mọi thứ liên quan đến cửa sổ thời gian, hình mờ, điểm kiểm tra
hoặc xử lý song song, Flink giúp bạn không phải tự mình xây dựng tất cả
.

Bạn có thể thực hiện tạo cửa sổ, tạo hình mờ, xử lý dữ liệu trễ và khôi phục công việc
với người dùng đơn giản - hãy tự mình quản lý. Nhưng như Zach đặt
: "chúc may mắn." Với người dùng thông thường, bạn cũng cần tự mình theo dõi các điểm kiểm tra
- lưu dấu thời gian được xử lý mới nhất vào một tệp hoặc cơ sở dữ liệu
và quản lý nó mỗi lần khởi động lại. Flink giữ trạng thái cho bạn.

Nó giống như hỏi "tại sao lại sử dụng Spark khi bạn có thể sử dụng Pandas?" Bạn có thể, nhưng
Pandas sẽ không hoạt động ở quy mô cao hơn theo cách phân tán.

## Điều gì xảy ra với các sự kiện bị trì hoãn ngoài hình mờ (kịch bản "đường hầm")?
Có hai loại độ trễ. Hình mờ xử lý độ trễ có thể chấp nhận được -
có độ trễ nhỏ khi các sự kiện đến muộn vài giây. Đối với các sự kiện đến
muộn hơn nhiều (như sau đường hầm 5 phút), Flink có tham số
có độ trễ cho phép.

Theo mặc định, độ trễ được phép bằng 0 - các sự kiện đến sau hình mờ
đóng cửa sổ sẽ bị loại bỏ. Nếu bạn đặt độ trễ cho phép là 10 phút,
Flink sẽ quay lại, tìm cửa sổ đã đóng cũ, tạo tập hợp
mới với sự kiện muộn và gửi nó đến hệ thống lưu trữ dưới dạng bản ghi hoàn toàn mới.
này có nghĩa là bạn cần logic chống trùng lặp ở phía chìm (khóa chính có hành vi cập nhật
- chính xác là những gì chúng tôi thiết lập trong phần tổng hợp).

Sự đánh đổi: độ trễ cho phép yêu cầu Flink phải giữ tất cả các cửa sổ
đó trên đĩa trong khoảng thời gian cho phép.

## Khi nào chúng ta thực sự cần phát trực tuyến? Đối với nhiều thứ, lô nhỏ là đủ.
Câu hỏi quan trọng: có điều gì đó sắp xảy ra trong thời gian thực ở phía
bên kia không? Nếu có một quy trình tự động sẽ thay đổi điều gì đó dựa trên dữ liệu
thì phát trực tuyến là một lựa chọn tuyệt vời. Nếu con người chỉ nhìn vào dữ liệu thì thời gian thực của
là không cần thiết và vi lô sẽ dễ bảo trì hơn.

Trong 10 năm làm kỹ sư dữ liệu, Zach đã gặp phải hai trường hợp sử dụng mà
thực sự cần phát trực tuyến - phát hiện gian lận/bảo mật Netflix (
chậm trễ 5 phút đồng nghĩa với việc tài khoản bị hack thêm 5 phút) và giá
tăng vọt của Airbnb (cung và cầu thay đổi nhanh chóng). Mọi thứ khác đều được thực hiện theo lô hàng ngày hoặc vi lô
theo giờ/mỗi 15 phút cho nhu cầu về độ trễ thấp hơn.

Trước khi cam kết phát trực tuyến, hãy xem xét chi phí hoạt động. Công việc
phát trực tuyến chạy 24/7 - nếu nó bị hỏng lúc 3 giờ sáng thì cần có người sửa nó. Nếu bạn là
là người duy nhất trong nhóm hiểu Flink, thì bạn sẽ luôn sẵn sàng sử dụng
. Hãy trao đổi với người quản lý của bạn trước khi triển khai tính năng phát trực tuyến - bạn sẽ cần
hướng dẫn toàn bộ nhóm của mình trước khi có thể chia sẻ gánh nặng trong cuộc gọi.

## Truyền phát Spark và Truyền phát Flink?
Ngày nay chúng khác nhau về cơ bản nhưng có thể sẽ hội tụ. Điểm khác biệt chính của
: Spark Streaming là micro-batch - nó phát xung cứ sau 15-30 giây,
kéo dữ liệu theo từng đợt nhỏ (kiến trúc kéo). Flink là
xử lý liên tục chính hãng - các sự kiện diễn ra khi chúng đến (kiến trúc đẩy
). Đối với hầu hết các trường hợp sử dụng, sự khác biệt là không đáng kể, nhưng Flink
có độ trễ thấp hơn cho nhu cầu thực sự trong thời gian thực.

Đối với các khoảng thời gian vi lô, Zach nhận thấy
Spark cứ 5 phút một lần là quá thường xuyên vì chỉ riêng việc khởi động đã mất khoảng một phút, khiến tỷ lệ chi phí cho công việc của
kém. Điểm hấp dẫn của anh ấy là hàng giờ và cứ sau 15 phút
.

## Việc gửi công việc diễn ra như thế nào trong sản xuất?
Trong hội thảo này, chúng tôi gắn các tệp cục bộ vào Docker và gửi công việc với
`docker compose exec` - đó là sự thuận tiện cho việc phát triển. Trong quá trình sản xuất, việc gửi công việc
trông khác nhau tùy thuộc vào việc triển khai:

- Các dịch vụ được quản lý (AWS Kinesis Data Analytics, Google Cloud Dataflow,
Confluent Cloud) - bạn tải lên tệp JAR hoặc Python zip thông qua bảng điều khiển web
hoặc CLI. Dịch vụ xử lý cụm.
- Flink tự lưu trữ trên Kubernetes - bạn thường xây dựng hình ảnh Docker với
mã công việc của bạn đã được cài sẵn hoặc sử dụng Toán tử Flink Kubernetes để lấy các tạo phẩm công việc
từ S3/GCS khi khởi động.
- Cụm Flink độc lập - bạn sử dụng CLI `flink run` trỏ đến tệp cục bộ
hoặc URL HTTP/S3. Đường dẫn CI/CD thường tải tạo phẩm
công việc lên S3 rồi gọi `flink run` bằng URL đó.

Mẫu phổ biến: mã của bạn tồn tại trong git, CI xây dựng một tạo phẩm (JAR,
Python zip hoặc hình ảnh Docker), đẩy nó đến sổ đăng ký hoặc kho lưu trữ đối tượng và sau đó
kích hoạt cụm Flink để chọn nó.
