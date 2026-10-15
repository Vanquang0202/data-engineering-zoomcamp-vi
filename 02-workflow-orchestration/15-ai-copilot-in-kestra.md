---
video_url: https://www.youtube.com/watch?v=3IbjHfC8bMg
prev_url: 14-context-engineering-with-chatgpt.md
next_url: 16-retrieval-augmented-generation.md
---
# Phi công phụ AI trong Kestra

AI Copilot của Kestra được thiết kế đặc biệt để tạo và sửa đổi các luồng Kestra với bối cảnh đầy đủ về các plugin mới nhất, cú pháp quy trình làm việc và các phương pháp hay nhất.


*Ưu điểm của Copilot là hỗ trợ theo ngữ cảnh: nó soạn thảo trong mô hình luồng của Kestra trong khi vẫn duy trì việc xem xét và thực hiện rõ ràng.*

## Thiết lập AI Copilot
Trước khi sử dụng AI Copilot, bạn cần định cấu hình quyền truy cập API Gemini trong phiên bản Kestra của mình.

**Bước 1: Nhận khóa API Gemini của bạn**

1. Truy cập Google AI Studio: https://aistudio.google.com/app/apikey
2. Đăng nhập bằng tài khoản Google của bạn
3. Nhấp vào "Tạo khóa API"
4. Sao chép khóa đã tạo (giữ an toàn!)

> [!CẢNH BÁO]
> Không bao giờ cam kết khóa API với Git. Luôn sử dụng các biến môi trường hoặc Cửa hàng KV của Kestra.

**Bước 2: Định cấu hình Kestra AI Copilot**

Thêm phần sau vào cấu hình Kestra của bạn. Bạn có thể thực hiện việc này bằng cách sửa đổi tệp `docker-compose.yml` của mình từ 2.2:

```yaml
services:
  kestra:
    environment:
      KESTRA_CONFIGURATION: |
        kestra:
          ai:
            type: gemini
            gemini:
              model-name: gemini-2.5-flash
              api-key: ${GEMINI_API_KEY}
```

Sau đó khởi động lại Kestra:
```bash
cd 02-workflow-orchestration/docker
export GEMINI_API_KEY="your-api-key-here"
docker compose up -d
```

## Bài tập: So sánh ChatGPT và AI Copilot
**Mục tiêu:** Tìm hiểu lý do tại sao kỹ thuật ngữ cảnh lại quan trọng.

1. **Mở Kestra UI** tại http://localhost:8080
2. **Tạo luồng mới** và mở bảng soạn thảo Mã
3. **Nhấp vào nút AI Copilot** (biểu tượng lấp lánh ✨) ở góc trên bên phải
4. **Nhập chính xác lời nhắc** chúng tôi đã sử dụng với ChatGPT:
   ```
   Create a Kestra flow that loads NYC taxi data from a CSV file to BigQuery. The flow should extract data, upload to GCS, and load to BigQuery.
   ```
5. **So sánh các kết quả đầu ra:**
- ✅ Copilot tạo ra tệp thực thi, đang hoạt động YAML
- ✅ Copilot sử dụng đúng loại plugin và thuộc tính
- ✅ Copilot tuân theo các phương pháp hay nhất hiện tại của Kestra

**Bài học quan trọng:** Bối cảnh rất quan trọng! AI Copilot có quyền truy cập vào tài liệu Kestra hiện tại, tạo ra các luồng Kestra tốt hơn so với trợ lý ChatGPT chung.
