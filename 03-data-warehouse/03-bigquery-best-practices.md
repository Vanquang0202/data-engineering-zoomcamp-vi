---
video_url: https://www.youtube.com/watch?v=k81mLJVX08w
prev_url: 02-partitioning-vs-clustering.md
next_url: 04-internals-of-bigquery.md
---
# Các phương pháp hay nhất về BigQuery

Đơn vị này là danh sách kiểm tra ngắn về các phương pháp hay nhất để chạy truy vấn trong
BigQuery. Mọi thứ trên đó phục vụ một trong hai mục tiêu: giảm chi phí hoặc
cải thiện hiệu suất truy vấn.

## Giảm chi phí

Hầu hết nỗ lực của chúng tôi đều tập trung vào việc giảm chi phí hoặc hiệu suất truy vấn và cả hai
đều có liên quan với nhau: truy vấn rẻ hơn thường là truy vấn đọc ít dữ liệu hơn.

Slide liệt kê 5 thói quen:

- Tránh `SELECT *`. BigQuery lưu trữ cột dữ liệu: mỗi cột được lưu trữ
riêng biệt, không phải là một phần của hàng. Khi bạn đặt tên cho các cột mình cần,
BigQuery chỉ đọc những cột đó. Với `*`, nó phải đọc tất cả chúng,
ngay cả những thứ bạn chưa bao giờ nhìn vào. Đối với một hoặc hai cột, đây là điểm khác biệt của
giữa việc hầu như không đọc gì và đọc toàn bộ bảng.
- Định giá các truy vấn của bạn trước khi chạy chúng. Giá ước tính hiển thị ở
ở góc trên bên phải của trình chỉnh sửa truy vấn. Hãy xem nó trước khi nhấn nút chạy
.
- Sử dụng các bảng được phân cụm hoặc phân vùng. Chúng tôi đã trình bày chi tiết vấn đề này trong
[bài học trước](02-partitioning-vs-clustering.md): cả hai đều cho phép BigQuery bỏ qua
phần lớn của bảng.
- Thận trọng khi sử dụng tính năng chèn phát trực tuyến. Các phần chèn trực tuyến có thể làm tăng đáng kể chi phí
của bạn.
- Cụ thể hóa kết quả truy vấn theo từng giai đoạn. Giả sử bạn viết một truy vấn với
CTE (một biểu thức bảng chung, mệnh đề `WITH`) và sử dụng lại nó trong
ở một số vị trí. Thay vì tính toán lại mỗi lần, hãy chạy nó một lần, lưu kết quả
vào một bảng và sử dụng bảng đó trong các bước sau.

Một điều nữa: BigQuery lưu trữ kết quả truy vấn. Khi bạn chạy lại cùng một truy vấn
, nó có thể cung cấp kết quả được lưu trong bộ nhớ đệm thay vì tính toán lại.

## Hiệu suất truy vấn

Nhóm phương pháp hay nhất thứ hai là thực hiện truy vấn nhanh chóng.

- Luôn lọc theo cột đã phân vùng, hoặc theo cột đã cluster.
Nếu không thì việc phân vùng và phân cụm mà bạn thiết lập sẽ không có tác dụng gì.
- Không chuẩn hóa dữ liệu của bạn. Trong cơ sở dữ liệu được chuẩn hóa, bạn chia dữ liệu thành nhiều bảng nhỏ
để tránh trùng lặp; trong một nhà kho, bạn thường thực hiện ngược lại
và giữ mọi thứ lại với nhau, do đó, một truy vấn không cần phải nối lại
với chúng.
- Nếu bạn có cấu trúc phức tạp, hãy sử dụng các cột lồng nhau hoặc lặp lại.
Chúng cho phép bạn giữ các dữ liệu liên quan cùng nhau trong một bảng mà không cần
không chuẩn hóa hoàn toàn dữ liệu đó.
- Sử dụng nguồn dữ liệu ngoài hợp lý nhưng đừng lạm dụng. Ví dụ: đọc
từ Google Cloud Storage có thể phải chịu nhiều chi phí hơn so với đọc
từ bộ nhớ của chính BigQuery.
- Giảm dữ liệu trước khi bạn sử dụng trong THAM GIA: lọc trước, tham gia sau.
- Không coi mệnh đề `WITH` là câu lệnh đã chuẩn bị sẵn. Mệnh đề `WITH` đặt tên
là một truy vấn con bên trong một truy vấn, nó không phải là thứ bạn xác định một lần và
tái sử dụng trên các truy vấn.
- Tránh phân chia quá mức các bảng: phân chia dữ liệu của bạn thành nhiều bảng nhỏ
, chẳng hạn như một bảng mỗi ngày. Quá nhiều bảng nhỏ hoạt động kém hơn
so với một bảng được phân vùng.

## Thêm mẹo về hiệu suất

Một vài thứ nữa giúp tăng tốc truy vấn:

- Tránh dùng các hàm JavaScript do người dùng định nghĩa (UDF, các hàm bạn tự viết
bằng SQL).
- Sử dụng các hàm tổng hợp gần đúng thay vì các hàm tổng hợp chính xác, chẳng hạn như
như HyperLogLog++ để đếm các giá trị riêng biệt. Các câu lệnh
- `ORDER` phải là phần cuối cùng trong truy vấn của bạn.
- Tối ưu hóa các kiểu tham gia của bạn. Đặt bảng có số hàng
lớn nhất trước, sau đó là bảng có ít hàng nhất, sau đó là các bảng
còn lại bằng cách giảm kích thước. Bảng lớn nhất được phân bổ đều
trên các nút và bảng tiếp theo sẽ được phát tới tất cả các nút đó.

Lý do thứ tự tham gia không rõ ràng cho đến khi bạn thấy BigQuery
thực sự thực hiện một truy vấn như thế nào. Chúng tôi xem xét điều đó một cách chi tiết trong
[thiết bị tiếp theo](04-internals-of-bigquery.md).
