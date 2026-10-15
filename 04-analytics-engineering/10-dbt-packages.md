---
video_url: https://www.youtube.com/watch?v=KfhUA9Kfp8Y
prev_url: 09-dbt-tests.md
next_url: 11-dbt-commands.md
---
# Gói dbt

> 📄 Tài liệu chính thức: [Gói](https://docs.getdbt.com/docs/build/packages)
> 📄 Trung tâm gói: [hub.getdbt.com](https://hub.getdbt.com)

Một trong những điều khiến cộng đồng dbt trở nên mạnh mẽ là các gói. Gói dbt về cơ bản là một dự án dbt độc lập — nó có macro, thử nghiệm, mô hình, nguồn riêng — nhưng thay vì tự mình sử dụng, bạn phân phối nó để người khác có thể thả nó vào dự án của riêng họ. Hãy nghĩ đến các thư viện Python, nhưng đối với dbt. Video này bao gồm các gói hữu ích nhất hiện có cũng như cách cài đặt và sử dụng chúng.


---

## Các gói đáng biết về

### dbt-utils

Cái lớn. Được bảo trì bởi dbt Labs nên nó được bảo quản tốt và an toàn khi sử dụng. Nó gói rất nhiều tiện ích SQL phổ biến dưới dạng macro - những thứ như tạo khóa thay thế, sao chép, xoay vòng, phân chia an toàn, trích xuất các tham số URL. Những thứ mà hầu hết chúng ta đều đã tự viết vào một lúc nào đó.

Điểm mấu chốt thực sự là **khả năng tương thích giữa nhiều cơ sở dữ liệu**. Các macro dbt-utils biên dịch theo phương ngữ SQL chính xác tùy thuộc vào kho của bạn. Vì vậy, cùng một macro hoạt động trên BigQuery, DuckDB, Snowflake, v.v. — không cần phải duy trì các phiên bản mã riêng biệt.

### dbt-codegen

Một cách tiết kiệm thời gian đáng kể cho quá trình xay YAML. Codegen thực hiện hai việc:

- **YAML from SQL** — trỏ nó vào một mô hình hoặc nguồn và nó tự động tạo `schema.yml` với tất cả các cột được liệt kê. Không còn phải gõ thủ công hàng trăm tên cột.
- **SQL từ YAML** — ngược lại. Cung cấp cho nó một thông số YAML và nó tạo ra một tệp SQL mô hình dàn dựng theo các quy ước dbt (CTE đơn để đổi tên, đặt tên tệp thích hợp, v.v.).

### dbt-người đánh giá dự án

Chấm điểm dự án dbt của bạn theo các phương pháp hay nhất. Phù hợp cho những nhóm muốn kiểm tra nhanh chóng xem liệu họ có tuân thủ các quy ước hay không.

### dbt-audit-helper

Tiện dụng khi bạn tái cấu trúc. Nó so sánh mô hình cũ với mô hình mới và xác nhận rằng chúng tạo ra kết quả giống nhau - cùng cột, cùng số hàng, cùng giá trị. Loại bỏ sự lo lắng khi viết lại SQL hiện có.

### dbt-kỳ vọng

Đây là điều khiến các bài kiểm tra tùy chỉnh gần như không cần thiết. Đó là một thư viện khổng lồ gồm các bài kiểm tra chung được tạo sẵn bao gồm hầu hết mọi xác nhận mà bạn có thể nghĩ tới — số hàng, phạm vi giá trị, cách viết hoa nhất quán, so khớp biểu thức chính quy, đẳng thức gần đúng, v.v. Trong thực tế, nếu bạn cần kiểm tra một cái gì đó, rất có thể kỳ vọng dbt đã có nó.

> 📄 [dbt-kỳ vọng trên Package Hub](https://hub.getdbt.com/calogica/dbt_expectations/latest/)

### Gói dành riêng cho kho

Trung tâm có nhiều gói được điều chỉnh cho phù hợp với các nền tảng cụ thể — Snowflake, BigQuery, v.v. Các gói này thường đi kèm với các mô hình hoặc macro để theo dõi chi tiêu, đánh giá các phương pháp hay nhất, áp dụng các ràng buộc hoặc làm việc với các tính năng dành riêng cho nền tảng như chế độ xem ngữ nghĩa.

---

## Một lưu ý về độ tin cậy

Các gói trên dbt Hub đã trải qua quá trình kiểm tra của dbt Labs — nhìn chung chúng an toàn khi sử dụng. Các gói bạn tìm thấy trôi nổi trên GitHub nhưng không có trên Hub? Hãy xem xét kỹ hơn những gì họ thực sự làm trước khi đưa họ vào dự án của bạn.

---

## Cách cài đặt gói — bản demo

Video hướng dẫn cài đặt dbt-utils và sử dụng nó để tạo khóa thay thế. Đây là quy trình làm việc:

### 1. Tạo packages.yml

Ở thư mục gốc của dự án dbt của bạn (cùng cấp với `dbt_project.yml`), hãy tạo một tệp có tên `packages.yml`. Khai báo gói và ghim phiên bản.

```yaml
packages:
  - package: dbt-labs/dbt_utils
    version: 1.1.1
```

### 2. Chạy `dbt deps`

Điều này tải xuống và cài đặt gói. Sau khi chạy, có hai thứ xuất hiện:

- Tệp `package-lock.yml` — chứa hàm băm của chính xác những gì đã được cài đặt. Cam kết điều này với việc kiểm soát phiên bản để mọi người trong nhóm của bạn có được các phiên bản giống nhau.
- Thư mục `dbt_packages/` — đây là nơi chứa mã gói đã cài đặt. Theo mặc định, nó bị bỏ qua git (bạn không muốn đưa mã nguồn của người khác vào kho lưu trữ của mình), nhưng bạn có thể duyệt nó nếu bạn tò mò về cách các macro hoạt động.

### 3. Sử dụng

Sau khi cài đặt, macro của gói sẽ có sẵn ngay lập tức. Bạn gọi chúng bằng cú pháp Jinja tiêu chuẩn, thêm tiền tố vào tên gói.

**Trước (khóa thay thế thủ công):**
```sql
select
    -- Manual concatenation approach
    concat(
        cast(vendorid as string), '-',
        cast(lpep_pickup_datetime as string)
    ) as tripid,
    vendorid,
    pickup_datetime
from {{ source('staging', 'green_tripdata') }}
```

**Sau (sử dụng dbt_utils.generate_surrogate_key):**
```sql
select
    -- Clean, cross-database macro
    {{ dbt_utils.generate_surrogate_key(['vendorid', 'lpep_pickup_datetime']) }} as tripid,
    vendorid,
    pickup_datetime
from {{ source('staging', 'green_tripdata') }}
```

Thế thôi. Macro xử lý phần còn lại — biên dịch thành SQL phù hợp cho bất kỳ kho nào bạn đang nhắm mục tiêu (hàm băm MD5 cho BigQuery, hàm băm cho Snowflake, v.v.).

> 📄 [dbt deps command — docs](https://docs.getdbt.com/reference/commands/deps)
