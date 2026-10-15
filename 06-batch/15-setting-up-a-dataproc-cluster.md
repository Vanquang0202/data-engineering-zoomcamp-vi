---
video_url: https://www.youtube.com/watch?v=osAiAYahvh8
prev_url: 14-creating-a-local-spark-cluster.md
next_url: 16-connecting-spark-to-bigquery.md
---
# Thiết lập cụm Dataproc

Trong bài học này, cuối cùng chúng tôi cũng di chuyển Spark lên đám mây: chúng tôi tạo cụm Dataproc
trong Google Cloud và chạy công việc Spark từ các đơn vị
trước đó trên đó, trước tiên thông qua giao diện người dùng web và sau đó từ thiết bị đầu cuối với
`gcloud` SDK. Dataproc - rất có thể là viết tắt của xử lý dữ liệu - là dịch vụ Spark được quản lý của
Google Cloud: nó tạo ra
chính và công nhân cho chúng tôi và chúng tôi chỉ gửi công việc cho nó.

## Tạo cụm

Trong bảng điều khiển Google Cloud, hãy mở Dataproc. Lần đầu tiên, nó yêu cầu bạn kích hoạt API
- một cú nhấp chuột. Sau đó nhấp vào tạo cụm và định cấu hình nó:

- Tên: `<cluster-name>`.
- Vùng và vùng: chọn vùng nơi nhóm của bạn tồn tại để cụm
gần với dữ liệu.
- Loại cụm: trong thực tế, bạn sẽ sử dụng tiêu chuẩn, một chủ cộng với
một số công nhân. Vì chúng tôi chỉ đang thử nghiệm và tập dữ liệu của chúng tôi không lớn
nên một nút duy nhất là đủ.
- Trong các thành phần bổ sung, hãy chọn thành phần sổ ghi chép Jupyter -
cho phép bạn chạy thử nghiệm ngay trên cụm - và Docker mà
mà chúng tôi sẽ sử dụng trong phần sau.

Các phần ổn định của biểu mẫu tạo cụm là:

| Cài đặt | Giá trị |
|---|---|
| Tên cụm | `<cluster-name>` |
| Vùng và khu vực | khu vực và khu vực nơi xô sinh sống |
| Loại cụm cho thử nghiệm này | nút đơn |
| Thành phần bổ sung | Máy tính xách tay và Docker Jupyter |
| Các loại máy | mặc định |

Mọi thứ khác - loại máy chủ và máy công nhân - vẫn giữ nguyên
ở mặc định. Nhấp vào tạo và sau vài phút, cụm
sẽ chạy. Dataproc đã tạo một máy ảo cho nó ở hậu trường; bạn
có thể xem nó trong phần Công cụ tính toán. Chúng tôi không cần kết nối với nó
- chúng tôi chỉ gửi công việc đến cụm.

Một thứ chúng tôi không cần nữa: thiết lập đầu nối GCS từ một vài thiết bị
trở lại. Cụm Dataproc đã có thể truy cập ngay vào Google Cloud Storage
. Cấu hình đó chỉ dành cho Spark chạy trên máy
của riêng bạn hoặc máy ảo chưa được định cấu hình.

## Gửi công việc từ web UI

Dataproc cần tập lệnh công việc ở nơi nào đó nó có thể đọc được - chúng tôi tải nó lên nhóm
của mình, vào thư mục `code`. Trong thực tế, bạn sẽ sử dụng một nhóm riêng
cho mã, nhưng để đơn giản, chúng tôi đặt nó vào cùng một nhóm:

```bash
BUCKET="<bucket-name>"
gsutil -m cp -r 06_spark_sql.py "gs://${BUCKET}/code/06_spark_sql.py"
```

Hãy nhớ rằng trong phần trước chúng ta đã loại bỏ phần chính được mã hóa cứng khỏi tập lệnh
. Điều quan trọng ở đây là: khi Dataproc chạy công việc, nó sẽ tự thiết lập bản gốc
.

Mở cụm, nhấp vào gửi công việc và điền vào biểu mẫu:

| Trường biểu mẫu | Giá trị |
|---|---|
| Loại công việc | `PySpark` |
| Tệp Python chính | `gs://<bucket-name>/code/06_spark_sql.py` |
| Tệp phụ thuộc và tệp jar | không |
| `--input_green` | `gs://<bucket-name>/pq/green/2021/*/` |
| `--input_yellow` | `gs://<bucket-name>/pq/yellow/2021/*/` |
| `--output` | `gs://<bucket-name>/report-2021` |

Gửi và chờ đợi. Trang công việc hiển thị đầu ra của trình điều khiển trong khi nó chạy; khi
hoàn tất, kết quả sẽ nằm trong nhóm: một thư mục `report-2021` với các tệp sàn gỗ
của báo cáo doanh thu hàng tháng - được tính toán bởi cụm mà chúng tôi
vừa tạo.

## Gửi công việc với gcloud

Giao diện người dùng web phù hợp để dùng thử, nhưng chúng tôi sẽ không thúc đẩy việc sản xuất
theo cách này - bạn không thể dễ dàng gửi công việc từ Airflow bằng cách nhấp vào nút
. Có ba cách để gửi công việc tới cụm Dataproc
: giao diện người dùng web, Google Cloud SDK và API REST. Trang chi tiết
của công việc hiển thị lệnh gọi REST tương đương cho những gì chúng ta vừa thực hiện và
từ đó chúng ta có thể đọc những phần chúng ta cần: tên cụm, tệp Python
và các đối số.

Cách SDK được ghi lại trên trang
[gửi công việc](https://cloud.google.com/dataproc/docs/guides/submit-job#dataproc-submit-job-gcloud)
. Từ thiết bị đầu cuối của máy ảo:

```bash
CLUSTER_NAME="<cluster-name>"
REGION="<bucket-region>"
BUCKET="<bucket-name>"

gcloud dataproc jobs submit pyspark \
    --cluster="${CLUSTER_NAME}" \
    --region="${REGION}" \
    "gs://${BUCKET}/code/06_spark_sql.py" \
    -- \
        --input_green="gs://${BUCKET}/pq/green/2020/*/" \
        --input_yellow="gs://${BUCKET}/pq/yellow/2020/*/" \
        --output="gs://${BUCKET}/report-2020"
```

Mọi thứ trước dấu trừ kép sẽ định cấu hình quá trình gửi - cụm, vùng
, tập lệnh - và mọi thứ sau dấu trừ kép được chuyển cho chính công việc
, giống hệt như với `spark-submit` trong đơn vị trước. Tại đây
chúng tôi thực hiện công việc cho năm 2020.

## Sửa quyền

Lần thử đầu tiên không thành công với quyền bị từ chối: không được phép yêu cầu tài nguyên
. Lý do là chúng tôi sử dụng một tài khoản dịch vụ cho
mọi thứ trong khóa học này - một Terraform được thiết lập trong mô-đun một - và
không có quyền gửi các công việc Dataproc.

Trong một dự án thực tế, bạn sẽ giữ các vai trò riêng biệt: một vai trò mạnh mẽ cho
Terraform và một vai trò hẹp cho các công nhân và người lập lịch trình mà chỉ
mới cho phép những gì họ cần - gửi công việc Dataproc, truy cập các nhóm và
, v.v. Để đơn giản hóa khóa học, chúng tôi chỉ cần thêm một vai trò vào cùng một tài khoản dịch vụ
: mở IAM & quản trị viên, tìm tài khoản và thêm vai trò Quản trị viên Dataproc
.


Sau khi cập nhật chính sách, hãy chạy lại lệnh `gcloud` tương tự. Bây giờ,
sẽ đi qua: công việc được gửi, thiết bị đầu cuối hiển thị cùng một đầu ra trình điều khiển
mà chúng ta đã thấy trong giao diện người dùng web và quá trình hoàn tất. Chạy nó một lần nữa trong một năm
khác để xem hoạt động tham số hóa - báo cáo năm 2020 nằm cạnh
báo cáo năm 2021 trong nhóm.

Bố cục đối tượng ổn định là:

```text
<bucket-name>/
├── code/
├── pq/
├── report-2020/
└── report-2021/
```

Khi chúng tôi kết nối điều này vào Airflow sau này, cách tiếp cận đơn giản nhất có thể là
BashOperator chạy chính xác lệnh `gcloud` này; còn có các toán tử Dataproc chuyên dụng
.

## Còn thiếu gì

Bây giờ chúng tôi có vòng lặp đầy đủ: đọc dữ liệu taxi từ Google Cloud Storage,
xử lý dữ liệu đó trên cụm Spark và viết báo cáo trở lại Google Cloud
Storage. Tuy nhiên, đối với các dự án, bạn có thể muốn kết quả trong kho dữ liệu
chứ không phải trong bộ chứa - vì vậy bạn có thể xây dựng trang tổng quan trên chúng.
của bạn có thể tạo một bảng bên ngoài trên các tệp sàn gỗ và sao chép chúng vào
một bảng BigQuery, nhưng có một cách trực tiếp hơn: Spark có thể ghi thẳng
vào BigQuery. Đó là đơn vị tiếp theo.
