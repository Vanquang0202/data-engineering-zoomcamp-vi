---
prev_url: 08-the-pass-through-flink-job.md
next_url: 10-aggregation-with-tumbling-windows.md
---
# Mức chênh lệch - sớm nhất so với
mới nhất
Khi Flink kết nối với Kafka, nó cần biết bắt đầu đọc từ đâu.
này là cài đặt `scan.startup.mode`:


*Vị trí bắt đầu kiểm soát xem công việc mới có phát lại lịch sử, chờ sự kiện mới hay bắt đầu từ một điểm đã chọn trong nhật ký hay không.*

| Chế độ | Hành vi |
|---|---|
| `latest-offset` | Chỉ đọc tin nhắn đến sau khi công việc bắt đầu |
| `earliest-offset` | Đọc mọi thứ từ đầu chủ đề |
| `timestamp` | Bắt đầu từ một thời điểm cụ thể |

`earliest` thường được sử dụng để chèn lấp hoặc khôi phục dữ liệu - bạn là
đang sử dụng Flink để xử lý dữ liệu đã tồn tại trong Kafka một thời gian chứ không phải dữ liệu thời gian thực
. `latest` là cài đặt sản xuất phổ biến hơn - công việc
khởi động và chỉ xử lý các sự kiện mới khi mọi người nhấp vào nút trên trang web
của bạn hoặc bất kỳ nguồn cấp dữ liệu sự kiện nào bạn đang sử dụng.

Công việc chuyển tiếp của chúng tôi sử dụng `latest-offset`. Hãy xem điều gì xảy ra với
`earliest-offset`:

1. Hủy công việc đang chạy từ Flink UI (nhấp vào công việc, sau đó Hủy)
2. Xóa bảng:
   ```sql
   TRUNCATE processed_events;
   ```
3. Chỉnh sửa `src/job/pass_through_job.py` - thay đổi cả hai cài đặt bù:
   ```
   'scan.startup.mode' = 'earliest-offset',
   'properties.auto.offset.reset' = 'earliest',
   ```
4. Gửi lại:
   ```bash
   docker compose exec jobmanager ./bin/flink run \
       -py /opt/src/job/pass_through_job.py \
       --pyFiles /opt/src -d
   ```
5. Đợi 15 giây rồi kiểm tra:
   ```sql
   SELECT count(*) FROM processed_events;
   ```

Flink đọc tất cả tin nhắn từ chủ đề - bao gồm dữ liệu từ các lần chạy
của nhà sản xuất trước đó. Nếu bạn đã chạy trình sản xuất hai lần trước đó, bạn sẽ thấy ~ 2000 hàng (trùng lặp
của mọi thứ đã được xử lý).

Tại sao trùng lặp? Điểm kiểm tra được xác định trong phạm vi một trường hợp công việc cụ thể. Khi bạn hủy
và gửi lại, đó là một công việc hoàn toàn mới và không biết gì về các điểm kiểm tra
trước đó. Với `earliest-offset`, mọi chuyện sẽ bắt đầu lại từ đầu. Cài đặt
bù đắp chỉ quan trọng khi khởi động - khi công việc đang chạy, điểm kiểm tra
sẽ tiếp quản và theo dõi tiến trình. Nhưng nếu bạn hủy công việc và tạo một công việc
mới thì các điểm kiểm tra đó sẽ biến mất.

Có tùy chọn thứ ba - chế độ `timestamp`. Nếu công việc của bạn
vẫn chạy tốt cho đến 2 giờ chiều và sau đó gặp sự cố, thì bạn có thể khởi động lại công việc đó từ đúng 2 giờ chiều.
Điều này rất hữu ích để khôi phục sau lỗi mà không cần xử lý lại mọi thứ
từ đầu hoặc thiếu dữ liệu đến khi công việc không hoạt động.

Một mẫu sản xuất phổ biến (kiến trúc Lambda): chạy tác vụ phát trực tuyến của bạn với
`latest-offset` để có kết quả theo thời gian thực và nếu nó gặp sự cố, hãy sử dụng tác vụ hàng loạt
riêng biệt để lấp đầy khoảng trống. Bằng cách này, công việc phát trực tuyến luôn nhanh chóng và
của bạn không bị mất dữ liệu.

> Thay đổi giá trị bù về `latest-offset` khi bạn thử nghiệm xong.
