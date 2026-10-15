# Nhập dữ liệu bằng dlt

​Trong hội thảo thực hành này, chúng ta sẽ tìm hiểu cách xây dựng quy trình nhập dữ liệu.

​Chúng tôi sẽ thực hiện các bước sau:

* ​Trích xuất dữ liệu từ APIs hoặc các tệp.
* ​Bình thường hóa và tải dữ liệu
* ​Incremental loading

​Khi kết thúc hội thảo này, bạn sẽ có thể viết các đường dẫn dữ liệu như một kỹ sư dữ liệu cấp cao: Nhanh chóng, chính xác, có thể mở rộng và tự bảo trì.

Video: https://www.youtube.com/live/oLXhBM7nf2Q

--- 

# Điều hướng

* [Nội dung hội thảo](dlt_resources/data_ingestion_workshop.md)
* [Sổ tay hội thảo](dlt_resources/workshop.ipynb)
* [Sổ tay bắt đầu bài tập về nhà](dlt_resources/homework_starter.ipynb)

# Tài nguyên

- Trang web và cộng đồng: Truy cập [docs](https://dlthub.com/docs/intro) của chúng tôi, thảo luận về sự chậm chạp của chúng tôi (Liên kết ở đầu tài liệu).
- Khóa học hợp tác: [Notebook](https://colab.research.google.com/drive/1kLyD3AL-tYf_HqCXYnA3ZLwHGpzbLmoj#scrollTo=5aPjk0O3S_Ag&forceEdit=true&sandboxMode=true).
- dlthub [Slack cộng đồng](https://dlthub.com/community).

---

# Thầy

Chào mừng bạn đến với câu lạc bộ trò chuyện dữ liệu data engineering zoomcamp, hội thảo nhập dữ liệu.

- Tên tôi là [Adrian](https://www.linkedin.com/in/data-team/) và tôi làm việc trong lĩnh vực dữ liệu từ năm 2012
    - I built many data warehouses some lakes, and a few data teams
    - 10 years into my career I started working on dlt “data load tool”, which is an open source library to enable data engineers to build faster and better.
    - I started working on dlt because data engineering is one of the few areas of software engineering where we do not have developer tools to do our work.
    - Building better pipelines would require more code re-use - we cannot all just build perfect pipelines from scratch every time.
    - And so dlt was born, a library that automates the tedious part of data ingestion: Loading, schema management, data type detection, scalability, self healing, scalable extraction… you get the idea - essentially a data engineer’s “one stop shop” for best practice data pipelining.
    - Due to its **simplicity** of use, dlt enables **laymen** to
        - Build pipelines 5-10x faster than without it
        - Build self healing, self maintaining pipelines with all the best practices of data engineers. Automating schema changes removes the bulk of maintenance efforts.
        - Govern your pipelines with schema evolution alerts and data contracts.
        - and generally develop pipelines like a senior, commercial data engineer.

--- 

# Khóa học
Bạn có thể tìm thấy tệp khóa học [tại đây](./dlt_resources/data_ingestion_workshop.md) Khóa học có 3 phần
- [Phần trích xuất](./dlt_resources/data_ingestion_workshop.md#extracting-data): Trong phần này chúng ta sẽ tìm hiểu về trích xuất có thể mở rộng
- [Chuẩn hóa Mục](./dlt_resources/data_ingestion_workshop.md#normalisation): Trong phần này, chúng ta sẽ học cách chuẩn bị dữ liệu để tải
- [Phần tải](./dlt_resources/data_ingestion_workshop.md#incremental-loading)): Ở đây chúng ta sẽ tìm hiểu về các chế độ incremental loading

---

# Bài tập về nhà

[sổ tay colab được liên kết](https://colab.research.google.com/drive/1Te-AT0lfh0GpChg1Rbd0ByEKOHYtWXfm#scrollTo=wLF4iXf-NR7t&forceEdit=true&sandboxMode=true) cung cấp một số bài tập để thực hành những gì bạn đã học hôm nay.


#### Câu hỏi 1: Tổng đầu ra của máy phát điện cho giới hạn = 5 là bao nhiêu?
- **A**: 10.23433234744176
- **B**: 7.892332347441762
- **C**: 8.382332347441762
- **D**: 9.123332347441762

#### Câu hỏi 2: Số thứ 13 do máy tạo ra là gì?
- **A**: 4.236551275463989
- **B**: 3.605551275463989
- **C**: 2.345551275463989
- **D**: 5.678551275463989

#### Câu 3: Nối 2 máy phát điện. Sau khi nối dữ liệu một cách chính xác, hãy tính tổng của mọi lứa tuổi của mọi người.
- **A**: 353
- **B**: 365
- **C**: 378
- **D**: 390

#### Câu 4: Hợp nhất 2 máy phát điện bằng cột ID. Tính tổng số tuổi của tất cả những người được chở như mô tả ở trên.
- **A**: 215
- **B**: 266
- **C**: 241
- **D**: 258

Gửi giải pháp tại đây: https://courses.datatalks.club/de-zoomcamp-2024/homework/workshop1

--- 
# Các bước tiếp theo

Khi bạn đang tìm hiểu các khái niệm khác nhau của data engineering, 
hãy cân nhắc việc tạo một dự án danh mục đầu tư để nâng cao kiến ​​thức của riêng bạn.

Bằng cách thể hiện khả năng hoàn thành công việc từ đầu đến cuối, bạn sẽ dễ dàng tìm được vai diễn đầu tiên của mình hơn. 
Điều này sẽ hữu ích bất kể người quản lý tuyển dụng có đánh giá dự án của bạn hay không, phần lớn là vì bạn sẽ hiểu 
tốt hơn và có thể nói chuyện.

Dưới đây là một số dự án mẫu mà những người khác đã thực hiện với dlt:
- Serverless dlt-dbt trên các chức năng đám mây: [Bài viết](https://docs.getdbt.com/blog/serverless-dlt-dbt-stack)
- Công cụ tìm chim: [Phần 1](https://publish.obsidian.md/lough-on-data/blogs/bird-finder-via-dlt-i), [Phần 2](https://publish.obsidian.md/lough-on-data/blogs/bird-finder-via-dlt-ii)
- Nhập sự kiện trên GCP: [Bài viết và repo](https://dlthub.com/docs/blog/streaming-pubsub-json-gcp)
- Nhập sự kiện trên AWS: [Bài viết và repo](https://dlthub.com/docs/blog/dlt-aws-taktile-blog)
- Hoặc xem một trong nhiều bản demo do các sinh viên đang làm việc của chúng tôi tạo: [Tin tức về hacker](https://dlthub.com/docs/blog/hacker-news-gpt-4-dashboard-demo), 
[Sự kiện GA4](https://dlthub.com/docs/blog/ga4-internal-dashboard-demo), 
[Thương mại điện tử](https://dlthub.com/docs/blog/postgresql-bigquery-metabase-demo), 
[google trang tính](https://dlthub.com/docs/blog/google-sheets-to-data-warehouse-pipeline), 
[Motherduck](https://dlthub.com/docs/blog/dlt-motherduck-demo), 
[MongoDB + Holistics](https://dlthub.com/docs/blog/MongoDB-dlt-Holistics), 
[Deepnote](https://dlthub.com/docs/blog/deepnote-women-wellness-violence-tends), 
[Prefect](https://dlthub.com/docs/blog/dlt-prefect),
[PowerBI vs GoodData vs Metabase](https://dlthub.com/docs/blog/semantic-modeling-tools-comparison),
[Dagster](https://dlthub.com/docs/blog/dlt-dagster),
[Nhập sự kiện qua gcp webhooks](https://dlthub.com/docs/blog/dlt-webhooks-on-cloud-functions-for-event-capture),
[SAP để sao chép bông tuyết](https://dlthub.com/docs/blog/sap-hana-to-snowflake-demo-blog),
[Đọc email và gửi tổng hợp tới Slack với AI và Kestra](https://dlthub.com/docs/blog/dlt-kestra-demo-blog),
[Chế độ +dlt khả năng](https://dlthub.com/docs/blog/dlt-mode-blog),
[dbt trên các chức năng đám mây](https://dlthub.com/docs/blog/dlt-dbt-runner-on-cloud-functions)
- Nếu bạn muốn sử dụng dlt trong dự án của mình, [hãy kiểm tra danh sách APIs công khai này](https://dlthub.com/docs/blog/practice-api-sources)


Nếu bạn tạo một dự án cá nhân, hãy cân nhắc việc gửi nó lên blog của chúng tôi - chúng tôi sẽ rất vui được giới thiệu nó. Chỉ cần gửi cho chúng tôi một dòng trong phần dlt.



**Và đừng quên, nếu bạn thích dlt**
- **Hãy cho chúng tôi [GitHub Star!](https://github.com/dlt-hub/dlt)**
- **Join [Cộng đồng Slack](https://dlthub.com/community)**


# Ghi chú

* Thêm ghi chú của bạn tại đây
