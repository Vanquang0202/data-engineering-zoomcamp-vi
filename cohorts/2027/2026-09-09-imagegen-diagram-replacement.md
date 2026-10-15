# Thay thế sơ đồ Imagegen — 2026-09-09

Tất cả 45 hình minh họa raster được tạo bằng mô hình hình ảnh
(`*-imagegen.png`) và được tham chiếu trong các bài học DE 2027 đều đã được kiểm tra và
được xác nhận là sơ đồ (dòng, phân cấp, mốc thời gian, kiến ​​trúc, cây quyết định
) chứ không phải là ảnh hoặc nghệ thuật trang trí. Chúng được tạo lại dưới dạng sơ đồ SVG xác định
với kỹ năng `diagram-creator` và được xuất bản dưới dạng
2x PNG được kết xuất bằng Chrome. Mọi sơ đồ được xuất bản đều được kiểm tra bởi cơ quan đánh giá độc lập
dựa trên quan điểm giảng dạy của hình.

Đối với mỗi hình, kho lưu trữ hiện giữ thông số JSON có thể chỉnh sửa, nguồn SVG,
và PNG đã xuất bản cạnh nhau trong thư mục `images/` của bài học:

```
<figure>.json   diagram-creator spec (edit this to change the diagram)
<figure>.svg    deterministic render of the spec
<figure>.png    2x Chromium render referenced by the lesson markdown
```

## Số liệu được thay thế

| Mô-đun | Bài học | Tài sản mới (`.json`/`.svg`/`.png`) |
| --- | --- | --- |
| Hội thảo 2024 | dlt_resource | `incremental_loading` |
| 01 docker-địa hình | 01-giới thiệu | `docker-volume-mapping` |
| 01 docker-địa hình | 12-địa hình-tổng quan | `terraform-provider-flow` |
| 01 docker-địa hình | 13-gcp-tổng quan | `cloud-service-families` |
| 03 kho dữ liệu | 01-data-kho-và-bigquery | `01-data-warehouse-and-bigquery-02-data-warehouse-diagram` |
| 03 kho dữ liệu | 04-internals-of-bigquery | `04-internals-of-bigquery-01-architecture` |
| 03 kho dữ liệu | 04-internals-of-bigquery | `04-internals-of-bigquery-02-columnar-storage` |
| 03 kho dữ liệu | 04-internals-of-bigquery | `04-internals-of-bigquery-03-dremel-tree` |
| 04 phân tích-kỹ thuật | 01-phân tích-kỹ thuật-cơ bản | `analytics-engineering-toolchain` |
| 04 phân tích-kỹ thuật | 02-dbt là gì | `dbt-model-warehouse-flow` |
| 04 phân tích-kỹ thuật | 08-tài liệu | `dbt-lineage-graph` |
| 05 nền tảng dữ liệu | 03-nyc-taxi-đường ống | `bruin-pipeline-lineage` |
| 05 nền tảng dữ liệu | 06-concept-dự án | `bruin-project-structure` |
| 05 nền tảng dữ liệu | 07-khái niệm-lõi-đường ống | `bruin-project-pipelines`, `bruin-pipeline-configuration` |
| 05 nền tảng dữ liệu | 08-khái niệm-tài sản cốt lõi | `bruin-asset-lineage` |
| 05 nền tảng dữ liệu | 10-khái niệm-lệnh lõi | `bruin-project-command-hierarchy` |
| đợt 06 | 01-giới thiệu-xử lý hàng loạt | `01-...-01-batch-vs-streaming`, `01-...-02-streaming-example`, `01-...-07-batch-vs-streaming-share` |
| đợt 06 | 02-giới thiệu-tia lửa | `02-...-02-data-processing-engine-whiteboard-redraw`, `02-...-03-when-to-use-spark-whiteboard-redraw`, `02-...-04-typical-workflow-whiteboard` |
| đợt 06 | 04-nhìn-tia lửa | `04-first-look-at-spark-04-partitions-slides` |
| đợt 06 | 08-giải phẫu-cụm-tia lửa | `08-...-01-spark-submit-master`, `08-...-02-executors-failure`, `08-...-03-executors-pull-partitions`, `08-...-04-s3-gcs-instead-of-hdfs` |
| đợt 06 | 09-groupby-in-spark | `09-groupby-in-spark-03-reshuffling-whiteboard` |
| đợt 06 | 11-hoạt động trên tia lửa-rdds | `11-operations-on-spark-rdds-02-map-key-value-whiteboard` |
| đợt 06 | 12-spark-rdd-mappartition | `12-spark-rdd-mappartition-01-map-partitions-diagram` |
| 07 phát trực tuyến | lý thuyết/README | `07-stream-processing-two-topic-flow`, `07-kafka-event-fanout-to-partitions`, `07-kafka-notice-board-topics`, `07-kafka-replication`, `07-kafka-retention-window`, `07-kafka-partitions-to-nodes`, `07-kafka-consumer-group-partition-assignment`, `07-kafka-key-count-flow`, `07-kafka-testing-topology`, `07-kafka-global-ktable-replication`, `07-kafka-stream-join-window`, `07-kafka-tumbling-window-timeline`, `07-kafka-schema-registry-flow`, `07-kafka-schema-forward-compatibility` |

## Hiện vật đã bị xóa

Với các tệp `*-imagegen.png` được tham chiếu được thay thế, các
không được tham chiếu còn lại là `*-imagegen-crop.png` / `*-imagegen-redraw.png` trung gian
(cắt ảnh chụp màn hình và các biến thể vẽ lại được giữ từ các lần sửa chữa trước đó) cũng bị xóa
. Các tài liệu kiểm tra tiền hình ảnh ở trên giữ lại hồ sơ lịch sử
của chúng; các bảng SHA-256 trong đó đề cập đến nội dung
raster đã bị loại bỏ.

## Tái tạo sơ đồ

```bash
cd /home/alexey/git/diagram-creator
uv run diagram-creator <images-dir>/<figure>.json <images-dir>/<figure>.svg
```

Sau đó xuất bản lại PNG 2x và cập nhật tham chiếu đánh dấu trong một bước:

```bash
python skills/diagram-creator/scripts/publish_svgs.py --scale 2 <lesson>.md
```
