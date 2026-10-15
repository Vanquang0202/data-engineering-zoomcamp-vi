# Hướng dẫn thiết lập đám mây

Hướng dẫn này hướng dẫn bạn cách thiết lập dbt để làm việc với kho dữ liệu BigQuery mà bạn đã tạo trong Mô-đun 3.

<div align="center">

[![dbt](https://img.shields.io/badge/dbt-FF694B?style=for-the-badge&logo=dbt&logoColor=white)](https://www.getdbt.com/)
[![BigQuery](https://img.shields.io/badge/BigQuery-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)](https://cloud.google.com/bigquery)

</div>

> [!NOTE]
> Hướng dẫn này giả sử bạn đã hoàn thành [Mô-đun 3: Kho dữ liệu](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/03-data-warehouse), trong đó bạn:
> - Đã tạo dự án GCP và bật API BigQuery
> - Đã tạo tài khoản dịch vụ với các quyền BigQuery
> - Đã tìm hiểu cách tải dữ liệu vào BigQuery (trong tập dữ liệu `nytaxi`)
>
> Mô-đun 4 sử dụng **dữ liệu khác** so với Mô-đun 3 (dữ liệu taxi màu xanh lá cây và màu vàng cho năm 2019-2020 thay vì chỉ có màu vàng cho năm 2024). Bạn sẽ tải dữ liệu mới trong [Bước 1](#load-the-taxi-data) bên dưới.

## Bước 1: Xác minh thiết lập BigQuery
của bạn
Trước khi thiết lập dbt Cloud, hãy xác nhận rằng bạn có dữ liệu và thông tin xác thực cần thiết từ Mô-đun 3.

### Kiểm tra tài khoản dịch vụ của bạn

Bạn đã có sẵn tệp khóa JSON của tài khoản dịch vụ từ Mô-đun 3. Hãy đảm bảo tệp đó có các quyền sau:

- **Trình chỉnh sửa dữ liệu BigQuery**
- **Người dùng công việc BigQuery**
- **Người dùng BigQuery**

Nếu bạn cần tạo tài khoản dịch vụ mới hoặc tải xuống khóa mới, hãy làm theo hướng dẫn bên dưới.

### Cách tải xuống khóa JSON của tài khoản dịch vụ

Nếu bạn không có tệp khóa JSON hoặc cần tải xuống tệp mới:

1. Đi tới [Google Cloud Console](https://console.cloud.google.com/)

2. Điều hướng đến **IAM & Quản trị viên** > **Tài khoản dịch vụ**
- Hoặc sử dụng thanh tìm kiếm và nhập "Tài khoản dịch vụ"

3. Tìm tài khoản dịch vụ của bạn trong danh sách
- Nó sẽ có dạng: `service-account-name@project-id.iam.gserviceaccount.com`
- Nếu bạn chưa có tài khoản dịch vụ, hãy nhấp vào **+ TẠO TÀI KHOẢN DỊCH VỤ** và:
- Nhập tên (ví dụ: `dbt-bigquery-service-account`)
- Nhấp vào **TẠO VÀ TIẾP TỤC**
- Thêm các vai trò sau:
- **Quản trị viên BigQuery** (hoặc tối thiểu: BigQuery Data Editor, BigQuery Job User, BigQuery User)
- Nhấp vào **TIẾP TỤC** > **XONG**

4. Nhấp vào tên tài khoản dịch vụ của bạn để mở chi tiết

5. Chuyển đến tab **KEYS**

6. Nhấp vào **THÊM KHÓA** > **Tạo khóa mới**

7. Chọn **JSON** làm loại khóa

8. Nhấp vào **TẠO**

9. Tệp khóa JSON sẽ tự động tải xuống máy tính của bạn
- Lưu tệp ở vị trí an toàn
- **Không bao giờ cam kết tệp này với Git hoặc chia sẻ công khai** - nó chứa thông tin xác thực để truy cập tài nguyên GCP của bạn

Tệp JSON đã tải xuống sẽ trông giống như thế này:

```json
{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "service-account-name@project-id.iam.gserviceaccount.com",
  ...
}
```

Bạn sẽ sử dụng tệp JSON này trong Bước 4 để kết nối dbt Cloud với BigQuery.

### Tải dữ liệu taxi

Mô-đun này sử dụng **dữ liệu taxi màu vàng và xanh lục cho năm 2019-2020**, khác với dữ liệu bạn đã tải trong Mô-đun 3. Sử dụng phương pháp tương tự mà bạn đã học trong Mô-đun 3, hãy tải dữ liệu sau vào tập dữ liệu BigQuery `nytaxi`:

- **Hồ sơ chuyến đi taxi màu vàng** cho tất cả các tháng năm 2019 và 2020
- **Hồ sơ chuyến đi taxi xanh** cho tất cả các tháng năm 2019 và 2020

> [!QUAN TRỌNG]
> Tải xuống dữ liệu từ [Kho lưu trữ dữ liệu DataTalksClub NYC TLC](https://github.com/DataTalksClub/nyc-tlc-data/releases), **không** từ trang web chính thức của NYC TLC. Trang web chính thức đã được cập nhật trở lại trong nhiều năm, vì vậy dữ liệu của nó khác với dữ liệu dựa trên câu trả lời bài tập về nhà.

Sau khi tải, hãy xác minh dữ liệu của bạn:

1. Đi tới [BigQuery Console](https://console.cloud.google.com/bigquery)
2. Trong bảng Explorer ở bên trái, hãy mở rộng dự án
của bạn 3. Bạn sẽ thấy tập dữ liệu `nytaxi`
4. Mở rộng tập dữ liệu `nytaxi` - bạn sẽ thấy các bảng:
- `green_tripdata`
- `yellow_tripdata`

### Lưu ý vị trí tập dữ liệu của bạn

Khi tạo tập dữ liệu BigQuery trong Mô-đun 3, bạn đã chọn một vị trí (ví dụ: `US`, `EU`, `us-central1`). Bạn sẽ cần sử dụng cùng một vị trí khi định cấu hình dbt.

**Để kiểm tra vị trí tập dữ liệu của bạn:**
1. Trong Bảng điều khiển BigQuery, hãy nhấp vào tập dữ liệu `nytaxi`
2. Tìm **Vị trí dữ liệu** trong chi tiết tập dữ liệu

## Bước 2: Đăng ký dbt Platform

Nền tảng dbt là môi trường phát triển dựa trên đám mây của dbt với IDE web, bộ lập lịch và các tính năng cộng tác. dbt cung cấp **gói dành cho nhà phát triển miễn phí**. Điều này là quá đủ để học dbt và theo dõi khóa học.

## Bước 3: Tạo dự án dbt mới

Bây giờ bạn sẽ tạo một dự án dbt mới từ đầu trong dbt Cloud.

1. Điều hướng đến **Cài đặt tài khoản** (biểu tượng bánh răng ở góc trên bên phải) và nhấp vào **+ Dự án mới**

2. Nhập tên dự án:
- Tên dự án: `taxi_rides_ny`

3. Nhấp vào **Tiếp tục**

## Bước 4: Định cấu hình kết nối BigQuery

Sau khi nhấp vào **Tiếp tục** ở bước trước, dbt Cloud sẽ nhắc bạn định cấu hình kết nối kho dữ liệu của mình.

> [!TIP]
> Nếu không được tự động chuyển sang phần thiết lập kết nối, bạn cũng có thể định cấu hình nó từ **Cài đặt tài khoản** > **Dự án** > **taxi_rides_ny** > **Kết nối**.

### Tải lên tài khoản dịch vụ JSON

1. Đối với loại kết nối, hãy chọn **BigQuery**

2. Nhấp vào **Tải lên tệp JSON của tài khoản dịch vụ**

3. Chọn tệp khóa JSON của tài khoản dịch vụ từ Mô-đun 3

4. dbt sẽ tự động trích xuất:
- ID dự án GCP của bạn
- Thông tin xác thực

### Định cấu hình cài đặt kết nối

1. **Bộ dữ liệu**: Nhập `dbt_prod`
- Đây là tên lược đồ cơ sở nơi dbt sẽ tạo bộ dữ liệu
- dbt sẽ sắp xếp các mô hình của bạn thành các lược đồ như:
- `dbt_prod_staging` - dành cho các mô hình dàn dựng
- `dbt_prod_intermediate` - dành cho các mô hình trung gian
- `dbt_prod_marts` - dành cho bảng phân tích cuối cùng

2. **Vị trí**: Chọn cùng vị trí với tập dữ liệu `nytaxi` của bạn từ Mô-đun 3
- Ví dụ: `US`, `EU` hoặc `us-central1`
- **Vị trí này phải khớp với vị trí tập dữ liệu nytaxi của bạn**
- Bạn có thể tìm thấy vị trí này trong **Tùy chọn Cài đặt** hoặc **Cài đặt nâng cao** tùy thuộc vào phiên bản giao diện người dùng
của bạn
3. **Hết thời gian**: `300` giây

4. **Số byte tối đa được thanh toán**: (tùy chọn)
- Để trống không giới hạn, HOẶC
- Đặt giới hạn như `1000000000` (1 GB) để ngăn các truy vấn chạy trốn

### Kiểm tra kết nối

1. Nhấp vào **Kiểm tra kết nối**

2. Bạn sẽ thấy thông báo thành công: "Kiểm tra kết nối thành công"

3. Nhấp vào **Tiếp tục**

## Bước 5: Thiết lập kho lưu trữ
của bạn
dbt Cloud cần kho lưu trữ Git để lưu trữ mã dự án của bạn. Bạn có hai lựa chọn:

- Để dbt quản lý kho lưu trữ (Được khuyến nghị cho người mới bắt đầu)
- Kết nối Kho lưu trữ GitHub của riêng bạn (Được khuyến nghị cho sản xuất)

Không quan trọng bạn thích cái nào hơn cho khóa học này.

## Bước 6: Xác minh môi trường phát triển
của bạn
### Môi trường trong dbt là gì?

Trong dbt, **môi trường** xác định các bối cảnh khác nhau nơi quá trình chuyển đổi dữ liệu của bạn chạy:

- **Môi trường phát triển**: Không gian làm việc cá nhân của bạn để xây dựng và thử nghiệm các mô hình
- Sử dụng thông tin xác thực cá nhân của bạn
- Tạo các lược đồ tạm thời với tên của bạn (ví dụ: `dbt_<your_name>`)
- Các thay đổi chỉ ảnh hưởng đến công việc của bạn chứ không ảnh hưởng đến sản xuất
- Được sử dụng khi làm việc trong dbt Cloud IDE

- **Môi trường triển khai**: Không gian làm việc sản xuất nơi các mô hình cuối cùng chạy theo lịch
- Sử dụng thông tin xác thực tài khoản dịch vụ
- Tạo sơ đồ sản xuất (ví dụ: `dbt_prod_staging`, `dbt_prod_marts`)
- Được sử dụng bởi các công việc đã lên lịch để cập nhật kho dữ liệu của bạn

Hãy nghĩ về nó giống như có một thư mục nháp (phát triển) và một thư mục đã xuất bản (triển khai) cho mã phân tích của bạn.

### Kiểm tra môi trường phát triển của bạn

dbt Cloud **tự động tạo môi trường phát triển** khi bạn thiết lập dự án. Bạn không cần phải tạo thủ công.

Để xác minh nó đã được tạo:

1. Điều hướng đến **Triển khai** > **Môi trường** trong thanh điều hướng trên cùng
2. Bạn sẽ thấy môi trường **Phát triển** đã được liệt kê

### Tùy chỉnh thông tin xác thực phát triển của bạn (Tùy chọn)

Nếu bạn cần thay đổi cách dbt kết nối với BigQuery trong quá trình phát triển hoặc điều chỉnh lược đồ phát triển của mình:

1. Nhấp vào biểu tượng hồ sơ của bạn (góc dưới bên trái) > **Hồ sơ của bạn** > **Thông tin xác thực**
2. Chọn thông tin xác thực được liên kết với dự án của bạn
3. Từ đây bạn có thể cập nhật:
- **Lược đồ phát triển**: Nơi các mô hình phát triển cá nhân của bạn sẽ được tạo
- dbt tự động đề xuất: `dbt_<your_name>` (ví dụ: `dbt_john_smith`)
- Lược đồ này tách biệt với sản xuất (`dbt_prod`)
- **Tên mục tiêu**: Để nguyên là `dev` (mặc định)

## Bước 7: Bắt đầu phát triển

Khi dự án, kết nối và kho lưu trữ của bạn được định cấu hình, bạn đã sẵn sàng bắt đầu xây dựng các mô hình dbt.

1. Nhấp vào **Bắt đầu phát triển trong Studio IDE**
- Nếu bạn không thấy tùy chọn này, hãy điều hướng đến **Develop** trong thanh điều hướng trên cùng

2. dbt Cloud sẽ khởi tạo không gian làm việc của bạn (việc này có thể mất một phút)

3. Sau khi IDE tải, bạn sẽ có một dự án mới sẵn sàng để phát triển!

## Tài nguyên bổ sung

* [Tài liệu BigQuery](https://cloud.google.com/bigquery/docs)
* [Tài liệu dbt](https://docs.getdbt.com/docs/cloud/about-cloud/dbt-cloud-features)
* [Các phương pháp hay nhất về BigQuery](https://cloud.google.com/bigquery/docs/best-practices)
* [Từ điển dữ liệu taxi NYC](https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf)
