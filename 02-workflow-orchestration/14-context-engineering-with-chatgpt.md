---
video_url: https://www.youtube.com/watch?v=LmnfjGKwnVU
prev_url: 13-why-ai-for-workflows.md
next_url: 15-ai-copilot-in-kestra.md
---
# Kỹ thuật bối cảnh với ChatGPT


*Sự so sánh mang tính nền tảng: các phiên bản, tài liệu và ví dụ có liên quan biến một lời nhắc mơ hồ thành một quy trình làm việc có thể xem lại.*

Hãy bắt đầu bằng cách xem điều gì sẽ xảy ra khi AI thiếu bối cảnh thích hợp.

## Thử nghiệm: ChatGPT không có ngữ cảnh
1. **Mở ChatGPT trong cửa sổ trình duyệt riêng tư** (để tránh mọi ngữ cảnh trò chuyện hiện có): https://chatgpt.com

2. **Nhập dấu nhắc này:**
   ```
   Create a Kestra flow that loads NYC taxi data from a CSV file to BigQuery. The flow should extract data, upload to GCS, and load to BigQuery.
   ```

3. **Quan sát kết quả:**
- ChatGPT sẽ tạo luồng Kestra, nhưng có thể chứa:
- **Cú pháp plugin lỗi thời** ví dụ: các loại tác vụ cũ đã được đổi tên thành
- **Tên thuộc tính không chính xác** ví dụ: các thuộc tính không tồn tại trong phiên bản hiện tại
- **Tính năng ảo giác** ví dụ: tác vụ, trình kích hoạt hoặc thuộc tính chưa từng tồn tại

## Tại sao điều này lại xảy ra?
Các mô hình ngôn ngữ lớn (LLM) như mô hình GPT từ OpenAI được đào tạo về dữ liệu cho đến một thời điểm cụ thể (ngưỡng kiến ​​thức). Họ không tự động biết về:
- Cập nhật phần mềm và bản phát hành mới
- Đã đổi tên plugin hoặc thay đổi API

Đây là thách thức cơ bản của việc sử dụng AI: **mô hình chỉ có thể hoạt động với thông tin mà nó có quyền truy cập.**

## Bài học quan trọng: Ngữ cảnh là tất cả
Không có ngữ cảnh phù hợp:
- ❌ Trợ lý AI thông thường ảo giác mã lỗi thời hoặc không chính xác
- ❌ Bạn không thể tin tưởng vào kết quả đầu ra để sử dụng trong sản xuất

Với ngữ cảnh phù hợp:
- ✅ AI tạo mã chính xác, hiện hành, sẵn sàng sản xuất
- ✅ Bạn có thể lặp lại nhanh hơn bằng cách để AI tạo mã quy trình làm việc soạn sẵn

Trong phần tiếp theo, chúng ta sẽ xem AI Copilot của Kestra giải quyết vấn đề này như thế nào.
