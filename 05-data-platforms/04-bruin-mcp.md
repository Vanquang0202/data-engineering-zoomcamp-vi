---
video_url: https://www.youtube.com/watch?v=224xH7h8OaQ
prev_url: 03-nyc-taxi-pipeline.md
next_url: 05-bruin-cloud.md
---
# Sử dụng Bruin MCP với AI Agent

## Bruin MCP là gì?

MCP là viết tắt của **Giao thức bối cảnh mô hình**. Bruin MCP là một cách để các tác nhân AI (trong Cursor, VS Code, Claude, v.v.) giao tiếp với Bruin — truy vấn tài liệu, chạy lệnh thay mặt bạn, xem qua mã của bạn, khắc phục sự cố và phân tích dữ liệu.

Với Bruin MCP và tác nhân AI, bạn có thể:

- Viết mã đường ống và cấu hình nội dung
- Viết tài liệu và siêu dữ liệu
- Khắc phục sự cố và gỡ lỗi
- Chạy truy vấn và phân tích dữ liệu bằng ngôn ngữ tự nhiên
- Đặt câu hỏi về logic và cấu trúc đường ống


*Máy chủ MCP cung cấp cho tác nhân các cách có cấu trúc để kiểm tra và vận hành dự án Bruin thay vì chỉ đoán từ ngữ cảnh trò chuyện.*

## Cài đặt Bruin MCP

Trước tiên, hãy đảm bảo bạn đã cài đặt [Bruin CLI](https://getbruin.com/docs/bruin/getting-started/introduction/installation).

### Con trỏ

Đi tới **Cài đặt → Công cụ & MCP → Máy chủ MCP mới** và thêm:

```json
{
  "mcpServers": {
    "bruin": {
      "command": "bruin",
      "args": ["mcp"]
    }
  }
}
```

Nếu nó hiển thị lỗi/không thành công, hãy đóng và mở lại IDE của bạn - bạn sẽ thấy thông báo "Bruin đã bật".

### Mã VS (Phi công phụ)

Tạo `.vscode/mcp.json` trong thư mục dự án của bạn:

```json
{
  "servers": {
    "bruin": {
      "command": "bruin",
      "args": ["mcp"]
    }
  }
}
```

### Mã Claude

```bash
claude mcp add bruin -- bruin mcp
```

Xem [tài liệu đầy đủ về Bruin MCP](https://getbruin.com/docs/bruin/getting-started/bruin-mcp) để biết các tác nhân khác và cách khắc phục sự cố.

## Xây dựng đường ống với MCP

### Sử dụng lời nhắc mẫu

Mẫu zoomcamp bao gồm một lời nhắc ví dụ trong README mà bạn có thể cung cấp cho tác nhân AI để tạo toàn bộ quy trình từ đầu đến cuối:

```bash
bruin init zoomcamp my-taxi-pipeline
```

Mở `README.md` đã tạo - nó chứa lời nhắc bạn có thể dán vào tác nhân để tự động tạo giàn giáo cho toàn bộ đường ống.

### Đại lý làm gì

Khi được đưa ra lời nhắc về quy trình, tác nhân sẽ:

1. Tạo tất cả nội dung quy trình (nhập, dàn dựng, báo cáo)
2. Định cấu hình chiến lược cụ thể hóa và phần phụ thuộc
3. Thiết lập kiểm tra chất lượng và siêu dữ liệu cột
4. Xác thực quy trình bằng `bruin validate`
5. Chạy quy trình với phạm vi ngày kiểm tra
6. Chạy kiểm tra tùy chỉnh để xác thực logic truy vấn
7. Thực hiện truy vấn xác minh bằng `bruin query`

### Làm việc tăng dần

Trong thực tế, bạn có thể thích sử dụng từng tài sản hơn là tạo ra mọi thứ cùng một lúc. Điều này cho phép bạn tham gia vào mọi lựa chọn thiết kế:

- Tạo và kiểm tra nội dung nhập trước
- Sau đó xây dựng lớp dàn
- Sau đó thêm lớp báo cáo
- Xem xét và điều chỉnh kiểm tra chất lượng ở từng bước

## Truy vấn dữ liệu với tác nhân

Sau khi quy trình của bạn đã chạy, bạn có thể sử dụng tác nhân theo cách trò chuyện để truy vấn dữ liệu của mình:

**Truy vấn ví dụ:**
- "Truy vấn bảng phân tầng và cho tôi biết chúng tôi có bao nhiêu ngày dữ liệu"
- "Ngày nào có số chuyến đi và tổng giá vé cao nhất?"
- "Chúng tôi đang tổng hợp dữ liệu ở nội dung nào?"

Tác nhân hiểu ngữ cảnh quy trình của bạn — nó biết cấu trúc bảng, có thể viết truy vấn SQL và có thể giải thích logic đằng sau mỗi nội dung. Điều này hữu ích cho:

- Phân tích đặc biệt mà không cần viết SQL theo cách thủ công
- Hiểu logic quy trình không quen thuộc
- Xác thực dữ liệu và khắc phục sự cố
- Đưa thành viên nhóm mới vào quy trình hiện có
