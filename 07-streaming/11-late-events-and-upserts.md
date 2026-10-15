---
prev_url: 10-aggregation-with-tumbling-windows.md
next_url: 12-understanding-window-types.md
---
# Sự kiện muộn và nâng cao

Nhà sản xuất CSV gửi các sự kiện theo thứ tự, do đó hình mờ không bao giờ phải để
xử lý những sự kiện đến muộn. Hãy sử dụng trình tạo thời gian thực tạo ra các sự kiện tổng hợp
thỉnh thoảng có độ trễ để xem điều gì sẽ xảy ra.


*Việc cập nhật khóa chính cho phép một sự kiện muộn sửa chữa tổng hợp đã xuất bản tại chỗ.*

Tải xuống và chạy trình tạo thời gian thực:

```bash
PREFIX="https://raw.githubusercontent.com/DataTalksClub/data-engineering-zoomcamp/main/07-streaming/workshop"
wget ${PREFIX}/src/producers/producer_realtime.py -P src/producers/
```

```bash
uv run python src/producers/producer_realtime.py
```

Nó tạo ra các chuyến đi taxi ngẫu nhiên với dấu thời gian hiện tại, nhưng ~20% sự kiện
được gửi với dấu thời gian cách đây 3-10 giây (mô phỏng độ trễ của mạng
). Nhãn đầu ra cho mỗi sự kiện:

```
  on time   -> PU=79 ts=14:23:05
  on time   -> PU=107 ts=14:23:05
  LATE (8s) -> PU=234 ts=14:22:58
  on time   -> PU=48 ts=14:23:06
```

Với hình mờ 5 giây và khoảng thời gian 1 giờ của chúng tôi, sẽ không có sự kiện nào bị bỏ qua -
ngay cả một sự kiện trễ 10 giây cũng sẽ diễn ra trong khoảng thời gian hiện tại.
Nhưng hành vi hình mờ + upsert vẫn hiển thị: Flink đầu tiên phát ra kết quả cửa sổ
khi hình mờ vượt qua cuối cửa sổ, sau đó các sự kiện muộn
cập nhật các kết quả đó thông qua KHÓA CHÍNH.

Để thấy điều này hoạt động, hãy mở hai thiết bị đầu cuối:

Nhà ga 1 - chạy nhà sản xuất thời gian thực:

```bash
uv run python src/producers/producer_realtime.py
```

Nhà ga 2 - thay đổi số lượng tổng hợp đồng hồ:

```bash
watch -n 1 'PGPASSWORD=postgres docker compose exec postgres psql -U postgres -d postgres -c "SELECT window_start, sum(num_trips) as trips, round(sum(total_revenue)::numeric, 2) as revenue FROM processed_events_aggregated GROUP BY window_start ORDER BY window_start;"'
```

Bạn sẽ thấy số lượng cửa sổ cũ tăng lên khi các sự kiện muộn đến
và cập nhật tổng hợp thông qua upsert. Đây là lý do tại sao chúng tôi thiết lập KHÓA CHÍNH
- nếu không có khóa này, các sự kiện muộn sẽ bị loại bỏ hoặc tạo ra các bản sao.
