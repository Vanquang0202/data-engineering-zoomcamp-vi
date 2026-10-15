# Bài tập Module 1: Docker và SQL

Trong bài tập này, chúng ta sẽ chuẩn bị môi trường và thực hành
Docker, SQL.

Khi nộp bài, bạn cần cung cấp link đến repository GitHub
hoặc một trang lưu trữ code công khai khác.

Repository này phải chứa code giải bài tập của bạn. 

Nếu lời giải gồm câu lệnh SQL hoặc shell nhưng không được lưu
thành file code (ví dụ file Python), hãy ghi chúng trực tiếp vào
file README của repository.


## Câu hỏi 1. Tìm hiểu lần chạy Docker đầu tiên 

Chạy Docker ở chế độ tương tác với image `python:3.12.8`, dùng entrypoint `bash`.

Phiên bản `pip` trong image là gì?

- 24.3.1
- 24.2.1
- 23.3.1
- 23.2.1


## Câu hỏi 2. Tìm hiểu mạng Docker và docker-compose

Với file `docker-compose.yaml` dưới đây, **pgadmin** cần dùng `hostname` và `port` nào để kết nối đến cơ sở dữ liệu postgres?

```yaml
services:
  db:
    container_name: postgres
    image: postgres:17-alpine
    environment:
      POSTGRES_USER: 'postgres'
      POSTGRES_PASSWORD: 'postgres'
      POSTGRES_DB: 'ny_taxi'
    ports:
      - '5433:5432'
    volumes:
      - vol-pgdata:/var/lib/postgresql/data

  pgadmin:
    container_name: pgadmin
    image: dpage/pgadmin4:latest
    environment:
      PGADMIN_DEFAULT_EMAIL: "pgadmin@pgadmin.com"
      PGADMIN_DEFAULT_PASSWORD: "pgadmin"
    ports:
      - "8080:80"
    volumes:
      - vol-pgadmin_data:/var/lib/pgadmin  

volumes:
  vol-pgdata:
    name: vol-pgdata
  vol-pgadmin_data:
    name: vol-pgadmin_data
```

- postgres:5433
- localhost:5432
- db:5433
- postgres:5432
- db:5432

Nếu có nhiều đáp án đúng, chỉ chọn một đáp án.

##  Chuẩn bị Postgres

Chạy Postgres và nạp dữ liệu theo hướng dẫn trong video.
Chúng ta sẽ dùng dữ liệu chuyến đi taxi green tháng 10/2019:

```bash
wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-10.csv.gz
```

Bạn cũng cần bộ dữ liệu về các khu vực:

```bash
wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv
```

Tải các bộ dữ liệu này và nạp vào Postgres.

Bạn có thể dùng code của khóa học. Hãy chọn Jupyter hoặc script Python
tùy theo cách làm của bạn.

## Câu hỏi 3. Đếm chuyến đi theo khoảng quãng đường

Từ ngày 01/10/2019 (tính cả ngày này) đến trước ngày 01/11/2019, số chuyến thuộc từng khoảng sau **lần lượt** là bao nhiêu?
1. Không quá 1 dặm
2. Trên 1 đến 3 dặm (tính cả 3 dặm),
3. Trên 3 đến 7 dặm (tính cả 7 dặm),
4. Trên 7 đến 10 dặm (tính cả 10 dặm),
5. Trên 10 dặm 

Các lựa chọn:

- 104,802;  197,670;  110,612;  27,831;  35,281
- 104,802;  198,924;  109,603;  27,678;  35,189
- 104,793;  201,407;  110,612;  27,831;  35,281
- 104,793;  202,661;  109,603;  27,678;  35,189
- 104,838;  199,013;  109,645;  27,688;  35,202


## Câu hỏi 4. Chuyến đi dài nhất theo ngày

Ngày đón khách nào có chuyến đi dài nhất?
Hãy dùng thời điểm đón khách để tính toán.

Gợi ý: Với mỗi ngày, chỉ xét một chuyến có quãng đường dài nhất. 

- 2019-10-11
- 2019-10-24
- 2019-10-26
- 2019-10-31


## Câu hỏi 5. Ba khu vực đón khách có tổng tiền lớn nhất

Những khu vực đón khách nào có tổng `total_amount` trên 13.000
(cộng mọi chuyến đi) vào ngày 2019-10-18?

Khi lọc theo ngày, chỉ xét `lpep_pickup_datetime`.
 
- East Harlem North, East Harlem South, Morningside Heights
- East Harlem North, Morningside Heights
- Morningside Heights, Astoria Park, East Harlem South
- Bedford, East Harlem North, Astoria Park


## Câu hỏi 6. Tiền tip lớn nhất

Trong các chuyến đón khách tháng 10/2019 tại khu vực
"East Harlem North", khu vực trả khách nào có khoản tip lớn nhất?

Lưu ý: đây là `tip`, không phải `trip`.

Cần tên khu vực, không phải ID.

- Yorkville West
- JFK Airport
- East Harlem North
- East Harlem South


## Terraform

Trong phần bài tập này, chúng ta sẽ chuẩn bị môi trường bằng cách tạo tài nguyên trên GCP với Terraform.

Cài Terraform trên VM GCP, laptop hoặc GitHub Codespace của bạn. 
Sao chép các file từ repository khóa học
[tại đây](../../../01-docker-terraform/1_terraform_gcp/terraform) sang VM/laptop/GitHub Codespace.

Sửa các file cần thiết để tạo GCP Bucket và BigQuery Dataset.


## Câu hỏi 7. Workflow Terraform

Chuỗi lệnh nào sau đây **lần lượt** mô tả các bước: 
1. Tải plugin provider và thiết lập backend,
2. Tạo kế hoạch thay đổi rồi tự động thực thi,
3. Xóa mọi tài nguyên do terraform quản lý?

Các lựa chọn:
- terraform import, terraform apply -y, terraform destroy
- teraform init, terraform plan -auto-apply, terraform rm
- terraform init, terraform run -auto-approve, terraform destroy
- terraform init, terraform apply -auto-approve, terraform destroy
- terraform import, terraform apply -y, terraform rm


## Nộp bài

* Biểu mẫu nộp bài: https://courses.datatalks.club/de-zoomcamp-2025/homework/hw1
