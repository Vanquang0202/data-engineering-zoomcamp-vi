#Khắc phục lỗi DuckDB Out of Memory

Nếu bạn gặp lỗi `Out of Memory` khi chạy lệnh xây dựng dbt, đừng hoảng sợ. Đây là một vấn đề phổ biến, đặc biệt là trên các máy có RAM hạn chế. Hướng dẫn này giải thích lý do tại sao điều đó xảy ra và bạn có thể làm gì với nó.

## Tại sao điều này lại xảy ra?

DuckDB là **cơ sở dữ liệu đang xử lý**, có nghĩa là nó chạy bên trong bộ nhớ (RAM) máy tính của bạn chứ không phải trên máy chủ từ xa. Tập dữ liệu taxi NYC mà chúng tôi sử dụng trong dự án này chứa **hàng chục triệu hàng** dữ liệu taxi màu vàng và xanh lục trong 24 tháng. Khi dbt xây dựng mô hình, DuckDB cần tải, chuyển đổi và ghi dữ liệu này (tất cả đều sử dụng RAM cục bộ của bạn).

Một số thao tác tốn nhiều bộ nhớ hơn các thao tác khác:

| Hoạt động | Tại sao nó đắt | Nó xảy ra ở đâu |
|---|---|---|
| `QUALIFY` có chức năng cửa sổ | Yêu cầu sắp xếp và phân vùng toàn bộ tập dữ liệu trong bộ nhớ | `int_trips.sql` (khử trùng lặp) |
| `UNION ALL` trên bàn lớn | Kết hợp hai bộ dữ liệu lớn thành một | `int_trips_unioned.sql` |
| Tạo khóa thay thế (`generate_surrogate_key`) | Tính toán giá trị băm trên toàn bộ tập dữ liệu | `int_trips.sql` |
| `JOIN` trên các bảng dữ kiện lớn | Mở rộng dung lượng bộ nhớ khi làm phong phú chuyến đi bằng các khu vực | `fct_trips.sql` |

## Kiểm tra RAM
có sẵn của bạn
Trước khi khắc phục sự cố, hãy biết bạn đang làm việc với cái gì. Bạn thường có thể tìm thấy điều này trong menu cài đặt của mình.

Theo nguyên tắc chung:

- **RAM 4 GB**: Rất có thể bạn sẽ gặp OOM. Thay vào đó, hãy cân nhắc sử dụng GitHub Codespaces hoặc Cloud Setup.
- **RAM 8 GB**: Bạn có thể gặp OOM trên một số kiểu máy. Điều chỉnh cài đặt bộ nhớ hoặc sử dụng GitHub Codespaces.
- **RAM 16+ GB**: Bạn sẽ ổn với cài đặt mặc định.

## Tùy chọn A: Sử dụng GitHub Codespaces hoặc Cloud Setup

Nếu máy cục bộ của bạn không có đủ RAM, giải pháp đơn giản nhất là tránh chạy DuckDB cục bộ hoàn toàn.

### Không gian mã GitHub

Chạy dự án trong **Không gian mã GitHub**. Bậc miễn phí bao gồm các máy có **4 lõi / RAM 8 GB** và **8 lõi / RAM 16 GB** khả dụng trong hạn mức miễn phí hàng tháng cho tài khoản cá nhân. Một máy 16 GB có thể thoải mái chạy toàn bộ dự án này mà không cần bất kỳ cách giải quyết nào dưới đây.

Để bắt đầu:

1. Đi tới [kho khóa học trên GitHub](https://github.com/DataTalksClub/data-engineering-zoomcamp).
2. Nhấp vào **Code** > **Codespaces** > **Tạo vùng mã trên main**.
3. Chọn loại máy **8 lõi** để có trải nghiệm tốt nhất.

Không gian mã được cài đặt sẵn Python, pip và git nên việc thiết lập là tối thiểu.

### Thiết lập đám mây (BigQuery)

Ngoài ra, hãy sử dụng đường dẫn **Thiết lập đám mây (BigQuery)**. BigQuery chạy trên máy chủ của Google nên RAM cục bộ của bạn không thành vấn đề. Xem [Hướng dẫn thiết lập đám mây](cloud_setup.md).

## Tùy chọn B: Làm cho nó hoạt động trên máy cục bộ
của bạn
Nếu bạn muốn chạy dự án cục bộ, hãy làm theo các bước bên dưới để giảm mức sử dụng bộ nhớ.

### Bước 1: Điều chỉnh cài đặt bộ nhớ DuckDB trong `profiles.yml`

`~/.dbt/profiles.yml` của bạn kiểm soát lượng bộ nhớ mà DuckDB có thể sử dụng. Đây là những gì bạn có thể điều chỉnh:

- **`memory_limit`**: Theo mặc định, DuckDB sẽ cố gắng sử dụng tới 80% RAM hệ thống của bạn. Điều đó nghe có vẻ hợp lý nhưng hệ điều hành, trình duyệt, IDE và các ứng dụng khác của bạn cũng cần bộ nhớ. Nếu DuckDB yêu cầu quá nhiều, hệ điều hành có thể hủy tiến trình - đó là lỗi OOM của bạn. Việc đặt giới hạn rõ ràng (khoảng **50% tổng RAM**) sẽ có đủ chỗ cho mọi thứ khác. Vì vậy, nếu bạn có 8 GB, hãy thử `'4GB'`.
- **`threads`**: Điều này kiểm soát số lượng **mô hình dbt** được xây dựng song song. Việc giảm `threads` xuống `1` có nghĩa là có ít mô hình đồng thời hơn, giúp giảm áp lực bộ nhớ tổng thể.
- **`preserve_insertion_order: false`**: Cho DuckDB biết rằng nó không cần duy trì thứ tự hàng, điều này giúp tiết kiệm bộ nhớ.

### Bước 2: Sử dụng `dbt retry` sau khi gặp lỗi

Nếu `dbt build` của bạn bị lỗi giữa chừng, bạn **không cần phải xây dựng lại mọi thứ từ đầu**. sử dụng:

```bash
dbt retry
```

Lệnh này tiếp tục nơi lần chạy cuối cùng còn lại, chỉ chạy các mô hình bị lỗi hoặc bị bỏ qua. Điều này rất hữu ích khi một lỗi OOM làm chết một mô hình — hãy khắc phục sự cố, sau đó thử lại mà không chạy lại các mô hình đã thành công.

### Bước 3: Xây dựng mô hình có chọn lọc với `--select`

Thay vì xây dựng toàn bộ dự án cùng một lúc, hãy xây dựng từng mô hình một để giảm mức sử dụng bộ nhớ cao nhất:

```bash
dbt build --select stg_yellow_tripdata --target prod
dbt build --select stg_green_tripdata --target prod
dbt build --select int_trips_unioned --target prod
dbt build --select int_trips --target prod
dbt build --select fct_trips --target prod
```

Bằng cách này, DuckDB chỉ cần xử lý một mô hình tại một thời điểm.

### Bước 4: Tận dụng các mô hình gia tăng

Mô hình `fct_trips` trong dự án này đã được định cấu hình là **gia tăng**. Điều này có nghĩa là sau lần xây dựng đầy đủ đầu tiên, các lần chạy tiếp theo chỉ xử lý **bản ghi mới** thay vì xử lý lại toàn bộ tập dữ liệu.

Nếu bản dựng đầy đủ đầu tiên của bạn không thành công do OOM nhưng một số mô hình đã thành công, hãy sử dụng `dbt retry` (Bước 2). Khi `fct_trips` được xây dựng lần đầu tiên, các lần chạy trong tương lai sẽ nhẹ hơn nhiều về bộ nhớ.

## Các phương pháp hay nhất về hiệu suất DuckDB

Những mẹo này đến từ [hướng dẫn hiệu suất chính thức của DuckDB](https://duckdb.org/docs/guides/performance/environment.html):

1. **Đóng các ứng dụng khác**: Trình duyệt, IDE và các ứng dụng khác tranh giành RAM. Đóng những gì bạn không cần trước khi chạy `dbt build`.
2. **Sử dụng ổ SSD**: DuckDB tràn vào đĩa khi hết bộ nhớ. Ổ SSD giúp quá trình tràn vào đĩa này nhanh hơn nhiều so với ổ cứng HDD.
3. **Tránh chạy bên trong Docker** (nếu có thể): Bộ chứa Docker có giới hạn bộ nhớ có thể thấp hơn tổng RAM của hệ thống của bạn. Nếu bạn phải sử dụng Docker, hãy tăng giới hạn bộ nhớ của vùng chứa.

## Vẫn bị kẹt?

Nếu bạn đã thử mọi cách ở trên mà vẫn không thể xây dựng dự án, hãy yêu cầu trợ giúp trong [kênh Slack khóa học](https://datatalks-club.slack.com/). Bao gồm RAM, hệ điều hành và thông báo lỗi chính xác.
