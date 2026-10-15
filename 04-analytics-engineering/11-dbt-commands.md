---
video_url: https://www.youtube.com/watch?v=t4OeWHW3SsA
prev_url: 10-dbt-packages.md
next_url: ../05-data-platforms/01-introduction.md
---
# lệnh dbt

> 📄 Tài liệu chính thức: [tham chiếu lệnh dbt](https://docs.getdbt.com/reference/dbt-commands)
> 📄 Cú pháp lựa chọn: [Cú pháp chọn nút](https://docs.getdbt.com/reference/node-selection/syntax)

Chúng ta đã sử dụng các lệnh dbt trong suốt loạt bài này mà không thực sự dừng lại để nói về tất cả chúng. Video này là chuyến tham quan đầy đủ — mọi lệnh bạn sẽ thực sự sử dụng, cùng với những lá cờ khiến chúng trở nên mạnh mẽ. Tốt nhất để đánh dấu.


---

## Các lệnh thiết lập — chạy các lệnh này một lần (hoặc khi cần)

### dbt khởi tạo

Tạo dự án dbt của bạn từ đầu. Tạo cấu trúc thư mục đầy đủ — `models/`, `seeds/`, `snapshots/`, `tests/`, `analysis/`, tất cả. Bạn chỉ chạy cái này một lần, ngay từ đầu.

### dbt gỡ lỗi

Kiểm tra xem `profiles.yml` của bạn có hợp lệ không và dbt đó thực sự có thể kết nối với kho của bạn hay không. Chạy nó bất cứ khi nào bạn đang thiết lập một môi trường mới hoặc có điều gì đó không ổn với kết nối của bạn.

### dbt phụ thuộc vào

Cài đặt các gói từ `packages.yml` của bạn. Chúng tôi đã đề cập đến vấn đề này trong phiên bản 4.5.3 — chỉ cần biết rằng nó cũng nằm trong đội hình chỉ huy.

### dbt sạch

Xóa các thư mục được liệt kê trong `clean-targets` trong `dbt_project.yml` của bạn. Theo mặc định đó là `target/` và `dbt_packages/`. Hữu ích cho một sự khởi đầu mới, nhưng hãy nhớ rằng bạn sẽ cần chạy lại `dbt deps` sau khi dọn dẹp nếu bạn đã xóa `dbt_packages/`. Bạn có thể thêm các thư mục khác vào `clean-targets` nếu muốn.

> 📄 [dbt clean — docs](https://docs.getdbt.com/reference/commands/clean)

---

## Các lệnh dành riêng cho tính năng

Chúng được gắn với các tính năng dbt cụ thể hơn là mục đích chung.

### hạt giống dbt

Tải tất cả các CSV trong thư mục `seeds/` của bạn vào kho. Nhanh chóng và đơn giản — tuyệt vời cho dữ liệu tham khảo hoặc các bảng tra cứu nhỏ.

### ảnh chụp nhanh dbt

Chạy bất kỳ ảnh chụp nhanh nào bạn đã xác định trong dự án của mình. Ảnh chụp nhanh là cách dbt theo dõi cách dữ liệu nguồn thay đổi theo thời gian (hãy nghĩ đến SCD Loại 2). Không phải thứ bạn sử dụng hàng ngày nhưng nó luôn ở đó khi bạn cần.

### độ tươi của nguồn dbt

Kiểm tra xem dữ liệu nguồn của bạn có cũ không. Nếu bạn đã xác định các khối `freshness` trong YAML nguồn của mình (chúng tôi đã đề cập đến vấn đề này trong 4.5.2), thì đây là lệnh thực sự chạy kiểm tra.

### tài liệu dbt tạo / tài liệu dbt phục vụ

`dbt docs generate` biên dịch tài liệu YAML, mã mô hình và siêu dữ liệu kho của bạn thành một tạo phẩm `catalog.json` trong `target/`. `dbt docs serve` tạo ra một trang web địa phương (localhost:8080) để bạn có thể duyệt qua nó. Trên dbt Cloud, `docs serve` không cần thiết - nó được xử lý tự động. Đối với người dùng dbt Core, việc tìm ra một cách có thể mở rộng để lưu trữ trang tài liệu đó là điều bạn cần phải tự mình giải quyết.

> 📄 [lệnh tài liệu dbt — docs](https://docs.getdbt.com/reference/commands/cmd-docs)

---

## Bốn yếu tố lớn — đây là trình điều khiển hàng ngày của bạn

### dbt biên dịch

Có vẻ như nó chẳng có tác dụng gì nhưng thực ra lại rất hữu ích. Nhận tất cả các mô hình của bạn — với các lệnh gọi Jinja, `ref()`, `source()` và mọi thứ — và xuất SQL được phân giải đầy đủ thành `target/compiled/`. Không có dữ liệu di chuyển, không có gì vào kho. Đó chỉ là SQL thuần túy để bạn kiểm tra.

Tại sao phải bận tâm? Hai lý do. Đầu tiên, đó là cách nhanh nhất để phát hiện lỗi Jinja — nhanh hơn nhiều so với việc chờ `dbt run` đầy đủ. Thứ hai, nó hoàn toàn miễn phí — không tính toán, không tốn chi phí lưu kho. Thói quen tốt để chạy sau khi thực hiện thay đổi.

> 📄 [biên dịch dbt — docs](https://docs.getdbt.com/reference/commands/compile)

### dbt chạy

Hiện thực hóa mọi mô hình trong dự án của bạn. Chế độ xem trở thành chế độ xem, bảng trở thành bảng, mô hình gia tăng được áp dụng logic gia tăng — bất kể bạn đã định cấu hình gì. Các mô hình chạy theo thứ tự phụ thuộc, do đó dbt sẽ tìm ra trình tự cho bạn.

Đây là điều bạn nên làm trong quá trình phát triển tích cực khi bạn chỉ muốn xem các mô hình của mình được xây dựng.

> 📄 [dbt run — docs](https://docs.getdbt.com/reference/commands/run)

### kiểm tra dbt

Chạy tất cả các thử nghiệm trong dự án của bạn - thử nghiệm chung, thử nghiệm đơn lẻ, thử nghiệm đơn vị, tất cả. Báo cáo đạt/không đạt ở cuối. Không có gì được xây dựng ở đây, nó chỉ xác nhận những gì đã có trong kho.

> 📄 [kiểm tra dbt — tài liệu](https://docs.getdbt.com/reference/commands/test)

### bản dựng dbt ⭐

Lệnh quan trọng nhất. Đó là sự kết hợp thông minh của `dbt run` + `dbt test` + `dbt seed` + `dbt snapshot`, tất cả trong một. Nhưng nó không chỉ chạy chúng một cách tuần tự - nó còn nhận biết DAG. Nó biết thứ tự đúng và nếu có lỗi xảy ra trong quá trình thực hiện, nó sẽ bỏ qua mọi thứ phía sau lỗi đó thay vì lãng phí tính toán vào các mô hình sắp hỏng.

Đây là những gì bạn muốn cho CI, quá trình sản xuất hoặc bất kỳ lúc nào bạn cần sự tự tin rằng toàn bộ dự án của bạn đều ổn định.

> 📄 [bản dựng dbt — tài liệu](https://docs.getdbt.com/reference/commands/build)

### dbt thử lại

Nếu `dbt build` hoặc `dbt run` bị lỗi giữa chừng, đừng chạy lại toàn bộ từ đầu. `dbt retry` thực thi lại từ điểm bị lỗi bằng cách đọc tệp `run_results.json` từ lần chạy trước. Nó tự động xác định các nút nào bị lỗi và chạy lại các nút đó cùng với mọi thứ ở phía dưới chúng.

Cách hoạt động:
- dbt xem xét `target/run_results.json` từ lệnh cuối cùng
- Nó xác định các nút bị lỗi và các nút bị bỏ qua (bất cứ thứ gì ở phía dưới của lỗi)
- Nó chỉ chạy lại các nút đó, sử dụng lại cùng tiêu chí lựa chọn từ lệnh ban đầu
- Nếu lệnh trước đó hoàn tất thành công, `dbt retry` kết thúc dưới dạng
không hoạt động
Tiết kiệm rất nhiều thời gian cho các dự án lớn, đặc biệt khi một mô hình duy nhất bị lỗi sâu trong DAG.

---

## Cờ - những cờ quan trọng

### --help / -h

Hoạt động trên bất kỳ lệnh nào. `dbt --help` cung cấp cho bạn danh sách đầy đủ, `dbt run --help` cung cấp cho bạn các cờ dành riêng cho `run`. Những thứ tiêu chuẩn, nhưng đáng để biết nó ở đó.

### --version / -V

Cho bạn biết phiên bản dbt nào bạn đã cài đặt. Đồng thời cho bạn biết nếu có bản cập nhật.

### --làm mới đầy đủ / -f

Được sử dụng với `dbt run` hoặc `dbt build`. Khi bạn có một mô hình gia tăng, nó thường chỉ thêm các hàng mới. `--full-refresh` bỏ toàn bộ và xây dựng lại từ đầu. Hữu ích khi dữ liệu lịch sử đã thay đổi, bạn có dữ liệu trùng lặp hoặc bạn chỉ muốn đảm bảo mọi thứ đều sạch sẽ. Hầu hết các nhóm đều thực hiện việc này theo lịch trình thường xuyên - có thể mỗi tháng một lần - chỉ để giữ mọi thứ ngăn nắp.

```bash
dbt run --full-refresh
```

### --
không nhanh
Chạy phiên bản chặt chẽ hơn của dbt. Thông thường, các cảnh báo không dừng quá trình thực thi — với `--fail-fast` thì điều đó sẽ xảy ra. Tốt cho CI hoặc bất cứ lúc nào bạn muốn chắc chắn rằng không có gì lọt qua. Thà thất bại một cách ồn ào còn hơn là dễ dãi và tìm thấy những điều bất ngờ sau đó.

### --target / -t

Kiểm soát dbt mục tiêu hồ sơ nào sẽ chạy theo. Theo mặc định, mọi thứ đều chạy trên `dev`. Nhưng bạn có thể ghi đè lên nó:

```bash
dbt run --target prod
```

Hoạt động với `dbt run`, `dbt build`, `dbt test`, `dbt snapshot` — về cơ bản là bất kỳ lệnh nào chạm vào kho. Cách thực hành tốt nhất: nhà phát triển làm việc trong `dev`, quá trình sản xuất sử dụng `--target prod`.

### --select / -s

Đây là cái lớn. Cho phép bạn chỉ chạy các phần cụ thể của dự án thay vì chạy mọi thứ. Có một số cách để sử dụng nó:

**Theo tên mẫu máy** — chỉ cần đặt tên mẫu máy (không cần `.sql`):

```bash
dbt run --select stg_green_tripdata
```

**Theo đường dẫn thư mục** — mọi thứ trong một thư mục:

```bash
dbt run --select models/staging
```

**Theo thẻ:**

```bash
dbt run --select tag:nightly
```

**Với các toán tử đồ thị (dấu +)** — đây là lúc nó thực sự hữu ích. `+` cho phép bạn lấy các phần phụ thuộc ngược dòng hoặc xuôi dòng:

```bash
# Run stg_green_tripdata and all upstream dependencies
dbt run --select +stg_green_tripdata

# Run fct_trips and all downstream dependencies
dbt run --select fct_trips+

# Run dim_zones plus everything upstream AND downstream
dbt run --select +dim_zones+
```

- `+my_model` — xây dựng `my_model` và mọi thứ ở thượng nguồn của nó (tất cả các tổ tiên của nó)
- `my_model+` — xây dựng `my_model` và mọi thứ ở hạ lưu của nó (tất cả các hậu duệ của nó)
- `+my_model+` — cả hai hướng. Mọi thứ ở thượng nguồn, chính mô hình và mọi thứ ở hạ nguồn

> 📄 [Toán tử đồ thị — docs](https://docs.getdbt.com/reference/node-selection/graph-operators)

**Với bộ chọn trạng thái** — thay vì đoán xem điều gì đã thay đổi, hãy để dbt tìm hiểu:

```bash
dbt build --select state:modified+ --state ./prod-artifacts
```

- `state:new` — chỉ các tệp bạn vừa tạo
- `state:modified` — mọi thứ đã thay đổi kể từ lần chạy cuối cùng
- Thêm `+` sau để bao gồm các phần phụ thuộc xuôi dòng của các mô hình đã sửa đổi

Cách hoạt động của so sánh trạng thái:
- Bạn cần các tạo phẩm từ **lần chạy trước** được lưu trữ ở đâu đó liên tục (không phải cùng thư mục `target/` mà bạn hiện đang ghi vào)
- Trên **dbt Cloud**, việc này được xử lý tự động — các tạo phẩm sản xuất được lưu trữ và có thể truy cập để so sánh
- Trên **dbt Core**, bạn cần lưu trữ các tạo phẩm theo cách thủ công (đặc biệt là `manifest.json`) ở đâu đó — một nhóm đám mây, một thư mục riêng, kiểm soát phiên bản, v.v.
- Trỏ `--state` đến nơi tồn tại của các tạo phẩm trước đó
- dbt so sánh mã hiện tại của bạn với các tạo phẩm đó để xác định xem
có gì mới hoặc được sửa đổi
Điều quan trọng là bạn đang so sánh với *các tạo phẩm của môi trường khác* (thường là sản xuất) hoặc *thời điểm trước đó* — không phải với thư mục mà bạn hiện đang xây dựng. Điều này cho phép bạn chỉ chạy những gì đã thay đổi kể từ lần triển khai sản xuất gần đây nhất của bạn, điều này cực kỳ hữu ích cho quy trình công việc CI/CD.

Việc lưu trữ liên tục các tạo phẩm JSON đó nói chung cũng chỉ là một phương pháp hay — bạn có thể sử dụng chúng để phân tích dự án của mình phát triển như thế nào theo thời gian.

> 📄 [Cú pháp chọn nút — docs](https://docs.getdbt.com/reference/node-selection/syntax)
