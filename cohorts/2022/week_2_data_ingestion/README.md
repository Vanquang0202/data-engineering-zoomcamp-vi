## Tuần 2: Nhập dữ liệu

### Hồ dữ liệu (GCS)

* Hồ dữ liệu
là gì * ELT so với ETL
* Các lựa chọn thay thế cho các thành phần (S3/HDFS, Redshift, Snowflake, v.v.)

:movie_Camera: [Video](https://www.youtube.com/watch?v=W3Zm6rjOq70&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb)

[Trang trình bày](https://docs.google.com/presentation/d/1RkH-YhBz2apIjYZAxUz2Uks4Pt51-fVWVN9CcH9ckyY/edit?usp=sharing)


### Giới thiệu về điều phối quy trình công việc

* Đường ống điều phối là gì?
* DAG là gì?
* [Video](https://www.youtube.com/watch?v=0yK7LXwYeD0&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb)


### Thiết lập luồng khí cục bộ

* Thiết lập luồng khí bằng Docker-Compose
* [Video](https://www.youtube.com/watch?v=lqDMzReAtrw&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb)
* Thông tin thêm trong [thư mục luồng khí](airflow)

Nếu bạn muốn chạy phiên bản Airflow nhẹ hơn với ít dịch vụ hơn, hãy xem [video](https://www.youtube.com/watch?v=A1p5LQ0zzaQ&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb) này. Đó là tùy chọn.


### Nhập dữ liệu vào GCP bằng Airflow

* Trích xuất: Tải xuống và giải nén dữ liệu
* Xử lý trước: Chuyển đổi dữ liệu thô này sang parquet
* Tải các tệp parquet lên GCS
* Tạo bảng bên ngoài trong BigQuery
* [Video](https://www.youtube.com/watch?v=9ksX9REfL8w&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=19)

### Nhập dữ liệu vào Postgres cục bộ bằng Airflow

* Chuyển đổi tập lệnh nhập để tải dữ liệu sang Postgres thành Airflow DAG
* [Video](https://www.youtube.com/watch?v=s2U8MWJH5xA&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb)


### Dịch vụ chuyển (AWS -> GCP)

Di chuyển tệp từ AWS sang GCP.

Bạn sẽ cần một tài khoản AWS cho việc này. Phần này là tùy chọn

* [Video 1](https://www.youtube.com/watch?v=rFOFTfD1uGk&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb)
* [Video 2](https://www.youtube.com/watch?v=VhmmbqpIzeI&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb)


### Bài tập về nhà

Trong bài tập về nhà, bạn sẽ tạo một số DAG để xử lý dữ liệu NY Taxi cho năm 2019-2021

Thông tin thêm [tại đây](homework.md)


## Ghi chú cộng đồng

Bạn đã ghi chép chưa? Bạn có thể chia sẻ chúng ở đây.

* [Ghi chú từ Alvaro Navas](https://github.com/ziritrion/dataeng-zoomcamp/blob/main/notes/2_data_ingestion.md)
* [Ghi chú từ Aaron Wright](https://github.com/ABZ-Aaron/DataEngineerZoomCamp/blob/master/week_2_data_ingestion/README.md)
* [Ghi chú từ Abd](https://itnadigital.notion.site/Week-2-Data-Ingestion-ec2d0d36c0664bc4b8be6a554b2765fd)
* [Bài đăng trên blog của Isaac Kargar](https://kargarisaac.github.io/blog/data%20engineering/jupyter/2022/01/25/data-engineering-w2.html)
* [Blog, ghi chú, hướng dẫn của Sandy Behrens](https://learningdataengineering540969211.wordpress.com/2022/01/30/week-2-de-zoomcamp-2-3-2-ingesting-data-to-gcp-with-airflow/)
* [Ghi chú từ Apurva Hegde](https://github.com/apuhegde/Airflow-LocalExecutor-In-Docker#readme)
* [Ghi chú từ Vincenzo Galante](https://binchentso.notion.site/Data-Talks-Club-Data-Engineering-Zoomcamp-8699af8e7ff94ec49e6f9bdec8eb69fd)
* Thêm ghi chú của bạn vào đây (phía trên dòng này)
