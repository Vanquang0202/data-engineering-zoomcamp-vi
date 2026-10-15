---
video_url: https://www.youtube.com/watch?v=hqUbB9c8sKg
prev_url: 02-introduction-to-spark.md
next_url: 04-first-look-at-spark.md
---
#Cài đặt Spark

Phần này hướng dẫn cài đặt Spark trên Linux, trên máy
ảo trên đám mây từ tuần đầu tiên - các bước tương tự hoạt động trên Linux thuần túy và trên Hệ thống con Windows
dành cho Linux. Video hiển thị cách cài đặt thủ công Spark
3.0.3; hướng dẫn bằng văn bản trong phần Tài liệu bên dưới có lộ trình
đơn giản hơn với Spark 4.x, trong đó việc cài đặt gói pip `pyspark` sẽ mang đến cho
một Spark đi kèm.

## Cài đặt Java

Spark chạy trên JVM nên trước tiên chúng ta cài đặt Java. Đối với Spark 3.0.3, chúng tôi
cần JDK 8 hoặc 11 - JDK hiện tại vào thời điểm đó, 17, không hoạt động với
, vì vậy chúng tôi sử dụng một phiên bản cũ hơn. Trang tải xuống liệt kê tất cả các phiên bản; chúng tôi
chọn 11 và chọn bản dựng Linux. Đối với Windows, có một hướng dẫn
riêng và ở đó tốt hơn nên sử dụng Oracle JDK; trên Linux OpenJDK
vẫn ổn.

Chúng tôi tạo thư mục `spark` trong thư mục chính và tải xuống kho lưu trữ
OpenJDK tại đó:

```bash
mkdir ~/spark
cd ~/spark
wget <the openjdk 11 link copied from the download page>
tar xzf <the archive>
rm <the archive>
```

Điều này cung cấp cho chúng tôi một thư mục `jdk-11.0.1`. Bây giờ chúng tôi đặt hai biến môi trường
. `JAVA_HOME` phải được gọi chính xác như vậy - Các tập lệnh
của Spark sẽ tìm kiếm nó. Sử dụng `$HOME` thay vì `~`: cả hai đều có nghĩa giống nhau, nhưng
`$HOME` thường hoạt động tốt hơn trong các tập lệnh.

```bash
export JAVA_HOME=$HOME/spark/jdk-11.0.1
export PATH=$JAVA_HOME/bin:$PATH
```

Kiểm tra xem nó có hoạt động không:

```bash
which java
java --version
```

Phiên bản phải là 11.0.1 - một phiên bản cũ, như dự định.

## Cài đặt Spark

Tiếp theo, chính Spark. Đi đến trang tải xuống Spark và chọn bản phát hành
3.0.3. Lý do cho bản phát hành cũ hơn này là vì nó hoạt động tốt trên Windows
; nếu bạn cảm thấy thích phiêu lưu, bạn có thể thử một cái mới hơn, nhưng
không đảm bảo sẽ hoạt động. Đối với loại gói, hãy chọn "Được tạo sẵn cho
Apache Hadoop 3.2" - một lần nữa hầu hết đều quan trọng đối với người dùng Windows, nhưng
giúp mọi người nhất quán.

Nhấp vào liên kết tải xuống, sau đó tải xuống bằng `wget` trên máy
từ xa. Hãy cẩn thận ở đây: trong video, máy nhân bản đầu tiên cung cấp kho lưu trữ
bị hỏng và quá trình tải xuống phải được thực hiện lại từ một máy nhân bản khác.
Sau khi giải nén chúng ta được thư mục `spark-3.0.3-bin-hadoop3.2`, chúng ta thực hiện
tương tự như với Java:

```bash
tar xzf spark-3.0.3-bin-hadoop3.2.tgz
rm spark-3.0.3-bin-hadoop3.2.tgz
export SPARK_HOME=$HOME/spark/spark-3.0.3-bin-hadoop3.2
export PATH=$SPARK_HOME/bin:$PATH
```

## Thử nghiệm với spark-shell

Bây giờ chúng ta có thể kiểm tra xem mọi thứ có hoạt động không. Khởi động vỏ Spark:

```bash
spark-shell
```

Bạn sẽ thấy một số cảnh báo - bạn có thể bỏ qua chúng. Shell Spark chạy mã Scala
. Hãy thử nghiệm nó bằng một công việc nhỏ:

```scala
val data = 1 to 10000
val distData = sc.parallelize(data)
distData.filter(_ < 10).collect()
```

Shell trả về các giá trị từ 1 đến 9:

```text
res0: Array[Int] = Array(1, 2, 3, 4, 5, 6, 7, 8, 9)
```

Ở đây `data` là một dãy số từ 1 đến 10000. `parallelize` biến
thành RDD - một thứ nội bộ của Spark, một bộ sưu tập phân tán.
Dữ liệu trở nên song song: dữ liệu hiện nằm trên cụm (trong trường hợp
của chúng tôi chỉ là một máy này). Sau đó, chúng tôi xem xét tất cả các con số và
chỉ giữ lại những con số dưới 10 và `collect` sẽ trả về kết quả. Đầu ra của
là các số từ 1 đến 9 - một công việc Spark đơn giản để xác nhận mọi thứ mà
hoạt động.

## Tạo các biến vĩnh viễn

Chúng tôi không muốn nhập những bản xuất này mỗi khi đăng nhập. Mở
`~/.bashrc` bằng trình chỉnh sửa như `nano`, dán bốn dòng `export`
ở cuối, lưu và thoát. Sau đó đánh giá lại tệp:

```bash
source ~/.bashrc
```

hoặc đơn giản là ngắt kết nối và kết nối lại với máy. Bây giờ `which java`
và `which spark-shell` đều tìm thấy các tệp nhị phân của chúng - các biến được đặt
mỗi khi chúng tôi mở một thiết bị đầu cuối.

## Chạy PySpark

Đối với PySpark, chúng tôi tạo thư mục `notebooks` và khởi động Jupyter ở đó.
Vì đây là máy từ xa nên chúng tôi chuyển tiếp cổng 8888 - trong Mã VS,
mở thiết bị đầu cuối bằng `` ctrl+` `` và sử dụng tab Cổng để chuyển tiếp
8888, cổng mà Jupyter sử dụng.

Trước khi bắt đầu Jupyter, chúng ta cần cho Python biết PySpark tồn tại ở đâu.
Trước tiên hãy chạy các bản xuất này từ hướng dẫn thiết lập:

```bash
export PYTHONPATH="$SPARK_HOME/python/:$PYTHONPATH"
export PYTHONPATH="$SPARK_HOME/python/lib/py4j-0.10.9-src.zip:$PYTHONPATH"
```

`PYTHONPATH` giống như `PATH`, nhưng đối với Python: nó cho Python biết nơi
tìm gói. Dòng đầu tiên thêm `$SPARK_HOME/python`, nơi
PySpark tồn tại. Phần thứ hai bổ sung thêm các phụ thuộc bổ sung mà PySpark cần.
Nếu không có những thứ này, `import pyspark` sẽ không hoạt động.

Bây giờ hãy khởi động Jupyter, tạo sổ ghi chép và kiểm tra quá trình nhập:

```python
import pyspark
pyspark.__file__
```

Điều này trỏ đến thư mục Spark mà chúng ta vừa cài đặt. Sau đó:

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .master("local[*]") \
    .appName('test') \
    .getOrCreate()
```

SparkSession là thứ cho chúng tôi biết chính xác cách chúng tôi kết nối với
Spark. Với `master("local[*]")`, chúng tôi tạo một cụm cục bộ:
chính là thứ điều phối các công việc của cụm Spark, `local` có nghĩa là nó chạy
trên máy này và `*` có nghĩa là sử dụng tất cả các CPU có sẵn - chúng tôi cũng có thể nói
là `local[2]` cho hai CPU. `getOrCreate` trả về phiên
hiện có hoặc tạo một phiên mới nếu không có. Các cảnh báo tương tự như trước khi
xuất hiện và chúng tôi lại bỏ qua chúng.

## Đọc CSV và viết sàn

Hãy làm điều gì đó thực tế. Tải xuống tệp tra cứu khu vực taxi - bạn đã thấy
trong các tuần trước - và đọc nó bằng Spark:

```python
df = spark.read.csv('taxi+_zone_lookup.csv')
df.show()
```

Nhìn vào đầu ra, Spark không hiểu rằng `LocationID`,
`Borough` và phần còn lại là các tiêu đề của tệp CSV - các cột
lấy những cái tên không có nhiều ý nghĩa. Chúng ta cần yêu cầu nó tải tiêu đề
:

```python
df = spark.read \
    .option("header", "true") \
    .csv('taxi+_zone_lookup.csv')
df.show()
```

Bây giờ tên cột đã đúng. Hãy lưu nó dưới dạng sàn gỗ:

```python
df.write.parquet('zones')
```

Công việc diễn ra nhanh đến mức chúng tôi khó có thể nhìn thấy sự tiến triển. Nếu chúng ta nhìn vào thư mục
, `zones` không phải là một tệp mà là một thư mục và bên trong có hai thứ
: chính tệp sàn gỗ và một tệp `_SUCCESS`, đánh dấu công việc
là thành công.

## Giao diện người dùng Spark

Một điều nữa trước khi chúng ta kết thúc: chuyển tiếp một cổng khác, 4040 và mở
localhost:4040 trong trình duyệt của bạn. Đây là giao diện của Spark
master - nó hiển thị tất cả các công việc chúng tôi đã thực hiện và chúng tôi sẽ sử dụng nó
trong suốt mô-đun để xem chính xác Spark đang làm gì. Nếu bạn chạy
Spark cục bộ thì bạn không cần chuyển tiếp bất kỳ thứ gì: thời điểm Spark
khởi động, nó khởi động bản gốc cục bộ và giao diện người dùng ở ngay trên cổng
đó.

Đó là cài đặt Linux. Đối với Windows, các bước cũng tương tự, cộng thêm phần Hadoop
mà Linux không cần. Đối với Mac, hướng dẫn Linux
có thể hoạt động mà không gặp vấn đề gì. Trong video tiếp theo, chúng tôi viết ứng dụng PySpark
đầu tiên của mình và thử nghiệm nó với tập dữ liệu taxi FHV khối lượng lớn
cho tháng 1 năm 2021.

## Vật liệu

Video hướng dẫn cài đặt Linux và được đánh dấu là tùy chọn trong mô-đun
README. Hướng dẫn bằng văn bản bao gồm cả ba nền tảng:

* [Windows](setup/windows.md)
* [Linux](setup/linux.md)
* [MacOS](setup/macos.md)

Ngoài ra, nếu các thiết lập ở trên không hoạt động, bạn có thể chạy Spark trong Google Colab.

> [!NOTE]
> Bạn nên đầu tư một chút thời gian vào việc thiết lập mọi thứ cục bộ thay vì lao ngay vào giải pháp này

* [Hướng dẫn về Google Colab](https://medium.com/gitconnected/launch-spark-on-google-colab-and-connect-to-sparkui-342cad19b304)
* [Sổ tay khởi đầu Google Colab](https://github.com/aaalexlit/medium_articles/blob/main/Spark_in_Colab.ipynb)

Spark on YARN, cần thiết cho vật liệu Spark-and-Docker thay vì thiết bị
này, có hướng dẫn riêng: [Hadoop và YARN](setup/hadoop-yarn.md).
