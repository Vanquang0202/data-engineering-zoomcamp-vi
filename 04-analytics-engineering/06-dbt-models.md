---
video_url: https://www.youtube.com/watch?v=JQYz-8sl1aQ
prev_url: 05-dbt-sources.md
next_url: 07-dbt-seeds-and-macros.md
---
# dbt Model

> 📄 Tài liệu chính thức: [Mô hình SQL](https://docs.getdbt.com/docs/build/sql-models)
> 📄 ref() hàm: [Giới thiệu về ref](https://docs.getdbt.com/reference/dbt-jinja-functions/ref)

Việc dàn dựng đã được thực hiện. Từ đây trở đi, không chỉ là gõ SQL sau máy tính — bạn thực sự cần **khám phá dữ liệu**, hiểu nội dung trong đó và hiểu một số **ngữ cảnh kinh doanh**. Trong một tổ chức thực tế, điều đó có nghĩa là truy vấn một cách thấu đáo cho đến khi bạn hiểu các vấn đề phổ biến về chất lượng dữ liệu, hàng thông thường trông như thế nào và trao đổi với mọi người về ý nghĩa của mã cũng như thời điểm kích hoạt hàng. Tất cả sự hiểu biết đó cuối cùng sẽ được mã hóa dưới dạng SQL.


---

## Chúng ta đang xây dựng cái gì?

Trước khi viết bất kỳ mã nào, điều hữu ích là hãy suy nghĩ xem kết quả cuối cùng sẽ như thế nào. Nhìn chung có hai thứ bạn muốn trong siêu thị của mình:

### Báo cáo và trang tổng quan
- Nếu có một trang tổng quan hoặc ứng dụng dữ liệu quan trọng — đặc biệt là một trang yêu cầu nhiều thao tác thủ công hoặc bảo trì bảng tính — thì đó là dấu hiệu cho thấy trang đó sẽ trở thành mô hình dbt
- Ví dụ: hãy tưởng tượng có một trang tổng quan với tập dữ liệu có tên **doanh thu hàng tháng trên mỗi vị trí**. Đó là thứ chúng tôi muốn xây dựng và kiểm soát phiên bản đúng cách

### Mô hình thứ nguyên
- Ngoài báo cáo, bạn muốn có **lược đồ sao** thích hợp — loại cấu trúc bạn thấy trong kho dữ liệu
- Hai loại bảng chính cần biết:
- **Bảng dữ kiện** — một hàng cho mỗi sự kiện/quy trình. Một hàng cho mỗi chuyến đi, một hàng cho mỗi lần bán, một hàng cho mỗi đơn hàng. Được đặt tên bằng tiền tố `fct_` (ví dụ: `fct_trips`)
- **Bảng thứ nguyên** — thuộc tính của một thực thể. Được đặt tên bằng tiền tố `dim_` (ví dụ: `dim_zones`, `dim_vendors` không được hiển thị ở đây)
- Sức mạnh của lược đồ sao tốt: trả lời "có bao nhiêu?" những câu hỏi trở nên tầm thường. *Chúng ta có bao nhiêu vùng?* → `COUNT(*)` trên `dim_zones`. *Có bao nhiêu chuyến?* → `COUNT(*)` trên `fct_trips`. Các bảng đơn giản, tập trung mà bạn tham gia khi cần thứ gì đó phức tạp hơn

### Những gì chúng tôi đang xây dựng trong khóa học này
- `dim_zones` — thuộc tính vùng/vị trí
- `fct_trips` — một hàng mỗi chuyến (kết hợp màu vàng + xanh lục)
- Mô hình báo cáo về doanh thu hàng tháng trên mỗi khu vực (bên trong thư mục `models/core/`)

---

## source() so với ref() — điểm khác biệt chính

Đây là một thời điểm quan trọng trong khóa học. Cho đến nay chúng tôi vẫn đang sử dụng `{{ source() }}` để lấy dữ liệu thô. Nhưng đó **chỉ** đối với những thứ được khai báo trong nguồn YAML của bạn - tức là các bảng thô nằm bên ngoài dbt.

Nếu đầu vào cho mô hình của bạn là **một mô hình dbt khác**, thì bạn hãy sử dụng `{{ ref() }}` để thay thế.

- `{{ source('name', 'table') }}` → dữ liệu thô được xác định trong YAML
của bạn - `{{ ref('model_name') }}` → mô hình dbt khác

> 📄 [ref() — tham khảo đầy đủ](https://docs.getdbt.com/reference/dbt-jinja-functions/ref)

Sự khác biệt này quan trọng vì `ref()` cũng thực hiện một số tính năng hữu ích: nó tự động xây dựng **biểu đồ phụ thuộc**. dbt biết rằng nếu mô hình B tham chiếu mô hình A thì A phải chạy trước. Bạn không bao giờ phải tự mình quản lý thứ tự chạy.

---

## Lớp trung gian - tại sao nó tồn tại

Chúng tôi muốn `fct_trips` là sự kết hợp giữa dữ liệu chuyến đi màu vàng và màu xanh lá cây. Nhưng thực hiện sự kết hợp đó trực tiếp bên trong mô hình thực tế sẽ khiến nó trở nên lộn xộn. Vì vậy, thay vào đó, chúng tôi đặt nó trong một **mô hình trung gian** — một thứ không phải là thô và chưa sẵn sàng hiển thị cho người dùng cuối.

- Quy ước: tiền tố của các mô hình trung gian với `int_`
- Trong trường hợp này: `int_trips_unioned.sql`
- Ý tưởng là loại bỏ công việc trung gian ra khỏi siêu thị. Siêu thị chỉ nên chứa những thứ sẵn sàng tiêu dùng

```sql
with green_data as (
    select *,
        'Green' as service_type
    from {{ ref('stg_green_tripdata') }}
),

yellow_data as (
    select *,
        'Yellow' as service_type
    from {{ ref('stg_yellow_tripdata') }}
),

trips_unioned as (
    select * from green_data
    union all
    select * from yellow_data
)

select * from trips_unioned
```

---

## Vấn đề kết hợp - màu vàng và màu xanh lá cây không giống nhau

Khi bạn cố gắng hợp nhất hai mô hình dàn dựng thì không thành công. Lỗi: *chỉ có thể áp dụng thao tác thiết lập với các biểu thức có cùng số cột*. Hóa ra màu xanh lá cây có **hai cột bổ sung** còn màu vàng thì không:

### `trip_type`
- Giá trị là `1` hoặc `2`
- `1` = mưa đá trên đường (bạn vẫy taxi)
- `2` = đặt qua điện thoại hoặc ứng dụng
- Taxi màu vàng **không có cột này** vì theo luật, bạn chỉ có thể bắt được taxi màu vàng bằng cách gọi xe trên đường — nó luôn là loại 1
- Cách khắc phục: thêm `trip_type` vào mô hình dàn màu vàng và mã hóa cứng là `1` (mưa đá đường phố)

### `ehail_fee` (phí mưa đá)
- Một khoản phí bổ sung có thể áp dụng khi bạn yêu cầu taxi thông qua ứng dụng
- Trong thực tế, hầu hết dữ liệu này là rỗng — tính năng không được triển khai nhất quán giữa các nhà cung cấp
- Taxi màu vàng theo định nghĩa **không bao giờ** có phí mưa đá điện tử
- Khắc phục: thêm `ehail_fee` sang mô hình dàn màu vàng và mã hóa cứng là `0`

```sql
-- Updated stg_yellow_tripdata.sql to match green schema
with tripdata as (
  select *
  from {{ source('staging','yellow_tripdata') }}
  where vendorid is not null
),

renamed as (
    select
        -- identifiers
        cast(vendorid as integer) as vendor_id,
        cast(ratecodeid as integer) as ratecode_id,
        cast(pulocationid as integer) as pickup_location_id,
        cast(dolocationid as integer) as dropoff_location_id,

        -- timestamps
        cast(tpep_pickup_datetime as timestamp) as pickup_datetime,
        cast(tpep_dropoff_datetime as timestamp) as dropoff_datetime,

        -- trip info
        store_and_fwd_flag,
        cast(passenger_count as integer) as passenger_count,
        cast(trip_distance as numeric) as trip_distance,
        cast(1 as integer) as trip_type,  -- Yellow only does street-hail

        -- payment info
        cast(fare_amount as numeric) as fare_amount,
        cast(extra as numeric) as extra,
        cast(mta_tax as numeric) as mta_tax,
        cast(tip_amount as numeric) as tip_amount,
        cast(tolls_amount as numeric) as tolls_amount,
        cast(0 as numeric) as ehail_fee,  -- Yellow doesn't have ehail
        cast(improvement_surcharge as numeric) as improvement_surcharge,
        cast(total_amount as numeric) as total_amount,
        cast(payment_type as integer) as payment_type,
    from tripdata
)

select * from renamed
```

Lưu ý: việc thêm các cột này trực tiếp vào dàn dựng về mặt kỹ thuật là vi phạm quy tắc "sao chép 1: 1". Nó được thực hiện ở đây để giữ cho mọi thứ đơn giản, nhưng trong một dự án chặt chẽ hơn, bạn sẽ xử lý việc này ở lớp trung gian.

**Liên kết được cập nhật sau khi căn chỉnh lược đồ:**

```sql
-- models/staging/int_trips_unioned.sql
with green_data as (
    select *,
        'Green' as service_type
    from {{ ref('stg_green_tripdata') }}
),

yellow_data as (
    select *,
        'Yellow' as service_type
    from {{ ref('stg_yellow_tripdata') }}
),

trips_unioned as (
    select * from green_data
    union all
    select * from yellow_data
)

select * from trips_unioned
```

---

## Tại sao bối cảnh kinh doanh lại quan trọng

Sự khác biệt giữa cột màu vàng và màu xanh lá cây không chỉ là vấn đề kỹ thuật — đó là **câu chuyện kinh doanh**. Taxi màu vàng và màu xanh lá cây tồn tại nhờ cách hoạt động của việc cấp phép taxi của NYC: taxi màu vàng ở lại Manhattan, taxi màu xanh lá cây được tạo ra để người dân ở các quận bên ngoài cũng có thể đi xe. Hiểu được bối cảnh đó là điều cho phép bạn đưa ra quyết định đúng đắn về cách xử lý `trip_type` và `ehail_fee` — không chỉ về mặt kỹ thuật mà còn về mặt ngữ nghĩa.

Đây là một phần của kỹ thuật phân tích, nơi bạn dừng việc viết SQL và bắt đầu hiểu dữ liệu thực sự đại diện cho điều gì.
