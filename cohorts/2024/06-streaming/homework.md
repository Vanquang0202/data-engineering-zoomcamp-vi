## Bài tập về nhà của Mô-đun 6 

Trong bài tập về nhà này, chúng ta sẽ mở rộng Bài tập về nhà của Mô-đun 5 và tìm hiểu về streaming với PySpark.

Thay vì Kafka, chúng tôi sẽ sử dụng Red Panda, một giải pháp thay thế
có sẵn cho Kafka. 

Đảm bảo bạn đã thiết lập các nội dung sau (nếu bạn đã làm bài tập về nhà và mô-đun trước đó):

- Docker (xem [mô-đun 1](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/01-docker-terraform))
- PySpark (xem [mô-đun 5](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/05-batch/setup))

Đối với bài tập về nhà này, chúng ta sẽ sử dụng các tệp từ bài tập về Mô-đun 5:

- Màu xanh lá cây Dữ liệu 2019-10 từ [tại đây](https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-10.csv.gz)



## Bắt đầu Red Panda

Hãy bắt đầu redpanda trong vùng chứa docker. 

Có file `docker-compose.yml` trong thư mục bài tập về nhà (lấy từ [tại đây](https://github.com/redpanda-data-blog/2023-python-gsg/blob/main/docker-compose.yml))

Copy file này vào thư mục bài tập về nhà và chạy

```bash
docker-compose up
```

(Thêm `-d` nếu bạn muốn chạy ở chế độ tách rời)


## Câu 1: Phiên bản Redpanda

Bây giờ chúng ta cùng tìm hiểu phiên bản của redpandas nhé. 

Để biết điều đó, hãy kiểm tra đầu ra của lệnh `rpk help` _bên trong vùng chứa_. Tên của thùng chứa là `redpanda-1`.

Tìm hiểu những gì bạn cần thực hiện dựa trên đầu ra `help`.

Phiên bản dựa trên đầu ra của lệnh bạn đã thực hiện là gì? (copy toàn bộ bản)


## Câu 2. Tạo chủ đề

Trước khi gửi dữ liệu đến máy chủ redpanda, chúng ta cần tạo chủ đề. Chúng tôi cũng thực hiện điều đó bằng lệnh `rpk`
mà chúng tôi đã sử dụng trước đây để tìm ra phiên bản của 
redpandas.

Đọc đầu ra của `help` và dựa vào đó tạo một chủ đề với tên `test-topic` 

Đầu ra của lệnh tạo chủ đề là gì? Bao gồm toàn bộ đầu ra trong câu trả lời của bạn.


## Câu hỏi 3. Kết nối với máy chủ Kafka

Chúng tôi cần đảm bảo có thể kết nối với máy chủ để sau này có thể gửi một số dữ liệu đến các chủ đề của nó

Trước tiên, hãy cài đặt trình kết nối kafka (tùy bạn nếu bạn muốn có một môi trường ảo riêng cho việc đó)

```bash
pip install kafka-python
```

Bạn có thể khởi động sổ ghi chép jupyter trong thư mục giải pháp của mình hoặc tạo một tập lệnh

Hãy bắt đầu hãy thử kết nối với máy chủ của chúng tôi:

```python
import json
import time 

from kafka import KafkaProducer

def json_serializer(data):
    return json.dumps(data).encode('utf-8')

server = 'localhost:9092'

producer = KafkaProducer(
    bootstrap_servers=[server],
    value_serializer=json_serializer
)

producer.bootstrap_connected()
```

Với điều kiện là bạn có thể kết nối với máy chủ, đầu ra của lệnh cuối cùng là gì?


## Câu hỏi 4. Gửi dữ liệu tới luồng

Bây giờ chúng ta đã sẵn sàng gửi một số dữ liệu thử nghiệm:

```python
t0 = time.time()

topic_name = 'test-topic'

for i in range(10):
    message = {'number': i}
    producer.send(topic_name, value=message)
    print(f"Sent: {message}")
    time.sleep(0.05)

producer.flush()

t1 = time.time()
print(f'took {(t1 - t0):.2f} seconds')
```

Mất bao nhiêu thời gian? Nó đã dành phần lớn thời gian ở đâu?

* Gửi tin nhắn
* Xả
* Cả hai đều mất khoảng thời gian gần như nhau

(Không xóa `time.sleep` khi trả lời câu hỏi này)


## Đọc dữ liệu bằng `rpk`

Bạn có thể xem các tin nhắn mà bạn gửi đến chủ đề bằng `rpk`:

```bash
rpk topic consume test-topic
```

Chạy lệnh trên và gửi tin nhắn một lần nữa để 
xem chúng


## Gửi dữ liệu taxi

Bây giờ hãy gửi dữ liệu thực tế của chúng ta:

* Đọc tệp csv.gz màu xanh lá cây
* Chúng ta sẽ chỉ cần các cột sau:
  * `'lpep_pickup_datetime',`
  * `'lpep_dropoff_datetime',`
  * `'PULocationID',`
  * `'DOLocationID',`
  * `'passenger_count',`
  * `'trip_distance',`
  * `'tip_amount'`

Lặp lại các bản ghi trong dataframe

```python
for row in df_green.itertuples(index=False):
    row_dict = {col: getattr(row, col) for col in row._fields}
    print(row_dict)
    break

    # TODO implement sending the data here
```

Lưu ý: cách lặp qua các bản ghi này hiệu quả hơn so với
to `iterrows`


## Câu hỏi 5: Gửi dữ liệu chuyến đi

* Tạo chủ đề `green-trips` và gửi dữ liệu đến đó
* Mất bao nhiêu thời gian tính bằng giây? (Bạn có thể làm tròn nó thành số nguyên)
* Đảm bảo bạn không bao gồm các khoảng ngủ trong mã của mình


## Tạo đối tượng tiêu dùng PySpark

Bây giờ hãy đọc dữ liệu với PySpark. 

Spark cần một thư viện (jar) để có thể kết nối với Kafka, 
vì vậy chúng ta cần nói với PySpark rằng nó cần sử dụng nó:

```python
import pyspark
from pyspark.sql import SparkSession

pyspark_version = pyspark.__version__
kafka_jar_package = f"org.apache.spark:spark-sql-kafka-0-10_2.12:{pyspark_version}"

spark = SparkSession \
    .builder \
    .master("local[*]") \
    .appName("GreenTripsConsumer") \
    .config("spark.jars.packages", kafka_jar_package) \
    .getOrCreate()
```

Bây giờ chúng ta có thể kết nối với luồng:

```python
green_stream = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "green-trips") \
    .option("startingOffsets", "earliest") \
    .load()
```

Để kiểm tra xem chúng ta có thể tiêu thụ từ luồng hay không, 
hãy xem bản ghi đầu tiên ở đó sẽ là gì. 

Trong Spark streaming, luồng được biểu diễn dưới dạng một chuỗi gồm 
lô nhỏ, mỗi lô batch là một RDD nhỏ (hoặc một dataframe nhỏ).

Vậy là chúng ta có thể thực thi một hàm trên mỗi mini-batch. Hãy chạy `take(1)` ở đó để xem chúng ta có gì trong luồng:

```python
def peek(mini_batch, batch_id):
    first_row = mini_batch.take(1)

    if first_row:
        print(first_row[0])

query = green_stream.writeStream.foreachBatch(peek).start()
```

Bạn sẽ thấy một bản ghi như thế này:

```
Row(key=None, value=bytearray(b'{"lpep_pickup_datetime": "2019-10-01 00:26:02", "lpep_dropoff_datetime": "2019-10-01 00:39:58", "PULocationID": 112, "DOLocationID": 196, "passenger_count": 1.0, "trip_distance": 5.88, "tip_amount": 0.0}'), topic='green-trips', partition=0, offset=0, timestamp=datetime.datetime(2024, 3, 12, 22, 42, 9, 411000), timestampType=0)
```

Bây giờ hãy dừng truy vấn để nó không tiếp tục tiêu thụ các tin nhắn từ luồng

```python
query.stop()
```

## Câu hỏi 6. Phân tích dữ liệu

Dữ liệu là JSON, nhưng hiện tại nó ở định dạng nhị phân. Chúng ta cần phân tích cú pháp và biến nó thành streaming dataframe với các cột thích hợp.

Tương tự như PySpark, chúng tôi xác định lược đồ

```python
from pyspark.sql import types

schema = types.StructType() \
    .add("lpep_pickup_datetime", types.StringType()) \
    .add("lpep_dropoff_datetime", types.StringType()) \
    .add("PULocationID", types.IntegerType()) \
    .add("DOLocationID", types.IntegerType()) \
    .add("passenger_count", types.DoubleType()) \
    .add("trip_distance", types.DoubleType()) \
    .add("tip_amount", types.DoubleType())
```

Và áp dụng lược đồ này:

```python
from pyspark.sql import functions as F

green_stream = green_stream \
  .select(F.from_json(F.col("value").cast('STRING'), schema).alias("data")) \
  .select("data.*")
```

Bản ghi trông như thế nào sau khi phân tích cú pháp? Sao chép đầu ra. 


### Câu hỏi 7: Điểm đến phổ biến nhất

Bây giờ, cuối cùng chúng ta hãy thực hiện một số phân tích streaming. Chúng tôi sẽ
xem đâu là điểm đến phổ biến nhất hiện nay 
dựa trên luồng dữ liệu của chúng tôi (lý tưởng nhất là chúng tôi nên 
gửi với độ trễ như chúng tôi đã làm trong hội thảo 2)


Đây là cách bạn có thể thực hiện:

* Thêm cột "dấu thời gian" bằng chức năng `current_timestamp`
* Nhóm theo:
  * Cửa sổ 5 phút dựa trên cột dấu thời gian (`F.window(col("timestamp"), "5 minutes")`)
  * `"DOLocationID"`
* Sắp xếp theo số lượng

Bạn có thể in đầu ra ra bảng điều khiển bằng cách này 
code

```python
query = popular_destinations \
    .writeStream \
    .outputMode("complete") \
    .format("console") \
    .option("truncate", "false") \
    .start()

query.awaitTermination()
```

Viết điểm đến phổ biến nhất, câu trả lời của bạn phải là *hoặc* khu vực ID hoặc tên khu vực của điểm đến này. (Bạn sẽ cần gửi lại dữ liệu để việc này hoạt động)


## Gửi giải pháp

* Mẫu gửi: https://courses.datatalks.club/de-zoomcamp-2024/homework/hw6


## Giải pháp

Chúng tôi sẽ công bố giải pháp tại đây sau thời hạn.


