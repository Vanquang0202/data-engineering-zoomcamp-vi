---
video_url: https://www.youtube.com/watch?v=lT4fmTDEqVk
prev_url: 06-dbt-models.md
next_url: 08-documentation.md
---
# dbt Hạt giống và Macro

> 📄 Tài liệu về hạt giống: [Hạt giống](https://docs.getdbt.com/docs/build/seeds)
> 📄 Tài liệu về macro: [Jinja và macro](https://docs.getdbt.com/docs/build/jinja-macros)

Mô hình liên minh đã hoàn tất, nhưng hiện tại ID nhà cung cấp và ID vị trí chỉ là những con số - những mã vô nghĩa. Video này nói về việc làm phong phú thêm dữ liệu đó. Có hai tính năng dbt: **seed** để đưa dữ liệu tra cứu vào và **macro** để biến logic SQL có thể sử dụng lại thành thứ mà bạn không cần phải sao chép-dán ở mọi nơi.


---

## Vấn đề — mã ở mọi nơi

Nếu bạn truy vấn `vendor_id`, bạn sẽ nhận được các giá trị: 1 và 2. Những giá trị đó ánh xạ tới các công ty thực:
- **1** → Creative Mobile Technologies
- **2** → VeriFone Inc.

Câu chuyện tương tự với các địa điểm - 265 ID địa điểm có thể có tên, quận, tọa độ, v.v. Dữ liệu thô không có bất kỳ thứ gì trong số đó. Vậy làm thế nào để chúng ta thêm nó?

---

## Seeds — đưa dữ liệu tra cứu

###
là gì - Một cách **tải tệp CSV** và cung cấp dưới dạng mô hình dbt
- Bạn thả CSV vào thư mục `seeds/`, chạy `dbt seed` và nó có thể truy vấn giống như bất kỳ mô hình nào khác
- Bạn tham chiếu nó với `{{ ref('filename') }}` — giống như bất kỳ mô hình nào khác mẫu khác

### Khi nào nên sử dụng chúng
- **Bảng tra cứu** chưa tồn tại ở bất kỳ đâu trong kho của bạn
- Các trường hợp bạn không có quyền ghi để tải dữ liệu đúng cách
- Thử nghiệm nhanh hoặc thử nghiệm cục bộ trước khi thực hiện tải dữ liệu phù hợp
- Bộ dữ liệu tĩnh, nhỏ

### Khi KHÔNG sử dụng chúng
- **Không bao giờ cam kết dữ liệu bí mật** — hạt giống đi vào kho git của bạn
- Giữ dữ liệu **nhỏ** — CSV lớn trong git sẽ làm chậm quá trình kéo và đẩy
- Nếu bạn có tùy chọn tải dữ liệu đúng cách tại nguồn, thay vào đó hãy làm như vậy. Hạt giống là giải pháp nhanh chóng và dễ dàng

> 📄 [Hạt giống — tham khảo đầy đủ](https://docs.getdbt.com/docs/build/seeds)

---

## dim_zones — sử dụng hạt giống trong thực tế

CSV tra cứu khu vực taxi có chính xác những gì chúng tôi cần: ID vị trí, quận, tên khu vực và khu vực dịch vụ. Thả nó vào `seeds/`, chạy `dbt seed` và nó hoạt động.

Bây giờ chúng tôi xây dựng `dim_zones`. Mô hình chỉ cần chọn từ hạt giống và đổi tên các cột thành thứ gì đó sạch sẽ hơn.

```sql
select
    locationid as location_id,
    borough,
    zone,
    service_zone
from {{ ref('taxi_zone_lookup') }}
```

Thế là xong - bảng chiều thứ nhất đã xong. Hạt giống đã thực hiện công việc nặng nhọc.

---

## dim_vendors — vấn đề TRƯỜNG HỢP KHI (không được triển khai trong dự án này nhưng được hiển thị để học)

Đối với các nhà cung cấp, chúng tôi có thể lấy `vendor_id` riêng biệt từ mô hình liên kết trung gian bằng cách sử dụng `ref()`. Đủ dễ dàng. Nhưng chúng tôi muốn làm phong phú thêm nó bằng **tên nhà cung cấp**.

### Cách tiếp cận ngây thơ: TRƯỜNG HỢP KHI
Bạn chỉ có thể viết nó nội tuyến:

```sql
with vendors as (
    select distinct vendorid
    from {{ ref('stg_green_tripdata') }}
)

select
    vendorid,
    case
        when vendorid = 1 then 'Creative Mobile Technologies, LLC'
        when vendorid = 2 then 'VeriFone Inc.'
        else 'Unknown'
    end as vendor_name
from vendors
```

Điều này hoạt động. Nhưng nó có một vấn đề thực sự: **điều gì xảy ra khi một nhà cung cấp mới xuất hiện hoặc một nhà cung cấp thay đổi tên?** Bạn phải mở tệp này, tìm khối CASE và thêm một dòng khác. Và nếu bạn cần ánh xạ tương tự ở một nơi khác trong dự án, bạn sao chép-dán toàn bộ. Cuối cùng có người quên cập nhật một trong các bản sao.

### Cách tiếp cận tốt hơn: macro

Macro là câu trả lời của dbt cho vấn đề này. Hãy coi chúng như **hàm SQL có thể tái sử dụng** — ý tưởng tương tự như hàm Python, nhưng dành cho các đoạn mã SQL.

> 📄 [Jinja và macro — tham khảo đầy đủ](https://docs.getdbt.com/docs/build/jinja-macros)

### Cách macro hoạt động
- Được xác định trong các tệp `.sql` bên trong thư mục `macros/`
- Bạn gói logic SQL của mình trong `{% macro macro_name(argument) %}` ... `{% endmacro %}`
- Đối số hoạt động giống như một tham số hàm — bạn truyền một giá trị khi gọi nó
- Bạn gọi nó trong các mô hình của mình bằng `{{ macro_name(argument) }}`
- dbt biên dịch nó — SQL cuối cùng trông giống hệt như bạn đã nhập khối CASE nội tuyến, nhưng mã nguồn của bạn vẫn sạch

```sql
{% macro get_vendor_data(vendor_id_column) %}

{% set vendors = {
    1: 'Creative Mobile Technologies',
    2: 'VeriFone Inc.',
    4: 'Unknown/Other'
} %}

case {{ vendor_id_column }}
    {% for vendor_id, vendor_name in vendors.items() %}
    when {{ vendor_id }} then '{{ vendor_name }}'
    {% endfor %}
end

{% endmacro %}

```

**Sử dụng macro trong mô hình:**

```sql
with trips as (
    select * from {{ ref('fct_trips') }}
),

vendors as (
    select distinct
        vendor_id,
        {{ get_vendor_data('vendor_id') }} as vendor_name
    from trips
)

select * from vendors
```

### Tại sao điều này lại tốt hơn
- **Có thể tái sử dụng** — cần logic loại thanh toán tương tự ở một nơi khác? Chỉ cần gọi lại macro
- **Nguồn tin cậy duy nhất** — loại thanh toán thay đổi? Cập nhật macro ở một nơi, nó được sửa ở mọi nơi
- **Có thể kiểm tra** — logic được tách biệt trong tệp riêng, dễ lý giải hơn về

---

## Xem trước bài tập về nhà — fct_trips

Mô hình chuyến đi thực tế được coi là một bài tập. Đây là những gì được mong đợi:

- **Một hàng mỗi chuyến** — kết hợp màu vàng và xanh lục (việc kết hợp đã được thực hiện trong mô hình trung gian)
- **Thêm khóa chính** (`trip_id`) — nó phải **duy nhất**
- **Tìm và sửa các khóa trùng lặp** — có khá nhiều khóa trong tập dữ liệu này. Một số đến từ nguồn, một số được giới thiệu trong quá trình đoàn kết. Tìm chúng, hiểu lý do tại sao chúng xảy ra và sửa chúng
- **Làm giàu `payment_type`** (có một hạt giống cho điều này trong repo).
