## Tuần 2: Điều phối quy trình làm việc

Mã Python từ video được liên kết [bên dưới](#code-repository).

Ngoài ra, nếu bạn thấy các lệnh quá nhỏ để xem trong video của Kalise, thì đây là [bản ghi có mã cho video Huynh trưởng thứ hai](https://github.com/discdiver/prefect-zoomcamp/tree/main/flows/01_start) và [video Huynh trưởng thứ năm](https://github.com/discdiver/prefect-zoomcamp/tree/main/flows/03_deployments).

### Hồ dữ liệu (GCS)

* Hồ dữ liệu là gì
* ELT so với ETL
* Các lựa chọn thay thế cho các thành phần (S3/HDFS, Redshift, Snowflake, v.v.)
* [Video](https://www.youtube.com/watch?v=W3Zm6rjOq70&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb)
* [Trang trình bày](https://docs.google.com/presentation/d/1RkH-YhBz2apIjYZAxUz2Uks4Pt51-fVWVN9CcH9ckyY/edit?usp=sharing)


### 1. Giới thiệu về điều phối quy trình công việc

* Điều phối là gì?
* Trình điều phối quy trình làm việc so với các loại trình điều phối khác
* Các tính năng cốt lõi của công cụ điều phối quy trình công việc
* Các loại công cụ điều phối quy trình làm việc khác nhau hiện đang tồn tại 

:movie_camera: [Video](https://www.youtube.com/watch?v=8oLs6pzHp68&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb)


### 2. Giới thiệu về các khái niệm Trưởng nhóm

* Trưởng nhóm là gì?
* Cài đặt Trưởng
* Luồng hoàn hảo
* Tạo ETL
* Nhiệm vụ hoàn hảo
* Khối và bộ sưu tập
* Orion UI

:movie_camera: [Video](https://www.youtube.com/watch?v=cdtN6dhp708&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb)

### 3. ETL với GCP & Prefect

* Luồng 1: Đưa dữ liệu vào Google Cloud Storage 

:movie_camera: [Video](https://www.youtube.com/watch?v=W-rMz_2GwqQ&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb)


### 4. Từ Google Cloud Storage đến Big Query

* Luồng 2: Từ GCS đến BigQuery

:movie_camera: [Video](https://www.youtube.com/watch?v=Cx5jt-V5sgE&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb)

### 5. Tham số hóa quy trình và triển khai 

* Tham số hóa tập lệnh từ quy trình của bạn
* Xác thực tham số bằng Pydantic
* Tạo triển khai cục bộ
* Thiết lập Đại lý hoàn hảo
* Chạy quy trình
* Thông báo

:movie_camera: [Video](https://www.youtube.com/watch?v=QrDxPjX10iw&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb)

### 6. Lên lịch & Lưu trữ Docker với Cơ sở hạ tầng

* Lên lịch triển khai
* Lưu trữ mã luồng
* Chạy các tác vụ trong Docker

:movie_camera: [Video](https://www.youtube.com/watch?v=psNSzqTsi-s&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb)

### 7. Đám mây hoàn hảo và các tài nguyên bổ sung 


* Sử dụng Prefect Cloud thay vì Prefect cục bộ
* Không gian làm việc
* Luồng chạy trên GCP

:movie_camera: [Video](https://www.youtube.com/watch?v=gGC23ZK7lr8&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb)

* [Tài liệu trưởng](https://docs.prefect.io/)
* [Bài giảng hoàn hảo](https://discourse.prefect.io/)
* [Đám mây hoàn hảo](https://app.prefect.cloud/)
* [Tù trưởng](https://prefect-community.slack.com)

### Kho mã

[Mã từ video](https://github.com/discdiver/prefect-zoomcamp) (với một số cải tiến nhỏ)

### bài tập về nhà 
Bài tập về nhà có thể tìm thấy [tại đây](./homework.md).

## Ghi chú cộng đồng

Bạn đã ghi chép chưa? Bạn có thể chia sẻ chúng ở đây.

* [Blog của Marcos Torregrosa (Quận trưởng)](https://www.n4gash.com/2023/data-engineering-zoomcamp-semana-2/)
* [Ghi chú của Victor Padilha](https://github.com/padilha/de-zoomcamp/tree/master/week2)
* [Ghi chú của Alain Boisvert](https://github.com/boisalai/de-zoomcamp-2023/blob/main/week2.md)
* [Ghi chú của Candace Williams](https://github.com/teacherc/de_zoomcamp_candace2023/blob/main/week_2/week2_notes.md)
* [Ghi chú từ Xia He-Bleinagel](https://xiahe-bleinagel.com/2023/02/week-2-data-engineering-zoomcamp-notes-prefect/)
* [Ghi chú từ Froukje](https://github.com/froukje/de-zoomcamp/blob/main/week_2_workflow_orchestration/notes/notes_week_02.md)
* [Ghi chú từ Balaji](https://github.com/Balajirvp/DE-Zoomcamp/blob/main/Week%202/Detailed%20Week%202%20Notes.ipynb)
* Thông tin thêm về [Pandas vs SQL, Khả năng hoàn hảo và kiểm tra dữ liệu của bạn](https://medium.com/@verazabeida/zoomcamp-2023-week-3-7f27bb8c483f), bởi Vera
* Thêm ghi chú của bạn ở đây (phía trên dòng này)
