---
video_url: https://www.youtube.com/watch?v=E04yurp1tSU
prev_url: 08-scheduling-and-backfills.md
next_url: 10-setup-google-cloud-platform.md
---
# ETL so với ELT

Trong 2.3, chúng tôi đã tạo một đường dẫn ETL bên trong Kestra:
- **Extract:** Đầu tiên, chúng tôi trích xuất tập dữ liệu từ GitHub
- **Transform:** Tiếp theo, chúng tôi chuyển đổi nó bằng Python
- **Tải:** Cuối cùng, chúng tôi tải nó vào cơ sở dữ liệu Postgres

Mặc dù điều này rất tiêu chuẩn trong toàn ngành nhưng đôi khi việc thay đổi thứ tự khi làm việc với đám mây là điều hợp lý. Nếu bạn đang làm việc với một tập dữ liệu lớn, chẳng hạn như dữ liệu Yellow Taxi, thì việc trích xuất và tải thẳng vào kho dữ liệu, sau đó thực hiện các phép biến đổi trực tiếp trong kho dữ liệu có thể mang lại lợi ích. Khi làm việc với BigQuery, chúng ta sẽ sử dụng ELT:
- **Extract:** Đầu tiên, chúng ta trích xuất tập dữ liệu từ GitHub
- **Load:** Tiếp theo, chúng ta tải tập dữ liệu này (trong trường hợp này là tệp csv) vào hồ dữ liệu (Google Cloud Storage)
- **Transform:**Query Cuối cùng, chúng ta có thể tạo một bảng bên trong kho dữ liệu (Big) sử dụng dữ liệu từ dữ liệu của chúng tôi lake để thực hiện các phép biến đổi của chúng tôi.

Lý do tải vào kho dữ liệu trước khi chuyển đổi có nghĩa là chúng tôi có thể tận dụng lợi ích hiệu suất của đám mây để chuyển đổi các tập dữ liệu lớn. Những gì có thể mất nhiều thời gian hơn đối với máy cục bộ, có thể mất một phần nhỏ thời gian trên đám mây.


Trong một số video tiếp theo, chúng ta sẽ xem xét cách thiết lập BigQuery và chuyển đổi tập dữ liệu Yellow Taxi.

## Tài nguyên
- [Video ETL vs ELT](https://go.kestra.io/de-zoomcamp/etl-vs-elt)
- [Video kho dữ liệu 101](https://go.kestra.io/de-zoomcamp/data-warehouse-101)
- [Video hồ dữ liệu 101](https://go.kestra.io/de-zoomcamp/data-lakes-101)
