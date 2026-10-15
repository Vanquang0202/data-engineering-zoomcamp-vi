# Bài tập: Tự xây dựng pipeline dlt

Bạn đã thấy cách xây dựng pipeline từ source có scaffold sẵn. Bây giờ hãy tự làm từ đầu với một **API riêng**.

## Nội dung workshop

* [README của workshop](README.md)
* [Notebook tổng quan pipeline dlt (Google Colab)](https://colab.research.google.com/github/anair123/data-engineering-zoomcamp/blob/workshop/dlt_2026/cohorts/2026/workshops/dlt/dlt_Pipeline_Overview.ipynb)
* [Trang đăng ký workshop](https://luma.com/hzis1yzp)

## Thử thách

Hãy xây dựng pipeline dlt nạp dữ liệu chuyến đi taxi NYC từ API riêng vào DuckDB, rồi dùng dữ liệu đã nạp để trả lời các câu hỏi.

## Nguồn dữ liệu

Bạn sẽ dùng **dữ liệu chuyến đi taxi Yellow NYC** từ API riêng (không có sẵn scaffold trong dlt). Bộ dữ liệu gồm các bản ghi chuyến taxi tại Thành phố New York.

| Thuộc tính | Giá trị |
|----------|-------|
| Base URL | `https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api` |
| Định dạng | JSON phân trang |
| Kích thước trang | 1,000 bản ghi mỗi trang |
| Phân trang | Dừng khi API trả về trang rỗng |

## Hướng dẫn thiết lập

Vì đây là API riêng (không nằm trong các scaffold của dlt workspace), cách thiết lập hơi khác.

### Bước 1: Tạo dự án mới (hoặc dùng lại dự án demo)

Nếu đã tạo thư mục dự án khi làm theo demo workshop, bạn có thể dùng lại. Nếu chưa, hãy tạo thư mục mới:

```bash
mkdir taxi-pipeline
cd taxi-pipeline
```

Mở thư mục này trong Cursor (hoặc IDE có AI agent mà bạn thích).

### Bước 2: Thiết lập dlt MCP Server (nếu chưa làm)

Chọn cách thiết lập tương ứng với IDE của bạn:

Cursor - vào **Settings → Tools & MCP → New MCP Server** rồi thêm:

```json
{
  "mcpServers": {
    "dlt": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "dlt[duckdb]",
        "--with",
        "dlt-mcp[search]",
        "python",
        "-m",
        "dlt_mcp"
      ]
    }
  }
}
```

VS Code (Copilot) - tạo `.vscode/mcp.json` trong thư mục dự án:

```json
{
  "servers": {
    "dlt": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "dlt[duckdb]",
        "--with",
        "dlt-mcp[search]",
        "python",
        "-m",
        "dlt_mcp"
      ]
    }
  }
}
```

Claude Code - chạy trong terminal:

```bash
claude mcp add dlt -- uv run --with "dlt[duckdb]" --with "dlt-mcp[search]" python -m dlt_mcp
```

Bước này bật dlt MCP server để AI truy cập tài liệu dlt, ví dụ code và metadata của pipeline.

### Bước 3: Cài đặt dlt

```bash
pip install "dlt[workspace]"
```

### Bước 4: Khởi tạo dự án

```bash
dlt init dlthub:taxi_pipeline duckdb
```

Bạn có thể đặt tên dự án tùy ý. Vì API này không có scaffold, lệnh sẽ tạo:
- Các file dự án dlt
- Cursor rules để AI hỗ trợ

**Nhưng không có file YAML chứa metadata của API.** Bạn cần tự cung cấp thông tin API.

### Bước 5: Gửi prompt cho agent

Bây giờ hãy dùng AI assistant để xây dựng pipeline. Vì không có scaffold, bạn cần cung cấp chi tiết API trong prompt.

Dưới đây là prompt mẫu để bắt đầu:

```
Build a REST API source for NYC taxi data.

API details:
- Base URL: https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api
- Data format: Paginated JSON (1,000 records per page)
- Pagination: Stop when an empty page is returned

Place the code in taxi_pipeline.py and name the pipeline taxi_pipeline.
Use @dlt rest api as a tutorial.
```

### Bước 6: Chạy và debug

Chạy pipeline và tiếp tục điều chỉnh cùng agent cho đến khi hoạt động:

```bash
python taxi_pipeline.py
```

---

## Câu hỏi

Khi pipeline chạy thành công, hãy dùng những cách đã học trong workshop để tìm hiểu:

- **dlt Dashboard**: `dlt pipeline taxi_pipeline show`
- **dlt MCP Server**: Hỏi agent về pipeline của bạn
- **Marimo Notebook**: Tạo biểu đồ và chạy truy vấn

Hãy thử những cách khác nhau đã học trong workshop để trả lời câu hỏi, rồi xem cách nào phù hợp nhất. Bạn có thể chia sẻ trong bài nộp những gì hiệu quả (hoặc không hiệu quả) với mình!

### Câu hỏi 1: Ngày bắt đầu và kết thúc của bộ dữ liệu là ngày nào?

- 2009-01-01 to 2009-01-31
- 2009-06-01 to 2009-07-01
- 2024-01-01 to 2024-02-01
- 2024-06-01 to 2024-07-01

### Câu hỏi 2: Tỷ lệ chuyến đi được thanh toán bằng thẻ tín dụng là bao nhiêu?

- 16.66%
- 26.66%
- 36.66%
- 46.66%

### Câu hỏi 3: Tổng tiền tip thu được là bao nhiêu?

- $4,063.41
- $6,063.41
- $8,063.41
- $10,063.41


### Tài nguyên

| Tài nguyên | Link |
|----------|------|
| Tài liệu dlt Dashboard | [dlthub.com/docs/general-usage/dashboard](https://dlthub.com/docs/general-usage/dashboard) |
| Hướng dẫn marimo + dlt | [dlthub.com/docs/general-usage/dataset-access/marimo](https://dlthub.com/docs/general-usage/dataset-access/marimo) |
| Tài liệu dlt | [dlthub.com/docs](https://dlthub.com/docs) |

---

## Nộp bài

- Biểu mẫu nộp bài: https://courses.datatalks.club/de-zoomcamp-2026/homework/dlt
- Hạn nộp: Xem trên trang web

## Mẹo

- API trả dữ liệu theo trang. Hãy bảo đảm pipeline xử lý phân trang đúng cách.
- Nếu agent gặp lỗi, hãy dán thông báo lỗi vào cuộc trò chuyện để agent debug.
- Dùng dlt MCP server để hỏi về metadata của pipeline.


## Chia sẻ quá trình học công khai

Chúng tôi khuyến khích mọi người chia sẻ những gì mình đã học. Cách học này gọi là "learning in public".

Đọc thêm về lợi ích [tại đây](https://aishippingblog.com/p/benefits-of-learning-in-public-and).

### Bài đăng mẫu trên LinkedIn

```
🚀 dlt Workshop of Data Engineering Zoomcamp by @DataTalksClub complete!

Just finished the Data Ingestion workshop with @dltHub. Learned how to:

✅ Build REST API data pipelines with dlt
✅ Use AI-assisted development with dlt MCP Server
✅ Load paginated API data into DuckDB
✅ Inspect pipeline data with dlt Dashboard and marimo notebooks

Built a full NYC taxi data pipeline from a custom API - AI-assisted data engineering is the future!

Here's my homework solution: <LINK>

Following along with this amazing free course - who else is learning data engineering?

You can sign up here: https://github.com/DataTalksClub/data-engineering-zoomcamp/
```

### Bài đăng mẫu trên Twitter/X

```
🔄 dlt Workshop of Data Engineering Zoomcamp done!

- REST API pipelines with @dltHub
- AI-assisted pipeline building
- DuckDB as local data warehouse
- dlt Dashboard & marimo notebooks

My solution: <LINK>

Free course by @DataTalksClub: https://github.com/DataTalksClub/data-engineering-zoomcamp/
```
