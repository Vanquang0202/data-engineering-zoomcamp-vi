## Dự án cuối khóa

[🎥 Hướng dẫn làm dự án (hãy xem video!)](https://www.youtube.com/watch?v=BL0E8xO8OnE)


### Mục tiêu

Mục tiêu là vận dụng toàn bộ kiến thức đã học trong khóa
để xây dựng một data pipeline end-to-end.

### Yêu cầu bài toán

Xây dựng dashboard gồm hai ô nội dung bằng cách:

* Chọn bộ dữ liệu bạn quan tâm (xem [Bộ dữ liệu](#datasets))
* Tạo pipeline xử lý bộ dữ liệu và đưa vào Data Lake
* Tạo pipeline chuyển dữ liệu từ Data Lake sang Data Warehouse
* Biến đổi dữ liệu trong Data Warehouse để chuẩn bị cho dashboard
* Xây dựng dashboard trực quan hóa dữ liệu

### Bộ dữ liệu không được dùng

Bộ dữ liệu taxi NYC đã được dùng xuyên suốt các module và bài tập nên không được dùng cho dự án. Hãy chọn bộ dữ liệu khác.


## Data Pipeline 

Pipeline có thể xử lý theo **Streaming** hoặc **Batch**: đây là lựa chọn đầu tiên bạn cần đưa ra. 

* **Streaming**: Tiếp nhận dữ liệu theo thời gian thực rồi đưa vào Data Lake
* **Batch**: Xử lý dữ liệu định kỳ (ví dụ theo giờ hoặc theo ngày)

## Công nghệ 

Bạn không bắt buộc chỉ dùng công nghệ đã học trong khóa; có thể chọn công cụ khác:

* **Cloud**: AWS, GCP, Azure, ...
* **Infrastructure as Code (IaC)**: Terraform, Pulumi, Cloud Formation, ...
* **Điều phối workflow**: Airflow, Prefect, Luigi, ...
* **Data Warehouse**: BigQuery, Snowflake, Redshift, ...
* **Xử lý Batch**: Spark, Flink, AWS Batch, ...
* **Xử lý Streaming**: Kafka, Pulsar, Kinesis, ...

Nếu dùng công cụ chưa được giới thiệu trong khóa, hãy giải thích chức năng của công cụ đó.

Nếu chưa rõ về công cụ nào, hãy hỏi trên Slack.

## Dashboard

Bạn có thể xây dashboard bằng công cụ trong khóa (Looker Studio hoặc Streamlit) hay công cụ BI khác. Nếu dùng công cụ khác, hãy nêu rõ và bảo đảm học viên cùng khóa có thể truy cập dashboard. 

Dashboard cần có ít nhất hai ô nội dung. Chúng tôi gợi ý:

- 1 biểu đồ thể hiện phân bố theo nhóm giá trị
- 1 biểu đồ thể hiện dữ liệu thay đổi theo thời gian

Hãy thêm tiêu đề và chú thích để biểu đồ dễ hiểu.
 
Dashboard mẫu: ![image](https://user-images.githubusercontent.com/4315804/159771458-b924d0c1-91d5-4a8a-8c34-f36c25c31a3c.png)


## Đánh giá chéo

> [!IMPORTANT]  
> Các dự án sẽ được đánh giá chéo. Đây là cơ hội để các bạn học hỏi lẫn nhau.
> * Để dự án được tính điểm, bạn cần đánh giá dự án của 3 học viên khác
> * Bạn nhận thêm 3 điểm cho mỗi lượt đánh giá

## Tiêu chí đánh giá

* Mô tả bài toán
    * 0 điểm: Không mô tả bài toán
    * 2 điểm: Có mô tả nhưng quá ngắn hoặc chưa rõ ràng
    * 4 điểm: Mô tả rõ bài toán mà dự án giải quyết
* Cloud
    * 0 điểm: Không dùng Cloud; mọi thứ chỉ chạy cục bộ
    * 2 điểm: Dự án được phát triển trên Cloud
    * 4 điểm: Dự án được phát triển trên Cloud và dùng công cụ IaC
* Data Ingestion (chọn Batch hoặc Streaming)
    * Batch / Điều phối workflow
        * 0 điểm: Không có điều phối workflow
        * 2 điểm: Điều phối một phần; một số bước vẫn chạy thủ công
        * 4 điểm: Pipeline end-to-end gồm nhiều bước trong DAG và đưa dữ liệu vào Data Lake
    * Streaming
        * 0 điểm: Không dùng hệ thống Streaming (như Kafka, Pulsar, v.v.)
        * 2 điểm: Pipeline đơn giản với một consumer và một producer
        * 4 điểm: Dùng consumer/producer và công nghệ Streaming (như Kafka Streaming, Spark Streaming, Flink, v.v.)
* Data Warehouse
    * 0 điểm: Không dùng Data Warehouse
    * 2 điểm: Có bảng trong Data Warehouse nhưng chưa tối ưu
    * 4 điểm: Bảng được Partition và Cluster hợp lý cho các truy vấn phía trước, kèm giải thích
* Biến đổi dữ liệu (dbt, Spark, v.v.)
    * 0 điểm: Không có bước biến đổi
    * 2 điểm: Biến đổi SQL đơn giản (không dùng dbt hay công cụ tương tự)
    * 4 điểm: Bước biến đổi được định nghĩa bằng dbt, Spark hoặc công nghệ tương tự
* Dashboard
    * 0 điểm: Không có dashboard
    * 2 điểm: Dashboard có 1 ô nội dung
    * 4 điểm: Dashboard có 2 ô nội dung
* Khả năng tái tạo kết quả
    * 0 điểm: Hoàn toàn không có hướng dẫn chạy code
    * 2 điểm: Có hướng dẫn nhưng chưa đầy đủ
    * 4 điểm: Hướng dẫn rõ ràng, code dễ chạy và hoạt động đúng


> [!NOTE]
> Bạn nên tạo repository mới cho dự án (không đặt trong repository sẵn có), đặt tên có ý nghĩa như
> "Quake Analytics Dashboard" hoặc "Bike Data Insights", và ghi càng nhiều thông tin hữu ích càng tốt trong README. ChatGPT có thể hỗ trợ bạn. Điều này vừa giúp bạn giới thiệu dự án khi tìm việc, vừa tạo cơ hội đưa dự án lên [Projects Gallery App](#projects-gallery).
> Nếu README trống hoặc quá sơ sài, bạn có thể bị trừ điểm theo [Tiêu chí đánh giá](#evaluation-criteria).

## Làm thêm (không bắt buộc)

> [!NOTE]
> Những nội dung sau không có trong khóa học, hoàn toàn tùy chọn và không được tính điểm.

Tuy vậy, triển khai chúng có thể cải thiện đáng kể chất lượng dự án:

* Thêm test
* Dùng make
* Thêm pipeline CI/CD

Nếu muốn đưa dự án vào portfolio, những tính năng bổ sung này sẽ giúp bạn nổi bật hơn.

## Gợi ý từ người đánh giá chéo

Những gợi ý này đến từ các học viên đã đánh giá nhiều dự án và nhận thấy các lỗi lặp lại. Làm theo sẽ giúp bạn tránh lỗi thường gặp và giúp người khác đánh giá dự án dễ hơn.

From Pável Kalmykov Razgovórov:

* Thử chạy repository từ một bản clone mới trước khi nộp. Có dự án tham chiếu đến file hoặc thư mục chưa commit (thư mục config, requirements.txt sai path, volume trỏ đến thư mục không tồn tại). Nếu tài nguyên không có trong repository, người đánh giá không thể dùng nó.
* Đừng ghi cứng path cục bộ hoặc ID dự án Cloud cá nhân. Hãy dùng environment variable.
* Xử lý lỗi của API bên ngoài. Nếu script lấy dữ liệu từ URL, hãy xử lý phù hợp khi URL trả về 404 hoặc 500.
* Chạy `docker compose up` ít nhất một lần trước khi nộp. Đã có dự án gặp SyntaxError trong file cấu hình khiến mọi container đều không khởi động được.
* Giữ README nhất quán với code. Kiểm tra file docker-compose còn trỏ đến service cũ hay không, .env.example có sai cổng không, hoặc hướng dẫn có nhắc đến thư mục không tồn tại không.
* Nếu dự án dbt dùng package bên ngoài, hãy bảo đảm có bước chạy `dbt deps`. Một số dự án cần dbt_utils nhưng chưa cài đặt.

## Gian lận và đạo văn

Không chấp nhận đạo văn dưới bất kỳ hình thức nào. Ví dụ:

* Dùng toàn bộ hoặc một phần notebook, dự án của người khác cho dự án cuối khóa
* Dùng lại toàn bộ hoặc một phần dự án của chính mình từ khóa học hoặc bootcamp khác
* Dùng lại dự án giữa kỳ của ML Zoomcamp cho dự án cuối khóa
* Dùng lại dự án ML Zoomcamp từ khóa học những năm trước

Vi phạm bất kỳ quy định nào ở trên sẽ khiến dự án bị chấm 0 điểm.

## Tài nguyên

### Bộ dữ liệu

Tham khảo danh sách [bộ dữ liệu](datasets.md) để chọn dữ liệu phù hợp.

### Link hữu ích

* [Unit test và CI cho Airflow](https://www.astronomer.io/events/recaps/testing-airflow-to-bulletproof-your-code/)
* [CI/CD for Airflow (with Gitlab & GCP state file)](https://engineering.ripple.com/building-ci-cd-with-airflow-gitlab-and-terraform-in-gcp)
* [CI/CD for Airflow (with GitHub and S3 state file)](https://programmaticponderings.com/2021/12/14/devops-for-dataops-building-a-ci-cd-pipeline-for-apache-airflow-dags/)
* [CD for Terraform](https://medium.com/towards-data-science/git-actions-terraform-for-data-engineers-scientists-gcp-aws-azure-448dc7c60fcc)
* [Spark + Airflow](https://medium.com/doubtnut/github-actions-airflow-for-automating-your-spark-pipeline-c9dff32686b)
* [Phối hợp dbt và Airflow](https://docs.getdbt.com/blog/dbt-airflow-spiritual-alignment) — điều phối dbt bằng Airflow; tài khoản dbt dùng thử có API để Airflow Python operator kích hoạt job ([code mẫu](https://github.com/sungchun12/airflow-toolkit/blob/95d40ac76122de337e1b1cdc8eed35ba1c3051ed/dags/examples/dbt_cloud_example.py)) — đừng commit API key hoặc job ID
* [Airflow DataProc operators](https://airflow.apache.org/docs/apache-airflow-providers-google/stable/_api/airflow/providers/google/cloud/operators/dataproc/index.html) — cấp cho service account vai trò DataProc Administrator và Service Account User ([lý do](https://stackoverflow.com/questions/63941429/user-not-authorized-to-act-as-service-account-when-using-workload-identity)); khi dùng `DataprocSubmitPySparkJobOperator`, thêm BigQuery connector jar (`gs://spark-lib/bigquery/spark-bigquery-with-dependencies_2.12-0.24.0.jar`) vì DataProc không kèm sẵn file này


### Thư viện dự án

Khám phá các dự án do thành viên cộng đồng hoàn thành. Chúng bao quát nhiều chủ đề và sử dụng nhiều công cụ, kỹ thuật khác nhau. Bạn có thể xem cách người khác giải quyết bài toán dữ liệu thực tế, tổ chức code và trình bày kết quả. Đây là nguồn tham khảo hữu ích để học hỏi và tìm ý tưởng cho dự án của mình.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://datatalksclub-projects.streamlit.app/)

### DE Zoomcamp 2023

* [Dự án năm 2023](../cohorts/2023/project.md)

### DE Zoomcamp 2022

* [Dự án năm 2022](../cohorts/2022/project.md)
