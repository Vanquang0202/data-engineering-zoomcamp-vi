---
video_url: https://www.youtube.com/watch?v=HXBwSlXo5IA
prev_url: 13-connecting-to-google-cloud-storage.md
next_url: 15-setting-up-a-dataproc-cluster.md
---
# Tạo cụm Spark cục bộ

Trong phần này, chúng tôi lấy công việc Spark SQL từ các bài trước ra khỏi sổ ghi chép
: chúng tôi biến sổ ghi chép thành tập lệnh Python, tạo cụm
Spark độc lập với một bản chính và một trình thực hiện, đồng thời gửi công việc tới đó bằng
`spark-submit`. Mặc dù chúng tôi chạy mọi thứ trên cùng một máy, nhưng đây là
, cùng một quy trình mà bạn sẽ sử dụng để gửi công việc đến một cụm thực, bao gồm
mà chúng tôi tạo trong phần tiếp theo.

## Sổ ghi chép là một cụm dọc theo

Khi chúng tôi tạo SparkSession với `local[*]` trong sổ ghi chép, Spark khởi động
một cụm cục bộ phía sau hậu trường và sổ ghi chép của chúng tôi kết nối với nó - URL
là `local[*]` và giao diện người dùng web tồn tại trên cổng 4040. Khi chúng tôi tắt hạt nhân
, cụm đó sẽ biến mất cùng với nó.

Điều đó thuận tiện cho việc thử nghiệm nhưng nó gắn kết tuổi thọ của cụm với máy tính xách tay
. Để lên lịch công việc này sau - ví dụ từ Airflow - chúng tôi
cần một cụm tồn tại độc lập với bất kỳ sổ ghi chép nào và một tập lệnh mà chúng tôi
có thể gửi tới nó.

## Khởi động
chính
Spark cung cấp các tập lệnh để chạy cụm độc lập
(xem [Tài liệu độc lập về Spark](https://spark.apache.org/docs/latest/spark-standalone.html)).
Từ thư mục chính của Spark, khởi động bản gốc:

```bash
./sbin/start-master.sh
```

Bản gốc có giao diện người dùng web, nhưng không giống như cụm do sổ ghi chép tạo ra, nó không phải là
trên cổng 4040 - một bản gốc độc lập lắng nghe trên cổng 8080. Mở nó trong trình duyệt
và bạn thấy bản gốc chưa có nhân viên nào được kết nối:

Các phần ổn định của chế độ xem chính ban đầu là:

| Kiểm tra giao diện người dùng chính | Kết quả mong đợi |
|---|---|
| Cổng giao diện người dùng web | `8080` |
| Trạng thái | `ALIVE` |
| Công nhân | chưa đăng ký |
| Ứng dụng | chưa có |
| URL kết nối chính | `spark://<master-host>:7077` |

URL chính được hiển thị ở đầu giao diện người dùng dưới dạng
`spark://<master-host>:7077`. Đây là địa chỉ mà nhân viên và ứng dụng
sử dụng để kết nối. Thay thế `<master-host>` bằng tên máy chủ hoặc địa chỉ
được in bởi chủ của bạn.

## Đang kết nối với
chính
Chúng ta có thể trỏ sổ ghi chép của mình vào chủ này thay vì `local[*]`:

```python
master = "spark://<master-host>:7077"

spark = SparkSession.builder \
    .appName('test') \
    .master(master) \
    .getOrCreate()
```

Giờ đây, việc chạy một ô sẽ kết nối sổ ghi chép với bản chính độc lập - ứng dụng
hiển thị trong giao diện người dùng chính.

## Thêm công nhân

Nếu bây giờ chúng tôi thực hiện một công việc, nó sẽ bị treo với cảnh báo sau:

```
Initial job has not accepted any resources; check your cluster UI to
ensure that workers are registered and have sufficient resources
```

Lý do rất đơn giản: chúng tôi thành lập một ông chủ nhưng không có công nhân. Một tọa độ chính chỉ có tọa độ
- việc thực thi thực tế xảy ra ở các công nhân còn chúng tôi thì không.
Trong một thiết bị đầu cuối khác, vẫn trong thư mục Spark, hãy khởi động một:

```bash
URL="spark://<master-host>:7077"
./sbin/start-slave.sh ${URL}

# for newer versions of spark use that:
#./sbin/start-worker.sh ${URL}
```

Phiên bản Spark của chúng tôi cũ hơn, trong đó công nhân được gọi là nô lệ - trên các phiên bản
mới hơn, tập lệnh là `start-worker.sh`. Sau khi khởi động,
worker xuất hiện trong giao diện người dùng chính. Các phần ổn định của chế độ xem tiếp theo đó là:

| Kiểm tra giao diện người dùng chính | Kết quả mong đợi |
|---|---|
| Công nhân | một công nhân đã đăng ký |
| Trạng thái ứng dụng | công việc đang chờ xử lý có thể nhận tài nguyên và chạy |
| Mã định danh thời gian chạy | máy chủ, IP, ID nhân viên, ID ứng dụng và giá trị người dùng là cục bộ và bị bỏ qua |

Bây giờ công việc đang chờ xử lý sẽ nhận được tài nguyên và thực thi. Ứng dụng sổ ghi chép
được kết nối với một cụm thực với một nhân viên.

## Biến sổ ghi chép thành tập lệnh

Jupyter có thể chuyển đổi sổ ghi chép thành tập lệnh Python đơn giản với nbconvert:

```bash
jupyter nbconvert --to=script 06_spark_sql.ipynb
```

`06_spark_sql.py` được tạo cần dọn dẹp một chút: xóa nhận xét `In
[...]` và các dòng ma thuật, giữ lại nội dung nhập và thiết lập SparkSession
. Trong video, chúng tôi cũng thay thế danh sách cột được tạo bằng danh sách
rõ ràng `common_columns`, danh sách này đọc tốt hơn trong tập lệnh.

Nếu chúng tôi chạy tập lệnh ngay lập tức với `python 06_spark_sql.py`, nó sẽ kết nối
với tập lệnh chính và bắt đầu thực thi. Nhưng hãy nhìn vào giao diện người dùng chính: công việc
lại nằm ở "Công việc ban đầu chưa chấp nhận bất kỳ tài nguyên nào". Lần này nguyên nhân của
lại khác - ứng dụng notebook vẫn được kết nối và lấy đi tất cả các lõi có sẵn của
nên không còn gì cho tập lệnh. Việc tắt
trong nhân máy tính xách tay sẽ giải phóng các lõi và tập lệnh sẽ chạy qua.

## Tạo tập lệnh có thể định cấu hình

Kịch bản mã hóa đường dẫn đầu vào và đầu ra của nó. Đối với một công việc, chúng tôi muốn lập lịch
- chạy nó trong một tháng, một năm hoặc một đầu ra khác -
, những đường dẫn đó phải đến từ dòng lệnh. Chúng tôi sử dụng `argparse`, cùng gói
mà chúng tôi đã sử dụng cho tập lệnh nhập trong mô-đun một:

```python
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--input_green', required=True)
parser.add_argument('--input_yellow', required=True)
parser.add_argument('--output', required=True)

args = parser.parse_args()

input_green = args.input_green
input_yellow = args.input_yellow
output = args.output
```

Các đối số được phân tích cú pháp thay thế các đường dẫn được mã hóa cứng trong tập lệnh. Bây giờ chúng tôi có thể
chạy cùng một công việc trong bất kỳ khoảng thời gian nào, ví dụ: chỉ năm 2020:

```bash
python 06_spark_sql.py \
    --input_green=data/pq/green/2020/*/ \
    --input_yellow=data/pq/yellow/2020/*/ \
    --output=data/report-2020
```

Nó kết thúc nhanh chóng - không có nhiều dữ liệu năm 2020 - và báo cáo đưa ra
trong `data/report-2020`.

## Gửi bằng spark-submit

Mã hóa cứng URL chính bên trong tập lệnh vẫn không thực tế: cùng một tập lệnh
có thể cần chạy trên một cụm cục bộ hôm nay và một cụm
khác với Airflow vào ngày mai. Và có những thứ khác mà chúng tôi có thể muốn định cấu hình
mỗi lần chạy, chẳng hạn như số lượng trình thực thi sẽ sử dụng và dung lượng bộ nhớ
mà chúng nhận được. Trong thực tế, cấu hình này nằm ngoài tập lệnh và
công cụ cung cấp nó là `spark-submit`, đi kèm với Spark:

```bash
URL="spark://<master-host>:7077"

spark-submit \
    --master="${URL}" \
    06_spark_sql.py \
        --input_green=data/pq/green/2021/*/ \
        --input_yellow=data/pq/yellow/2021/*/ \
        --output=data/report-2021
```

Mọi thứ trước tệp Python là cấu hình cho Spark -
master và những thứ tùy chọn như bộ nhớ thực thi hoặc số lõi
. Mọi thứ sau tên tệp đều được chuyển đến chính công việc đó, vì vậy các đối số
`argparse` của chúng tôi sẽ ở cuối.

Đây là cách bạn gửi các công việc Spark trong thực tế và đó cũng là cách
kết nối chúng vào Airflow sau này. Khi quá trình kết thúc, `data/report-2021`
xuất hiện bên cạnh báo cáo năm 2020 - cùng một tập lệnh, cùng một cụm, các tham số
khác nhau.

Tập lệnh đầy đủ là [`code/06_spark_sql.py`](code/06_spark_sql.py).

## Dừng cụm

Một điều cần nhớ: khi bạn hoàn tất, hãy dừng nhân viên và
chính bằng các tập lệnh phù hợp từ cùng thư mục `sbin`:

```bash
./sbin/stop-slave.sh ${URL}   # ./sbin/stop-worker.sh on newer versions
./sbin/stop-master.sh
```

Sau đó, không có gì chạy và cố gắng kết nối sẽ báo lỗi - cụm
thực sự đã biến mất.
