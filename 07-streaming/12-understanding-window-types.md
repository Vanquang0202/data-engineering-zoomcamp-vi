---
prev_url: 11-late-events-and-upserts.md
next_url: 13-cleanup.md
---
# Tìm hiểu các loại cửa sổ

Chúng tôi đã sử dụng cửa sổ lật ở trên. Flink hỗ trợ ba loại:


*Loại cửa sổ xác định xem một sự kiện thuộc về một nhóm cố định, một số nhóm chồng chéo hay một nhóm bị giới hạn bởi trạng thái không hoạt động.*

## Cửa sổ lật
Kích thước cố định, không chồng chéo. Mỗi sự kiện thuộc về chính xác một cửa sổ.
Nếu bạn đến từ thế giới hàng loạt, cửa sổ lộn xộn là quen thuộc nhất -
chúng chỉ cắt dữ liệu của bạn thành các phân đoạn cố định. Về cơ bản, đây là một cách để
tăng tốc độ xử lý hàng loạt.

```
|  Window 1  |  Window 2  |  Window 3  |
|  1 hour    |  1 hour    |  1 hour    |
```

Ca sử dụng: Đếm số chuyến đi mỗi giờ, tóm tắt doanh thu hàng ngày.

## Cửa sổ trượt
Kích thước cố định, chồng lên nhau. Một sự kiện có thể thuộc về nhiều cửa sổ. Khi bạn
nghĩ đến khung thời gian 1 giờ, hầu hết mọi người đều nghĩ đến 00:00-01:00. Nhưng còn có
00:15-01:15, 00:30-01:30 - đó cũng là những khoảng thời gian 1 giờ, chỉ là
bắt đầu ở các điểm khác nhau. Cửa sổ trượt chụp tất cả chúng.

```
|--- Window 1 (1 hour) ---|
      |--- Window 2 (1 hour) ---|
            |--- Window 3 (1 hour) ---|
      <- 15 min slide ->
```

```sql
HOP(TABLE events, DESCRIPTOR(event_timestamp), INTERVAL '15' MINUTE, INTERVAL '1' HOUR)
```

Trường hợp sử dụng: tìm đỉnh và đáy - "lưu lượng truy cập cao nhất của chúng tôi trong bất kỳ khoảng thời gian 1 giờ nào của
là bao nhiêu?" Các cửa sổ chồng chéo này cho phép bạn tìm thấy thời điểm
nơi bạn có giá trị cao nhất hoặc thấp nhất. Tốt cho việc tối đa hóa mức tối thiểu, di chuyển mức trung bình
và phát hiện đột biến (ví dụ: giá tăng đột biến khi chia sẻ chuyến đi).

## Cửa sổ phiên
Cửa sổ động dựa trên khoảng trống không hoạt động. Không giống như cửa sổ
lật và trượt, kích thước cửa sổ không cố định - cửa sổ không đóng vào thời gian được chỉ định của
, nó sẽ đóng sau một khoảng thời gian không hoạt động được chỉ định.

```
|--events--| gap |--events------| gap |--events--|
| Session 1|     |  Session 2   |     | Session 3|
```

Ca sử dụng: nhóm hành vi của người dùng lại với nhau. Hãy tưởng tượng người dùng đăng nhập vào một ứng dụng,
nhấp vào một loạt nút, rời đi trong 2 phút rồi quay lại - về mặt kỹ thuật thì
vẫn là phiên đó. Bạn đặt khoảng cách phiên (giả sử là 30 phút
không hoạt động) và Flink nhóm tất cả các sự kiện trong phiên đó lại với nhau. Phiên bản
rất mạnh mẽ cho phân tích hành vi.
