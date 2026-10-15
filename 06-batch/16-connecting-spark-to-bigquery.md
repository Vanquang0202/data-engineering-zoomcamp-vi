---
video_url: https://www.youtube.com/watch?v=HIm2BOj8C0Q
prev_url: 15-setting-up-a-dataproc-cluster.md
next_url: ../07-streaming/01-introduction.md
---
# Kết nối Spark với BigQuery

Trong các bài học trước, chúng tôi đã tạo cụm Dataproc, chạy công việc Spark trên
và viết báo cáo cho Google Cloud Storage. Đơn vị này đóng phần
: thay vì ghi vào bộ chứa, chúng tôi ghi thẳng kết quả
vào BigQuery, kho dữ liệu của chúng tôi. Đối với các dự án, đây thường là thứ
bạn muốn - báo cáo sẽ được đưa vào kho, sẵn sàng cho bảng điều khiển.

## Từ đầu ra sàn gỗ đến đầu ra BigQuery

Spark cũng không thể ghi vào BigQuery ngay lập tức - nó cần có trình kết nối
. Google ghi lại điều này trong hướng dẫn
[Trình kết nối BigQuery dành cho Spark](https://cloud.google.com/dataproc/docs/tutorials/bigquery-connector-spark-example#pyspark)
và chúng tôi làm theo ví dụ của nó.

Chúng ta bắt đầu từ tập lệnh của các bài trước và tạo một bản sao,
`06_spark_sql_big_query.py` - việc đọc và tổng hợp dữ liệu SQL
giữ nguyên, chỉ có đầu ra thay đổi. Thay vì

```python
df_result.coalesce(1) \
    .write.parquet(output, mode='overwrite')
```

chúng tôi viết

```python
df_result.write.format('bigquery') \
    .option('table', output) \
    .save()
```

Đầu ra không còn là một thư mục mà là một bảng BigQuery, được chuyển dưới dạng
`schema.table` từ dòng lệnh và chúng tôi không cần `coalesce(1)`
để hợp nhất các tệp đầu ra - BigQuery sẽ đảm nhiệm việc đó.

Trình kết nối cần một bộ chứa tạm thời: Trước tiên, Spark ghi kết quả vào
Google Cloud Storage rồi tải chúng vào BigQuery. Chúng tôi định cấu hình nó
trong tập lệnh:

```python
spark.conf.set('temporaryGcsBucket', 'dataproc-temp-europe-west6-828225226997-fckhkym8')
```

Khi bạn tạo một cụm Dataproc, nó cũng tạo một nhóm tạm thời
giống như nhóm này - chúng tôi sẽ sử dụng lại nó.

Tải tập lệnh lên GCS:

```bash
gsutil -m cp -r 06_spark_sql_big_query.py gs://dtc_data_lake_de-zoomcamp-nytaxi/code/06_spark_sql_big_query.py
```

## Lần thử đầu tiên

Quay lại giao diện người dùng Dataproc, chúng tôi gửi công việc theo cách tương tự như trước: PySpark,
tập lệnh mới và các đối số - hai đầu vào và đầu ra bằng gỗ,
hiện là bảng BigQuery. Dự án của chúng tôi là `trips_data_all`, vì vậy đầu ra là
`trips_data_all.reports-2020`:

* `--input_green=gs://dtc_data_lake_de-zoomcamp-nytaxi/pq/green/2020/*/`
* `--input_yellow=gs://dtc_data_lake_de-zoomcamp-nytaxi/pq/yellow/2020/*/`
* `--output=trips_data_all.reports-2020`

Công việc thất bại nhanh chóng với `Failed to find data source: bigquery`. Trong khóa học
- chúng tôi chưa bao giờ cung cấp đầu nối cho Spark. Không giống như Google Cloud Storage,
, trình kết nối BigQuery không đi kèm với mọi cụm và Dataproc
không thể đoán được rằng chúng tôi muốn nó.

## Thêm bình kết nối

Cách khắc phục giống như thủ thuật mà chúng tôi đã sử dụng cho trình kết nối GCS trên
Spark cục bộ của chúng tôi: giao cho công việc một cái bình. Google lưu trữ trình kết nối BigQuery trên bộ chứa công khai
, vì vậy chúng tôi có thể trỏ thẳng nội dung gửi tới nó bằng
`--jars`:

```bash
gcloud dataproc jobs submit pyspark \
    --cluster=de-zoomcamp-cluster \
    --region=europe-west6 \
    --jars=gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar \
    gs://dtc_data_lake_de-zoomcamp-nytaxi/code/06_spark_sql_big_query.py \
    -- \
        --input_green=gs://dtc_data_lake_de-zoomcamp-nytaxi/pq/green/2020/*/ \
        --input_yellow=gs://dtc_data_lake_de-zoomcamp-nytaxi/pq/yellow/2020/*/ \
        --output=trips_data_all.reports-2020
```

Có thể có sự cố giữa phiên bản Spark mới nhất và trình kết nối BigQuery
. Bạn có thể tìm thấy liên kết tải xuống tệp jar cho các phiên bản Spark
tương ứng trong kho lưu trữ
[Spark BigQuery Connector](https://github.com/GoogleCloudDataproc/spark-bigquery-connector)
. Lưu ý rằng hình ảnh Dataproc trên GCE 2.1 và mới hơn đi kèm với trình kết nối
được cài đặt sẵn
([Dataproc Release 2.2](https://cloud.google.com/dataproc/docs/concepts/versioning/dataproc-release-2.2)),
nên trên cụm gần đây, bạn hoàn toàn không cần cờ `--jars`.

## Bảng xuất hiện trong BigQuery

Lần này công việc đã trôi qua. Một câu hỏi mở trước khi chạy:
xảy ra khi bảng đầu ra không tồn tại? Hóa ra Spark chỉ đơn giản là
tạo ra nó. Mở BigQuery, làm mới và có `reports-2020` trong tập dữ liệu
`trips_data_all` - với bản xem trước các hàng doanh thu hàng tháng mà công việc
của chúng tôi được tính toán trên cụm.

Bảng có các trường nhóm dự kiến ​​và thước đo doanh thu. Các trường
đầu tiên trong lược đồ của nó là:

| Lĩnh vực | Loại | Chế độ |
| --- | --- | --- |
| `revenue_zone` | SỐ LIỆU | KHÔNG THỂ |
| `revenue_month` | DẤU THỜI GIAN | KHÔNG THỂ |
| `service_type` | CHUỖI | BẮT BUỘC |
| `revenue_monthly_fare` | PHỔI | KHÔNG THỂ |

Điều đó khép lại phần chạy Spark trên đám mây: chúng tôi đã kết nối Spark cục bộ
với Google Cloud Storage, tạo cụm Dataproc được quản lý,
đã gửi công việc tới cụm đó từ giao diện người dùng và bằng `gcloud`, đồng thời cuối cùng ghi kết quả
trực tiếp vào BigQuery.

Tập lệnh là [`code/06_spark_sql_big_query.py`](code/06_spark_sql_big_query.py).
