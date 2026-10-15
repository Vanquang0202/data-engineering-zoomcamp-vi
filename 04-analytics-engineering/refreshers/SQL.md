# Trình giới thiệu SQL

### Mục lục


- [Chức năng cửa sổ](#window-funtions)
- [Số hàng](#row-number)
- [Xếp hạng và Xếp hạng dày đặc](#rank-and-dense-rank)
- [Lag và Lead](#lag-and-lead)
- [Phần trăm tiếp theo](#percentile-cont)
- [Biểu thức bảng chung](#common-table-expression)
- [mô hình dbt và CTE](#dbt-models-and-ctes)



## Chức năng cửa sổ

Hàm cửa sổ thực hiện phép tính trên một tập hợp các hàng của bảng có liên quan đến hàng hiện tại trong một "cửa sổ" hoặc tập hợp con dữ liệu cụ thể. Điều này có thể so sánh với loại tính toán có thể được thực hiện bằng hàm tổng hợp (chẳng hạn như SUM(), AVG(), COUNT(), v.v.).

Nhưng không giống như các hàm tổng hợp thông thường, việc sử dụng hàm cửa sổ không khiến các hàng được nhóm thành một hàng đầu ra duy nhất — các hàng vẫn giữ nguyên các đặc tính nhận dạng riêng biệt của chúng.


**Cú pháp:**

```sql
FUNCTION() OVER (PARTITION BY column_name ORDER BY column_name)
```

Một hàm cửa sổ luôn có hai thành phần. Phần thứ hai ở đây xác định cửa sổ của bạn:

```sql
OVER (PARTITION BY column_name ORDER BY column_name)
```

Cửa sổ của bạn ở đây là cách bạn muốn xem dữ liệu của mình khi áp dụng chức năng

- PARTITION BY: chia tập kết quả thành các nhóm (tùy chọn).

- ORDER BY: xác định thứ tự xử lý các hàng trong phân vùng.


**Chức năng cửa sổ chung:**

Chức năng xếp hạng:

- ROW_NUMBER(): Gán một số hàng duy nhất trong một phân vùng.
- RANK(): Tương tự ROW_NUMBER(), nhưng gán cùng thứ hạng cho các giá trị trùng lặp, bỏ qua số.
- DENSE_RANK(): Giống như RANK(), nhưng không có khoảng trống trong cách đánh số.

Các hàm tổng hợp dưới dạng hàm cửa sổ:

- SUM() OVER(): Tính tổng đang chạy.
- AVG() OVER(): Tính đường trung bình động.

Chức năng trễ và dẫn đầu:

- LAG(): Lấy giá trị ở hàng trước đó.
- LEAD(): Lấy giá trị từ hàng tiếp theo.

### Số hàng

ROW_NUMBER() thực hiện đúng như tên gọi—hiển thị số của một hàng nhất định. Nó bắt đầu từ 1 và đánh số các hàng theo phần ORDER BY của câu lệnh cửa sổ. Sử dụng mệnh đề PARTITION BY sẽ cho phép bạn bắt đầu đếm lại 1 trong mỗi phân vùng.

**Cú pháp:**

```sql
ROW_NUMBER() OVER (PARTITION BY column_name ORDER BY column_name)
```

**Sử dụng phổ biến:**

- Loại bỏ các hàng trùng lặp: Bạn có thể sử dụng ROW_NUMBER() để xác định các hàng trùng lặp và chỉ giữ lại một hàng bằng cách lọc ra các hàng có số hàng lớn hơn 1.

- Dữ liệu xếp hạng: Được sử dụng khi xếp hạng các hàng dựa trên tiêu chí cụ thể nhưng yêu cầu số hàng duy nhất.

- Chọn bản ghi mới nhất: Giúp chọn mục nhập gần đây nhất cho mỗi danh mục khi kết hợp với PARTITION BY.

**Ví dụ 1:**

```sql

SELECT 
  total_amount,
  ROW_NUMBER() OVER (ORDER BY total_amount DESC) AS ranking

FROM `greentaxi_trips` 
LIMIT 10;

```

Truy vấn trả về 10 giá trị tổng_số tiền cao nhất từ ​​bảng, cùng với số hàng cho biết thứ hạng của chúng.


| tổng_số tiền | xếp hạng |
|--------|--------|
| 4012.3 | 1 |
| 2878.3 | 2 |
| 2438.8 | 3 |
| 2156.3 | 4 |
| 2109.8 | 5 |
| 2017.3 | 6 |
| 05/1971| 7 |
| 1958,8 | 8 |
| 1762.8 | 9 |
| 1600,8 | 10 |

Cột được tạo bằng ROW_NUMBER() là cột tạm thời và không sửa đổi bảng gốc. Nó chỉ là một phép tính được áp dụng cho dữ liệu trong kết quả truy vấn.

**Ví dụ 2:**

Hãy sửa đổi truy vấn trước đó để thêm phân vùng bằng cách lấy ID vị trí

```sql

SELECT 

  total_amount,
  PULocationID,
  ROW_NUMBER() OVER (PARTITION BY PULocationID ORDER BY total_amount DESC) AS ranking

FROM `greentaxi_trips` 
LIMIT 10;

```

Truy vấn SQL này chỉ định xếp hạng cho mỗi hàng dựa trên tổng_amount theo thứ tự giảm dần trong mỗi nhóm PULocationID
:

| tổng_số tiền | PULocationID | xếp hạng |
|-----------|-----------|-----------|
| 8,51 | 224 | 432 |
| 8.3 | 224 | 433 |
| 8.3 | 224 | 434 |
| 7.3 | 224 | 435 |
| 3.3 | 224 | 436 |
| 86,42 | 234 | 1 |
| 73,5 | 234 | 2 |
| 62,7 | 234 | 3 |
| 61,94 | 234 | 4 |
| 61,94 | 234 | 5 |

Sử dụng mệnh đề PARTITION BY sẽ cho phép bạn bắt đầu đếm lại 1 trong mỗi phân vùng.

### Thứ hạng và Thứ hạng dày đặc

ROW_NUMBER(), RANK() và DENSE_RANK() là các hàm cửa sổ được sử dụng để gán thứ hạng cho các hàng dựa trên thứ tự đã chỉ định. Tuy nhiên, chúng hoạt động khác nhau khi có các giá trị trùng lặp trong cột xếp hạng.

RANK() ấn định thứ hạng nhưng bỏ qua các con số nếu có sự ngang bằng. DENSE_RANK() tương tự như RANK(), nhưng không bỏ qua các số khi có mối quan hệ.

Ví dụ:

| Điểm | ROW_NUMBER() | NGỨA() | DENSE_RANK() |
|-------|--------------|--------|--------------|
| 95 | 1 | 1 | 1 |
| 90 | 2 | 2 | 2 |
| 90 | 3 | 2 | 2 |
| 85 | 4 | 4 | 3 |


### Lag và dẫn đầu

Việc so sánh các hàng với các hàng trước hoặc sau thường có thể hữu ích. Bạn có thể sử dụng LAG hoặc LEAD để tạo các cột lấy giá trị từ các hàng khác mà không cần phải tự nối. Tất cả những gì bạn cần làm là nhập cột cần kéo và bạn muốn kéo bao nhiêu hàng. LAG kéo từ các hàng trước và LEAD kéo từ các hàng sau


**Cú pháp:**

```sql

LAG(expression) OVER (PARTITION BY partition_expression ORDER BY order_expression)
```

- biểu thức: Cột có giá trị bạn muốn lấy từ hàng trước
- offset (tùy chọn): Số hàng lùi về từ hàng hiện tại cần tìm. Giá trị mặc định là 1, nghĩa là nó nhìn vào hàng ngay trước đó.
- PARTITION BY (tùy chọn): Chia tập kết quả thành các phân vùng để áp dụng chức năng cho từng phân vùng riêng biệt.
- ORDER BY: Chỉ định thứ tự xử lý các hàng.

**Ví dụ:**

```sql

SELECT 

lpep_pickup_datetime,
total_amount,
LAG(total_amount) OVER (ORDER BY lpep_pickup_datetime) as prev_total_amount,
LEAD(total_amount) OVER (ORDER BY lpep_pickup_datetime) as next_total_amount

FROM `greentaxi_trips` 
ORDER BY lpep_pickup_datetime

```

Truy vấn truy xuất lpep_pickup_datetime, Total_amount, tổng_amount của chuyến đi trước và tổng_amount của chuyến đi tiếp theo.

| lpep_pickup_datetime | tổng_số tiền | trước_total_số tiền | next_total_amount |
|---------------------------|--------------|-------------------|-------------------|
| 31-12-2008 23:33:38 UTC | 7.3 | 6.3 | 5.3 |
| 31-12-2008 23:42:31 UTC | 5.3 | 7.3 | 14:55 |
| 31-12-2008 23:47:51 UTC | 14:55 | 5.3 | 19:55 |
| 31-12-2008 23:57:46 UTC | 19:55 | 14:55 | 9,8 |
| 2009-01-01 00:00:00 UTC | 9,8 | 19:55 | 81.3 |


### Phần trăm tiếp theo

Tính toán giá trị phân vị được chỉ định cho biểu thức value_, bằng phép nội suy tuyến tính.

**Cú pháp:**

```sql

PERCENTILE_CONT(value_expression, percentile ) OVER (PARTITION BY partition_expression)
```

**Ví dụ:**

Hãy tính phân vị thứ 90 của tổng_số tiền cho mỗi địa điểm nhận hàng duy nhất (PULocationID)

```sql

SELECT 
  PULocationID,
  total_amount,
  PERCENTILE_CONT(total_amount, 0.9 ) OVER (PARTITION BY PULocationID) AS p90

FROM `greentaxi_trips` 

```

- PERCENTILE_CONT(total_amount, 0.9): tính phân vị thứ 90 (p90) của tổng_amount
- PARTITION BY PULocationID: Phần này nhóm các phép tính theo PULocationID, do đó phân vị thứ 90 được tính riêng cho từng vị trí.


Kết quả truy vấn trông như thế này:

| PULocationID | tổng_số tiền | p90 |
|------|-------|-------|
| 224 | 17.3 | 51,9 |
| 224 | 20,67 | 51,9 |
| 224 | 21 | 51,9 |
| 224 | 26.06 | 51,9 |
| 224 | 27.13 | 51,9 |
| 224 | 40.14 | 51,9 |
| 224 | 55,46 | 51,9 |
| 224 | 25,74 | 51,9 |
| 224 | 27.02 | 51,9 |
| 224 | 37 | 51,9 |


Giá trị P90 về cơ bản là số tiền mà 90% giá trị rơi xuống dưới đó. Trong bảng này, P90
không đổi ở mức 51,9, có nghĩa là đối với vị trí "224", 90% tổng số tiền là dưới 51,9.


## Biểu thức bảng chung

CTE, viết tắt của Biểu thức bảng chung, giống như một truy vấn trong một truy vấn. Với câu lệnh WITH, bạn có thể tạo các bảng tạm thời để lưu trữ kết quả, làm cho các truy vấn phức tạp trở nên dễ đọc và dễ bảo trì hơn. Các bảng tạm thời này chỉ tồn tại trong suốt thời gian truy vấn chính.

CTE và truy vấn phụ đều là những công cụ mạnh mẽ và có thể được sử dụng để đạt được các mục tiêu tương tự, nhưng chúng có các trường hợp sử dụng và lợi thế khác nhau. Điểm khác biệt là CTE có thể tái sử dụng trong toàn bộ phiên và
dễ đọc hơn
Bằng cách khai báo CTE ở đầu truy vấn, bạn nâng cao khả năng đọc mã, cho phép bạn nắm bắt logic phân tích rõ ràng hơn.

**Cú pháp:**

```sql

WITH cte_name AS (
    SELECT column1, column2
    FROM some_table
    WHERE condition
)
SELECT * FROM cte_name;
```

**Ví dụ: Hãy tìm chuyến đi có tổng_amount lớn thứ hai**

```sql

WITH cte AS(

  SELECT
  lpep_pickup_datetime,
  total_amount,
  RANK() OVER (ORDER BY total_amount DESC) AS rank

  FROM `greentaxi_trips` 

)


SELECT * FROM cte WHERE rank = 2;

```

Truy vấn bắt đầu bằng Biểu thức bảng chung (CTE) có tên cte. Chúng ta sử dụng hàm cửa sổ RANK() để
gán thứ hạng (thứ hạng) cho mỗi hàng dựa trên tổng_amount theo thứ tự giảm dần (từ cao nhất đến thấp nhất).

Bây giờ, chúng tôi sử dụng CTE trong truy vấn chính: ```SELECT * FROM cte WHERE rank = 2;```

Kết quả truy vấn:


| lpep_pickup_datetime | tổng_số tiền | xếp hạng |
|---------------------------|--------------|-------------------|
| 2019-10-10 15:22:49 UTC | 2878.3 | 2 |

## mô hình dbt và CTE

CTE và các hàm cửa sổ sẽ được sử dụng nhiều trong mô-đun 4 trên dbt. Hãy xem một ví dụ về ứng dụng trong các mô hình dbt

**Ví dụ:**

Giả sử chúng ta bắt đầu từ tập dữ liệu FHV và muốn tạo một mô hình dbt để làm phong phú dữ liệu bằng cách tính thời lượng chuyến đi và phân vị thứ 90.

```sql

WITH trip_duration_calculated AS (

    SELECT
        *,
        timestamp_diff(dropOff_datetime, pickup_datetime, second) as trip_duration

    FROM `fhv_trips`
)

SELECT 

    PUlocationID,
    trip_duration,
    PERCENTILE_CONT(trip_duration, 0.90) OVER (PARTITION BY PUlocationID) AS trip_duration_p90


FROM trip_duration_calculated


```

**Bước 1: Tìm hiểu CTE**

Mệnh đề WITH tạo một CTE có tên trip_duration_calcated. CTE này hoạt động như một bảng tạm thời mà
chứa tất cả các cột từ bảng fhv_trips. Ngoài ra, nó còn tính toán thời lượng chuyến đi cho mỗi chuyến đi

**Bước 2: Truy vấn chính bằng CTE và Chức năng cửa sổ**

Truy vấn này tính toán phân vị thứ 90 của thời lượng chuyến đi cho mỗi PUlocationID bằng cách sử dụng chức năng cửa sổ:

Mệnh đề PARTITION BY PUlocationID đảm bảo rằng phép tính phân vị được thực hiện riêng
cho mỗi PUlocationID duy nhất.

Phân vị thứ 90 có nghĩa là 90% chuyến đi có thời lượng bằng hoặc thấp hơn giá trị này

**Kết quả truy vấn trông như thế này:**

| PUlocationID | chuyến đi_duration | chuyến_duration_p90 |
|-------------|---------------|--------------------|
| 190 | 451 | 2170.0 |
| 190 | 1373 | 2170.0 |
| 190 | 817 | 2170.0 |
| 190 | 589 | 2170.0 |
| 190 | 1648 | 2170.0 |
| 32 | 546 | 1988.0 |
| 32 | 151 | 1988.0 |
| 32 | 1752 | 1988.0 |
| 32 | 2426 | 1988.0 |
| 32 | 888 | 1988.0 |


- Với PUlocationID = 190, 90% chuyến đi có thời lượng ≤ 2170,0 giây.
- Đối với PUlocationID = 32, 90% chuyến đi có thời lượng ≤ 1988,0 giây.
