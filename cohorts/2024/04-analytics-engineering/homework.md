## Bài tập về nhà của Mô-đun 4 

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

**Điều gì xảy ra khi chúng tôi thực thi dbt build --vars '{'is_test_run':'true'}'**
Bạn cần phải hoàn thành ["Xây dựng các mô hình dbt đầu tiên"](https://www.youtube.com/watch?v=UVI30Vxzd6c) video. 
- Nó giống như chạy *bản dựng dbt*
- Nó áp dụng _limit 100_ cho tất cả các mô hình của chúng tôi
- Nó chỉ áp dụng _limit 100_ cho các mô hình dàn dựng của chúng tôi
- Không có gì

### Câu hỏi 2: 

**Mã mà công việc CI của chúng tôi sẽ chạy là gì? Mã này đến từ đâu?**  

- Mã đã được hợp nhất vào nhánh chính
- Mã đằng sau đối tượng tạo trên lược đồ dbt_cloud_pr_
- Mã từ bất kỳ nhánh phát triển nào đã được mở dựa trên nhánh chính
- Mã từ nhánh phát triển mà chúng tôi đang yêu cầu hợp nhất vào chính


### Câu hỏi 3 (2 điểm)

**Số lượng bản ghi trong mô hình là bao nhiêu fact_fhv_trips sau khi chạy tất cả các phần phụ thuộc với biến chạy thử nghiệm bị vô hiệu hóa (:false)?**  
Tạo mô hình phân tầng cho dữ liệu fhv, tương tự như mô hình được tạo cho dữ liệu màu vàng và xanh lục. Thêm bộ lọc bổ sung để chỉ giữ lại các bản ghi có thời gian lấy hàng trong năm 2019. Không thêm bước loại bỏ trùng lặp. Chạy mô hình này không giới hạn (is_test_run: false).

Tạo mô hình cốt lõi tương tự như các chuyến đi thực tế, nhưng chọn từ stg_fhv_tripdata và tham gia với dim_zones.
Tương tự như những gì chúng tôi đã thực hiện trong fact_trips, chỉ lưu giữ các bản ghi có các mục nhập địa điểm đón và trả khách đã biết cho các địa điểm đón và trả khách. 
Chạy mô hình dbt không giới hạn (is_test_run: false).

- 12998722
- 22998722
- 32998722
- 42998722

### Câu hỏi 4 (2 điểm)

**Dịch vụ nào có nhiều chuyến đi nhất trong tháng 7 năm 2019 với số lượng chuyến đi lớn nhất sau khi tạo ô cho bảng fact_fhv_trips và ô fact_trips như trong video?**

Tạo trang tổng quan với một số ô mà bạn thấy thú vị để khám phá dữ liệu. Một ô sẽ hiển thị số lượng chuyến đi mỗi tháng, như được thực hiện trong video về fact_trips, bao gồm cả dữ liệu fact_fhv_trips.

- FHV
- Xanh
- Vàng
- FHV và Xanh


## Nộp giải pháp

* Mẫu nộp hồ sơ: https://courses.datatalks.club/de-zoomcamp-2024/homework/hw4

Hạn chót: 22 tháng 2 (Thứ Năm), 22:00 CET


## Giải pháp (Sẽ được xuất bản sau thời hạn)

* Video: https://youtu.be/3OPggh5Rca8
* Trả lời:
  * Câu hỏi 1: Nó chỉ áp dụng _limit 100_ cho các mô hình dàn dựng của chúng tôi
  * Câu hỏi 2: Mã từ nhánh phát triển mà chúng tôi đang yêu cầu hợp nhất thành chính
  * Câu hỏi 3: 22998722
  * Câu 4: Màu vàng
