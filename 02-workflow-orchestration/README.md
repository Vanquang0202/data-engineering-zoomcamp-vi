# Điều phối quy trình làm việc

## Đơn vị

1. [Điều phối quy trình làm việc là gì?](01-what-is-workflow-orchestration.md)
2. [Kestra là gì?](02-what-is-kestra.md)
3. [Cài đặt Kestra](03-installing-kestra.md)
4. [Kestra Các khái niệm](04-kestra-concepts.md)
5. [Mã Python dàn dựng](05-orchestrate-python-code.md)
6. [Quy trình bắt đầu](06-getting-started-pipeline.md)
7. [DB cục bộ: Tải dữ liệu Taxi tới Postgres](07-load-taxi-data-to-postgres.md)
8. [Cơ sở dữ liệu cục bộ: Tìm hiểu cách lập kế hoạch và chèn lấp](08-scheduling-and-backfills.md)
9. [ETL vs ELT](09-etl-vs-elt.md)
10. [Thiết lập Google Cloud Platform (GCP)](10-setup-google-cloud-platform.md)
11. [Quy trình làm việc của GCP: Tải dữ liệu taxi vào BigQuery](11-load-taxi-data-to-bigquery.md)
12. [Quy trình làm việc của GCP: Lên lịch và chèn lấp toàn bộ bộ dữ liệu](12-schedule-and-backfill-full-dataset.md)
13. [Giới thiệu: Tại sao dùng AI cho quy trình làm việc?](13-why-ai-for-workflows.md)
14. [Kỹ thuật ngữ cảnh với ChatGPT](14-context-engineering-with-chatgpt.md)
15. [AI Copilot trong Kestra](15-ai-copilot-in-kestra.md)
16. [Phần thưởng: Thế hệ tăng cường truy xuất (RAG)](16-retrieval-augmented-generation.md)
17. [Phần thưởng: Triển khai lên đám mây (Tùy chọn)](17-deploy-to-the-cloud.md)
18. [Tài nguyên bổ sung](18-additional-resources.md)

## Bài tập về nhà


## Phần

### 2.1 Giới thiệu về Điều phối quy trình công việc
Trong phần này, bạn sẽ tìm hiểu các nền tảng của điều phối quy trình công việc, tầm quan trọng của nó và cách Kestra phù hợp với bối cảnh điều phối.

### 2.2 Bắt đầu với Kestra
Trong phần này, bạn sẽ tìm hiểu cách cài đặt Kestra, cũng như các khái niệm chính cần thiết để xây dựng quy trình làm việc đầu tiên của bạn. Khi quy trình làm việc đầu tiên của chúng tôi được xây dựng, chúng tôi có thể mở rộng quy trình này hơn nữa bằng cách thực thi tập lệnh Python bên trong quy trình làm việc.

Bạn sẽ:
1. Cài đặt Kestra bằng Docker Compose
2. Tìm hiểu các khái niệm về Kestra để xây dựng quy trình làm việc đầu tiên của bạn
3. Thực thi tập lệnh Python bên trong Kestra Flow

### 2.3 Dự án mã hóa thực hành: Xây dựng đường ống dữ liệu với Kestra
Tiếp theo, chúng tôi sẽ xây dựng đường ống ETL cho dữ liệu Taxi Vàng và Xanh từ Ủy ban Taxi và Limousine (TLC) của NYC. Bạn sẽ:
1. Trích xuất dữ liệu từ [tệp CSV](https://github.com/DataTalksClub/nyc-tlc-data/releases).
2. Tải nó vào Postgres hoặc Google Cloud (GCS + BigQuery).
3. Khám phá quy trình lập kế hoạch và lấp đầy.

### 2.4 Đường ống ELT trong Kestra: Google Cloud Platform
Bây giờ bạn đã tìm hiểu cách xây dựng đường ống ETL cục bộ bằng Postgres, chúng tôi đã sẵn sàng chuyển sang đám mây. Trong phần này, chúng tôi sẽ tải cùng một dữ liệu Taxi màu vàng và màu xanh lá cây lên Google Cloud Platform (GCP) bằng cách sử dụng:
1. Google Cloud Storage (GCS) dưới dạng hồ dữ liệu
2. BigQuery dưới dạng kho dữ liệu.

### 2.5 Sử dụng AI cho Kỹ thuật dữ liệu trong Kestra
Phần này dựa trên những gì bạn đã học trước đó trong Mô-đun 2 để chỉ cho bạn cách AI có thể tăng tốc độ phát triển quy trình làm việc.

Đến cuối phần này, bạn sẽ:
- Hiểu lý do tại sao kỹ thuật ngữ cảnh lại quan trọng khi cộng tác với LLM
- Sử dụng AI Copilot để xây dựng luồng Kestra nhanh hơn
- Sử dụng Thế hệ tăng cường truy xuất (RAG) trong đường ống dữ liệu

#### Điều kiện tiên quyết
- Hoàn thành các phần trước trong Mô-đun 2 (Điều phối quy trình công việc với Kestra)
- Kestra chạy cục bộ
- Tài khoản Google Cloud có quyền truy cập vào API Gemini (có một cấp miễn phí hào phóng!)

---

### Phần thưởng 2.6: Triển khai lên đám mây (Tùy chọn)
Bây giờ, chúng tôi đã làm cho tất cả các quy trình của mình hoạt động và chúng tôi biết cách nhanh chóng tạo các luồng mới bằng AI Copilot của Kestra, chúng tôi có thể triển khai Kestra lên đám mây để nó có thể tiếp tục điều phối các quy trình đã lên lịch của chúng tôi.

Trong phần thưởng này, chúng tôi sẽ đề cập đến cách bạn có thể triển khai Kestra trên Google Cloud và tự động đồng bộ hóa quy trình công việc của bạn từ kho lưu trữ Git.

Lưu ý: Khi chuyển giao quy trình làm việc của bạn cho Kestra, hãy đảm bảo quy trình làm việc của bạn không chứa bất kỳ thông tin nhạy cảm nào. Bạn có thể sử dụng [Bí mật](https://go.kestra.io/de-zoomcamp/secret) và [KV Store](https://go.kestra.io/de-zoomcamp/kv-store) để loại bỏ dữ liệu nhạy cảm ra khỏi logic quy trình công việc của bạn.

##### Tài nguyên
- [Cài đặt Kestra trên Google Cloud](https://go.kestra.io/de-zoomcamp/gcp-install)
- [Chuyển từ phát triển sang sản xuất](https://go.kestra.io/de-zoomcamp/dev-to-prod)
- [Sử dụng Git trong Kestra](https://go.kestra.io/de-zoomcamp/git)
- [Triển khai các luồng với GitHub Hành động](https://go.kestra.io/de-zoomcamp/deploy-github-actions)

### 2.7 Tài nguyên bổ sung
- Kiểm tra [Kestra Docs](https://go.kestra.io/de-zoomcamp/docs)
- Khám phá thư viện [Blueprints](https://go.kestra.io/de-zoomcamp/blueprints)
của chúng tôi - Duyệt qua hơn 600 [plugin](https://go.kestra.io/de-zoomcamp/plugins) có sẵn trong Kestra
- Hãy cho chúng tôi một ngôi sao trên [GitHub](https://go.kestra.io/de-zoomcamp/github)
- Tham gia [cộng đồng Slack](https://go.kestra.io/de-zoomcamp/slack) của chúng tôi nếu bạn có bất kỳ câu hỏi nào
- Tìm tất cả video trong [Danh sách phát YouTube](https://go.kestra.io/de-zoomcamp/yt-playlist)
này

#### Mẹo khắc phục sự cố
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

---

## File đồng hành

* [`docker-compose.yml`](docker-compose.yml) — Kestra, Postgres và pgAdmin
* [`flows/`](flows/) — mọi luồng Kestra được sử dụng trong mô-đun này

# Ghi chú cộng đồng

Bạn đã ghi chép chưa? Bạn có thể chia sẻ chúng bằng cách tạo PR cho tệp này!

* Thêm ghi chú của bạn phía trên dòng này

---
