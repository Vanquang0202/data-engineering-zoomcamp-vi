---
video_url: https://www.youtube.com/watch?v=7CrrXazV_8k
prev_url: 04-dbt-project-structure.md
next_url: 06-dbt-models.md
---
# dbt Nguồn

> 📄 Tài liệu chính thức: [Nguồn](https://docs.getdbt.com/docs/build/sources)
> 📄 Các phương pháp hay nhất: [Cách chúng tôi cấu trúc các dự án dbt của mình — Dàn dựng](https://docs.getdbt.com/best-practices/how-we-structure/03-staging)

Video này nói về việc cho dbt biết dữ liệu thô của bạn thực sự tồn tại ở đâu. Nguồn là cách dbt biết nên lấy bảng nào trước khi có bất kỳ chuyển đổi nào xảy ra. Mọi thứ trong video này diễn ra bên trong thư mục `models/staging/` mà chúng tôi thiết lập trong 4.3.1.


---

## Xác định nguồn

### `sources.yml`
- **Tệp YAML** bên trong `models/staging/` cho dbt biết dữ liệu thô của bạn ở đâu là
- **tên** của tệp là tùy ý — các lựa chọn phổ biến là `sources.yml`, `_sources.yml` (gạch dưới để sắp xếp lên trên cùng) hoặc tên nào đó được đặt tên theo nguồn gốc như `bigquery_sources.yml`
- Bạn đặt **tên** cho nguồn của mình — điều này cũng tùy ý. Hãy coi nó như một nhãn: `raw`, `raw_data` hoặc nhãn nào đó mang tính mô tả hơn như `google_analytics_data` hoặc `finance_data`
- Sau đó, bạn cung cấp ba trường **không** tùy ý — chúng phải khớp chính xác với kho của bạn:
- **database** — tên cơ sở dữ liệu hoặc dự án GCP
- **lược đồ** — lược đồ bên trong cơ sở dữ liệu đó hoặc tập dữ liệu BigQuery
- **bảng** — các bảng riêng lẻ mà bạn muốn tham chiếu

```yaml
sources:
  - name: nytaxi
    database: taxi_rides_ny # Or name of your GCP project
    schema: prod # Or name of your BigQuery dataset

    tables:
      - name: green_tripdata
      - name: yellow_tripdata
```

> 📄 [Nguồn — tham khảo đầy đủ](https://docs.getdbt.com/docs/build/sources)

### Cục bộ (DuckDB) so với BigQuery — điều gì sẽ xảy ra ở đâu

Ý nghĩa của cơ sở dữ liệu, lược đồ và bảng thay đổi tùy theo thiết lập của bạn:

| Lĩnh vực | Địa phương (DuckDB) | BigQuery |
|---|---|---|
| **cơ sở dữ liệu** | `taxi_rides_ny` | ID dự án GCP của bạn |
| **lược đồ** | `main` | Tên Tập dữ liệu BigQuery của bạn (ví dụ: `trips_data_all`) |
| **bàn** | `green_tripdata`, `yellow_tripdata` | Tên bảng giống nhau |

- Nếu bạn làm theo thiết lập cục bộ mặc định thì những tên này sẽ xuất hiện ngay lập tức
- Nếu bạn đang sử dụng BigQuery, chỉ cần kiểm tra kỹ xem tên bảng có khớp với tên bạn thực sự có trong tập dữ liệu
hay không
---

## Sử dụng nguồn trong mô hình của bạn

### Hàm `source()`
- Thay vì mã hóa cứng đường dẫn đầy đủ đến bảng của bạn (ví dụ: `FROM production.trips_data_all.green_tripdata`), bạn sử dụng hàm **`source()`**
- Đó là **Jinja macro** — bạn sẽ nhận ra nó bằng dấu ngoặc nhọn `{{ }}`
- Cần có hai đối số:
- **tên nguồn** — tên bạn đã xác định trong YAML (ví dụ: `staging`)
- **tên bảng** — phải khớp chính xác với tên bạn đặt bên dưới `tables` trong YAML
- Miễn là có tệp YAML ở đâu đó trong dự án của bạn có khai báo nguồn phù hợp, điều này sẽ giải quyết chính xác tại thời điểm biên dịch

```sql
select * from {{ source('staging', 'green_tripdata') }}
```

- Chạy bản xem trước và bạn sẽ thấy dữ liệu bảng thô quay trở lại
- Nếu nó hoạt động, đó là nền tảng — mọi thứ khác đều được xây dựng trên
này
---

## Xây dựng mô hình dàn dựng phù hợp

### Quy ước đặt tên
- Đặt tiền tố **`stg_`** vào các tệp mô hình dàn dựng của bạn để làm rõ chúng thuộc lớp nào
- Vì vậy, `green_tripdata.sql` trở thành `stg_green_tripdata.sql`
- Các tiền tố phổ biến khác: `int_` dành cho mẫu trung gian và đôi khi không có gì cả đối với mẫu mart cuối cùng

### Đổi tên và sắp xếp lại các cột
- Liệt kê rõ ràng từng cột và đặt cho chúng **bí danh rõ ràng hơn**
- Hãy có chủ đích về **thứ tự** — cần tuân theo một nhóm logic:
- **Số nhận dạng trước tiên** — `vendor_id`, `trip_id`, bất kỳ thứ gì là ID
- **Dấu thời gian tiếp theo** — `pickup_datetime`, `dropoff_datetime`
- **Chi tiết chuyến đi** — `passenger_count`, `trip_distance`, `trip_type`
- **Thông tin thanh toán cuối cùng** — `fare_amount`, `extra`, `mta_tax`, `tip_amount`, `tolls_amount`, `total_amount`, `payment_type`

### Truyền các kiểu dữ liệu một cách rõ ràng
- Đừng dựa vào bất cứ điều gì nguồn cung cấp cho bạn — truyền mọi thứ đến loại bạn thực sự muốn:
- ID → `integer`
- Dấu thời gian → `timestamp`
- Đếm → `integer`
- Giá trị tiền tệ → `numeric` hoặc `float` (tùy thuộc vào nền tảng của bạn)

```sql
with tripdata as (
  select *
  from {{ source('staging','green_tripdata') }}
  where vendorid is not null
),

renamed as (
  select
      -- identifiers
      cast(vendorid as integer) as vendorid,
      cast(ratecodeid as integer) as ratecodeid,
      cast(pulocationid as integer) as pickup_locationid,
      cast(dolocationid as integer) as dropoff_locationid,

      -- timestamps
      cast(lpep_pickup_datetime as timestamp) as pickup_datetime,
      cast(lpep_dropoff_datetime as timestamp) as dropoff_datetime,

      -- trip info
      store_and_fwd_flag,
      cast(passenger_count as integer) as passenger_count,
      cast(trip_distance as numeric) as trip_distance,
      cast(trip_type as integer) as trip_type,

      -- payment info
      cast(fare_amount as numeric) as fare_amount,
      cast(extra as numeric) as extra,
      cast(mta_tax as numeric) as mta_tax,
      cast(tip_amount as numeric) as tip_amount,
      cast(tolls_amount as numeric) as tolls_amount,
      cast(ehail_fee as numeric) as ehail_fee,
      cast(improvement_surcharge as numeric) as improvement_surcharge,
      cast(total_amount as numeric) as total_amount,
      cast(payment_type as integer) as payment_type,
      {{ get_payment_type_description('payment_type') }} as payment_type_description
  from tripdata
)

select * from renamed
```

---

## Lưu ý khi lọc

- Khuyến nghị chung là giữ các mô hình dàn dựng ở dạng **bản sao 1:1** của nguồn — cùng số hàng, cùng số cột, vừa dọn sạch
- Tuy nhiên, tập dữ liệu này có một số vấn đề về chất lượng dữ liệu (chúng tôi sẽ đề cập đến những vấn đề đó sau), vì vậy, sẽ hợp lý hơn khi lọc ra các hàng có **`vendor_id IS NULL`** ngay tại đây trong quá trình dàn dựng
- Đó là một sự khác biệt so với quy ước, nhưng là một điều thực tế cho dự án này

---

## Bài tập của bạn

Thực hiện tương tự với bảng **tripdata màu vàng**. Các cột gần giống với màu xanh lá cây nên sẽ không quá đau. Cuối cùng, bạn sẽ có:
- A `sources.yml` khai báo cả hai bảng
- Mô hình dàn dựng `stg_green_tripdata.sql`
- Mô hình dàn dựng `stg_yellow_tripdata.sql`
