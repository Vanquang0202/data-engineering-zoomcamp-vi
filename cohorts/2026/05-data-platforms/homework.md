# Bài tập Module 5: Data Platforms với Bruin

Trong bài tập này, chúng ta sẽ dùng Bruin để xây dựng một data pipeline hoàn chỉnh, từ Data Ingestion đến báo cáo.

## Chuẩn bị

1. Cài đặt Bruin CLI: `curl -LsSf https://getbruin.com/install/cli | sh`
2. Khởi tạo template zoomcamp: `bruin init zoomcamp my-pipeline`
3. Cấu hình kết nối DuckDB trong `.bruin.yml`
4. Làm theo hướng dẫn ở [README của module chính](../../../05-data-platforms/)

Sau khi chuẩn bị xong, bạn sẽ có một data pipeline xử lý dữ liệu taxi NYC hoạt động được.

---

### Câu hỏi 1. Cấu trúc pipeline Bruin

Một dự án Bruin bắt buộc phải có những file/thư mục nào?

- `bruin.yml` and `assets/`
- `.bruin.yml` and `pipeline.yml` (assets can be anywhere)
- `.bruin.yml` and `pipeline/` with `pipeline.yml` and `assets/`
- `pipeline.yml` and `assets/` only

---

### Câu hỏi 2. Chiến lược Materialization

Bạn đang xây dựng pipeline xử lý dữ liệu taxi NYC theo tháng dựa trên `pickup_datetime`. Chiến lược Incremental nào phù hợp nhất để xử lý một khoảng thời gian cụ thể bằng cách xóa rồi chèn lại dữ liệu của khoảng đó?

- `append` - luôn thêm dòng mới
- `replace` - xóa toàn bộ rồi xây dựng lại
- `time_interval` - nạp gia tăng dựa trên cột thời gian
- `view` - chỉ tạo bảng ảo

---

### Câu hỏi 3. Biến trong pipeline

Bạn có biến sau được định nghĩa trong `pipeline.yml`:

```yaml
variables:
  taxi_types:
    type: array
    items:
      type: string
    default: ["yellow", "green"]
```

Khi chạy pipeline, bạn ghi đè biến này thế nào để chỉ xử lý taxi yellow?

- `bruin run --taxi-types yellow`
- `bruin run --var taxi_types=yellow`
- `bruin run --var 'taxi_types=["yellow"]'`
- `bruin run --set taxi_types=["yellow"]`

---

### Câu hỏi 4. Chạy kèm các dependency

Bạn đã sửa asset `ingestion/trips.py` và muốn chạy nó cùng tất cả asset downstream. Bạn cần dùng lệnh nào?

- `bruin run ingestion.trips --all`
- `bruin run ingestion/trips.py --downstream`
- `bruin run pipeline/trips.py --recursive`
- `bruin run --select ingestion.trips+`

---

### Câu hỏi 5. Kiểm tra chất lượng dữ liệu

Bạn muốn đảm bảo cột `pickup_datetime` trong bảng trips không bao giờ chứa giá trị NULL. Bạn cần thêm quality check nào vào định nghĩa asset?

- `name: unique`
- `name: not_null`
- `name: positive`
- `name: accepted_values, value: [not_null]`

---

### Câu hỏi 6. Lineage và dependency

Sau khi xây dựng pipeline, bạn muốn trực quan hóa đồ thị dependency giữa các asset. Bạn cần dùng lệnh Bruin nào?

- `bruin graph`
- `bruin dependencies`
- `bruin lineage`
- `bruin show`

---

### Câu hỏi 7. Chạy lần đầu

Bạn chạy pipeline Bruin lần đầu trên một cơ sở dữ liệu DuckDB mới. Cần dùng flag nào để bảo đảm các bảng được tạo từ đầu?

- `--create`
- `--init`
- `--full-refresh`
- `--truncate`

---

## Nộp bài

- Form for submitting: <https://courses.datatalks.club/de-zoomcamp-2026/homework/hw5>

=======

## Chia sẻ quá trình học công khai

Chúng tôi khuyến khích mọi người chia sẻ những gì mình đã học. Cách học này gọi là "learning in public".

Đọc thêm về lợi ích [tại đây](https://aishippingblog.com/p/benefits-of-learning-in-public-and).

### Bài đăng mẫu trên LinkedIn

```
🚀 Week 5 of Data Engineering Zoomcamp by @DataTalksClub complete!

Just finished Module 5 - Data Platforms with Bruin. Learned how to:

✅ Build end-to-end ELT pipelines with Bruin
✅ Configure environments and connections
✅ Use materialization strategies for incremental processing
✅ Add data quality checks to ensure data integrity
✅ Deploy pipelines from local to cloud (BigQuery)

Modern data platforms in a single CLI tool - no vendor lock-in!

Here's my homework solution: <LINK>

Following along with this amazing free course - who else is learning data engineering?

You can sign up here: https://github.com/DataTalksClub/data-engineering-zoomcamp/
```

### Bài đăng mẫu trên Twitter/X

```
📊 Module 5 of Data Engineering Zoomcamp done!

- Data Platforms with Bruin
- End-to-end ELT pipelines
- Data quality & lineage
- Deployment to BigQuery

My solution: <LINK>

Free course by @DataTalksClub: https://github.com/DataTalksClub/data-engineering-zoomcamp/
```
