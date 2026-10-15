---
video_url: https://www.youtube.com/watch?v=uAlp2VuZZPY
prev_url: 06-preparing-taxi-data.md
next_url: 08-anatomy-of-a-spark-cluster.md
---
# SQL với Spark

Trong bài học này, chúng tôi lấy truy vấn doanh thu từ tuần 4 (kỹ thuật phân tích)
và chạy truy vấn đó với Spark SQL. Chúng tôi kết hợp dữ liệu taxi màu xanh lá cây và màu vàng vào một tập dữ liệu
, đăng ký dưới dạng bảng tạm thời và thực thi báo cáo doanh thu
dưới dạng truy vấn SQL.

## Dữ liệu

Chúng ta dùng dữ liệu đã chuẩn bị trong [bài học trước](06-preparing-taxi-data.md).
Đơn vị đó là tùy chọn: nếu bỏ qua, bạn chỉ có thể thực thi hai tệp
từ phần Vật liệu - tập lệnh tải xuống (dành cho màu vàng và xanh lục,
2020 và 2021) và sổ ghi chép lược đồ, biến các tệp CSV thành sàn gỗ
.

Bạn không cần phải sử dụng sàn gỗ. Thay vào đó, nếu bạn muốn sử dụng các tệp CSV,
hãy đảm bảo bạn sử dụng lược đồ rõ ràng khi đọc chúng để tránh những điều bất ngờ khó chịu về
. Với sàn gỗ, lược đồ đã được tích hợp sẵn.

## Kết hợp
xanh và vàng
Truy vấn chúng tôi muốn chạy sử dụng `trips_data` - sự kết hợp giữa taxi màu vàng và
màu xanh lá cây. Vì vậy, trước tiên chúng tôi kết hợp hai DataFrames thành một.

Chúng tôi đọc cả hai bộ dữ liệu. Bởi vì trong một năm chúng ta có các thư mục tháng nên chúng ta sử dụng
`*/*` để vào các thư mục con và đọc cùng lúc 2020 và 2021:

```python
df_green = spark.read.parquet('data/pq/green/*/*')
df_yellow = spark.read.parquet('data/pq/yellow/*/*')
```

Hai lược đồ này tương tự nhau nhưng không giống nhau. Một số trường được chia sẻ, như
`fare_amount` và `congestion_surcharge`, nhưng màu xanh lá cây có các trường mà
màu vàng không có (như `ehail_fee`) và ngược lại. Chúng tôi muốn chỉ giữ lại
các cột mà cả hai bộ dữ liệu đều có.

Cách dễ nhất để tìm thấy chúng là lấy giao điểm của hai bộ
:

```python
set(df_green.columns) & set(df_yellow.columns)
```

Đối với các tập dữ liệu này, giao điểm chứa:

```text
{
    'DOLocationID',
    'PULocationID',
    'RatecodeID',
    'VendorID',
    'congestion_surcharge',
    'extra',
    'fare_amount',
    'improvement_surcharge',
    'mta_tax',
    'passenger_count',
    'payment_type',
    'store_and_fwd_flag',
    'tip_amount',
    'tolls_amount',
    'total_amount',
    'trip_distance'
}
```

Một vấn đề: các cột thời gian lấy và trả hàng được đặt tên khác nhau -
`lpep_pickup_datetime` màu xanh lá cây và `tpep_pickup_datetime` màu vàng. Chúng tôi
đổi tên chúng (với `withColumnRenamed`) thành `pickup_datetime` và
`dropoff_datetime` trong cả hai DataFrame. Sau đó, chúng tôi tính toán lại các cột chung
, giữ nguyên thứ tự của các cột màu xanh lá cây:

```python
common_colums = []

yellow_columns = set(df_yellow.columns)

for col in df_green.columns:
    if col in yellow_columns:
        common_colums.append(col)
```

Bây giờ, chúng tôi chọn các cột này từ cả hai DataFrame và trong khi thực hiện,
thêm một cột `service_type`, để sau này chúng tôi biết mỗi bản ghi đến từ đâu:

```python
from pyspark.sql import functions as F

df_green_sel = df_green \
    .select(common_colums) \
    .withColumn('service_type', F.lit('green'))

df_yellow_sel = df_yellow \
    .select(common_colums) \
    .withColumn('service_type', F.lit('yellow'))

df_trips_data = df_green_sel.unionAll(df_yellow_sel)
```

`F.lit` thêm một chữ - một giá trị không đổi - vào mỗi bản ghi. `unionAll`
đặt hai DataFrames lại với nhau thành một. Để kiểm tra tính chính xác, chúng tôi có thể đếm
các bản ghi của từng loại dịch vụ:

```python
df_trips_data.groupBy('service_type').count().show()
```

```text
+------------+--------+
|service_type|   count|
+------------+--------+
|       green| 2304517|
|      yellow|39649199|
+------------+--------+
```

Lưu ý rằng chỉ riêng `groupBy` không kích hoạt bất kỳ tính toán nào - đó là một thao tác
lười biếng trả về một DataFrame khác. `show()` thực sự là
thực thi nó.

## Từ DataFrames đến SQL

Bây giờ chúng ta có thể sử dụng SQL để truy vấn dữ liệu này. Spark có phương thức `sql` lấy
một chuỗi truy vấn - nhưng chúng ta không thể chỉ đặt tên của DataFrame trong mệnh đề
`FROM`. Đầu tiên chúng ta cần nói với Spark rằng DataFrame này là một bảng:

```python
df_trips_data.registerTempTable('trips_data')
```

Và bây giờ chúng ta có thể chạy SQL chống lại nó:

```python
spark.sql("""
SELECT
    service_type,
    count(1)
FROM
    trips_data
GROUP BY
    service_type
""").show()
```

Kết quả hoàn toàn giống với API DataFrame - cùng số,
chỉ có tên cột hơi khác một chút (`count(1)` thay vì `count`).

## Báo cáo doanh thu

Bây giờ truy vấn chúng tôi thực sự muốn chạy. Đó là cách tính doanh thu từ
tuần 4: đối với mỗi địa điểm lấy hàng (khu vực doanh thu), cho mỗi tháng và đối với
cho mỗi loại dịch vụ, chúng tôi tính toán doanh thu:

```python
df_result = spark.sql("""
SELECT
    -- Revenue grouping
    PULocationID AS revenue_zone,
    date_trunc('month', pickup_datetime) AS revenue_month,
    service_type,

    -- Revenue calculation
    SUM(fare_amount) AS revenue_monthly_fare,
    SUM(extra) AS revenue_monthly_extra,
    SUM(mta_tax) AS revenue_monthly_mta_tax,
    SUM(tip_amount) AS revenue_monthly_tip_amount,
    SUM(tolls_amount) AS revenue_monthly_tolls_amount,
    SUM(improvement_surcharge) AS revenue_monthly_improvement_surcharge,
    SUM(total_amount) AS revenue_monthly_total_amount,
    SUM(congestion_surcharge) AS revenue_monthly_congestion_surcharge,

    -- Additional calculations
    AVG(passenger_count) AS avg_monthly_passenger_count,
    AVG(trip_distance) AS avg_monthly_trip_distance
FROM
    trips_data
GROUP BY
    1, 2, 3
""")
```

Bởi vì chúng tôi đã tải dữ liệu trong hai năm cùng một lúc nên việc này sẽ tính toán số liệu thống kê
cho mỗi tháng cùng một lúc. Cuối cùng chúng ta lưu kết quả:

```python
df_result.write.parquet('data/report/revenue/', mode='overwrite')
```

Trong khi nó thực thi, chúng ta có thể xem giao diện người dùng Spark master: có 215 tác vụ
đang chạy và công việc kết hợp hai đầu vào - DataFrame taxi màu vàng
và DataFrame taxi màu xanh lá cây - sau đó thực hiện nhóm và ghi kết quả
vào sàn gỗ.

## Một tệp thay vì 200

Nếu xem xét `data/report/revenue` sau khi công việc kết thúc, chúng ta sẽ nhận được khá nhiều tệp
- khoảng 200, mỗi tệp chỉ có vài kilobyte. Thật thuận tiện khi
giảm số lượng tệp và để làm được điều đó, chúng tôi sử dụng `coalesce`.
giống như phân vùng lại, nhưng chúng tôi sử dụng nó khi muốn giảm số lượng phân vùng
- ở đây chỉ còn một:

```python
df_result.coalesce(1).write.parquet('data/report/revenue/', mode='overwrite')
```

Vì đường dẫn đã tồn tại nên chúng tôi cần `mode='overwrite'`. Quá trình này mất
khoảng 26 giây và sau đó chúng tôi có một tệp khoảng 500 KB với tất cả dữ liệu doanh thu
- cho mỗi tháng, cho từng loại taxi, cho từng địa điểm.

Lưu ý những gì đã xảy ra ở đây: chúng tôi đã viết lại kết quả vào cái mà chúng tôi giả vờ là hồ dữ liệu
- nó vẫn là một loạt tệp. Chúng tôi không ghi bất cứ điều gì vào kho dữ liệu
. Với Spark chúng ta có thể vận hành hoàn toàn trên hồ dữ liệu.

Tôi đã nói trước đó rằng nếu bạn có thể sử dụng SQL, có thể bạn không cần Spark - các công cụ
như Hive hoặc Presto có thể làm được. Nhưng không phải lúc nào bạn cũng có những công cụ đó và nếu
bạn đã có cụm Spark, tại sao không sử dụng nó để thực thi các truy vấn SQL?
Ngoài ra, bạn còn nhận được API DataFrame cho những thứ dễ dàng hơn để
thể hiện bằng mã.

## Vật liệu

* [`code/06_spark_sql.ipynb`](code/06_spark_sql.ipynb) - kết hợp màu xanh lá cây và màu vàng
vào một bảng tạm thời `trips_data` và chạy báo cáo doanh thu dưới dạng SQL.
* [`code/06_spark_sql.py`](code/06_spark_sql.py) - báo cáo tương tự như tập lệnh được tham số hóa
mà các đơn vị đám mây sau đó gửi đến một cụm.
