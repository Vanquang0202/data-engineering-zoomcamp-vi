##Bài tập tuần 1

Trong bài tập về nhà này, chúng ta sẽ chuẩn bị môi trường
và thực hành với terraform và SQL


## Câu hỏi 1. Google Cloud SDK

Cài đặt Google Cloud SDK. Phiên bản bạn có là gì?

Để có phiên bản, hãy chạy `gcloud --version`

## Tài khoản Google Cloud

Tạo một tài khoản trong Google Cloud và tạo một dự án.


## Câu 2. Terraform

Bây giờ hãy cài đặt terraform và vào thư mục terraform (`week_1_basics_n_setup/1_terraform_gcp/terraform`)

Sau đó chạy

* `terraform init`
* `terraform plan`
* `terraform apply`

Áp dụng kế hoạch và sao chép kết quả đầu ra (sau khi chạy `apply`) vào biểu mẫu.

Nó phải là toàn bộ đầu ra - kể từ thời điểm bạn gõ `terraform init` cho đến cuối cùng.

## Chuẩn bị Postgres

Chạy Postgres và tải dữ liệu như trong video

Chúng tôi sẽ sử dụng các chuyến taxi màu vàng từ tháng 1 năm 2021:

```bash
wget https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2021-01.csv
```

Bạn cũng sẽ cần tập dữ liệu có các vùng:

```bash 
wget https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv
```

Tải xuống dữ liệu này và đặt nó vào Postgres

## Câu 3. Đếm bản ghi

Có bao nhiêu chuyến taxi vào ngày 15 tháng 1?

Chỉ xem xét các chuyến đi bắt đầu vào ngày 15 tháng 1.


## Câu 4. Tip lớn nhất mỗi ngày

Tìm mẹo lớn nhất cho mỗi ngày.
Vào ngày nào là số tiền boa lớn nhất trong tháng 1?

Sử dụng thời gian lấy hàng để tính toán.

(lưu ý: không phải lỗi đánh máy mà là "tip" chứ không phải "trip")


## Câu 5. Điểm đến phổ biến nhất

Điểm đến phổ biến nhất của hành khách đón
ở công viên trung tâm vào ngày 14 tháng 1 là gì?

Sử dụng thời gian lấy hàng để tính toán.

Nhập tên vùng (không phải id). Nếu không xác định được tên vùng (thiếu), hãy ghi "Unknown"


## Câu 6. Vị trí đắt giá nhất

Cặp xe đón-trả khách có giá trung bình
lớn nhất cho một chuyến đi (được tính dựa trên `total_amount`) là bao nhiêu?

Nhập hai tên vùng cách nhau bằng dấu gạch chéo

Ví dụ:

"Vịnh Jamaica / Đông Clinton"

Nếu bất kỳ tên vùng nào không xác định (thiếu), hãy viết "Không xác định". Ví dụ: "Không xác định / Clinton East".


## Đệ trình giải pháp

* Hình thức gửi: https://forms.gle/yGQrkgRdVbiFs8Vd7
* Bạn có thể gửi bài tập về nhà nhiều lần. Trong trường hợp này, chỉ lần gửi cuối cùng sẽ được sử dụng.

Hạn chót: 26 tháng 1 (Thứ Tư), 22:00 CET


## Giải pháp

Đây là lời giải cho câu hỏi 3-6: [video](https://www.youtube.com/watch?v=HxHqH2ARfxM&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb)

