## Bài tập về nhà Tuần 6 

Trong bài tập về nhà này, sẽ có hai phần, phần đầu tiên tập trung vào các câu hỏi lý thuyết liên quan đến khái niệm Kafka 
và streaming và phần thứ hai yêu cầu tạo một ứng dụng streaming nhỏ bằng cách sử dụng ngôn ngữ lập trình 
ưa thích (Python hoặc Java).

### Câu hỏi 1: 

**Hãy chọn các câu đúng**

- Nút Kafka chịu trách nhiệm lưu trữ các chủ đề [x]
- Zookeeper bị xóa khỏi cụm Kafka bắt đầu từ phiên bản 4.0 [x]
- Cấu hình lưu giữ đảm bảo các tin nhắn không bị mất trong một khoảng thời gian cụ thể. [x]
- Group-Id đảm bảo thông điệp được phân phối đến những người tiêu dùng được liên kết [x]


### Câu hỏi 2: 

**Vui lòng chọn các khái niệm Kafka hỗ trợ độ tin cậy và tính sẵn có**

- Sao chép chủ đề [x]
- Phân chia chủ đề
- Id nhóm người tiêu dùng
- Ack All [x]



### Câu hỏi 3: 

**Vui lòng chọn Các khái niệm Kafka hỗ trợ mở rộng quy mô**  

- Sao chép chủ đề
- Phân vùng chủ đề [x]
- Id nhóm người tiêu dùng [x]
- Ack All


### Câu hỏi 4: 

** Vui lòng chọn các thuộc tính phù hợp cho khóa partitioning. 
Xem xét số lượng của trường bạn đã chọn và mở rộng các khía cạnh của ứng dụng của bạn**  

- payment_type [x]
- vendor_id [x]
- passenger_count
- total_amount
- tpep_pickup_datetime
- tpep_dropoff_datetime


### Câu hỏi 5: 

**Cấu hình nào dưới đây nên được cung cấp cho Kafka Consumer nhưng không cần thiết cho Kafka Nhà sản xuất**

- Cấu hình Deserializer [x]
- Đăng ký chủ đề [x]
- Máy chủ Bootstrap 
- Group-Id [x]
- Offset [x]
- Khóa cụm và Bí mật cụm


### Câu hỏi 6:

Vui lòng triển khai ứng dụng streaming để tìm hiểu mức độ phổ biến của PUlocationID trên các bộ dữ liệu chuyến đi xanh và fhv.
Vui lòng sử dụng bộ dữ liệu [fhv_tripdata_2019-01.csv.gz](https://github.com/DataTalksClub/nyc-tlc-data/releases/tag/fhv) 
và [green_tripdata_2019-01.csv.gz](https://github.com/DataTalksClub/nyc-tlc-data/releases/tag/green)

PS: Nếu gặp vấn đề liên quan đến bộ nhớ, bạn có thể sử dụng phần nhỏ hơn của hai bộ dữ liệu này 
không cần thiết phải tìm con số chính xác trong câu hỏi.

Mã của bạn phải bao gồm phần sau
1. Nhà sản xuất đọc tệp csv và xuất bản các chuyến đi trong các chủ đề kafka tương ứng (chẳng hạn như rides_green, rides_fhv)
2. Ứng dụng Pyspark-streaming đọc hai chủ đề kafka
   và viết cả hai chủ đề đó vào chủ đề rides_all và áp dụng các phép tổng hợp để tìm địa điểm đón phổ biến nhất.

   
## Nộp bài giải

* Hình thức nộp bài: https://forms.gle/rK7268U92mHJBpmW7
* Có thể nộp bài tập về nhà nhiều lần. Trong trường hợp này, chỉ lần gửi cuối cùng sẽ được sử dụng. 

Hạn chót: 13 tháng 3 (Thứ Hai), 22:00 CET


## Giải pháp

Chúng tôi sẽ công bố giải pháp tại đây sau thời hạn #

Đối với Câu hỏi 6, hãy đảm bảo, 

1) Tải xuống fhv_tripdata_2019-01.csv và green_tripdata_2019-01.csv trong resources/fhv_tripdata 
và resources/green_tripdata tương ứng. ps: Bạn cần giải nén các tệp nén

2) Cập nhật cài đặt client.properties bằng cách sử dụng cụm và khóa api Confluent Cloud của bạn. 
3) Và tạo các chủ đề (all_rides, fhv_taxi_rides, green_taxi_rides) trong Confluent Cloud UI

4) Chạy Trình sản xuất cho hai tập dữ liệu
```
python3 producer_confluent --type green
python3 producer_confluent --type fhv
```

5) Chạy pyspark streaming
```
./spark-submit.sh streaming_confluent.py
```


