# Ví dụ PubSub cơ bản với Redpanda

Mục đích của mô-đun này là nắm bắt tốt nền tảng của các khái niệm Kafka/Redpanda này, để có thể gửi dự án capstone bằng cách sử dụng tính năng phát trực tuyến:
- cụm
- nhà môi giới
- chủ đề
- nhà sản xuất
- người tiêu dùng và nhóm người tiêu dùng
- tuần tự hóa dữ liệu và khử lưu huỳnh
- sao chép và lưu giữ
- bù đắp

## 1. Điều kiện tiên quyết

Nếu bạn đã theo dõi video [module-07](../../../README.md), có thể bạn đã cài đặt thư viện `kafka-python`, vì vậy, bạn có thể chuyển sang phần [Docker](#2-docker).

Nếu chưa thì đây là gói duy nhất bạn cần cài đặt trong môi trường ảo của mình cho bài học Redpanda này.

1. kích hoạt môi trường của bạn
2. `pip install kafka-python`

## 2. Docker

Bắt đầu một cụm Redpanda. Redpanda là một hình ảnh nhị phân duy nhất, vì vậy rất dễ dàng để bắt đầu học các khái niệm kafka với Redpanda.

```bash
cd 07-streaming/extras/python/redpanda_example/
docker-compose up -d
```

## 3. Đặt bí danh RPK

Redpanda có lệnh console `rpk`, có nghĩa là `Redpanda keeper`, công cụ CLI đi kèm với Redpanda và đã có sẵn trong hình ảnh Docker.

Đặt bí danh `rpk` sau để chúng tôi có thể sử dụng nó từ thiết bị đầu cuối của mình mà không cần phải mở thiết bị đầu cuối tương tác Docker. Chúng tôi có thể sử dụng bí danh `rpk` này trực tiếp trong thiết bị đầu cuối của mình.

```bash
alias rpk="docker exec -ti redpanda-1 rpk"
rpk version
```

Tại thời điểm này, phiên bản được hiển thị là `v23.2.26 (rev 328d83a06e)`. Phiên bản quan trọng là phiên bản chính `v23` tuân theo ngữ nghĩa phiên bản `major.minor[.build[.revision]]`, để đảm bảo rằng bạn nhận được kết quả tương tự như bất kỳ kết quả nào được chia sẻ trong tài liệu này.

> [!TIP]
> Nếu bạn đọc nội dung này sau tháng 3 năm 2024 và muốn cập nhật tệp Docker để sử dụng hình ảnh Redpanda mới nhất, chỉ cần truy cập [Docker hub](https://hub.docker.com/r/vectorized/redpanda/tags) và dán số phiên bản mới.


## 4. Nhà sản xuất Kafka - Ví dụ người tiêu dùng

Để chạy các ví dụ về nhà sản xuất-người tiêu dùng, hãy mở 2 thiết bị đầu cuối shell trong 2 tab cạnh nhau và chạy các lệnh sau. Đảm bảo kích hoạt môi trường ảo của bạn trong mỗi thiết bị đầu cuối.

```bash
# Start consumer script, in 1st terminal tab
python -m consumer.py
# Start producer script, in 2nd terminal tab
python -m producer.py
```

Chạy lại lệnh `python -m producer.py` để quan sát rằng tab nhân viên `consumer` sẽ tự động sử dụng các tin nhắn trong thời gian thực khi xảy ra `events` mới

##5. Giao diện người dùng Redpanda

Bạn cũng có thể xem cluster, topic và thông tin khác trên Redpanda Console qua trình duyệt tại [http://localhost:8080](http://localhost:8080)


## 6. Bảng thuật ngữ lệnh rpk

Hãy truy cập [bài đăng trên blog get-started-rpk](https://redpanda.com/blog/get-started-rpk-manage-streaming-data-clusters) để biết thêm.

```bash
# set alias for rpk
alias rpk="docker exec -ti redpanda-1 rpk"

# get info on cluster
rpk cluster info

# create topic_name with m partitions and n replication factor
rpk topic create [topic_name] --partitions m --replicas n

# get list of available topics, without extra details and with details
rpk topic list
rpk topic list --detailed

# inspect topic config
rpk topic describe [topic_name]

# consume [topic_name]
rpk topic consume [topic_name]

# list the consumer groups in a Redpanda cluster
rpk group list

# get additional information about a consumer group, from above listed result
rpk group describe my-group
```

## 7. Tài nguyên bổ sung

Đại học Redpanda (cần có tài khoản Redpanda và miễn phí đăng ký và tham gia (các) khóa học)
- [RP101: Bắt đầu với Redpanda](https://university.redpanda.com/courses/hands-on-redpanda-getting-started)
- [RP102: Xử lý luồng với Redpanda](https://university.redpanda.com/courses/take/hands-on-redpanda-stream-processing/lessons/37830192-intro)
- [SF101: Nguyên tắc cơ bản về phát trực tuyến](https://university.redpanda.com/courses/streaming-fundamentals)
- [SF102: Khối xây dựng Kafka](https://university.redpanda.com/courses/kafka-building-blocks)

Nếu bạn cảm thấy rằng mình đã có nền tảng cơ bản tốt về Truyền phát và Kafka, vui lòng bỏ qua các khóa học bổ sung này.

