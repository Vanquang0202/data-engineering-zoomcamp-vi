---
video_url: https://www.youtube.com/watch?v=TLGFAOHpOYM
prev_url: 09-etl-vs-elt.md
next_url: 11-load-taxi-data-to-bigquery.md
---
# Thiết lập Nền tảng đám mây của Google (GCP)

Trước khi bắt đầu tải dữ liệu lên GCP, chúng tôi cần thiết lập Google Cloud Platform.

Trước tiên, hãy điều chỉnh luồng sau [`06_gcp_kv.yaml`](flows/06_gcp_kv.yaml) để bao gồm tài khoản dịch vụ của bạn, ID dự án GCP, tập dữ liệu BigQuery và tên nhóm GCS (_cùng với vị trí của chúng_) làm giá trị KV Store:
- GCP_PROJECT_ID
- GCP_LOCATION
- GCP_BUCKET_NAME
- GCP_DATASET.


## Tạo tài nguyên GCP
Nếu chưa tạo bộ chứa GCS và tập dữ liệu BigQuery trong tuần đầu tiên của khóa học, bạn có thể sử dụng quy trình này để tạo chúng: [`07_gcp_setup.yaml`](flows/07_gcp_setup.yaml).

> [!CẢNH BÁO]
> Tài khoản dịch vụ `GCP_CREDS` chứa thông tin nhạy cảm. Đảm bảo bạn giữ nó an toàn và không cam kết với Git. Giữ nó an toàn như mật khẩu của bạn.

## Tài nguyên
- [Thiết lập tài khoản dịch vụ Google Cloud trong Kestra](https://go.kestra.io/de-zoomcamp/google-sa)
