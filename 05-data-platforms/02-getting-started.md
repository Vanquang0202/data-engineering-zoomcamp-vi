---
video_url: https://www.youtube.com/watch?v=JJwHKSidX_c
prev_url: 01-introduction.md
next_url: 03-nyc-taxi-pipeline.md
---
# Bắt đầu với Bruin


*Đường dẫn thiết lập kết nối các công cụ dành cho nhà phát triển với một dự án có nội dung, phần phụ thuộc và xác thực tạo thành một biểu đồ.*

## Cài đặt

Cài đặt Bruin CLI:

```bash
curl -LsSf https://getbruin.com/install/cli | sh
bruin version
```

Cài đặt tiện ích mở rộng Bruin cho Mã VS hoặc Con trỏ. Điều này bổ sung bảng kết xuất Bruin cho phép bạn chạy nội dung và đường dẫn trực tiếp từ IDE.

## Bruin MCP

Bruin cung cấp máy chủ MCP (Giao thức bối cảnh mô hình) mà bạn có thể thêm vào IDE (Con trỏ, Mã VS) của mình để sử dụng các tác nhân AI nhằm tạo đường ống. Thêm Bruin MCP trong cài đặt IDE > Công cụ và MCP của bạn.

### Tích hợp Bruin MCP cho VS Code

Tạo một tệp mới `mcp.json` trong Kho lưu trữ gốc của bạn:
Trong thư mục gốc của dự án của bạn (cùng cấp với thư mục `.git` hoặc `package.json`), hãy tạo một tệp mới có tên `mcp.json`.

Thêm cấu hình:
Mở tệp `mcp.json` và dán cấu hình JSON sau vào đó:

```json
{
  "servers": {
    "bruin": {
      "type": "stdio",
      "command": "bruin",
      "args": [
        "mcp"
      ]
    }
  },
  "inputs": []
}
```

Cấu hình này hướng dẫn VS Code khởi chạy lệnh `bruin mcp`, thiết lập kết nối đầu vào/đầu ra tiêu chuẩn với máy chủ Bruin MCP.

## Khởi tạo dự án

```bash
bruin init default my-first-pipeline
cd my-first-pipeline
```

Điều này tạo ra một dự án từ một mẫu, khởi tạo git, thêm `.gitignore` và tạo tệp `bruin.yaml`.

Bruin yêu cầu dự án phải được khởi tạo git. Lệnh `bruin init` tự động xử lý việc này.

## Cấu trúc dự án

```text
my-first-pipeline/
├── .bruin.yml              # Environment and connection configuration
├── pipeline.yml            # Pipeline name, schedule, default connections
└── assets/
    ├── players.asset.yml   # Ingestr asset (data ingestion)
    ├── player_stats.sql    # SQL asset with quality checks
    └── my_python_asset.py  # Python asset
```

### .bruin.yml

- Chỉ lưu cục bộ (được tự động thêm vào `.gitignore`)
- Không bao giờ đẩy phần này vào kho lưu trữ của bạn — nó chứa các kết nối cơ sở dữ liệu và bí mật
- Xác định môi trường (mặc định, sản xuất, dàn dựng, v.v.)
- Trong mỗi môi trường, hãy xác định kết nối (ví dụ: DuckDB, Chess.com, bí mật tùy chỉnh)

```yaml
default_environment: default

environments:
  default:
    connections:
      duckdb:
        - name: duckdb-default
          path: duckdb.db
```

### pipe.yml

Định cấu hình đường dẫn: tên, lịch trình, kết nối mặc định, ngày bắt đầu.

```yaml
name: my-pipeline
schedule: daily
start_date: "2022-01-01"
default_connections:
  duckdb: duckdb-default
```

## Loại tài sản

### Tài sản Python

Hình thức đơn giản nhất: tập lệnh Python có tên in hoặc xử lý dữ liệu. Chạy từ bảng Bruin trong IDE của bạn.

### Nội dung trình nhập YAML

Sử dụng bộ nạp tích hợp của Bruin. Xác định kết nối nguồn, đích và bảng. Hỗ trợ nhiều nguồn và đích tích hợp: Redshift, MySQL, Postgres, Motherduck, BigQuery, v.v. Tự động tạo cơ sở dữ liệu/bảng đích nếu nó không tồn tại.

### Nội dung SQL

Chạy các truy vấn SQL đối với cơ sở dữ liệu của bạn. Xác định phần phụ thuộc cho các nội dung khác — khi phần phụ thuộc kết thúc, nội dung này sẽ tự động chạy.

## Khoảng thời gian và mức nhập tăng dần

- Đặt các tham số `start_date` và `end_date` để nhập dữ liệu trong một khoảng thời gian cụ thể
- Bruin cung cấp các tham số này dưới dạng các biến mà bạn có thể đưa vào mã của mình
- Nội dung nhập tích hợp tự động sử dụng ngày bắt đầu/kết thúc

## Phụ thuộc và dòng

- Xác định các phần phụ thuộc giữa các nội dung để chúng chạy theo đúng thứ tự
- Khi nội dung đầu tiên hoàn thành, nó sẽ tự động kích hoạt nội dung phụ thuộc tiếp theo
- Bruin xây dựng biểu đồ dòng từ các phần phụ thuộc này

## Lệnh CLI chính

| Lệnh | Mục đích |
|---------|---------|
| `bruin validate <path>` | Kiểm tra cú pháp và phần phụ thuộc mà không cần chạy |
| `bruin run <path>` | Thực thi đường ống hoặc tài sản riêng lẻ |
| `bruin run --downstream` | Chạy nội dung và tất cả các phần phụ thuộc ở hạ nguồn |
| `bruin run --full-refresh` | Cắt bớt và xây dựng lại bảng từ đầu |
| `bruin lineage <path>` | Xem phần phụ thuộc của tài sản |
| `bruin query --connection <conn> --query "..."` | Thực hiện các truy vấn SQL đặc biệt |
