---
video_url: https://www.youtube.com/watch?v=ti3aC1m3rE8
prev_url: 04-first-look-at-spark.md
next_url: 06-preparing-taxi-data.md
---
# Spark DataFrames

Trong phần này, chúng ta sẽ nói nhiều hơn về Spark DataFrames - `df` mà chúng tôi đã sử dụng
. Chúng trông tương tự như DataFrames của gấu trúc, nhưng không hoàn toàn:
chúng ta thấy chúng khác nhau như thế nào cũng như các hành động và biến đổi là gì.

## Đọc sàn gỗ

Hãy cùng đọc các file sàn gỗ mà chúng ta đã tạo ở video trước:

```python
df = spark.read.parquet('fhvhv/2021/01/')
```

Chúng tôi không chỉ định lược đồ ở đây vì các tệp sàn gỗ chứa thông tin lược đồ
- các loại cho mỗi cột: chuỗi, dấu thời gian, số nguyên
. Thay vì nhìn vào `df.schema`, có một cách hay hơn:

```python
df.printSchema()
```

Lược đồ được lưu trữ trong sàn gỗ là:

```text
root
 |-- hvfhs_license_num: string (nullable = true)
 |-- dispatching_base_num: string (nullable = true)
 |-- pickup_datetime: timestamp (nullable = true)
 |-- dropoff_datetime: timestamp (nullable = true)
 |-- PULocationID: integer (nullable = true)
 |-- DOLocationID: integer (nullable = true)
 |-- SR_Flag: string (nullable = true)
```

Đây cũng là một trong những lý do khiến tệp sàn gỗ nhỏ hơn: chúng biết lược đồ
và sử dụng các cách nén dữ liệu hiệu quả hơn. Đối với ví dụ
, một số nguyên chiếm 4 byte, thay vì nhiều byte, giá trị CSV văn bản thuần túy
cần có.

## Chọn và lọc

Chúng ta có thể làm những việc thông thường với gấu trúc. Để chỉ giữ lại một vài cột
, hãy sử dụng `select`:

```python
df.select('pickup_datetime', 'dropoff_datetime',
          'PULocationID', 'DOLocationID')
```

Kết quả là một DataFrame có bốn cột sau:

```text
DataFrame[pickup_datetime: timestamp, dropoff_datetime: timestamp,
          PULocationID: int, DOLocationID: int]
```

DataFrame này hiện chỉ chứa bốn cột này. Chúng tôi cũng có thể lọc các hàng
:

```python
df.filter(df.hvfhs_license_num == 'HV0003')
```

Chạy cái này và... không có gì xảy ra. Giao diện người dùng Spark không hiển thị công việc mới. Lý do
là các lệnh này lười biếng, giống như `repartition` trong đơn vị trước
. Chỉ khi chúng tôi thêm `.show()` thì Spark mới thực sự thực thi
- khi đó một công việc sẽ xuất hiện trong giao diện người dùng.

## Hành động và biến đổi

Spark phân biệt giữa những thứ được thực thi ngay lập tức và những thứ
không được thực thi. Những cái lười biếng được gọi là phép biến đổi: chúng
biến đổi dữ liệu - chọn cột, lọc hàng, áp dụng hàm
cho một cột - nhưng chúng không được thực thi ngay lập tức. Những người háo hức
được gọi là hành động: chúng kích hoạt đánh giá.

Cụ thể: chúng tôi bắt đầu với DataFrame gốc, áp dụng `select`, sau đó là
`filter`, sau đó có thể nhiều chuyển đổi hơn. Spark chỉ ghi lại chuỗi
này - chưa có dữ liệu nào được chạm vào. Thời điểm chúng tôi gọi `show()`, toàn bộ chuỗi
sẽ được đánh giá và chúng tôi sẽ thấy kết quả. Nếu chúng ta xem xét giao diện người dùng Spark
tại thời điểm đó, Spark dường như nén tất cả các phép biến đổi
này thành một giai đoạn và thực hiện chúng cùng một lúc.

Ví dụ về hành động:

- `show()` - in kết quả
- `take(5)` và `head(5)` - nhận năm bản ghi
- `write.csv(...)` và `write.parquet(...)` - có thể là bản ghi chính:
ghi kết quả sẽ kích hoạt toàn bộ biểu đồ chuyển đổi

Ngoài ra còn có `groupBy` - bạn chỉ định cột để nhóm theo và
cần tính toán. Chúng tôi sẽ không đi vào chi tiết ở đây; tài liệu chính thức của
khá tốt và thành thật mà nói, để tổng hợp, tôi sẽ sử dụng
với SQL mà chúng tôi sẽ đề cập trong video tiếp theo. Nó biểu cảm hơn.

Nhìn vào mã select-plus-filter, bạn có thể thắc mắc:
này không phải chỉ là SQL sao? Đó là - thứ tương tự được viết dưới dạng truy vấn sẽ là
`SELECT pickup_datetime, dropoff_datetime, PULocationID, DOLocationID
FROM df WHERE hvfhs_license_num = 'HV0003'`. Vậy tại sao phải bận tâm với API DataFrame
? Bởi vì nó linh hoạt hơn và một trong những thứ mà
mang lại cho chúng ta là các hàm do người dùng xác định.

## Chức năng tích hợp

Cách thực hiện mọi việc của DataFrame linh hoạt hơn SQL và một trong những thứ
mà nó mang lại cho chúng ta là các hàm do người dùng xác định. Trước khi có
ở đó, hãy xem Spark đã có những chức năng nào.

Spark cung cấp một tập hợp các chức năng tích hợp sẵn trong `pyspark.sql.functions`,
được nhập theo quy ước dưới dạng `F`:

```python
from pyspark.sql import functions as F
```

Nhập `F.` và nhấn tab - có khá nhiều trong số chúng. Cái mà chúng tôi muốn
là `to_date`: nó lấy một ngày giờ và chỉ giữ lại ngày, loại bỏ
giờ, phút và giây.

Để áp dụng nó, chúng tôi sử dụng `withColumn`, thêm một cột mới vào Khung dữ liệu
- cũng là một phép chuyển đổi:

```python
df.withColumn('pickup_date', F.to_date(df.pickup_datetime)) \
  .withColumn('dropoff_date', F.to_date(df.dropoff_datetime)) \
  .show()
```

Bây giờ có hai cột mới, `pickup_date` và `dropoff_date`. Nếu chúng tôi
đặt tên đã tồn tại, cột sẽ bị ghi đè - nhưng hãy cẩn thận với
: ghi đè `pickup_datetime` chỉ với một ngày sẽ thay đổi ngữ nghĩa của
, vì vậy tốt hơn nên chọn các cột mới:

```python
df.withColumn('pickup_date', F.to_date(df.pickup_datetime)) \
  .withColumn('dropoff_date', F.to_date(df.dropoff_datetime)) \
  .select('pickup_date', 'dropoff_date', 'PULocationID', 'DOLocationID') \
  .show()
```

## Hàm do người dùng định nghĩa

Có một danh sách rất lớn các hàm tích hợp, nhưng đôi khi bạn cần
logic của riêng mình. Trong kho dữ liệu, việc xác định các chức năng của riêng bạn là điều phức tạp của
. Nhưng PySpark là Python: bạn có thể đặt mã vào repo git
của mình, bao gồm các thử nghiệm và sau đó thực thi nó trên DataFrames của bạn.

Hãy viết một hàm thực hiện một điều gì đó điên rồ - điều mà
không dễ diễn đạt bằng SQL. Giả sử nó lấy số cơ sở gửi đi như
`B02884`, loại bỏ ký tự đầu tiên, biến phần còn lại thành số nguyên,
và sau đó:

```python
def crazy_stuff(base_num):
    num = int(base_num[1:])
    if num % 7 == 0:
        return f's/{num:03x}'
    elif num % 3 == 0:
        return f'a/{num:03x}'
    else:
        return f'e/{num:03x}'
```

Nếu số chia hết cho 7, kết quả bắt đầu bằng `s` và số
được hiển thị ở dạng hex; nếu chia hết cho 3 thì bắt đầu bằng
`a`; nếu không thì `e`. Hoàn toàn được tạo thành - nhưng giả sử đây là những yêu cầu kinh doanh của
. Việc thể hiện điều này bằng SQL không được tốt lắm,
, đặc biệt là khi các điều kiện ngày càng tăng.

Kiểm tra độ chính xác nhanh: `crazy_stuff('B02884')` mang lại `s/b44`.

Bây giờ chúng ta biến hàm Python thông thường này thành hàm
do người dùng xác định, UDF:

```python
crazy_stuff_udf = F.udf(crazy_stuff, returnType=types.StringType())
```

Theo mặc định kiểu trả về là chuỗi; nếu chúng tôi trả về một số nguyên,
chúng tôi sẽ cần phải nói điều đó một cách rõ ràng. Bây giờ chúng ta có thể sử dụng nó trong `withColumn`:

```python
df \
    .withColumn('base_id', crazy_stuff_udf(df.dispatching_base_num)) \
    .select('base_id', 'pickup_date', 'dropoff_date',
            'PULocationID', 'DOLocationID') \
    .show()
```

Đây cũng là một sự chuyển đổi - mọi thứ đều lười biếng cho đến khi chúng ta thực thi
hành động `show()`.

Mặc dù ví dụ này được tạo nên nhưng các quy tắc kinh doanh thực tế có thể gặp khá khó khăn về
. Trong SQL, bạn kết thúc với một loạt các câu lệnh `CASE` lồng nhau,
truy vấn trông xấu và SQL rất khó kiểm tra - dbt có ích,
nhưng vẫn không dễ như kiểm tra mã Python.

Đó là điều tuyệt vời về Spark: bạn có được những điều tốt nhất của cả hai thế giới.
Sử dụng SQL cho các phần có thể biểu thị tự nhiên bằng SQL và thả
vào Python với UDF cho những nội dung điên rồ - và logic học máy
thường trông giống như những nội dung điên rồ. Trong video tiếp theo, chúng ta sẽ xem cách sử dụng
SQL bên trong Spark.

## Vật liệu

* [`code/04_pyspark.ipynb`](code/04_pyspark.ipynb) - suy ra lược đồ thông qua gấu trúc
, khai báo `StructType` rõ ràng, phân vùng lại, viết sàn gỗ, hành động
so với chuyển đổi, hàm tích hợp và hàm do người dùng xác định.
