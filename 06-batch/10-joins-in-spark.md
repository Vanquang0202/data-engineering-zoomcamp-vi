---
video_url: https://www.youtube.com/watch?v=lu7TrqAWuH4
prev_url: 09-groupby-in-spark.md
next_url: 11-operations-on-spark-rdds.md
---
# Tham gia Spark

Trong phần này, chúng ta xem xét các phép nối trong Spark. Chúng tôi đề cập đến hai trường hợp - nối hai bảng
có kích thước tương tự nhau và nối một bảng lớn với một bảng nhỏ - và chúng tôi
xem cách cả hai được thực thi nội bộ: với sắp xếp hợp nhất bên ngoài và việc xáo trộn
mà chúng tôi đã biết từ [group by](09-groupby-in-spark.md).

## Nối hai bảng doanh thu

Nơi chúng tôi đã dừng lại lần trước: chúng tôi có hai bảng, doanh thu hàng giờ cho taxi xanh
và doanh thu hàng giờ cho taxi màu vàng. Mỗi cái có giờ, vùng
, số lượng và số chuyến đi. Chúng tôi muốn tham gia cùng họ theo giờ và vùng
và có một bảng rộng hơn: giờ, vùng, sau đó là doanh thu màu vàng và các chuyến đi
bên cạnh doanh thu và chuyến đi xanh.

```python
df_join = df_green_revenue_temp \
    .join(df_yellow_revenue_temp, on=['hour', 'zone'], how='outer')
```

Loại kết nối là `outer`: khi một bản ghi tồn tại ở màu xanh lục nhưng không có màu vàng,
chúng tôi vẫn muốn có bản ghi đó trong kết quả - với các giá trị rỗng trong các cột màu vàng - và ngược lại là
.

Lưu ý rằng `show()` (hoặc `write`) này thực thi toàn bộ chuỗi ngay từ đầu
: nó đọc các tệp sàn gỗ, chạy truy vấn doanh thu màu xanh lục,
đọc một tập hợp các tệp sàn khác, chạy truy vấn doanh thu màu vàng và sau đó chỉ
mới tham gia.

Trong kết quả đầu ra, chúng tôi thấy ngay một vấn đề: các cột chỉ có `amount`
và `number_records` hai lần - chúng tôi không thể biết cột nào có màu xanh lá cây và cột nào có màu vàng. Vì vậy trước khi tham gia chúng ta đổi tên các cột:

```python
df_green_revenue_temp = df_green_revenue \
    .withColumnRenamed('amount', 'green_amount') \
    .withColumnRenamed('number_records', 'green_number_records')

df_yellow_revenue_temp = df_yellow_revenue \
    .withColumnRenamed('amount', 'yellow_amount') \
    .withColumnRenamed('number_records', 'yellow_number_records')
```

Bây giờ kết quả có `green_amount`, `green_number_records`,
`yellow_amount` và `yellow_number_records`, chúng ta có thể lưu nó:

```python
df_join.write.parquet('data/report/revenue/total', mode='overwrite')
```

Xem xét công việc trong Spark UI: ba giai đoạn. Cái đầu tiên đọc dữ liệu
và thực hiện nhóm theo - đó là màu xanh lá cây (hoặc màu vàng, không thành vấn đề). Chiếc
thứ hai thực hiện tương tự với loại taxi khác. Và giai đoạn thứ ba
kết hợp cả hai - chính sự tham gia.

Kế hoạch có thể được biểu diễn dưới dạng DAG tĩnh. Hai nhánh đầu vào vẫn tách biệt
cho đến khi `SortMergeJoin`:

```text
Stage 53: Scan parquet -> WholeStageCodegen (3) -> Exchange
Stage 54: Scan parquet -> WholeStageCodegen (1) -> Exchange
Stage 55:
  Exchange -> WholeStageCodegen (2) --\
                                       -> SortMergeJoin -> WholeStageCodegen (5)
  Exchange -> WholeStageCodegen (4) --/
```

## Cách kết hợp hai bảng lớn hoạt động

Bây giờ là phiên bản bảng trắng. Chúng tôi có tập dữ liệu màu vàng với một loạt phân vùng
và tập dữ liệu màu xanh lá cây với một loạt phân vùng. Chúng tôi gọi bản ghi
màu vàng là `y1`, `y2`, v.v., bản ghi màu xanh lục - `g1`, `g2`, v.v. Mỗi bản ghi là sự tổng hợp của giờ, khu vực, doanh thu và số chuyến đi.

```text
yellow partitions        green partitions
+------------+           +------------+
| k1 -> y1   |           | k2 -> g1   |
| k1 -> y2   |           | k3 -> g2   |
| k3 -> y3   |           | k4 -> g3   |
+------------+           +------------+
        |                     |
        +---- reshuffle ------+
        |    by key           |
   +---------+  +---------+  +---------+
   | k1: y1  |  | k2: y2  |  | k3: y3  |
   |    y2   |  |    g1   |  |    g3*  |
   +---------+  +---------+  +---------+
        |             |
   (k1, y1, null)  (k2, y2, g1)
```

Đối với mỗi bản ghi, chúng tôi tạo một bản ghi phức tạp: khóa tham gia và tải trọng.
Vì chúng ta nối trên hai cột nên khóa là khóa tổng hợp của giờ và vùng
- trong bản phác thảo, `k1` đến `k4`.

Sau đó, chúng tôi thực hiện việc cải tổ lại, giống như trong từng nhóm. Mục đích giống nhau:
tất cả các bản ghi có cùng khóa phải nằm trong cùng một phân vùng. Mọi thứ
với `k1` đều chuyển đến phân vùng đầu tiên, mọi thứ có `k2` - đến
thứ hai, v.v.

Sau đó chúng ta kết hợp các bản ghi, tương tự như bước rút gọn trong nhóm.
Nếu chúng tôi thấy hai bản ghi có cùng khóa - như `k2` với `y2` và `g1` -
, chúng tôi biến chúng thành một bản ghi: `k2`, `y2`, `g1`. Nếu không có cặp, loại tham gia
sẽ quyết định điều gì sẽ xảy ra. Với phép nối ngoài, chúng ta xuất bản ghi
có giá trị rỗng: `k1`, `y1`, `null` hoặc `k4`, `null`, `g3`. Với phép nối bên trong,
sẽ không xuất ra các bản ghi này.

Thuật toán thực hiện việc sắp xếp lại này một lần nữa là sắp xếp hợp nhất bên ngoài. Đó là
tại sao trong kế hoạch thực hiện, điều này được gọi là phép nối hợp nhất sắp xếp. Và `shuffle
read` và `shuffle write` trong giao diện người dùng cho chúng ta thấy
thực tế đã xảy ra bao nhiêu sự xáo trộn.

## Hiện thực hóa kết quả trung gian

Trong phần chạy ở trên, chúng tôi đã không đọc các bảng doanh thu màu xanh lá cây và màu vàng mà
đã lưu lần trước - chúng tôi đã tính toán lại chúng một cách nhanh chóng. Thay vào đó, chúng ta có thể tải kết quả
đã chuẩn bị trước đó:

```python
df_green_revenue = spark.read.parquet('data/report/revenue/green')
df_yellow_revenue = spark.read.parquet('data/report/revenue/yellow')
```

Sau đó đổi tên các cột, nối và viết như trước. Việc lưu kết quả
trung gian và sử dụng lại nó được gọi là hiện thực hóa nó. Nó có thể hữu ích ngoài
trong lần tham gia này - có thể chúng tôi muốn một trang tổng quan hiển thị riêng doanh thu xanh.

Điều thú vị là kế hoạch cho phiên bản này trông không khác lắm - cũng là
gồm ba giai đoạn. Tập dữ liệu ở đây có lẽ quá nhỏ để có thể thấy được sự khác biệt của
. Trong mọi trường hợp, điểm chính của phần này là cách
thực hiện phép nối và đó là trường hợp của hai bảng tương đối lớn.

## Tham gia bằng bảng nhỏ: Broadcast join

Còn có một trường hợp khác: một cái bàn lớn và một cái bàn nhỏ. Chúng tôi lấy bảng doanh thu đã tham gia
(bây giờ được đọc lại từ sàn gỗ - chúng tôi không muốn đợi
cho toàn bộ quá trình tính toán nữa) và chúng tôi muốn xem mỗi vùng
thực sự là gì. Để làm được điều đó, chúng tôi có bảng vùng - nó được tạo ở một trong những video đầu tiên của
bằng cách tải CSV vùng và viết nó dưới dạng sàn gỗ:

```python
df_zones = spark.read.parquet('zones/')
```

Các hàng đầu tiên của bảng tra cứu là:

| ID vị trí | Quận | Khu | dịch vụ_zone |
| ---: | --- | --- | --- |
| 1 | EWR | Sân bay Newark | EWR |
| 2 | Nữ hoàng | Vịnh Jamaica | Khu Boro |
| 3 | Bronx | Vườn Allerton/Pelham | Khu Boro |
| 4 | Manhattan | Thành phố bảng chữ cái | Vùng màu vàng |
| 5 | Đảo Staten | Cao nguyên Arden | Khu Boro |
| 6 | Đảo Staten | Arrochar/Pháo đài Wadsworth | Khu Boro |
| 7 | Nữ hoàng | Astoria | Khu Boro |
| 8 | Nữ hoàng | Công viên Astoria | Khu Boro |
| 9 | Nữ hoàng | Auburndale | Khu Boro |
| 10 | Nữ hoàng | Công viên Baisley | Khu Boro |
| 11 | Brooklyn | Bãi Tắm | Khu Boro |

Đó là một bảng tra cứu nhỏ: ID vị trí, quận, tên vùng và vùng dịch vụ
. Bây giờ là phép nối - lần này tên cột khác nhau trong hai bảng
, vì vậy thay vì `on`, chúng tôi sử dụng một điều kiện:

```python
df_result = df_join \
    .join(df_zones, df_join.zone == df_zones.LocationID)
```

ID vùng trong bảng của chúng tôi là một số nguyên trong khi bảng vùng lưu trữ
theo cách khác, vì vậy chúng tôi cũng loại bỏ các cột ID bổ sung và chỉ giữ lại tên
của vùng. Sau đó, chúng tôi viết kết quả vào sàn gỗ.

Hãy xem kế hoạch thực hiện ngay bây giờ: có `BroadcastExchange` và chỉ có
một giai đoạn - không có sự xáo trộn nào cả. Lý do là các vùng DataFrame
rất nhỏ. Thay vì nối thêm các khóa và thực hiện phép nối hợp nhất sắp xếp,
Spark phát bảng nhỏ: nó gửi một bản sao đầy đủ của bảng đó tới mọi người thực thi
. Mỗi người thực thi xử lý phân vùng của bảng lớn và thực hiện
tham gia vào bộ nhớ: đối với mỗi bản ghi doanh thu, nó tra cứu vùng theo ID và
sẽ thêm thông tin vùng.

Không cần xáo trộn dữ liệu - chỉ có bảng nhỏ được gửi đi một lần.
Việc này nhanh hơn rất nhiều so với phép nối hợp nhất sắp xếp.

## Tóm tắt

- Hai bảng lớn: một phép nối hợp nhất sắp xếp. Thêm khóa vào mỗi bản ghi,
cải tổ lại để các bản ghi có cùng khóa sẽ nằm trong cùng một phân vùng,
sau đó kết hợp chúng ở đó.
- Một bảng lớn và một bảng nhỏ: tham gia phát sóng. Gửi một bản sao của bảng
nhỏ cho mọi người thực thi và thực hiện tra cứu trong bộ nhớ - không cần xáo trộn lại,
, đó là lý do tại sao nó chỉ là một giai đoạn và diễn ra nhanh chóng.

## Vật liệu

* [`code/07_groupby_join.ipynb`](code/07_groupby_join.ipynb) - nửa sau:
liên kết bên ngoài của hai bảng doanh thu và liên kết với bảng
`zones` nhỏ.
