---
video_url: https://www.youtube.com/watch?v=CI3P4tAtru4
prev_url: 05-spark-dataframes.md
next_url: 07-sql-with-spark.md
---
# Đang chuẩn bị dữ liệu Taxi Vàng và Xanh

Trong phần này (tùy chọn), chúng tôi chuẩn bị bộ dữ liệu taxi màu vàng và xanh lục cho
mô-đun này: chúng tôi tải xuống các tệp thô, xác định lược đồ rõ ràng cho từng loại taxi
và viết lại mọi thứ dưới dạng sàn gỗ. Mục đích là để đảm bảo rằng
sau này, khi chúng tôi kết hợp tháng và năm, các lược đồ khớp với nhau và không có bất ngờ nào về
.

## Dữ liệu chúng tôi cần

Trong các tuần trước, học sinh đã sao chép dữ liệu vào hồ dữ liệu theo nhiều cách khác nhau,
và điều đó đã gây ra sự cố với lược đồ và loại. Vì vậy, trong phần này, chúng tôi thực hiện việc chuẩn bị
một lần, cẩn thận và sử dụng kết quả cho phần còn lại của mô-đun.

Chúng tôi lấy dữ liệu taxi màu vàng và xanh lục cho năm 2020 và 2021. Chúng tôi chọn hai bộ dữ liệu
này vì trong tuần 4 (kỹ thuật phân tích), chúng tôi đã sử dụng chúng và
ở đây chúng tôi sẽ chạy các tính toán tương tự trên chúng bằng Spark.

Dữ liệu tồn tại trên trang web NYC TLC (Ủy ban taxi và xe limousine),
liệt kê các hồ sơ chuyến đi mỗi tháng:

Các URL tuân theo cùng một mẫu - chỉ có loại taxi, năm và tháng
thay đổi. Điều đó làm cho chúng dễ dàng được tạo ra trong một vòng lặp.

## Tập lệnh bash để tải xuống dữ liệu

Chúng tôi viết một tập lệnh bash nhỏ, `download_data.sh`, có hai tham số:
loại taxi (ví dụ `yellow`) và năm (ví dụ `2020`). Sau đó,
sẽ lặp lại trong các tháng từ 1 đến 12 và tải xuống một tệp CSV mỗi tháng.

Có một chi tiết nhỏ: trong URL, tháng không được đệm - Tháng 1 là
`01`, không phải `1`. Để thêm số 0 đứng đầu, chúng tôi sử dụng `printf` với mẫu
`%02d`: `%0` có nghĩa là "pad có số 0", `2` có nghĩa là "tổng cộng hai ký tự" và
`d` có nghĩa là "đó là một chữ số". Cú pháp định dạng này xuất phát từ C và bash
đã mượn nó:

```bash
FMONTH=`printf "%02d" ${MONTH}`
```

Với điều đó, chúng tôi có thể tập hợp URL cho mỗi tháng và kiểm tra nó bằng `echo`
trước khi thực sự tải xuống bất kỳ thứ gì. Tập lệnh hoàn chỉnh nằm trong phần tài liệu
bên dưới.

Đối với mỗi tệp, chúng tôi cũng xây dựng đường dẫn cục bộ: `data/raw/<taxi type>/<year>/<month>`,
để mỗi tháng đều có thư mục riêng. Chúng tôi tạo thư mục với `mkdir -p`
(`-p` cũng tạo thư mục mẹ) và lưu tệp vào đó với
`wget`:

```bash
mkdir -p ${LOCAL_PREFIX}
wget ${URL} -O ${LOCAL_PATH}
```

Tệp CSV có dung lượng lớn nên chúng tôi nén chúng bằng gzip. gzip là một lựa chọn tốt
vì cả pandas và Spark đều có thể đọc các tệp nén mà không cần giải nén thêm
. Theo mặc định, gzip sẽ xóa tệp gốc sau khi nén nó.

Một điều nữa: một số tháng không tồn tại (tại thời điểm ghi, không có dữ liệu
vào tháng 8 năm 2021). Đối với một tệp bị thiếu, `wget` nhận được 404 và thoát với mã
khác 0. Chúng tôi thêm `set -e` vào tập lệnh để nó dừng ở lỗi đầu tiên
thay vì tiếp tục với các tháng còn lại.

Sau khi tải xuống 2021 màu vàng, chúng tôi chạy cùng một tập lệnh cho 2021 màu xanh lá cây,
2020 màu vàng và 2020 màu xanh lá cây. Lưu ý rằng dữ liệu năm 2020 khá mất cân bằng: Tháng 1
lớn, sau đó vì Covid nên có rất ít chuyến đi và đến cuối năm
thì phục hồi một phần.

## Kiểm tra file đã tải về

Trong khi tập lệnh chạy, nó sẽ in những gì nó thực hiện: tải xuống và nén các tin nhắn
. Chúng ta có thể kiểm tra nội dung của tệp nén mà không cần giải nén
bằng `zcat` - giống như `cat`, nhưng đối với các tệp được nén bằng gzipped:

```bash
zcat data/raw/yellow/2021/01/yellow_tripdata_2021_01.csv.gz | head -n 10
```

Lệnh bắt đầu với tiêu đề này và hai hàng đầu tiên:

```text
VendorID,tpep_pickup_datetime,tpep_dropoff_datetime,passenger_count,trip_distance,RatecodeID,store_and_fwd_flag,PULocationID,DOLocationID,payment_type,fare_amount,extra,mta_tax,tip_amount,tolls_amount,improvement_surcharge,total_amount,congestion_surcharge
1,2021-01-01 00:30:10,2021-01-01 00:36:12,1,2.10,1,N,142,43,2,8,3,0.5,0,0,0.3,11.8,2.5
1,2021-01-01 00:51:20,2021-01-01 00:52:19,1,.20,1,N,238,151,2,3,0.5,0.5,0,0,0.3,4.3,0
```

Và `tree` hiển thị cho chúng tôi cấu trúc thư mục mà chúng tôi đã kết thúc: đối với mỗi loại và năm taxi
, một thư mục mỗi tháng có CSV nén bên trong:

```text
data/raw/
├── green/
│   ├── 2020/
│   │   └── <month>/green_tripdata_2020_<month>.csv.gz
│   └── 2021/
│       └── <month>/green_tripdata_2021_<month>.csv.gz
└── yellow/
    ├── 2020/
    │   └── <month>/yellow_tripdata_2020_<month>.csv.gz
    └── 2021/
        └── <month>/yellow_tripdata_2021_<month>.csv.gz
```

## Xác định lược đồ

Bây giờ chúng tôi muốn đọc các tệp CSV này trong Spark, xác định lược đồ cho chúng và
lưu chúng dưới dạng sàn gỗ với lược đồ đó. Bởi vì chúng tôi xác định lược đồ ở đây, nên các tính toán sau này của
sẽ không gặp bất ngờ.

Đầu tiên chúng ta đọc một tháng theo cách thông thường:

```python
df_green = spark.read \
    .option("header", "true") \
    .csv('data/raw/green/2021/01/*')
```

Chúng ta có thể trỏ tới một thư mục (hoặc thậm chí dùng `*` để đọc cả năm) - Spark
sẽ đọc tất cả các file trong đó. Nếu bây giờ in lược đồ, chúng ta sẽ thấy tên cột
, nhưng mọi thứ đều là một chuỗi:

```python
df_green.printSchema()
```

```text
root
 |-- VendorID: string (nullable = true)
 |-- lpep_pickup_datetime: string (nullable = true)
 |-- lpep_dropoff_datetime: string (nullable = true)
 |-- store_and_fwd_flag: string (nullable = true)
 |-- RatecodeID: string (nullable = true)
 |-- PULocationID: string (nullable = true)
 |-- DOLocationID: string (nullable = true)
 |-- passenger_count: string (nullable = true)
 |-- trip_distance: string (nullable = true)
 |-- fare_amount: string (nullable = true)
 |-- extra: string (nullable = true)
 |-- mta_tax: string (nullable = true)
 |-- tip_amount: string (nullable = true)
 |-- tolls_amount: string (nullable = true)
 |-- ehail_fee: string (nullable = true)
 |-- improvement_surcharge: string (nullable = true)
 |-- total_amount: string (nullable = true)
 |-- payment_type: string (nullable = true)
```

Cách chúng tôi suy ra các loại trước đây: đọc cùng một tệp với gấu trúc,
tìm ra các loại cho chúng tôi. Vì gấu trúc có thể đọc trực tiếp các tệp được nén nên
không cần giải nén:

```python
import pandas as pd

df_green_pd = pd.read_csv(
    'data/raw/green/2021/01/green_tripdata_2021_01.csv.gz',
    nrows=1000
)
```

Sau đó, chúng tôi biến DataFrame của gấu trúc này thành Spark DataFrame và xem lược đồ
của nó:

```python
spark.createDataFrame(df_green_pd).schema
```

Chúng tôi sao chép lược đồ đó và dọn dẹp nó trong một trình soạn thảo: thêm ngắt dòng, trích dẫn tên
, đặt `types.` trước các kiểu dữ liệu và viết hoa `True` - chúng tôi kết thúc
bằng `types.StructType` với một `types.StructField` trên mỗi cột mà chúng tôi gán cho
`green_schema`.

Lược đồ này chưa hoàn hảo nên chúng tôi chỉnh sửa một chút:

- thời gian lấy và trả phải là `TimestampType`, không phải ngày
- ID và số lượng (`VendorID`, `passenger_count`, `RatecodeID`,
`PULocationID`, `DOLocationID`) không phải là số lượng lớn, vì vậy `IntegerType`
là đủ - cần 4 byte thay vì 8 byte của `LongType`
- cột tiền giữ nguyên là `DoubleType` (số float hoặc số thập phân cũng được)

Chúng tôi làm tương tự với tập dữ liệu màu vàng và nhận được `yellow_schema`.

## Viết lại mọi thứ dưới dạng sàn gỗ

Bây giờ chúng tôi lấy từng CSV hàng tháng, đọc nó bằng lược đồ rõ ràng và viết nó
dưới dạng sàn gỗ:

```python
df_green = spark.read \
    .option("header", "true") \
    .schema(green_schema) \
    .csv(input_path)

df_green \
    .repartition(4) \
    .write.parquet(output_path)
```

Chúng tôi thực hiện việc này theo vòng lặp trong nhiều tháng (trong Python, `range(1, 13)` bao gồm các tháng
từ 1 đến 12; chúng tôi cũng định dạng tháng với số 0 đứng đầu bằng chuỗi f).
Đầu vào đến từ `data/raw/`, đầu ra chuyển sang `data/pq/` - cấu trúc tương tự, nhưng sàn gỗ
thay vì CSV.

Tại sao lại là `repartition(4)`? Khi Spark đọc một tệp được nén bằng gzipped, nó không thể chia
thành nhiều phân vùng - toàn bộ tệp sẽ chuyển vào một phân vùng. Chúng tôi có bốn lõi
trên máy này, vì vậy chúng tôi phân vùng lại thành bốn phân vùng để sử dụng tất cả
. Chúng ta có thể xem điều này trong Spark UI: đầu tiên chỉ có một tác vụ chạy (một trình thực thi
đi qua tệp CSV), sau đó ghi kết quả vào bốn tệp tạm thời
kết thúc trên đĩa:

Số lượng tác vụ quan trọng ổn định ngay cả khi Spark UI không:

| Bước | Nhiệm vụ/tập tin |
| --- | --- |
| Đọc CSV được nén | Một nhiệm vụ, vì gzip không thể chia nhỏ |
| Viết sàn gỗ sau `repartition(4)` | Bốn tệp tạm thời nằm trên đĩa |

Chúng tôi chạy điều này cho cả bốn kết hợp: xanh lá cây và vàng, 2020 và 2021.

## Kết quả

Xem xét `data/pq` với `tree`, mỗi tháng hiện có bốn tệp phần sàn gỗ
(kết quả của việc phân vùng lại) cùng với điểm đánh dấu `_SUCCESS`:

```text
data/pq/
└── <taxi type>/<year>/<month>/
    ├── _SUCCESS
    ├── part-00000-...snappy.parquet
    ├── part-00001-...snappy.parquet
    ├── part-00002-...snappy.parquet
    └── part-00003-...snappy.parquet
```

So sánh kích thước với `ls -lh`: CSV màu vàng nén cho tháng 1 năm 2020 là
111 MB và phiên bản sàn gỗ thực sự lớn hơn một chút - gzip nén
CSV khá tốt. Nhưng lợi ích của sàn gỗ ở đây không phải là kích thước: lược đồ
được tích hợp sẵn. Bởi vì chúng tôi đảm bảo rằng tất cả các tệp đều tuân theo cùng một lược đồ, nên
có thể kết hợp nhiều tháng và nhiều năm sau đó mà không có bất kỳ sự ngạc nhiên kỳ lạ nào.

Một cách nữa để suy ra lược đồ của tệp CSV (ngoài gấu trúc) là
đặt tùy chọn `inferSchema` thành `true` khi đọc chúng trong Spark.

Phiên bản cuối cùng của cả tập lệnh tải xuống và sổ ghi chép lược đồ là
trong phần Tài liệu bên dưới - bạn chỉ có thể thực thi chúng thay vì
theo sau.

## Vật liệu

* [`code/download_data.sh`](code/download_data.sh) - tải dữ liệu chuyến đi màu vàng và
màu xanh lá cây cho năm 2020 và 2021 vào `data/raw/`.
* [`code/05_taxi_schema.ipynb`](code/05_taxi_schema.ipynb) - lược đồ màu xanh lá cây rõ ràng
và màu vàng, cũng như vòng lặp ghi lại mỗi tháng dưới dạng sàn gỗ
được phân vùng trong `data/pq/`.
