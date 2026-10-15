---
prev_url: 17-deploy-to-the-cloud.md
next_url: ../03-data-warehouse/01-data-warehouse-and-bigquery.md
---
# Tài nguyên bổ sung

- Kiểm tra [Kestra Docs](https://go.kestra.io/de-zoomcamp/docs)
- Khám phá thư viện [Blueprints](https://go.kestra.io/de-zoomcamp/blueprints)
của chúng tôi - Duyệt qua hơn 600 [plugin](https://go.kestra.io/de-zoomcamp/plugins) có sẵn trong Kestra
- Hãy cho chúng tôi một ngôi sao trên [GitHub](https://go.kestra.io/de-zoomcamp/github)
- Tham gia [cộng đồng Slack](https://go.kestra.io/de-zoomcamp/slack) của chúng tôi nếu bạn có bất kỳ câu hỏi nào
- Tìm tất cả video trong [Danh sách phát YouTube](https://go.kestra.io/de-zoomcamp/yt-playlist)
này

*Bộ tài nguyên là bản đồ để tiếp tục sau bài học: tài liệu tham khảo, ví dụ, công cụ và kênh trợ giúp phục vụ các nhu cầu khác nhau.*

## Mẹo khắc phục sự cố
Nếu bạn gặp bất kỳ sự cố nào với luồng Kestra trong Mô-đun 2, hãy đảm bảo sử dụng các hình ảnh/cổng Docker sau:
- `image: kestra/kestra:v1.1` - ghim hình ảnh Kestra Docker của bạn vào phiên bản này để chúng tôi có thể đảm bảo khả năng tái tạo; KHÔNG sử dụng `kestra/kestra:develop` vì đây là phiên bản phát triển tiên tiến có thể chứa lỗi
- `postgres:18` — đảm bảo ghim hình ảnh Postgres của bạn vào phiên bản 18
- Nếu bạn chạy `pgAdmin` hoặc thứ gì khác trên cổng 8080, bạn có thể điều chỉnh Kestra `docker-compose` để sử dụng phiên bản khác cổng, ví dụ: thay đổi ánh xạ cổng thành 18080 thay vì 8080, sau đó truy cập Kestra UI trong trình duyệt của bạn từ http://localhost:18080/ thay vì từ http://localhost:8080/

Nếu bạn vẫn gặp phải bất kỳ sự cố nào, hãy dừng và xóa vùng chứa Kestra + Postgres hiện có của bạn rồi khởi động lại chúng bằng `docker-compose up -d`. Nếu cách này không hiệu quả, hãy đăng câu hỏi của bạn lên DataTalksClub Slack hoặc trên Slack http://kestra.io/slack.
của Kestra
Nếu bạn gặp lỗi tương tự như:
```
BigQueryError{reason=invalid, location=null,
message=Error while reading table: kestra-sandbox.zooomcamp.yellow_tripdata_2020_01,
error message: CSV table references column position 17, but line contains only 14 columns.;
line_number: 2103925 byte_offset_to_start_of_line: 194863028
column_index: 17 column_name: "congestion_surcharge" column_type: NUMERIC
File: gs://anna-geller/yellow_tripdata_2020-01.csv}
```

Điều đó có nghĩa là tệp CSV bạn đang cố tải vào BigQuery có số cột không khớp giữa bảng nguồn bên ngoài (tức là tệp trong GCS) và bảng đích trong BigQuery. Điều này có thể xảy ra khi do sự cố mạng/truyền tải, tệp không được tải xuống đầy đủ từ GitHub hoặc không được tải lên GCS đúng cách. Lỗi gợi ý các vấn đề về lược đồ nhưng thực tế không phải vậy. Chỉ cần chạy lại toàn bộ quá trình thực thi, bao gồm tải lại tệp CSV xuống và tải lại lên GCS. Điều này sẽ giải quyết vấn đề.
