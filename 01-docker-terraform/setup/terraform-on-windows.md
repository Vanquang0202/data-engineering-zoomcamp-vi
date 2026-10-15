## GCP và Terraform trên Windows

Bạn không cần những hướng dẫn này nếu bạn sử dụng WSL. Nó chỉ dành cho "Windows thuần túy"

### SDK đám mây của Google

* Đối với hướng dẫn này, bạn sẽ cần một môi trường giống Linux, ví dụ: [GitBash](https://gitforwindows.org/), [MinGW](https://www.mingw-w64.org/) hoặc [cygwin](https://www.cygwin.com/)
* Power Shell cũng sẽ hoạt động nhưng sẽ yêu cầu điều chỉnh
* Tải xuống SDK ở dạng zip: https://dl.google.com/dl/cloudsdk/channels/rapid/google-cloud-sdk.zip
* nguồn: https://cloud.google.com/sdk/docs/downloads-interactive
* Giải nén nó và chạy tập lệnh `install.sh`

Khi cài đặt nó, bạn có thể thấy một cái gì đó tương tự như sau:

```
The installer is unable to automatically update your system PATH. Please add
  C:\tools\google-cloud-sdk\bin
```

* Để khắc phục điều đó, hãy điều chỉnh `.bashrc` của bạn để đưa phần này vào `PATH` ([hướng dẫn](https://unix.stackexchange.com/questions/26047/how-to-correctly-add-a-path-to-path))
* Bạn cũng có thể thực hiện trên toàn hệ thống ([hướng dẫn](https://gist.github.com/nex3/c395b2f8fd4b02068be37c961301caa7))

Bây giờ chúng ta cần trỏ nó để sửa lỗi cài đặt Python. Giả sử bạn sử dụng [Anaconda](https://www.anaconda.com/products/individual):

```bash
export CLOUDSDK_PYTHON=~/Anaconda3/python
```

Bây giờ hãy kiểm tra xem nó có hoạt động không:

```bash
$ gcloud version
Google Cloud SDK 367.0.0
bq 2.0.72
core 2021.12.10
gsutil 5.5
```

### Xác thực SDK Google Cloud

* Bây giờ, hãy tạo một tài khoản dịch vụ và tạo các khóa như được hiển thị trong video
* Tải xuống khóa và đặt nó vào một số vị trí, ví dụ: `.gc/ny-rides.json`
* Đặt `GOOGLE_APPLICATION_CREDENTIALS` trỏ tới file

```bash
export GOOGLE_APPLICATION_CREDENTIALS=~/.gc/ny-rides.json
```

Bây giờ xác thực:

```bash
gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS
```

Ngoài ra, bạn có thể xác thực bằng OAuth như trong video

```bash
gcloud auth application-default login
```

Nếu bạn nhận được thông báo như `quota exceeded`

> CẢNH BÁO:
> Không thể tìm thấy dự án hạn ngạch để thêm vào ADC. Bạn có thể nhận được lỗi "vượt quá hạn ngạch" hoặc "API chưa được bật".
> Chạy `$ gcloud auth application-default set-quota-project` để thêm hạn ngạch dự án.

Sau đó chạy cái này:

```bash
PROJECT_NAME="ny-rides-alexey"
gcloud auth application-default set-quota-project ${PROJECT_NAME}
```

### Địa hình

* [Tải xuống Terraform](https://www.terraform.io/downloads)
* Đặt nó vào một thư mục trong [PATH](https://gist.github.com/nex3/c395b2f8fd4b02068be37c961301caa7)
* Đi đến vị trí có tệp Terraform và khởi tạo nó

```bash
terraform init
```

Tùy chọn, bạn có thể định cấu hình các tệp địa hình (`variables.tf`) để bao gồm id dự án của bạn:

```bash
variable "project" {
  description = "Your GCP Project ID"
  default = "ny-rides-alexey"
  type = string
}
```

* Bây giờ [làm theo hướng dẫn](../12-terraform-overview.md#execution-steps)
* Chạy `terraform plan`
* Tiếp theo, chạy `terraform apply`

Nếu bạn gặp lỗi như vậy:

> Lỗi: googleapi: Lỗi 403: terraform@ny-rides-alexey.iam.gserviceaccount.com không có
> storage.buckets.create quyền truy cập vào dự án Google Cloud.,
bị cấm
Sau đó, bạn cần cấp cho tài khoản dịch vụ của mình tất cả các quyền. Đảm bảo bạn làm theo hướng dẫn trong video

* Bạn cũng có thể sử dụng [tệp này](https://docs.google.com/document/d/e/2PACX-1vSZapy7gIj0TP-EFzub2OpAlAkuifGEVJ4XpkA1RvxZ45NjiQi29b6OhLuetdXXHWAn2lbbKxnbzMdd/pub), nhưng nó không liệt kê tất cả các quyền cần thiết
