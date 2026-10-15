---
video_url: https://www.youtube.com/watch?v=2dYDS4OQbT0
prev_url: 03-dbt-core-vs-dbt-cloud.md
next_url: 05-dbt-sources.md
---
#dbt Cấu trúc dự án

> 📄 Tài liệu chính thức: [Giới thiệu về các dự án dbt](https://docs.getdbt.com/docs/build/projects)
> 📄 Các phương pháp hay nhất: [Cách chúng tôi cấu trúc các dự án dbt của mình](https://docs.getdbt.com/best-practices/how-we-structure/1-guide-overview)

Khi bạn chạy `dbt init`, dbt sẽ tự động tạo một tập hợp các tệp và thư mục. Video này đi qua từng cái và giải thích mục đích của nó. Cấu trúc bên dưới áp dụng cho cả dbt Core và dbt Cloud (tệp cơ sở dữ liệu DuckDB và thư mục `data/` là các tạo phẩm chỉ cục bộ và có thể bỏ qua tại đây).


---

## Tệp và thư mục cấp cao nhất

### `analysis/`
- Nơi dành cho **tập lệnh SQL đặc biệt** mà bạn không nhất thiết muốn chia sẻ với các bên liên quan
- Không được mọi người sử dụng nhiều nhưng hữu ích cho những việc như **báo cáo chất lượng dữ liệu** hoặc **kiểm tra hành chính**
- Hãy coi nó như một bảng ghi nhớ — nếu bạn muốn điều tra mức độ tồi tệ của một vấn đề về chất lượng dữ liệu, hãy sử dụng SQL kịch bản ở đây

### `dbt_project.yml`
- **Tệp quan trọng nhất trong dự án dbt**
- Mỗi khi bạn chạy lệnh dbt, dbt sẽ tìm tệp này trước tiên — nếu thiếu, lệnh đó sẽ bị lỗi
- Nội dung chính trong đó:
- Tên dự án
- Tên hồ sơ (phải khớp với `profiles.yml` của bạn - quan trọng đối với người dùng dbt Core)
- Vật chất hóa mặc định
- Biến
- Cũng là nơi để đặt cấu hình và mặc định cho toàn dự án

> 📄 [tham chiếu dbt_project.yml](https://docs.getdbt.com/reference/dbt_project.yml)

### `macros/`
- Macro hoạt động giống như **các hàm có thể tái sử dụng** (tương tự như các hàm Python hoặc UDF)
- Sử dụng chúng khi bạn thấy mình **lặp lại cùng một logic SQL** ở nhiều nơi hoặc khi bạn muốn **đóng gói một đoạn logic** ở một nơi
- Lợi ích:
- Dễ kiểm tra hơn (bạn đang kiểm tra một phần nhỏ, tách biệt)
- Nếu định nghĩa thay đổi, bạn chỉ cập nhật nó ở một nơi
- Các trường hợp sử dụng phổ biến:
- **Chuyển đổi lịch** (ví dụ: chuyển đổi ngày tiêu chuẩn sang lịch tài chính của công ty)
- **Thuế suất hoặc định nghĩa quy định** có thể thay đổi theo thời gian
- Bất kỳ logic nghiệp vụ nào có thể tái sử dụng và không bị trùng lặp trên các mô hình

> 📄 [Jinja và macro](https://docs.getdbt.com/docs/build/jinja-macros)

### `models/`
- **thư mục quan trọng nhất** — đây là nơi chứa tất cả logic chuyển đổi SQL của bạn
- dbt khuyên bạn nên chia nó thành **ba thư mục con** (xem bên dưới)

### `README.md`
- Tài liệu dự án tiêu chuẩn — điều đầu tiên ai đó nhìn thấy khi họ mở dự án của bạn
- dbt tạo một tài liệu mặc định, nhưng hầu hết các nhóm đều tùy chỉnh nó
- Những điều thú vị cần bao gồm:
- Cách chạy dự án
- Cho dù bạn cần thông tin xác thực hay giới thiệu
- Thông tin liên hệ
- Hướng dẫn cài đặt/thiết lập

### `seeds/`
- Nơi **tải lên tệp CSV hoặc tệp phẳng** và nhập chúng dưới dạng mô hình dbt trong cơ sở dữ liệu của bạn
- Được coi là cách tiếp cận **nhanh và bẩn** — nếu bạn có tùy chọn này, tốt hơn hết bạn nên tải dữ liệu đúng cách tại nguồn
- Hữu ích cho:
- **Tra cứu bảng**
- Thử nghiệm nhanh hoặc nguyên mẫu
- Hiển thị nội dung nào đó cho bên liên quan trước khi cam kết hoàn toàn tải dữ liệu
- Sử dụng khi bạn không có quyền phù hợp hoặc dữ liệu dự kiến sẽ thay đổi thường xuyên trong quá trình thử nghiệm

> 📄 [Hạt giống](https://docs.getdbt.com/docs/build/seeds)

### `snapshots/`
- Giải quyết một vấn đề cụ thể: một bảng nguồn có một cột **ghi đè lên chính nó**, nhưng bạn cần **giữ lại lịch sử**
- Ví dụ: một bảng `orders` có cột `current_status` chỉ hiển thị trạng thái mới nhất. Đối với phân tích, bạn muốn biết *khi* mỗi trạng thái thay đổi
- Cách thức hoạt động: một ảnh chụp nhanh sẽ chụp **"hình ảnh" của một bảng tại một thời điểm**. Mỗi lần bạn chạy nó, nếu một giá trị đã thay đổi, thì một hàng mới sẽ được ghi lại bằng dấu thời gian — mà không ghi đè giá trị trước đó
- Giống như hạt giống, đây là **cách giải quyết** — lý tưởng nhất là bạn nên giải quyết vấn đề này tại nguồn. Nhưng nếu bạn không kiểm soát nguồn, ảnh chụp nhanh hoạt động tốt

> 📄 [Ảnh chụp nhanh](https://docs.getdbt.com/docs/build/snapshots)

### `tests/`
- Nơi dành cho **các bài kiểm tra đơn lẻ** được viết dưới dạng xác nhận SQL
- Logic rất đơn giản: **nếu truy vấn trả về nhiều hơn 0 hàng, quá trình xây dựng dbt không thành công**
- Ví dụ từ khóa học: cần có một khách hàng để đảm bảo rằng dấu thời gian của phương tiện luôn hoạt động chính xác trong 24 giờ mỗi ngày. Truy vấn kiểm tra được kiểm tra vào bất kỳ ngày nào có tổng số giờ lệch khỏi 24 — phát hiện các lỗi logic như bộ lọc ngẫu nhiên hoặc kết nối kém sớm
- Đây là một trong nhiều cách để kiểm tra trong dbt, nhưng các kiểm tra đơn lẻ đặc biệt tốt cho **quy tắc kinh doanh tùy chỉnh** không phù hợp với kiểm tra lược đồ tiêu chuẩn

> 📄 [Kiểm tra dữ liệu (số ít & chung)](https://docs.getdbt.com/docs/build/data-tests)

---

## Các thư mục con `models/`

dbt đề xuất tổ chức các mô hình thành ba lớp:

### `staging/`
- Chứa hai thứ:
- **Định nghĩa nguồn** — cho dbt biết dữ liệu thô của bạn nằm ở đâu trong cơ sở dữ liệu
- **Mô hình dàn dựng** — một **bản sao 1:1** của mỗi bảng nguồn chỉ **được áp dụng **làm sạch tối thiểu**
- Làm sạch tối thiểu có nghĩa là những thứ như:
- Sửa các kiểu dữ liệu
- Đổi tên cột
- Lọc ra các hàng trống rõ ràng
- Xóa các cột không cần thiết
- Chuẩn hóa giá trị
- Giữ nguyên **1:1** — cùng số hàng và cột như nguồn thô. Việc phá vỡ quy tắc này đôi khi thuận tiện nhưng phải là ngoại lệ

### `intermediate/`
- Mọi thứ **không phải là thô** và **chưa sẵn sàng để hiển thị** cho người dùng cuối
- Tất cả dành cho:
- Kết hợp phức hợp
- Làm sạch hoặc tiêu chuẩn hóa nặng nề
- Xử lý chất lượng dữ liệu
- Không nghiêm ngặt hướng dẫn về những gì diễn ra ở đây - nếu nó không vừa khít với dàn dựng hoặc siêu thị, thì nó thuộc về
trung gian
### `marts/`
- Nơi tất cả các bảng **cuối cùng, sẵn sàng sử dụng** hoạt động
- Nếu ở siêu thị, nó **sẵn sàng cho người dùng cuối**
- Trong một dự án dbt được quản lý tốt, **chỉ các bảng marts mới được hiển thị** với các công cụ BI, nhà phân tích và các bên liên quan kinh doanh — không có gì khác
- Thường chứa:
- Các bảng sẵn sàng cho bảng thông tin
- Các bảng rõ ràng, được mô hình hóa đúng cách
- Thường gắn dấu sao cho lược đồ nhưng không nhất thiết phải là

---

## Lưu ý về quy ước

Cấu trúc `staging → intermediate → marts` là khuyến nghị của dbt nhưng không bắt buộc. Người hướng dẫn đã thấy các đội sử dụng:
- **Kiến trúc huy chương** đặt tên: `bronze`, `silver`, `gold`
- Các lớp được đánh số: `first`, `second`, `third`, `last`
- Các quy ước tùy chỉnh khác

Nếu tổ chức của bạn đã có một quy ước, hãy làm theo nó. Mặt khác, hãy tuân theo cấu trúc mặc định của dbt - nó được tính toán kỹ lưỡng và khóa học này sử dụng những gì.
