---
prev_url: 16-retrieval-augmented-generation.md
next_url: 18-additional-resources.md
---
# Phần thưởng: Triển khai lên đám mây (Tùy chọn)

Giờ đây, khi tất cả các quy trình của chúng tôi đã hoạt động và chúng tôi biết cách nhanh chóng tạo các luồng mới bằng AI Copilot của Kestra, chúng tôi có thể triển khai Kestra lên đám mây để nó có thể tiếp tục điều phối các quy trình theo lịch trình của chúng tôi.

Trong phần thưởng này, chúng tôi sẽ đề cập đến cách bạn có thể triển khai Kestra trên Google Cloud và tự động đồng bộ hóa quy trình công việc của bạn từ kho lưu trữ Git.


*Triển khai trên đám mây kết nối mã quy trình làm việc đã được xem xét với quá trình thực thi theo lịch trình trong khi vẫn giữ thông tin xác thực trong một kho lưu trữ bí mật riêng biệt.*

Lưu ý: Khi chuyển giao quy trình làm việc của bạn cho Kestra, hãy đảm bảo quy trình làm việc của bạn không chứa bất kỳ thông tin nhạy cảm nào. Bạn có thể sử dụng [Bí mật](https://go.kestra.io/de-zoomcamp/secret) và [KV Store](https://go.kestra.io/de-zoomcamp/kv-store) để loại bỏ dữ liệu nhạy cảm ra khỏi logic quy trình công việc của bạn.

## Tài nguyên
- [Cài đặt Kestra trên Google Cloud](https://go.kestra.io/de-zoomcamp/gcp-install)
- [Chuyển từ phát triển sang sản xuất](https://go.kestra.io/de-zoomcamp/dev-to-prod)
- [Sử dụng Git trong Kestra](https://go.kestra.io/de-zoomcamp/git)
- [Triển khai các luồng với GitHub Hành động](https://go.kestra.io/de-zoomcamp/deploy-github-actions)
