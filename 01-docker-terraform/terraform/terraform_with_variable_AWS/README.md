# Hồ dữ liệu AWS Terraform (Tương đương GCP)

## ✔️ Tổng quan

Kho lưu trữ này chứa **triển khai Terraform dựa trên AWS** phản ánh cơ sở hạ tầng **Google Cloud Platform (GCP)** được sử dụng trong khóa học Kỹ thuật dữ liệu (ví dụ: GCS + BigQuery), nhưng được triển khai bằng cách sử dụng **dịch vụ AWS**.

Mục tiêu là giúp những người học:
- Đã đăng ký **khóa học Kỹ thuật dữ liệu tập trung vào GCP**
- Thích hoặc cần làm việc với **AWS**
- Muốn hiểu **khái niệm kỹ thuật dữ liệu bất khả tri trên nền tảng đám mây**

Quá trình thiết lập này tập trung vào việc xây dựng **nền tảng hồ dữ liệu cơ bản** bằng cách sử dụng:
- **Amazon S3** (tương đương với GCS)
- **Danh mục dữ liệu AWS Glue** (tương đương với bộ dữ liệu BigQuery/lớp siêu dữ liệu)
- **Terraform** làm Cơ sở hạ tầng dưới dạng Mã (IaC)

---

## 🏗️ Lập bản đồ kiến ​​trúc (GCP → AWS)

| Dịch vụ GCP | Tương đương AWS | Mục đích |
|------------|---------------|---------|
| Bộ nhớ đám mây của Google (GCS) | Amazon S3 | Lưu trữ hồ dữ liệu |
| Truy cập cấp độ nhóm thống nhất | Khối truy cập công cộng S3 | Truy cập nhóm an toàn |
| Quy tắc vòng đời đối tượng | Cấu hình vòng đời S3 | Tự động hết hạn dữ liệu |
| Bộ dữ liệu BigQuery | Cơ sở dữ liệu danh mục keo AWS | Lớp siêu dữ liệu & truy vấn |
| Terraform (nhà cung cấp GCP) | Terraform (nhà cung cấp AWS) | Cơ sở hạ tầng dưới dạng mã |

---

## 📁 Cấu trúc dự án

```text
.
├── main.tf            # Core infrastructure resources
├── variables.tf       # Input variable definitions
├── terraform.tfvars   # Environment-specific values
└── README.md          # Project documentation
