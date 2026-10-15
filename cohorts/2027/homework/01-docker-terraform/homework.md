# Bài tập Module 1: Docker và SQL [BẢN NHÁP]

> [!NOTE]
> Đây là bản nháp được chuyển từ khóa 2026. Câu hỏi, bộ dữ liệu và
> hạn nộp sẽ được cập nhật trước khi module bắt đầu.

Trong bài tập này, chúng ta sẽ chuẩn bị môi trường và thực hành
Docker, SQL.

Khi nộp bài, bạn cần cung cấp link đến repository GitHub
hoặc một trang lưu trữ code công khai khác.

Repository này phải chứa code giải bài tập của bạn.

Nếu lời giải gồm câu lệnh SQL hoặc shell nhưng không được lưu
thành file code (ví dụ file Python), hãy ghi chúng trực tiếp vào
file README của repository.


## Câu hỏi 1. Tìm hiểu Docker image

Chạy Docker với image `python:3.13`. Dùng entrypoint `bash` để tương tác với container.

Phiên bản `pip` trong image là gì?

- 25.3
- 24.3.1
- 24.2.1
- 23.3.1

> Lưu ý: nếu thực hiện sau khi khóa học kết thúc, phiên bản thực tế có thể khác các lựa chọn trên. Hãy dùng giá trị bạn nhận được. Các lựa chọn phản ánh phiên bản tại thời điểm khóa học diễn ra.


## Câu hỏi 2. Tìm hiểu mạng Docker và docker-compose

Với file `docker-compose.yaml` dưới đây, pgadmin cần dùng `hostname` và `port` nào để kết nối đến cơ sở dữ liệu postgres?

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

Nếu có nhiều đáp án đúng, bạn có thể chọn bất kỳ đáp án nào. 


## Chuẩn bị dữ liệu

Tải dữ liệu chuyến đi taxi green tháng 11/2025:

```bash
wget https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet
```

Bạn cũng cần bộ dữ liệu về các khu vực:

```bash
wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv
```

## Câu hỏi 3. Đếm các chuyến đi ngắn

Trong các chuyến đi tháng 11/2025 (`lpep_pickup_datetime` từ '2025-11-01' đến trước '2025-12-01'), có bao nhiêu chuyến có `trip_distance` không quá 1 dặm?

- 7,853
- 8,007
- 8,254
- 8,421


## Câu hỏi 4. Chuyến đi dài nhất theo ngày

Ngày đón khách nào có chuyến đi dài nhất? Chỉ xét các chuyến có `trip_distance` dưới 100 dặm để loại trừ dữ liệu lỗi.

Hãy dùng thời điểm đón khách để tính toán.

- 2025-11-14
- 2025-11-20
- 2025-11-23
- 2025-11-25


## Câu hỏi 5. Khu vực đón khách có tổng tiền lớn nhất

Khu vực đón khách nào có tổng `total_amount` (cộng tất cả chuyến đi) lớn nhất vào ngày 18/11/2025?

- East Harlem North
- East Harlem South
- Morningside Heights
- Forest Hills


## Câu hỏi 6. Tiền tip lớn nhất

Trong các chuyến đón khách tại khu vực "East Harlem North" tháng 11/2025, khu vực trả khách nào có khoản tip lớn nhất?

Lưu ý: đây là `tip`, không phải `trip`. Cần tên khu vực, không phải ID.

- JFK Airport
- Yorkville West
- East Harlem North
- LaGuardia Airport


## Terraform

Trong phần bài tập này, chúng ta sẽ chuẩn bị môi trường bằng cách tạo tài nguyên trên GCP với Terraform.

Cài Terraform trên VM GCP, laptop hoặc GitHub Codespace của bạn.
Sao chép các file từ repository khóa học
[tại đây](terraform) sang VM/laptop/GitHub Codespace.

Sửa các file cần thiết để tạo GCP Bucket và BigQuery Dataset.


## Câu hỏi 7. Workflow Terraform

Chuỗi lệnh nào sau đây lần lượt mô tả các bước:
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

* Biểu mẫu nộp bài: https://courses.datatalks.club/de-zoomcamp-2026/homework/hw1


## Chia sẻ quá trình học công khai

Chúng tôi khuyến khích mọi người chia sẻ những gì mình đã học. Cách học này gọi là "learning in public".

### Vì sao nên chia sẻ quá trình học?

- Trách nhiệm với bản thân: Chia sẻ tiến độ giúp bạn duy trì cam kết và động lực
- Phản hồi: Cộng đồng có thể góp ý và giúp sửa sai
- Kết nối: Bạn có thể gặp những người cùng chí hướng và cộng tác viên tiềm năng
- Ghi chép: Bài đăng trở thành nhật ký học tập để bạn xem lại
- Cơ hội: Nhà tuyển dụng và khách hàng có thể biết đến năng lực của bạn qua quá trình học công khai

Bạn có thể đọc thêm về lợi ích [tại đây](https://aishippingblog.com/p/benefits-of-learning-in-public-and).

Đừng lo phải làm mọi thứ hoàn hảo. Ai cũng có điểm khởi đầu, và mọi người thường thích theo dõi một hành trình học tập chân thực!

### Bài đăng mẫu trên LinkedIn

```
🚀 Week 1 of Data Engineering Zoomcamp by @DataTalksClub complete!

Just finished Module 1 - Docker & Terraform. Learned how to:

✅ Containerize applications with Docker and Docker Compose
✅ Set up PostgreSQL databases and write SQL queries
✅ Build data pipelines to ingest NYC taxi data
✅ Provision cloud infrastructure with Terraform

Here's my homework solution: <LINK>

Following along with this amazing free course - who else is learning data engineering?

You can sign up here: https://github.com/DataTalksClub/data-engineering-zoomcamp/
```

### Bài đăng mẫu trên Twitter/X


```
🐳 Module 1 of Data Engineering Zoomcamp done!

- Docker containers
- Postgres & SQL
- Terraform & GCP
- NYC taxi data pipeline

My solution: <LINK>

Free course by @DataTalksClub: https://github.com/DataTalksClub/data-engineering-zoomcamp/
```
