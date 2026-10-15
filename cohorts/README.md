# Các khóa học theo năm

Giáo trình hiện tại — gồm mọi module, bài học, hình ảnh và ví dụ code — nằm ở
**thư mục gốc của repository**, không nằm ở đây. `cohorts/<year>/` chỉ chứa
những nội dung riêng của từng khóa: lịch học, bài tập và (đối với khóa cũ)
bản lưu giáo trình đúng như đã giảng dạy trong năm đó.

**2027 là khóa hiện tại. Hãy sửa giáo trình ở thư mục gốc, không sửa trong
`cohorts/2027/`.** Thông tin này được khai báo một lần tại thư mục gốc để máy
có thể đọc: `course.yaml:current_cohort` xác định khóa hiện tại, còn
`course.yaml:cohorts` liệt kê mọi khóa và vị trí lưu nội dung. Lưu ý khóa 2027
hiện chưa được công bố (`published: false` trong `cohorts/2027/cohort.yaml`),
ngày tháng còn là giá trị tạm và bài tập vẫn mang nhãn `[DRAFT]`. Quá trình
chuyển schema chỉ giữ nguyên trạng thái bản nháp, không hoàn tất nội dung này.

## Cấu trúc

```
<repo root>/
├── course.yaml                   # course identity, incl. the description and cohorts index
├── 01-docker-terraform/          # the directory name IS the module slug
│   ├── module.yaml                 # module identity and unit list
│   ├── README.md                   # GitHub-facing module index, not published
│   ├── 01-introduction.md          # units: NN-kebab.md, the stem IS the unit slug
│   ├── 02-virtual-environment.md
│   └── images/                     # every image the module's units reference
├── ...
└── cohorts/
    ├── README.md                  # this file
    ├── 2027/                      # the directory name IS the cohort identifier
    │   ├── cohort.yaml            # dates, curriculum: current, homework list
    │   ├── README.md              # the human-readable schedule
    │   └── homework/
    │       ├── 01-docker-terraform/
    │       │   ├── homework.md    # homework instructions, fixed name
    │       │   └── homework.yaml  # homework identity, due date, form, questions
    │       └── ...
    ├── 2026/                      # earlier cohorts: frozen, full copies
    ├── 2025/
    ├── 2024/
    ├── 2023/
    └── 2022/
```

Hai quy tắc quan trọng nhất:

- **Tên chính là định danh.** Slug của module và bài học được lấy từ tên thư mục
  và tên file. YAML không khai báo lại các tên này; đổi tên sẽ làm thay đổi
  URL đã công bố.
- **Mỗi thư mục module tự chứa nội dung của mình.** Bài học, hình ảnh và code
  nằm bên trong; các file bài học cùng cấp với `module.yaml`. Link tương đối
  chỉ đi ra ngoài thư mục module khi trỏ tới module cùng cấp hoặc thư mục gốc.
  Với nội dung xa hơn, hãy dùng URL GitHub tuyệt đối.

## Khóa hiện tại và khóa được lưu trữ

File `cohort.yaml` cho biết khóa thuộc loại nào:

- **`curriculum: current`** — khóa học dùng giáo trình hiện có ở thư mục gốc.
  `cohorts/<year>/` chỉ chứa ngày tháng và bài tập
  (`cohorts/<year>/homework/<module>/`); không có bản sao module hay bài học
  tại đây để tránh nội dung khác với bản gốc.
- **`curriculum: github_archive`** — giáo trình của khóa khác đáng kể so với
  giáo trình hiện tại, nên được lưu thành bản độc lập gồm đầy đủ các module
  đã dạy. Bản này chỉ dành cho người đọc trên GitHub, không bao giờ được nhập
  lại làm nội dung hiện tại. Từ `cohorts/2022/` đến `cohorts/2026/` là các
  bản lưu trữ, được bổ sung `cohort.yaml` tối thiểu sau này. Cấu trúc bên
  trong (thư mục module, cách đánh số/đặt tên khác nhau theo năm — `week_N_*`
  ở 2022/2023, `01`-`06` ở 2024/2025, và chỉ từ 2026 mới có `01`-`07` giống
  2027) vẫn là nội dung trước khi chuyển schema, không được sắp xếp lại theo
  quy ước hiện tại. Vì vậy, `course.yaml:cohorts` đánh dấu cả năm khóa này
  là `legacy: true`.

## Chỉnh sửa

- Sửa nội dung giáo trình (bài học, hình ảnh, code) tại **thư mục gốc**.
  Pull request cho khóa hiện tại được tiếp nhận tại đây.
- Sửa lịch học hoặc bài tập của khóa hiện tại trong `cohorts/2027/`.
- Các khóa cũ là bản lưu trữ; những khác biệt phản ánh nội dung thực tế đã dạy.
  Chỉ cập nhật các lỗi sai thực tế hoặc lỗi gây hỏng, và sửa riêng cho từng khóa.
- Slug đã công bố phải được giữ nguyên. Đổi tên slug là quyết định của nền tảng,
  không phải thay đổi thông qua pull request vào repository.

## Nguồn quy ước

Repository này không trình bày lại các quy ước. Nguồn chuẩn là
`DataTalksClub/zoomcamp-ops`: `STRUCTURE.md` mô tả cấu trúc repository,
`docs/shared-curriculum-v2.md` mô tả schema dùng chung ở thư mục gốc,
còn tài liệu curriculum contract bên cạnh quy định schema YAML và các quy tắc
cho trang bài học.

Parser Data Ingestion của website là nguồn kiểm tra cuối cùng và sẽ báo lỗi
rõ ràng khi push nếu nội dung không hợp lệ.
