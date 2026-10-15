---
prev_url: 12-understanding-window-types.md
next_url: 14-questions-and-answers.md
---
#Dọn dẹp


*`docker compose down` loại bỏ các dịch vụ trong khi vẫn duy trì âm lượng; việc thêm `-v` cũng sẽ xóa dữ liệu cơ sở dữ liệu đã tồn tại.*

Dừng và xóa tất cả các container:

```bash
docker compose down
```

Để xóa khối lượng dữ liệu PostgreSQL:

```bash
docker compose down -v
```
