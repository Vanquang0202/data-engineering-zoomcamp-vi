# Bài tập Module 4: Analytics Engineering với dbt [BẢN NHÁP]

> [!NOTE]
> Đây là bản nháp được chuyển từ khóa 2026. Câu hỏi, bộ dữ liệu và
> hạn nộp sẽ được cập nhật trước khi module bắt đầu.

Trong bài tập này, chúng ta sẽ dùng dự án dbt tại `04-analytics-engineering/taxi_rides_ny/` để biến đổi dữ liệu taxi NYC và trả lời câu hỏi bằng cách truy vấn các model.

## Cài đặt

1. Thiết lập dự án dbt theo [hướng dẫn thiết lập](setup/)
2. Nạp dữ liệu taxi Green và Yellow giai đoạn 2019-2020 cùng dữ liệu chuyến đi FHV năm 2019 vào Data Warehouse (dùng các bảng dữ liệu tĩnh từ [dtc github](https://github.com/DataTalksClub/nyc-tlc-data/), không dùng bảng chính thức của TLC vì một số giá trị có thể thay đổi theo thời gian)
3. Chạy `dbt build --target prod` để tạo tất cả model và chạy test

> **Lưu ý:** Mặc định dbt dùng target `dev`. Bạn phải dùng `--target prod` để build model trong dataset production, đúng với các truy vấn của bài tập bên dưới.

Sau khi build thành công, Data Warehouse của bạn sẽ có các model như `fct_trips`, `dim_zones` và `fct_monthly_zone_revenue`.

---

### Câu 1. Lineage và thực thi dbt

Cho một dự án dbt có cấu trúc sau:

```
models/
├── staging/
│   ├── stg_green_tripdata.sql
│   └── stg_yellow_tripdata.sql
└── intermediate/
    └── int_trips_unioned.sql (depends on stg_green_tripdata & stg_yellow_tripdata)
```

Nếu bạn chạy `dbt run --select int_trips_unioned`, mô hình nào sẽ được xây dựng?

- `stg_green_tripdata`, `stg_yellow_tripdata` và `int_trips_unioned` (phụ thuộc ngược dòng)
- Bất kỳ mô hình nào có phụ thuộc ngược dòng và xuôi dòng vào `int_trips_unioned`
- `int_trips_unioned` chỉ
- `int_trips_unioned`, `int_trips` và `fct_trips` (phụ thuộc hạ lưu)

---

### Câu 2. dbt test

Bạn đã cấu hình một generic test như sau trong `schema.yml`:
```yaml
columns:
  - name: payment_type
    data_tests:
      - accepted_values:
          arguments:
            values: [1, 2, 3, 4, 5]
            quote: false
```

Mô hình `fct_trips` của bạn đã chạy thành công trong nhiều tháng. Giá trị mới `6` hiện xuất hiện trong dữ liệu nguồn.

Điều gì xảy ra khi bạn chạy `dbt test --select fct_trips`?

- dbt sẽ bỏ qua bài kiểm tra vì mô hình không thay đổi
- dbt sẽ thất bại trong bài kiểm tra, trả về mã thoát khác 0
- dbt sẽ vượt qua bài kiểm tra với cảnh báo về giá trị mới
- dbt sẽ cập nhật cấu hình để bao gồm giá trị mới

---

### Câu 3. Đếm bản ghi trong `fct_monthly_zone_revenue`

Sau khi chạy dự án dbt của bạn, hãy truy vấn mô hình `fct_monthly_zone_revenue`.

Số lượng bản ghi trong mô hình `fct_monthly_zone_revenue` là bao nhiêu?

- 12,998
- 14,120
- 12,184
- 15,421

---

### Câu 4. Khu vực có doanh thu cao nhất của taxi Green (2020)

Dùng bảng `fct_monthly_zone_revenue` để tìm khu vực đón khách có **tổng doanh thu cao nhất** (`revenue_monthly_total_amount`) của taxi **Green** năm 2020.

Khu vực nào có doanh thu cao nhất?

- East Harlem North
- Morningside Heights
- East Harlem South
- Washington Heights South

---

### Câu 5. Số chuyến taxi Green (tháng 10/2019)

Dùng bảng `fct_monthly_zone_revenue`, **tổng số chuyến đi** (`total_monthly_trips`) của taxi Green trong tháng 10/2019 là bao nhiêu?

- 500,234
- 350,891
- 384,624
- 421,509

---

### Câu 6. Xây dựng staging model cho dữ liệu FHV

Tạo staging model cho dữ liệu chuyến đi **For-Hire Vehicle (FHV)** năm 2019.

1. Nạp [dữ liệu chuyến đi FHV năm 2019](https://github.com/DataTalksClub/nyc-tlc-data/releases/tag/fhv) vào Data Warehouse
2. Tạo staging model `stg_fhv_tripdata` với các yêu cầu:
   - Lọc bỏ bản ghi có `dispatching_base_num IS NULL`
   - Đổi tên các trường theo quy ước đặt tên của dự án (ví dụ: `PUlocationID` → `pickup_location_id`)

Số lượng bản ghi trong `stg_fhv_tripdata` là bao nhiêu?

- 42,084,899
- 43,244,693
- 22,998,722
- 44,112,187

---

## Nộp bài

- Biểu mẫu nộp bài: <https://courses.datatalks.club/de-zoomcamp-2026/homework/hw4>

=======

## Chia sẻ quá trình học công khai

Chúng tôi khuyến khích mọi người chia sẻ những gì mình đã học. Cách học này gọi là "learning in public".

Đọc thêm về các lợi ích [tại đây](https://aishippingblog.com/p/benefits-of-learning-in-public-and).

### Bài đăng mẫu cho LinkedIn

```
🚀 Week 4 of Data Engineering Zoomcamp by @DataTalksClub complete!

Just finished Module 4 - Analytics Engineering with dbt. Learned how to:

✅ Build transformation models with dbt
✅ Create staging, intermediate, and fact tables
✅ Write tests to ensure data quality
✅ Understand lineage and model dependencies
✅ Analyze revenue patterns across NYC zones

Transforming raw data into analytics-ready models - the T in ELT!

Here's my homework solution: <LINK>

Following along with this amazing free course - who else is learning data engineering?

You can sign up here: https://github.com/DataTalksClub/data-engineering-zoomcamp/
```

### Bài đăng mẫu cho Twitter/X

```
📈 Module 4 of Data Engineering Zoomcamp done!

- Analytics Engineering with dbt
- Transformation models & tests
- Data lineage & dependencies
- NYC taxi revenue analysis

My solution: <LINK>

Free course by @DataTalksClub: https://github.com/DataTalksClub/data-engineering-zoomcamp/
```
