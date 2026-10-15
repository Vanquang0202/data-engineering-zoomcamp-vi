---
prev_url: 02-what-is-dbt.md
next_url: 04-dbt-project-structure.md
---
# dbt Core vs dbt Cloud


> 📄 So sánh tính năng chính thức: [dbt Core vs dbt Cloud](https://www.getdbt.com/product/dbt-core-vs-dbt-cloud)

## dbt Core
- Ra đời vào **2016** dưới dạng **công cụ dòng lệnh, mã nguồn mở**
- Miễn phí 100%, chạy cục bộ trên máy của riêng bạn
- Tất cả mã đều có sẵn trên GitHub (có thể phân nhánh, sửa đổi, v.v.)

## dbt Cloud
- Được giới thiệu **hai năm sau dbt Core** (~2018) bởi dbt Labs (ban đầu gọi là Fishtown Analytics)
- Được bán dưới dạng **nền tảng SaaS trả phí** — không cần tự mình quản lý cơ sở hạ tầng
- Xử lý những công việc nặng nhọc:
- Tài liệu dbt lưu trữ
- Điều phối
- Thiết lập môi trường
- Sao lưu các thành phần lạ dbt (ví dụ: cho Slim CI)
- Đi kèm với **các tính năng cộng tác và bảo mật** hữu ích cho các nhóm/công ty

## Chúng được sử dụng cùng nhau như thế nào (Phương pháp tiếp cận kết hợp)
- Mô hình phổ biến: nhiều người dùng kỹ thuật làm việc với dbt Core hơn; người dùng ít kỹ thuật hơn đã sử dụng dbt Cloud
- Cả hai đều được thiết kế để **tương thích** — ví dụ: các nhà phát triển có thể làm việc cục bộ với dbt Core trong khi quá trình sản xuất được thực hiện thông qua dbt Cloud
- dbt Labs đã xuất bản một bài viết vào **tháng 10 năm 2024** nêu rõ cách cả hai sản phẩm cùng tồn tại song song → [Cách chúng tôi nghĩ về dbt Core và dbt Cloud](https://www.getdbt.com/blog/how-we-think-about-dbt-core-and-dbt-cloud)

## dbt Fusion — Tương lai
- Vào **tháng 5 năm 2025**, dbt Labs đã công bố **viết lại toàn bộ cơ sở mã** bằng cách sử dụng một công cụ mới có tên **Fusion**
- Những cải tiến chính:
- **Biên dịch nhanh hơn** mã dbt (nhanh hơn tới 30 lần trong một số trường hợp)
- **Nhà phát triển tốt hơn trải nghiệm** — phát hiện nhiều lỗi *trước khi* chạy/xây dựng, tiết kiệm thời gian và tiền bạc
- dbt Core sẽ tiếp tục được duy trì, nhưng **Fusion là hướng đi trong tương lai** cho cả Core và Cloud

### Hạn chế của Fusion
- **Không được hỗ trợ bởi tất cả các bộ chuyển đổi** — kể từ đầu năm 2026, Fusion hỗ trợ các bộ chuyển đổi chính như Snowflake, Databricks, Postgres (và các sản phẩm phái sinh), BigQuery và Redshift
- Đáng chú ý **không hỗ trợ DuckDB** (chưa) hoặc nhiều bộ chuyển đổi do cộng đồng duy trì
- Nếu bạn sử dụng một bộ chuyển đổi ít phổ biến hơn, dbt Fusion và các phiên bản mới nhất của dbt Cloud có thể không hoạt động với bạn
- Hỗ trợ bộ điều hợp đang được mở rộng tích cực - kiểm tra tài liệu chính thức để biết danh sách hiện tại

> 📄 Hướng dẫn nâng cấp Fusion: [Nâng cấp lên dbt Fusion engine](https://docs.getdbt.com/docs/dbt-versions/core-upgrade/upgrading-to-fusion)
> 📄 Danh sách hỗ trợ bộ điều hợp đầy đủ: [Các tính năng được hỗ trợ](https://docs.getdbt.com/docs/fusion/supported-features)

## Tầm nhìn mới: Giấy phép hợp nhất
- Thay vì chia tách người dùng giữa Core và Cloud, Fusion hình dung **mọi người đều có giấy phép dbt**
- Người dùng có thể chọn làm việc trong:
- **dbt Cloud IDE** hoặc
- **VS Code** bằng tiện ích mở rộng dbt Labs chính thức
- Cả hai tùy chọn được hỗ trợ bởi cùng một công cụ Fusion

## Quyết định và đề xuất của khóa học
- Khóa học này sử dụng **DuckDB + dbt Core** (cục bộ, thông qua Mã VS) vì:
- Nó buộc người học phải hiểu những gì thực sự đang diễn ra bên trong
- dbt Cloud trừu tượng hóa rất nhiều — hiểu Core trước giúp Cloud dễ dàng tiếp thu sau này
- Nếu bạn theo dõi cùng với dbt Cloud + BigQuery, các khái niệm được truyền tải tốt
- Tài liệu và khóa học riêng của dbt Labs là tài nguyên tuyệt vời để học về dbt Cloud → [dbt Developer Hub](https://docs.getdbt.com)
- **Kết luận:** Không quan trọng bạn học cái nào trước — đặc biệt là với tư cách là nhà tư vấn, bạn có thể sẽ sử dụng cả hai. Tập trung vào các nguyên tắc cơ bản được chia sẻ.

---

*Lưu ý: Tài liệu này được cập nhật lần cuối vào tháng 2 năm 2026. Để biết thông tin mới nhất về hỗ trợ bộ chuyển đổi và dbt Fusion, hãy luôn tham khảo tài liệu dbt chính thức.*
