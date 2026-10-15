# Từ API đến Data Warehouse: Data Ingestion với dlt có AI hỗ trợ

Chào mừng bạn đến với workshop **Data Engineering Zoomcamp 2026**!

Trong workshop này, bạn sẽ dùng IDE có AI hỗ trợ để xây dựng một data pipeline hoàn chỉnh. Chỉ với vài prompt đơn giản, bạn có thể đưa dữ liệu từ API vào Data Warehouse cục bộ bằng [dlt](https://dlthub.com/docs) (data load tool). AI hỗ trợ tạo code, còn bạn tập trung kiểm tra kết quả.

## Bạn sẽ xây dựng gì

Sau workshop, bạn sẽ có:

1. Pipeline dlt hoạt động được, trích xuất dữ liệu từ [Open Library API](https://openlibrary.org/developers/api)
2. Các bảng quan hệ đã được chuẩn hóa và lưu trong DuckDB
3. Khả năng truy vấn, kiểm tra và trực quan hóa dữ liệu
4. Kinh nghiệm phát triển Data Engineering có AI hỗ trợ

**Không cần API key!** Open Library API hoàn toàn mở và không yêu cầu xác thực. Bạn có thể bắt đầu ngay.

---

## Kiến thức và công cụ cần chuẩn bị

Trước workshop, hãy chuẩn bị các mục sau:

### 1. Hiểu dlt làm gì (khuyến nghị cho người mới)

Nếu chưa quen với dlt, bạn nên đọc Jupyter notebook đi kèm trước workshop.

**[Mở notebook trong Google Colab](https://colab.research.google.com/github/anair123/data-engineering-zoomcamp/blob/workshop/dlt_2026/cohorts/2026/workshops/dlt/dlt_Pipeline_Overview.ipynb)**

Notebook giải thích dlt từng bước:

- Source và pipeline trong dlt là gì
- Dữ liệu đi qua các bước Extract, Normalize và Load thế nào
- Cách kiểm tra dữ liệu đã nạp

Hiểu những khái niệm này giúp bạn biết code do agent tạo thực sự đang làm gì.

> Bạn không cần clone repository để tham gia workshop. Lệnh `dlt init` tạo sẵn cấu trúc cần thiết.

### 2. IDE có AI agent

Bạn cần trình soạn thảo code có AI, hiểu ngữ cảnh và tạo code từ ngôn ngữ tự nhiên. Chúng tôi gợi ý:

| IDE | Mô tả |
|-----|-------------|
| [**Cursor**](https://cursor.sh) | Phiên bản dựa trên VS Code có AI tích hợp (khuyến nghị) |
| [Windsurf](https://codeium.com/windsurf) | IDE có AI agent khác |
| [VS Code + GitHub Copilot](https://github.com/features/copilot) | Dùng được nhưng mức độ tích hợp thấp hơn |

### 3. Python 3.11+

```bash
python --version  # Should be 3.11 or higher
```

### 4. uv (khuyến nghị) hoặc pip

Chúng ta dùng [uv](https://docs.astral.sh/uv/) để quản lý dependency nhanh:

```bash
# Install uv (if you don't have it)
curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

## Hướng dẫn workshop

### Bước 1: Tạo thư mục dự án mới

Tạo thư mục mới cho pipeline rồi mở trong Cursor (hoặc IDE có AI agent bạn thích):

```bash
mkdir my-dlt-pipeline
cd my-dlt-pipeline
```

### Bước 2: Thêm cấu hình dlt MCP Server

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

### Bước 3: Cài đặt dlt Workspace

```bash
pip install "dlt[workspace]"
```

### Bước 4: Khởi tạo dự án dlt

```bash
dlt init dlthub:open_library duckdb
```

Lệnh này tạo sẵn file pipeline và cấu hình cho Open Library. Giờ bạn đã có thể bắt đầu gửi prompt.

> 📖 **Tài liệu tham khảo:** [Hướng dẫn Open Library Workspace](https://dlthub.com/workspace/source/open-library)

### Bước 5: Yêu cầu agent xây dựng và chạy pipeline

Lệnh `dlt init` tạo sẵn các prompt mẫu. Bạn có thể bắt đầu với ví dụ sau:

```
Please generate a REST API Source for Open Library API, as specified in @open_library-docs.yaml
Start with endpoint(s) books and skip incremental loading for now.
Place the code in open_library_pipeline.py and name the pipeline open_library_pipeline.
If the file exists, use it as a starting point.
Do not add or modify any other files.
Use @dlt rest api as a tutorial.
After adding the endpoints, allow the user to run the pipeline with python open_library_pipeline.py and await further instructions.
```

Bạn có thể điều chỉnh prompt theo mục tiêu của mình. Agent sẽ:
1. Tạo code pipeline
2. Chạy pipeline
3. Nạp dữ liệu vào DuckDB cục bộ

Tất cả chỉ từ một prompt.

### Bước 6: Debug cùng agent

Nếu gặp lỗi, hãy dán thông báo lỗi vào cuộc trò chuyện để AI hỗ trợ xử lý. Cách phát triển có AI hỗ trợ giúp bạn lặp lại và cải tiến nhanh hơn.

### Bước 7: Kiểm tra dữ liệu pipeline bằng dlt Dashboard

Khi pipeline chạy thành công, mở dashboard để kiểm tra dữ liệu và metadata:

```bash
dlt pipeline open_library_pipeline show
```

Lệnh sẽ mở ứng dụng web để bạn:
- Xem trạng thái pipeline và lịch sử chạy
- Khám phá schema, bảng và cột
- Truy vấn dữ liệu đã nạp
- Debug khi gặp vấn đề

> 📖 **Tài liệu tham khảo:** [Tài liệu dlt Dashboard](https://dlthub.com/docs/general-usage/dashboard)

### Bước 8: Kiểm tra pipeline qua cuộc trò chuyện

Sau khi cấu hình dlt MCP server, bạn có thể hỏi AI trực tiếp về pipeline:

> "Pipeline đã tạo những bảng nào?"  
> "Cho tôi xem schema của bảng books."  
> "Đã nạp bao nhiêu dòng?"

Agent có thể truy cập metadata của pipeline để trả lời các câu hỏi này.

### Bước 9 (tùy chọn): Trực quan hóa bằng marimo + ibis

Bạn có thể phân tích sâu hơn bằng cách tạo báo cáo tương tác trong notebook [marimo](https://marimo.io/) và dùng [ibis](https://ibis-project.org/).

Yêu cầu agent tạo biểu đồ:

> "Tạo notebook marimo trực quan hóa 10 tác giả có nhiều sách nhất. Dùng ibis để truy cập dữ liệu. Tài liệu tham khảo: https://dlthub.com/docs/general-usage/dataset-access/marimo"

Cung cấp link tài liệu sẽ giúp agent dùng đúng bộ công cụ.

Chạy notebook:

```bash
# Edit mode (for development)
marimo edit your_notebook.py

# Run mode (view the report)
marimo run your_notebook.py
```

> 📖 **Tài liệu tham khảo:** [Khám phá dữ liệu với marimo](https://dlthub.com/docs/general-usage/dataset-access/marimo)

---

## Bài tập

Bạn đã xem phần minh họa; giờ đến lượt bạn thực hành!

Xem hướng dẫn trong [dlt_homework.md](dlt_homework.md).

---

## Tài nguyên

| Tài nguyên | Link |
|----------|------|
| Tài liệu dlt | [dlthub.com/docs](https://dlthub.com/docs) |
| Hướng dẫn Open Library Workspace | [dlthub.com/workspace/source/open-library](https://dlthub.com/workspace/source/open-library) |
| Tài liệu dlt Dashboard | [dlthub.com/docs/general-usage/dashboard](https://dlthub.com/docs/general-usage/dashboard) |
| Hướng dẫn marimo + dlt | [dlthub.com/docs/general-usage/dataset-access/marimo](https://dlthub.com/docs/general-usage/dataset-access/marimo) |
| Open Library API | [openlibrary.org/developers/api](https://openlibrary.org/developers/api) |

---

*Workshop do [dltHub](https://dlthub.com) thực hiện cho Data Engineering Zoomcamp 2026*
