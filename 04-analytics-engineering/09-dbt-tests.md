---
video_url: https://www.youtube.com/watch?v=bvZ-rJm7uMU
prev_url: 08-documentation.md
next_url: 10-dbt-packages.md
---
# dbt Kiểm tra

> 📄 Tài liệu chính thức: [Kiểm tra dữ liệu](https://docs.getdbt.com/docs/build/data-tests) | [Kiểm tra đơn vị](https://docs.getdbt.com/docs/build/unit-tests) | [Hợp đồng mẫu](https://docs.getdbt.com/docs/mesh/govern/model-contracts)

KPI sai trong bảng thông tin, số liệu không tốt trong báo cáo — thực sự chỉ có hai nguyên nhân: dữ liệu cơ bản không như bạn mong đợi hoặc bạn đã làm sai SQL. Là một kỹ sư phân tích, nếu bạn không thể biết đó là cái nào thì về mặt kỹ thuật thì cả hai đều là lỗi của bạn. Các bài kiểm tra là cách bạn chủ động cập nhật vấn đề này. dbt cung cấp một bộ tùy chọn thử nghiệm khá lớn và video này sẽ giới thiệu tất cả các tùy chọn đó.


---

## 1. Các bài kiểm tra đơn lẻ

Loại thử nghiệm đơn giản nhất. Bạn viết một truy vấn SQL đơn giản, dán nó vào thư mục `tests/` và thế là xong — giờ đây nó là một bản thử nghiệm.

Logic rất đơn giản: **nếu truy vấn trả về bất kỳ hàng nào, thử nghiệm sẽ thất bại.** Bạn đang viết truy vấn chọn các trường hợp "xấu". Không có hàng nào trở lại có nghĩa là mọi thứ đã được kiểm tra.

```sql
-- tests/assert_positive_fare_amount.sql
-- Fare amounts should always be positive

select
    tripid,
    fare_amount
from {{ ref('fct_trips') }}
where fare_amount <= 0
```

Đây là những điều tuyệt vời cho các quy tắc kinh doanh một lần rất cụ thể đối với tổ chức của bạn — loại điều mà không có thử nghiệm chung nào có thể bao quát được.

> 📄 [Kiểm tra dữ liệu đơn lẻ — docs](https://docs.getdbt.com/docs/build/data-tests#singular-data-tests)

---

## 2. Kiểm tra độ tươi của nguồn

Chúng nằm trong YAML nguồn của bạn chứ không phải trong một tệp riêng biệt. Bạn thêm khối `freshness` vào nguồn và cho dbt biết cột nào cho biết thời điểm dữ liệu được tải lần cuối. Sau đó, bạn chạy `dbt source freshness` và dbt kiểm tra xem dấu thời gian đó có đủ gần đây hay không.

Bạn có thể đặt cả hai ngưỡng `warn_after` và `error_after` - một để gắn cờ, một để thực sự thất bại.

```yaml
version: 2

sources:
  - name: staging
    database: production
    schema: trips_data_all
    tables:
      - name: green_tripdata
        loaded_at_field: lpep_pickup_datetime
        freshness:
          warn_after: {count: 6, period: hour}
          error_after: {count: 12, period: hour}

      - name: yellow_tripdata
        loaded_at_field: tpep_pickup_datetime
        freshness:
          warn_after: {count: 6, period: hour}
          error_after: {count: 12, period: hour}
```

Không phải thứ bạn thấy ở mọi nơi, nhưng đối với các đường ống nơi dữ liệu cũ có thể gây ra sự cố thực sự thì đó là cứu cánh.

> 📄 [Độ mới của nguồn — docs](https://docs.getdbt.com/reference/resource-properties/freshness)

---

## 3. Kiểm tra chung

Đây là loại thử nghiệm lớn — loại thử nghiệm phổ biến nhất mà bạn sẽ thấy trong các dự án dbt. Các bài kiểm tra chung được xác định trong YAML ngay bên cạnh các mô tả cột của bạn. Chúng được tham số hóa và có thể tái sử dụng, do đó, bạn viết logic một lần và áp dụng nó trên nhiều cột và mô hình mà bạn cần.

### Bốn bài kiểm tra chung được tích hợp sẵn

dbt xuất xưởng có chính xác bốn:

- **duy nhất** — không có giá trị trùng lặp trong cột này
- **không_null** — không cho phép giá trị rỗng
- **accepted_values** — các giá trị cột phải nằm trong danh sách xác định
- **mối quan hệ** — mọi giá trị trong cột này phải tồn tại trong một mô hình khác (tính toàn vẹn tham chiếu)

```yaml
version: 2

models:
  - name: stg_green_tripdata
    description: Staged green taxi data
    columns:
      - name: tripid
        description: Primary key for trips
        tests:
          - unique
          - not_null

      - name: vendorid
        tests:
          - not_null

      - name: payment_type
        description: Payment method code
        tests:
          - accepted_values:
              values: [1, 2, 3, 4, 5, 6]

      - name: pickup_locationid
        description: Taxi zone where trip started
        tests:
          - relationships:
              to: ref('taxi_zone_lookup')
              field: locationid
```

> 📄 [Kiểm tra dữ liệu chung — docs](https://docs.getdbt.com/docs/build/data-tests#generic-data-tests)

### Viết bài kiểm tra chung tùy chỉnh của riêng bạn

Bốn bài kiểm tra sẽ không bao gồm tất cả mọi thứ. Bạn có thể tự viết — chúng là các tệp SQL nằm trong `tests/generic/`. Cú pháp sử dụng các khối kiểm tra Jinja và dbt sẽ chọn chúng và cung cấp chúng giống như các phần dựng sẵn.

```sql
-- tests/generic/test_positive_values.sql
{% test positive_values(model, column_name) %}

select *
from {{ model }}
where {{ column_name }} < 0

{% endtest %}
```

**Cách sử dụng trong lược đồ.yml:**
```yaml
models:
  - name: fct_trips
    columns:
      - name: fare_amount
        tests:
          - positive_values

      - name: trip_distance
        tests:
          - positive_values
```

Và đây là vấn đề - bạn có thể không cần phải viết nhiều bài kiểm tra tùy chỉnh như bạn mong đợi. Cộng đồng dbt đã xây dựng rất nhiều trong số chúng trong các gói nguồn mở (dbt-utils, dbt-expectations, v.v.). Đáng để kiểm tra những thứ đó trước khi tự lăn.

> 📄 [Viết bài kiểm tra chung tùy chỉnh — docs](https://docs.getdbt.com/best-practices/writing-custom-generic-tests)

---

## 4. Kiểm tra đơn vị

Có sẵn từ dbt v1.8 trở đi (phát hành vào giữa năm 2024). Kiểm tra đơn vị cho phép bạn kiểm tra logic SQL của mình một cách riêng biệt mà không cần dùng dữ liệu thực vào kho.

Ý tưởng: bạn xác định một tập hợp nhỏ các hàng đầu vào mô phỏng và các hàng đầu ra dự kiến. dbt chạy SQL của mô hình của bạn dựa trên các mô hình giả đó và kiểm tra xem đầu ra có khớp với những gì bạn đã nói hay không. Điều này đặc biệt hữu ích cho logic phức tạp — cửa sổ cuộn, biểu thức chính quy, trường hợp cạnh — vì bạn có thể kiểm tra các kịch bản thậm chí chưa hiển thị trong dữ liệu thực của mình.

```yaml
version: 2

unit_tests:
  - name: test_payment_type_mapping
    description: Test that payment type codes map to correct descriptions
    model: stg_green_tripdata
    given:
      - input: source('staging', 'green_tripdata')
        rows:
          - {tripid: '1', payment_type: 1}
          - {tripid: '2', payment_type: 2}
          - {tripid: '3', payment_type: 5}
    expect:
      rows:
        - {tripid: '1', payment_type_description: 'Credit card'}
        - {tripid: '2', payment_type_description: 'Cash'}
        - {tripid: '3', payment_type_description: 'Unknown'}
```

Kiểm tra đơn vị được xác định trong YAML trong thư mục `models/` của bạn và hiện chỉ hỗ trợ các mô hình SQL. Vì đầu vào là tĩnh nên không có lý do gì để chạy chúng trong sản xuất — hãy sử dụng chúng trong quá trình phát triển và CI.

Tính đến đầu năm 2026, các thử nghiệm đơn vị đã có sẵn được khoảng 18 tháng và ngày càng được áp dụng nhiều hơn, đặc biệt đối với các nhóm có logic chuyển đổi phức tạp hoặc yêu cầu nghiêm ngặt về chất lượng dữ liệu. Chúng đặc biệt hữu ích trong quy trình CI/CD nơi bạn muốn phát hiện các lỗi logic trước khi chúng tấn công dữ liệu sản xuất.

> 📄 [Kiểm tra đơn vị — tài liệu](https://docs.getdbt.com/docs/build/unit-tests)

---

## 5. Hợp đồng mẫu

Loại cuối cùng được đề cập trong video này và hơi khác so với các loại khác. Hợp đồng mô hình không nhằm mục đích thu thập dữ liệu xấu sau khi thực tế xảy ra — chúng nhằm **ngăn chặn việc xây dựng mô hình của bạn** nếu nó không khớp với hình dạng xác định.

Bạn xác định các cột, loại dữ liệu dự kiến ​​và các ràng buộc tùy chọn trong YAML của mình. Sau đó bạn bật `contract: enforced: true` trong config của model. Từ thời điểm đó trở đi, nếu đầu ra mô hình của bạn không khớp - tên cột sai, loại sai, cột bị thiếu - dbt sẽ báo lỗi trước khi mọi thứ được hiện thực hóa.

```yaml
version: 2

models:
  - name: fct_trips
    config:
      contract:
        enforced: true
    columns:
      - name: tripid
        data_type: string
        constraints:
          - type: not_null
          - type: unique

      - name: pickup_datetime
        data_type: timestamp
        constraints:
          - type: not_null

      - name: service_type
        data_type: string

      - name: total_amount
        data_type: numeric
```

Ý tưởng đằng sau điều này xuất phát từ khái niệm **hợp đồng dữ liệu** — bạn ngồi lại với bên liên quan của mình, đồng ý về hình thức của tập dữ liệu đầu ra (tên cột, loại, kỳ vọng về độ mới) và hợp đồng sẽ tự động thực thi thỏa thuận đó. Nếu có ai thay đổi mô hình theo cách phá vỡ nó thì sẽ biết ngay.

> 📄 [Hợp đồng mẫu — docs](https://docs.getdbt.com/docs/mesh/govern/model-contracts)
