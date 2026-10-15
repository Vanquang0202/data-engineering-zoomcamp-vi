# Tập lệnh

## generate_thumbnails.py

Tạo hình thu nhỏ YouTube tự lưu trữ cho các README của khóa học.

README được sử dụng để nhúng hình thu nhỏ thông qua dịch vụ bên ngoài `markdown-videos-api.jorgenkh.no`, dịch vụ này hiển thị nhanh hình thu nhỏ bằng nút phát. Dịch vụ đó không ổn định nên bộ nhớ đệm hình ảnh của GitHub thường xuyên hết thời gian chờ và ngẫu nhiên không tải được hình thu nhỏ (vấn đề #591).

Tập lệnh này loại bỏ phần phụ thuộc thời gian chạy. Nó quét các tệp Markdown và đối với mọi liên kết vẫn trỏ đến dịch vụ bên ngoài, nó:

1. tải xuống hình thu nhỏ thô của YouTube (`https://img.youtube.com/vi/<id>/0.jpg`)
2. dán lớp phủ nút phát của riêng chúng tôi (`play.png`) lên trên
3. lưu kết quả bên cạnh README trong `images/thumbnail-<id>.jpg`
4. viết lại Markdown để trỏ vào ảnh đã commit

Script có tính Idempotency: các liên kết đã trỏ đến đường dẫn `images/...` cục bộ sẽ bị bỏ qua và các hình thu nhỏ hiện có sẽ không được tải xuống lại. Để thêm hình thu nhỏ cho video mới, hãy tiếp tục sử dụng liên kết `markdown-videos-api.jorgenkh.no` trong Markdown và chạy lại tập lệnh - chỉ những video mới được xử lý.

### Cách sử dụng

```bash
cd scripts
uv run generate_thumbnails.py            # scan the whole repo
uv run generate_thumbnails.py PATH ...   # only the given files/dirs
uv run generate_thumbnails.py --dry-run  # report changes without writing
```
