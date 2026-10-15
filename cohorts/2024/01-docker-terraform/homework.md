## Bài tập về nhà của Mô-đun 1

ATTENTION: Ở cuối biểu mẫu gửi, bạn sẽ được yêu cầu đính kèm liên kết tới kho lưu trữ GitHub của bạn hoặc trang web lưu trữ mã công khai khác. Kho lưu trữ này sẽ chứa mã của bạn để giải bài tập về nhà. Nếu giải pháp của bạn bao gồm mã không ở định dạng tệp (chẳng hạn như truy vấn SQL hoặc lệnh shell), vui lòng đưa chúng trực tiếp vào tệp README trong kho lưu trữ của bạn.

## Docker & SQL

Trong bài tập này chúng ta sẽ chuẩn bị môi trường 
và thực hành với Docker và SQL


## Câu hỏi 1. Biết thẻ docker

Chạy lệnh để lấy thông tin về Docker 

```docker --help```

Now run the command to get help on the "docker build" command:

```docker build --help```

Làm tương tự cho "dockerchạy".

Thẻ nào có nội dung sau? - *Tự động loại bỏ container khi nó thoát ra* 

- `--delete`
- `--rc`
- `--rmc`
- `--rm`


## Câu hỏi 2. Tìm hiểu về docker lần chạy đầu tiên 

Chạy docker với hình ảnh python:3.9 ở chế độ tương tác và điểm vào của bash.
Bây giờ hãy kiểm tra các mô-đun python đã được cài đặt ( sử dụng ```pip list``` ). 

Phiên bản của gói *wheel* là gì?

- 0.42.0
- 1.0.0
- 23.0.1
- 58.1.0


# Chuẩn bị Postgres

Chạy Postgres và tải dữ liệu như trong video Chúng tôi sẽ sử dụng các chuyến đi taxi xanh từ tháng 9 năm 2019:

```wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz```

You will also need the dataset with zones:

```wget https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv```

Tải xuống dữ liệu này và đưa vào Postgres (bằng sổ tay jupyter hoặc bằng đường ống)


## Câu hỏi 3. Đếm hồ sơ 

Tổng cộng có bao nhiêu chuyến taxi đã được thực hiện vào ngày 18 tháng 9 năm 2019?

Mẹo: bắt đầu và kết thúc vào ngày 18/09/2019. 

Hãy nhớ rằng các cột `lpep_pickup_datetime` và `lpep_dropoff_datetime` có định dạng dấu thời gian (ngày và giờ+phút+giây) chứ không phải theo ngày.

- 15767
- 15612
- 15859
- 89009

## Câu 4. Chuyến đi dài nhất trong ngày

Ngày đón khách có khoảng cách chuyến đi dài nhất là ngày nào? Sử dụng thời gian lấy hàng để tính toán.

Mẹo: Với mỗi chuyến đi trong ngày, chúng ta chỉ quan tâm đến chuyến đi có quãng đường dài nhất. 

- 2019-09-18
- 2019-09-16
- 2019-09-26
- 2019-09-21


## Câu hỏi 5. Ba Quận có lượt đón lớn nhất

Hãy xem xét lpep_pickup_datetime trong '2019-09-18' và bỏ qua Quận có Không xác định

3 Quận có lượt đón lớn nhất có total_amount tối đa là gì?
 
- "Brooklyn" "Manhattan" "Queens"
- "Bronx" "Brooklyn" "Manhattan"
- "Bronx" "Manhattan" "Queens" 
- "Brooklyn" "Queens" "Staten Island"


## Câu hỏi 6. Mẹo lớn nhất

Dành cho những hành khách được đón vào tháng 9 năm 2019 trong khu vực có tên Astoria khu vực thả hàng có tiền boa lớn nhất? Chúng tôi muốn tên của khu vực chứ không phải id.

Lưu ý: đó không phải là lỗi đánh máy, đó là `tip` , không phải `trip`

- Central Park
- Jamaica
- JFK Airport
- Long Island City/Queens Plaza



## Terraform

Trong phần bài tập về nhà này, chúng ta sẽ chuẩn bị môi trường bằng cách tạo tài nguyên trong GCP với Terraform.

Trong VM của bạn trên GCP/Laptop/GitHub Codespace hãy cài đặt Terraform. 
Sao chép các tệp từ kho lưu trữ khóa học
[tại đây](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/01-docker-terraform/1_terraform_gcp/terraform) vào Vùng mã VM/Laptop/GitHub của bạn.

Sửa đổi các tệp nếu cần để tạo Nhóm GCP và Bộ dữ liệu truy vấn lớn.


## Câu hỏi 7. Tạo tài nguyên

Sau khi cập nhật tệp main.tf và variable.tf, hãy chạy:

```
terraform apply
```

Dán đầu ra của lệnh này vào biểu mẫu nộp bài tập về nhà.


## Nộp bài giải

* Hình thức nộp bài: https://courses.datatalks.club/de-zoomcamp-2024/homework/hw01
* Có thể nộp bài tập về nhà nhiều lần. Trong trường hợp này, chỉ lần gửi cuối cùng sẽ được sử dụng. 

Hạn chót: 29/01, 23:00 CET
