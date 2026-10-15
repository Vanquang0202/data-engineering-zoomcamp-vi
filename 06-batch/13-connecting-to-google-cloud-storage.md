---
video_url: https://www.youtube.com/watch?v=Yyz293hBVcQ
prev_url: 12-spark-rdd-mappartition.md
next_url: 14-creating-a-local-spark-cluster.md
---
# Đang kết nối với Google Cloud Storage

Cho đến nay, công việc Spark của chúng tôi đọc các tệp sàn từ hệ thống tệp cục bộ. Trong
thiết bị này, chúng tôi di chuyển dữ liệu sang Google Cloud Storage và định cấu hình
Spark cục bộ của chúng tôi để đọc từ đó. Đây là đơn vị đầu tiên trong phần đám mây Spark-in-the-
đang chạy: sau đó sẽ tạo một cụm Spark cục bộ và chạy
Spark trên Dataproc.

Quá trình thiết lập tuân theo hướng dẫn do Alvin Do viết - cảm ơn Alvin! Chúng tôi
sẽ hướng dẫn từng bước một. Cấu hình đã hoàn tất là
[`code/09_spark_gcs.ipynb`](code/09_spark_gcs.ipynb).


## Tải dữ liệu lên Google Cloud Storage

Chúng tôi đã có một nhóm từ quá trình thiết lập Terraform trong mô-đun một. Dữ liệu
mà chúng tôi đã tạo trong các đơn vị trước đó - tệp sàn gỗ trong `data/pq` và báo cáo
- hiện được chuyển đến đó. `gsutil cp` sao chép tệp vào Bộ lưu trữ Google Cloud
và vì chúng tôi đang sao chép một thư mục có nhiều tệp nên chúng tôi thêm hai cờ
: `-r` cho đệ quy và `-m` cho tải lên đa luồng (song song),
sử dụng tất cả CPU của máy:

```bash
gsutil -m cp -r pq/ gs://dtc_data_lake_de-zoomcamp-nytaxi/pq
```

Việc tải lên các tệp sàn gỗ mất một lúc - thư mục chứa 380 tệp, tổng cộng
1.1 GiB:

Thiết bị đầu cuối kết thúc với quá trình chuyển hoàn tất:

```text
[2726/380 files][ 1.0 GiB/ 1.1 GiB] 97% Done
[380/380 files][ 1.1 GiB/ 1.1 GiB] 100% Done
```

Khi quá trình hoàn tất, thư mục `pq` chứa các tệp sàn màu xanh lá cây và màu vàng
sẽ nằm trong nhóm.

## Trình kết nối GCS cho Hadoop

Spark không thể đọc URL `gs://` ngay lập tức. Khi Spark nhìn thấy URI như

```
gs://dtc_data_lake_de-zoomcamp-nytaxi/pq/green/...
```

nó cần biết cách kết nối với Google Cloud Storage để tìm nạp các tệp
. Phần biết cách thực hiện việc này là trình kết nối Lưu trữ đám mây
dành cho Hadoop - một tệp jar, một thư viện Java. Bạn có thể bỏ qua phần Hadoop của
tên: chúng ta chỉ cần cho Spark biết cái bình ở đâu.

Đối với các phiên bản khác của trình kết nối GCS dành cho Hadoop, hãy xem tài liệu
[Trình kết nối lưu trữ đám mây](https://cloud.google.com/dataproc/docs/concepts/connectors/cloud-storage#connector-setup-on-non-dataproc-clusters)
.

Trình kết nối được lưu trữ trên chính Google Cloud Storage, vì vậy chúng tôi tải xuống lại
với `gsutil`. Chúng tôi cần bản dựng `hadoop3` - phiên bản Spark mà
đã cài đặt trong thiết lập được xây dựng cho Hadoop 3 - và phiên bản 2.2.5 của
trình kết nối:

```bash
mkdir lib
gsutil cp gs://hadoop-lib/gcs/gcs-connector-hadoop3-2.2.5.jar ./lib/
```

Thư mục `lib` không phải là một vị trí đặc biệt - chúng tôi đặt cái bình ở đó để giữ
bên cạnh mã:

## Định cấu hình phiên Spark

Bây giờ là cấu hình. Sổ ghi chép bắt đầu với một số thao tác nhập bổ sung:
chúng tôi cần `SparkConf` và `SparkContext` ngoài `SparkSession`.

Tiếp theo, chúng tôi trỏ Spark tới thông tin đăng nhập Google Cloud của chúng tôi. Đường dẫn này giống với khóa tài khoản dịch vụ
mà chúng tôi đã tạo bằng Terraform trong mô-đun một:

```python
credentials_location = '/home/alexey/.google/credentials/google_credentials.json'
```

Sau đó, chúng tôi xây dựng cấu hình. Thay vì để trình tạo phiên
tạo mọi thứ, chúng tôi thiết lập nó một cách rõ ràng:

```python
conf = SparkConf() \
    .setMaster('local[*]') \
    .setAppName('test') \
    .set("spark.jars", "./lib/gcs-connector-hadoop3-2.2.5.jar") \
    .set("spark.hadoop.google.cloud.auth.service.account.enable", "true") \
    .set("spark.hadoop.google.cloud.auth.service.account.json.keyfile",
         credentials_location)
```

Chúng tôi vẫn chạy ở chế độ `local[*]` với tên ứng dụng `test`. Các phần mới
là jar chúng tôi vừa tải xuống và hai cài đặt bật xác thực tài khoản dịch vụ
bằng tệp khóa của chúng tôi.

Với cấu hình, chúng tôi tạo bối cảnh Spark và thông qua đó,
định cấu hình lớp Hadoop thực sự xử lý hệ thống tệp `gs://`:

```python
sc = SparkContext(conf=conf)

hadoop_conf = sc._jsc.hadoopConfiguration()

hadoop_conf.set("fs.AbstractFileSystem.gs.impl",
                "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFS")
hadoop_conf.set("fs.gs.impl",
                "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem")
hadoop_conf.set("fs.gs.auth.service.account.json.keyfile",
                credentials_location)
hadoop_conf.set("fs.gs.auth.service.account.enable", "true")
```

Đây là phần có nội dung: khi bạn thấy một hệ thống tệp bắt đầu bằng
`gs`, hãy sử dụng triển khai đến từ jar trình kết nối và sử dụng
các thông tin xác thực này.

Cuối cùng, chúng tôi tạo phiên từ ngữ cảnh - luôn có cùng một trình tạo như
nhưng sử dụng lại cấu hình mà chúng tôi vừa tập hợp:

```python
spark = SparkSession.builder \
    .config(conf=sc.getConf()) \
    .getOrCreate()
```

## Kiểm tra kết nối

Bây giờ chúng ta đọc các tệp gỗ màu xanh lá cây ngay từ nhóm:

```python
df_green = spark.read.parquet('gs://dtc_data_lake_de-zoomcamp-nytaxi/pq/green/*/*')
```

Một `df_green.count()` đơn giản xác nhận rằng nó hoạt động - Spark kết nối với
Google Cloud Storage, tải xuống các tệp sàn và đếm các hàng:

Đó là tất cả những gì cấu hình cần. Lưu ý rằng chúng tôi chỉ cần điều này khi
tự chạy Spark - trên máy ảo hoặc trên máy tính xách tay. Ở phần sau của phần
này, chúng tôi sử dụng Dataproc, dịch vụ Spark được quản lý trên Google Cloud và
, ở đó không cần cấu hình này: cụm Dataproc có thể giao tiếp ngay với
với Google Cloud Storage.
