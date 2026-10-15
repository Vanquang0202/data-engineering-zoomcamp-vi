## Bài tập về nhà Tuần 4 

Trong bài tập về nhà này, chúng ta sẽ sử dụng các mô hình được phát triển trong video Tuần 4 và nâng cao dự án dbt đã được trình bày bằng cách sử dụng dữ liệu Taxi đã tải sẵn cho xe fhv trong năm 2019 trong DWH của chúng tôi.

Điều này có nghĩa là trong bài tập về nhà này, chúng tôi sử dụng dữ liệu sau [Danh sách bộ dữ liệu](https://github.com/DataTalksClub/nyc-tlc-data/)
* Dữ liệu taxi màu vàng - Năm 2019 và 2020
* Dữ liệu taxi xanh - Năm 2019 và 2020 
* Dữ liệu fhv - Năm 2019. 

Chúng tôi sẽ sử dụng dữ liệu được tải cho:

* Xây dựng bảng nguồn: `stg_fhv_tripdata`
* Xây dựng bảng dữ kiện: `fact_fhv_trips`
* Tạo trang tổng quan 

Nếu không có quyền truy cập vào GCP, bạn có thể thực hiện việc này cục bộ bằng cách sử dụng dữ liệu đã nhập từ cơ sở dữ liệu Postgres của mình. Nếu bạn có quyền truy cập vào GCP, bạn không cần phải làm điều đó đối với Postgres cục bộ - chỉ khi bạn muốn.

> **Lưu ý**: nếu câu trả lời của bạn không khớp chính xác, hãy chọn tùy chọn gần nhất 

### Câu hỏi 1: 

**Số lượng bản ghi trong mô hình fact_trips sau khi chạy tất cả các mô hình với biến chạy thử nghiệm bị vô hiệu hóa và chỉ lọc dữ liệu năm 2019 và 2020 (ngày nhận hàng)?** 

Bạn cần phải hoàn thành ["Xây dựng dbt đầu tiên models"](https://www.youtube.com/watch?v=UVI30Vxzd6c) video và có thể chạy các mô hình thông qua CLI. 
Bạn nên tìm các chế độ xem và mô hình để truy vấn trong DWH của mình.

- 41648442
- 51648442
- 61648442
- 71648442


### Câu hỏi 2: 

**Sự phân bổ giữa dữ liệu lọc loại dịch vụ theo năm 2019 và 2020 như được thực hiện trong video là gì?**

Bạn sẽ cần phải hoàn thành các video "Trực quan hóa dữ liệu" bằng cách sử dụng [google data studio](https://www.youtube.com/watch?v=39nLTs74A3E) hoặc [metabase](https://www.youtube.com/watch?v=BnLkrA7a6gM). 

- 89.9/10.1
- 94/6
- 76.3/23.7
- 99.1/0.9



### Câu hỏi 3: 

**Số lượng bản ghi trong mô hình stg_fhv_tripdata sau khi chạy tất cả các mô hình có biến chạy thử nghiệm bị vô hiệu hóa (:false)?**  

Tạo mô hình dàn dựng cho dữ liệu fhv cho năm 2019 và không thêm bước loại bỏ trùng lặp. Chạy nó thông qua CLI không giới hạn (is_test_run: false). Lọc các bản ghi với thời gian lấy hàng trong năm 2019.

- 33244696
- 43244696
- 53244696
- 63244696


### Câu hỏi 4: 

**Số lượng bản ghi trong mô hình fact_fhv_trips sau khi chạy tất cả các phần phụ thuộc với biến chạy thử nghiệm bị vô hiệu hóa (:false)?**  

Tạo mô hình cốt lõi cho stg_fhv_tripdata kết hợp với dim_zones.
Tương tự như những gì chúng tôi đã thực hiện trong fact_trips, chỉ lưu giữ các bản ghi có các mục nhập địa điểm đón và trả khách đã biết cho các địa điểm đón và trả khách. 
Chạy nó thông qua CLI không giới hạn (is_test_run: false) và lọc các bản ghi với thời gian lấy hàng trong năm 2019.

- 12998722
- 22998722
- 32998722
- 42998722

### Câu hỏi 5: 

**Tháng nào có số lượt đi nhiều nhất sau khi xây dựng ô cho bảng fact_fhv_trips?**

Tạo trang tổng quan với một số ô mà bạn thấy thú vị để khám phá dữ liệu. Một ô sẽ hiển thị số lượng chuyến đi mỗi tháng, như được thực hiện trong video về fact_trips, dựa trên bảng fact_fhv_trips.

- Tháng 3
- Tháng 4
- Tháng 1
- Tháng 12



## Gửi lời giải

* Hình thức gửi: https://forms.gle/6A94GPutZJTuT5Y16
* Bạn có thể gửi bài tập về nhà nhiều lần. Trong trường hợp này, chỉ lần gửi cuối cùng sẽ được sử dụng. 

Hạn chót: 25/02 (Thứ Bảy), 22:00 CET


## Giải pháp

* Video: https://www.youtube.com/watch?v=I_K0lNu9WQw&list=PL3MmuxUbc_hJjEePXIdE-LVUx_1ZZjYGW
* Đáp án:
  * Câu 1: 61648442,
  * Câu 2: 89.9/10.1
  * Câu 3: 43244696
  * Câu 4: 22998722
  * Câu 5: Tháng Giêng
