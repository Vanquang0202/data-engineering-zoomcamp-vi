---
video_url: https://www.youtube.com/watch?v=-CqXf7vhhDs
prev_url: 01-data-warehouse-and-bigquery.md
next_url: 03-bigquery-best-practices.md
---
# Phân vùng và phân cụm

Trong [bài học trước](01-data-warehouse-and-bigquery.md), chúng ta đã tạo các phiên bản
được phân vùng và phân cụm của bảng dữ liệu taxi màu vàng và thấy
kết quả là các truy vấn của chúng tôi đã quét ít dữ liệu hơn bao nhiêu. Phần này sẽ đi sâu vào chi tiết về
: các tùy chọn phân vùng mà BigQuery cung cấp cho bạn, cách phân cụm
sắp xếp dữ liệu của bạn và cách quyết định nên sử dụng cái nào trong hai tùy chọn đó.

## Tùy chọn phân vùng

Khi tạo bảng được phân vùng trong BigQuery, bạn chọn bảng
được phân vùng theo gì. Có ba lựa chọn:

- Cột đơn vị thời gian: cột có dấu thời gian hoặc ngày tháng, giống như thời gian đón
của một chuyến đi taxi.
- Thời gian nhập: BigQuery gán mỗi hàng cho một phân vùng dựa trên
khi nó được chèn, sử dụng cột giả có tên `_PARTITIONTIME`.
- Phạm vi số nguyên: một cột số nguyên được chia thành các phạm vi.

Với cột đơn vị thời gian hoặc thời gian nhập, bạn cũng có thể chọn mức độ chi tiết của
: hàng ngày (mặc định), hàng giờ hoặc hàng tháng và hàng năm.

Hàng ngày là một cách tốt để bắt đầu. Nó hoạt động tốt khi dữ liệu có kích thước trung bình
và trải đều trong các ngày.

Hàng giờ dành cho một lượng lớn dữ liệu được đưa vào khi bạn muốn xử lý
theo giờ. Hãy theo dõi số lượng phân vùng mà thao tác này tạo ra:
BigQuery cho phép tối đa 4000 phân vùng trên mỗi bảng. Với các phân vùng
hàng giờ, bạn có thể cần một chiến lược hết hạn để loại bỏ các phân vùng
cũ.

Hàng tháng hoặc hàng năm dành cho trường hợp ngược lại: một lượng nhỏ dữ liệu
trải rộng trên nhiều ngày.

## Cách phân cụm hoạt động

Khi bạn phân cụm một bảng, các cột bạn chỉ định sẽ được sử dụng để sắp xếp dữ liệu liên quan đến
- các hàng có giá trị tương tự sẽ được lưu trữ cùng nhau.

Thứ tự của các cột rất quan trọng vì nó xác định thứ tự sắp xếp
của dữ liệu. Nếu bạn phân cụm trên các cột a, b và c thì bảng
được sắp xếp trước tiên theo a, sau đó theo b, sau đó theo c.

Phân cụm cải thiện bộ lọc và truy vấn tổng hợp, đặc biệt khi bạn
lọc hoặc tổng hợp trên các cột mà bạn đã phân cụm theo đó.

Tuy nhiên, việc phân vùng và phân cụm không miễn phí. Nếu bảng của bạn có kích thước
nhỏ - dưới 1 GB - thì cũng không có sự cải thiện đáng kể nào về hiệu suất truy vấn
. Chúng thực sự làm tăng thêm chi phí: các bảng
được phân vùng và phân cụm phải chịu việc đọc siêu dữ liệu và bảo trì siêu dữ liệu. Đối với một bảng nhỏ
, sẽ hợp lý hơn nếu không có phân vùng hoặc phân cụm nào cả.

Bạn có thể chỉ định tối đa bốn cột phân cụm. Chúng phải là các cột
cấp cao nhất, không lặp lại và bạn có thể chọn từ các loại sau: DATE,
BOOLEAN, GEOGRAPHY, INT64, NUMERIC, STRING và DATETIME.

## Lựa chọn giữa phân vùng và phân cụm

Đôi khi bạn muốn cái này, đôi khi bạn muốn cái kia, đôi khi cả hai. Việc lựa chọn
dựa trên một số tiêu chí.

Trị giá. Với việc phân vùng, lợi ích chi phí được biết trước: một truy vấn
lọc trên cột phân vùng chỉ đọc một số phân vùng.
Với phân cụm, lợi ích sẽ không được xác định cho đến khi bạn chạy truy vấn.
này quan trọng vì BigQuery cho phép bạn chỉ định chi phí tối đa cho một truy vấn:
nếu vượt quá số tiền đó thì BigQuery sẽ không thực thi chi phí đó.
Bạn chỉ có thể làm điều đó khi biết trước chi phí, nghĩa là phân vùng
.

Độ chi tiết. Sử dụng phân cụm khi bạn cần mức độ chi tiết cao hơn mức phân vùng
có thể cung cấp.

Sự quản lý. Việc phân vùng cung cấp cho bạn khả năng quản lý cấp độ phân vùng: bạn có thể
xóa các phân vùng hoặc di chuyển các phân vùng giữa các kho lưu trữ. Việc phân cụm
không mang lại cho bạn điều gì trong số đó.

Cột. Với tính năng phân cụm, bạn thường lọc hoặc tổng hợp dữ liệu
của mình trên nhiều cột. Phân vùng chỉ hoạt động trên một cột duy nhất,
vì chỉ có thể phân vùng trên một cột.

Hồng y. Sử dụng phân cụm khi số lượng giá trị riêng biệt trong cột hoặc nhóm cột
lớn. Số lượng phần tử đó là trở ngại cho
đối với việc phân vùng do giới hạn 4000 phân vùng.

## Khi phân cụm nhịp phân vùng

Đặt các tiêu chí lại với nhau, đây là những tình huống mà
nên chọn phân cụm thay vì phân vùng:

- Việc phân vùng sẽ để lại một lượng nhỏ dữ liệu trên mỗi phân vùng -
khoảng dưới 1 GB.
- Việc phân vùng sẽ tạo ra nhiều phân vùng hơn giới hạn 4000 trên mỗi bảng
.
- Các hoạt động đột biến của bạn sẽ thường xuyên sửa đổi phần lớn các phân vùng
- ví dụ: ghi vào bảng vài phút một lần.

## Tự động phân cụm lại

Khi dữ liệu được thêm vào bảng được nhóm, các hàng mới được chèn là
được ghi thành các khối có phạm vi khóa có thể chồng lên phạm vi khóa được lưu trữ
trong các khối trước đó. Các khóa chồng chéo này làm suy yếu thuộc tính sắp xếp của bảng
và các truy vấn sẽ chậm hơn.

Để duy trì các đặc tính hiệu suất của một bảng được phân cụm,
BigQuery thực hiện tái phân cụm tự động ở chế độ nền: nó khôi phục thuộc tính sắp xếp của
mà bạn không cần phải làm gì cả. Đối với các bảng được phân vùng
, việc phân cụm được duy trì trong phạm vi của từng phân vùng
.

Việc phân cụm lại không ảnh hưởng đến hiệu suất truy vấn và bạn không phải trả bất kỳ chi phí nào cho
- BigQuery sẽ đảm nhiệm việc đó.

## Tóm tắt

Trong phần này, chúng ta đã thấy các tùy chọn phân vùng mà BigQuery cung cấp, cách phân cụm
định vị và sắp xếp dữ liệu, các tiêu chí để
lựa chọn giữa phân vùng và phân cụm cũng như cách BigQuery
tự động phân cụm lại.

Một bài tập hay: hãy nghĩ về tập dữ liệu taxi màu vàng từ đơn vị
trước đó. Bạn sẽ phân vùng nó theo cột nào và bạn sẽ phân cụm
vào cột nào? Hãy suy nghĩ về các truy vấn bạn muốn chạy - đó là lựa chọn của
.

## Vật liệu

- [`big_query.sql`](big_query.sql) — phân vùng và phân cụm một nửa của tệp
: tạo các bảng được phân vùng và phân vùng cộng với cụm từ bảng bên ngoài
, kiểm tra `INFORMATION_SCHEMA.PARTITIONS` và các truy vấn
được ghép nối cho biết mỗi biến thể quét bao nhiêu dữ liệu.
