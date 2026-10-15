# Cách xây dựng workshop hiệu quả

Những nguyên tắc và kinh nghiệm rút ra khi xây dựng workshop Streaming với PyFlink.

## Cấu trúc và nhịp độ

- Giới thiệu từng service thay vì tất cả cùng lúc. Bắt đầu với một container
  (ví dụ Redpanda), giải thích và sử dụng nó, rồi mới thêm PostgreSQL, v.v.
- Bắt đầu bằng cách đơn giản nhất có thể chạy được (Python consumer thuần),
  sau đó chỉ ra hạn chế để người học thấy vì sao cần công cụ phức tạp hơn (Flink).
- Dùng `docker compose up <service> -d` để khởi động từng service trong lúc
  xây dựng từng bước. Chỉ dùng `docker compose up --build -d` khi mọi thứ đã sẵn sàng.

## Dữ liệu

- Dùng dữ liệu thực thay vì dữ liệu thử nghiệm giả lập. Dữ liệu taxi NYC
  (`yellow_tripdata_YYYY-MM.parquet`) là một lựa chọn phù hợp.
- Giới hạn khối lượng ở mức dễ xử lý (ví dụ 1.000 dòng đầu) để workshop diễn ra nhanh.

## Thiết lập dự án

- Giả định người học bắt đầu từ đầu: `uv init -p 3.12` + `uv add <package>`.
- Thêm dependency dần khi nội dung cần đến chúng (ví dụ dùng
  `uv add kafka-python pandas pyarrow` trước, rồi mới dùng `uv add psycopg2-binary`
  khi giới thiệu PostgreSQL).
- Luôn ghi chú dưới dạng blockquote: "Nếu đã clone repository, hãy chạy `uv sync` thay thế".

## Trình bày code

- Chia code block lớn thành nhiều block nhỏ, mỗi block chỉ làm một việc.
  Đừng đưa cả script dài vào cùng một block.
- Với mỗi code block: viết một dòng giới thiệu ngắn về chức năng, trình bày
  code, rồi giải thích cách hoạt động bên dưới. Để người học xem code trước
  khi đọc phần giải thích chi tiết.
- Chỉ import những gì cần dùng trong từng block; đừng giới thiệu mọi import
  ngay từ đầu.
- Giới thiệu function và utility ở nơi chúng được dùng lần đầu. Ví dụ,
  trình bày `dataclasses.asdict()` ở block gọi nó, không phải ở block định nghĩa dataclass.
- Khi giới thiệu function, hãy thử nó với dữ liệu mẫu trước khi dùng trong
  code thực tế. Ví dụ, tạo chuỗi nhị phân thử để kiểm tra deserializer,
  rồi mới đưa nó vào consumer.
- Ưu tiên function có tên thay vì lambda viết tại chỗ: dễ tái sử dụng,
  kiểm thử và giải thích từng bước. Ví dụ dùng `value_deserializer=ride_deserializer`
  thay vì `value_deserializer=lambda m: json.loads(m.decode('utf-8'))`.
- Tách logic lặp lại thành function có tên. Ví dụ, việc chuyển dòng dữ liệu
  thành object xuất hiện nhiều nơi nên đặt trong function `ride_from_row(row)`.
- Tách function một dòng thành nhiều dòng để từng bước (decode, parse,
  tạo object) dễ theo dõi và giải thích.
- Trình bày cách đơn giản trước, rồi mới cải tiến. Ví dụ, dùng `json_serializer`
  chung với lời gọi `dataclasses.asdict()` thủ công, sau đó giới thiệu
  `ride_serializer` chuyên biệt tự xử lý bước chuyển đổi. Hãy để người học
  thấy sự bất tiện trước khi đưa ra cách giải quyết.
- Tách code dùng chung (dataclass, serializer, deserializer, converter) vào
  module chung (ví dụ `models.py`) để nhiều script có thể import cùng một nơi.
- Cuối bài, dẫn đến script hoàn chỉnh (ví dụ: "> Script đầy đủ nằm tại
  `src/producers/producer.py`.").
- Với file hạ tầng dài hoặc phức tạp (Dockerfile, cấu hình YAML), hãy dẫn
  link đến file trên GitHub và tóm tắt ngắn các chức năng của nó. Dùng `wget`
  để tải từ repository thay vì yêu cầu người học gõ lại.
- Nêu rõ người học có thể chạy Python trong Jupyter notebook
  (`uv add jupyter`, `uv run jupyter lab`) thay cho script .py.
  Cách trình bày code theo block nhỏ rất phù hợp với các cell notebook.
- Flink job phải là file .py (được submit vào cluster qua `docker compose exec`).
  Hãy giải thích rõ điểm khác biệt này.

## Định dạng

- Không dùng chữ đậm (`**text**`) trong file README; dùng văn bản thường.
- Không dùng dấu gạch ngang dài; thay bằng dấu gạch ngang có khoảng trắng (` - `).
- Dùng `python`, không dùng `python3`.
- Dùng `docker compose`, không dùng `docker-compose`.
- Dùng `uvx pgcli`, không chỉ dùng `pgcli`.
- Dùng `uv run python`, không chỉ dùng `python` khi chạy script.

## Đặt tên

- Đặt tên có ý nghĩa, phản ánh mục đích thay vì dùng tên chung chung.
  Ví dụ `group_id='rides-console'` hoặc `group_id='rides-to-postgres'`,
  không dùng `group_id='test-consumer-group'`.

## Giải thích

- Với cấu hình phức tạp (như lệnh docker-compose của Redpanda), hãy giải thích
  từng tham số bằng bảng hoặc danh sách.
- Giải thích cả "vì sao", không chỉ "làm gì" (vì sao có hai địa chỉ Kafka,
  vì sao checkpoint mỗi 10 giây, vì sao cần Watermark).
- Dùng bảng để giải thích và so sánh tham số.
- Kèm đầu ra mẫu cho mọi lệnh người học sẽ chạy.
- Dùng blockquote `>` cho mẹo, ghi chú về repository và lỗi thường gặp
  từ workshop hoặc buổi phát trực tiếp gốc.
- Với khái niệm phức tạp (Watermark, task slot, parallelism), hãy đưa phần
  giải thích ra khỏi danh sách gạch đầu dòng thành một mục gồm nhiều đoạn.
  Nêu giá trị hoặc cú pháp trong gạch đầu dòng, rồi giải thích riêng bên dưới.
- Dùng danh sách để tóm tắt nhiều ý thay vì dồn hết vào một câu dài.
- Khi giới thiệu cách làm tắt trong môi trường phát triển (như mount file
  cục bộ vào Docker), hãy ghi chú cách triển khai tương ứng ở production.
  Người học cần hiểu cả cách làm thực tế lẫn môi trường workshop.

## Tổ chức code

- Khi trình bày code block, hãy định nghĩa source (nơi đọc dữ liệu) trước sink
  (nơi ghi dữ liệu). Thiết lập consumer/reader trước, rồi mới kết nối cơ sở
  dữ liệu hoặc xác định đích đầu ra.

## Docker Compose

- Không dùng `container_name` hoặc `hostname` vì Docker Compose tự quản lý tên.
- Không dùng `extra_hosts` trừ khi thực sự cần.
- Tên service tự động được phân giải như hostname trong mạng Docker.
- Ưu tiên tên service ngắn (ví dụ `redpanda`, không phải `redpanda-1`).
- Chỉ dùng `restart: on-failure` cho service cần thiết (như cơ sở dữ liệu).

## Dependency và phiên bản

- Luôn dùng phiên bản stable mới nhất của image và thư viện.
- Pin chính xác phiên bản Flink và các connector vì chúng phải khớp nhau.
- Dùng `uv` cho mọi việc liên quan đến Python (quản lý package, chạy script,
  thậm chí cài Python bên trong Docker).
- Trong Dockerfile, ưu tiên `COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/`
  thay cho `apt-get install`.

## Phần đầu workshop

- Ghi nguồn và dẫn link video hoặc buổi phát trực tiếp gốc ở đầu tài liệu.
- Nếu chưa có video mới, ghi "TBA" kèm link đăng ký (ví dụ Luma).
- Mô tả ngắn sản phẩm sẽ xây dựng và kiến thức cần chuẩn bị.

## Mẫu tiến trình workshop

1. Giới thiệu thành phần đầu tiên (message broker, cơ sở dữ liệu, v.v.)
2. Thiết lập bằng docker-compose (giải thích tham số)
3. Tạo producer/writer đơn giản
4. Tạo consumer/reader đơn giản
5. Thêm cơ sở dữ liệu và lưu dữ liệu
6. Chỉ ra hạn chế của cách làm đơn giản
7. Giới thiệu framework (Flink, Spark, v.v.)
8. Làm lại ví dụ đơn giản bằng framework
9. Thực hiện việc cách làm đơn giản không làm được (aggregation, windowing)
10. Giải thích khái niệm nâng cao (loại window, offset, v.v.)
11. Dọn dẹp tài nguyên
12. Hỏi đáp từ buổi phát trực tiếp gốc. Đưa các chủ đề triển khai production
    vào đây thay vì tách thành mục riêng.
