##Bài tập tuần 2

Trong bài tập về nhà này, chúng ta sẽ chuẩn bị dữ liệu cho tuần tiếp theo. Chúng tôi sẽ cần
để đưa các bộ dữ liệu này vào hồ dữ liệu của chúng tôi:

* Đối với các bài học, chúng ta sẽ cần tập dữ liệu Xe taxi màu vàng (năm 2019 và 2020)
* Đối với bài tập về nhà, chúng ta sẽ cần Dữ liệu FHV (chỉ dành cho xe cho thuê trong năm 2019)

Bạn có thể tìm thấy tất cả các URL trên [trang tập dữ liệu](https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page)


Trong bài tập về nhà này, chúng ta sẽ:

* Sửa đổi DAG mà chúng ta đã tạo trong bài học để truyền dữ liệu taxi màu vàng
* Tạo một dag mới để truyền dữ liệu FHV
* Tạo một dag khác cho dữ liệu Vùng


Nếu không có quyền truy cập vào GCP, bạn có thể thực hiện việc đó cục bộ và nhập dữ liệu vào Postgres
. Nếu bạn có quyền truy cập vào GCP, bạn không cần phải làm điều đó đối với Postgres cục bộ -
chỉ khi bạn muốn.

Cũng lưu ý rằng đối với bài tập về nhà này, chúng ta không cần bước cuối cùng - tạo bảng trong GCP.
Sau khi đặt tất cả các tệp vào datalake, chúng ta sẽ tạo các bảng trong Tuần 3.



## Câu 1: Ngày bắt đầu lấy dữ liệu taxi màu vàng (1 điểm)

Bạn sẽ cần tham số hóa DAG để xử lý dữ liệu taxi màu vàng mà
mà chúng tôi đã tạo trong video.

Ngày bắt đầu cho công việc này là ngày nào?

* 2019-01-01
* 2020-01-01
* 2021-01-01
* ngày_ago(1)


## Câu 2: Tần suất dữ liệu taxi màu vàng (1 điểm)

Chúng ta cần chạy DAG này bao lâu một lần?

*
hàng ngày *
hàng tháng *
hàng năm * Một lần


## Chạy lại DAG cho những ngày trước đây

Để thực thi DAG của bạn cho những ngày trong quá khứ, hãy thử điều này:

* Trước tiên, hãy xóa DAG của bạn khỏi giao diện web (biểu tượng thùng rác)
* Đặt tham số `catchup` thành `True`
* Hãy cẩn thận khi chạy nhiều công việc song song - hệ thống của bạn có thể không thích nó. Không đặt nó cao hơn 3: `max_active_runs=3`
* Đổi tên DAG thành `data_ingestion_gcs_dag_v02`
* Thực thi nó từ GUI Airflow (nút phát)


Ngoài ra, không có dữ liệu nào trong những tháng gần đây nhưng `curl` sẽ thoát thành công.
Để khắc phục lỗi 404, hãy thêm cờ `-f`:

```bash
curl -sSLf { URL } > { LOCAL_PATH }
```

Khi bạn chạy lệnh này cho tất cả dữ liệu, các tệp tạm thời sẽ được lưu trong Docker và sẽ tiêu tốn dung lượng ổ đĩa
của bạn. Nếu nó gây ra sự cố cho bạn, hãy thêm một bước khác vào DAG để dọn dẹp mọi thứ.
Nó có thể là toán tử bash chạy lệnh này:

```bash
rm name-of-csv-file.csv name-of-parquet-file.parquet
```


## Câu 3: DAG cho dữ liệu FHV (2 điểm)

Bây giờ hãy tạo một DAG khác - để tải lên dữ liệu FHV.

Chúng tôi sẽ cần ba bước:

* Tải xuống dữ liệu
* Parquetize nó
* Tải lên GCS

Nếu bạn không có tài khoản GCP, để nhập cục bộ, bạn sẽ cần hai bước:

* Tải xuống dữ liệu
* Nhập vào Postgres

Sử dụng cùng tần suất và ngày bắt đầu như đối với tập dữ liệu taxi màu vàng

Câu hỏi: Có bao nhiêu lần chạy DAG có màu xanh cho dữ liệu trong năm 2019 sau khi hoàn thành mọi thứ?

Lưu ý: khi xử lý dữ liệu cho năm 2020-01, bạn có thể gặp lỗi.
có toàn quyền quyết định xem phải làm gì với nó - đối với bài tập về nhà Tuần 3, chúng tôi sẽ không cần dữ liệu năm 2020.


## Câu 4: DAG cho các Zone (2 điểm)


Tạo DAG cuối cùng - cho các Vùng:

* Tải xuống
* Parquetize
* Tải lên GCS

(Hoặc hai bước để nhập cục bộ: tải xuống -> nhập vào postgres)

Bao lâu thì nó cần phải chạy?

*
hàng ngày *
hàng tháng *
hàng năm * Một lần


## Đệ trình giải pháp

* Hình thức gửi: https://forms.gle/ViWS8pDf2tZD4zSu5
* Bạn có thể gửi bài tập về nhà nhiều lần. Trong trường hợp này, chỉ lần gửi cuối cùng sẽ được sử dụng.

Hạn chót: 17:00 CET ngày 7 tháng 2
