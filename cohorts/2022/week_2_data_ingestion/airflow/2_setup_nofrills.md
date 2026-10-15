## Cài đặt (Không rườm rà)

### Yêu cầu trước

1. Để tiêu chuẩn hóa cấu hình của hội thảo này,
đổi tên tệp gcp-service-accounts-credentials của bạn thành `google_credentials.json` và lưu trữ nó trong thư mục `$HOME`
    ``` bash
        cd ~ && mkdir -p ~/.google/credentials/
        mv <path/to/your/service-account-authkeys>.json ~/.google/credentials/google_credentials.json
    ```

2. Bạn có thể cần nâng cấp phiên bản docker-compose của mình lên v2.x+ và đặt bộ nhớ cho Docker Engine của bạn ở mức tối thiểu 4GB
(lý tưởng nhất là 8GB). Nếu không phân bổ đủ bộ nhớ, điều này có thể khiến máy chủ web luồng khí liên tục khởi động lại.

3. Phiên bản Python: 3.7+


### Thiết lập luồng khí

1. Tạo một thư mục con mới có tên `airflow` trong thư mục `project` của bạn (chẳng hạn như thư mục chúng tôi hiện đang ở)
   
2. **Đặt người dùng Luồng khí**:

Trên Linux, khởi động nhanh cần biết id người dùng máy chủ của bạn và cần đặt id nhóm thành 0.
Nếu không, các tệp được tạo trong `dags`, `logs` và `plugins` sẽ được tạo bằng người dùng root.
Bạn phải đảm bảo định cấu hình chúng cho docker-compose:

    ```bash
    mkdir -p ./dags ./logs ./plugins
    echo -e "AIRFLOW_UID=$(id -u)" >> .env
    ```

Trên Windows có thể bạn cũng sẽ cần nó. Nếu bạn sử dụng MINGW/GitBash, hãy thực hiện lệnh tương tự.

Để loại bỏ cảnh báo ("AIRFLOW_UID chưa được đặt"), bạn có thể tạo tệp `.env` với
nội dung này:

    ```
    AIRFLOW_UID=50000
    ```

3. **Bản dựng Docker**:

Khi muốn chạy Airflow cục bộ, bạn có thể muốn sử dụng hình ảnh mở rộng,
chứa một số phần phụ thuộc bổ sung - ví dụ: bạn có thể thêm gói python mới,
hoặc nâng cấp nhà cung cấp luồng khí lên phiên bản mới hơn.
    
Tạo `Dockerfile` trỏ đến phiên bản Airflow mới nhất như `apache/airflow:2.2.3`, cho hình ảnh cơ sở,
       
Và tùy chỉnh `Dockerfile` này bằng cách:
* Thêm các gói tùy chỉnh của bạn sẽ được cài đặt. Thứ chúng ta cần nhất là `gcloud` để kết nối với nhóm GCS (Data Lake).
* Ngoài ra, tích hợp `requirements.txt` để cài đặt thư viện qua `pip install`

4. Sao chép [docker-compose-nofrills.yml](docker-compose-nofrills.yml), [.env_example](.env_example) & [entrypoint.sh](scripts/entrypoint.sh) từ kho lưu trữ này.
Các thay đổi so với thiết lập chính thức là:
* Xóa hàng đợi `redis`, `worker`, `triggerer`, `flower` & `airflow-init` dịch vụ,
và thay đổi từ `CeleryExecutor` (đa nút) sang chế độ `LocalExecutor` (nút đơn)
* Bao gồm `.env` để tham số hóa và tính linh hoạt tốt hơn
* Bao gồm `entrypoint.sh` đơn giản vào vùng chứa `webserver`, chịu trách nhiệm khởi tạo cơ sở dữ liệu và tạo người dùng đăng nhập (quản trị viên).
* Đã cập nhật `Dockerfile` để cấp quyền thực thi `scripts/entrypoint.sh`
        
5. `.env`:
* Xây dựng lại tệp `.env` của bạn bằng cách tạo một bản sao của `.env_example` (nhưng hãy đảm bảo `AIRFLOW_UID` của bạn vẫn còn):
        ```shell
        mv .env_example .env
        ```
* Đặt các biến môi trường `AIRFLOW_UID`, `GCP_PROJECT_ID` & `GCP_GCS_BUCKET`, theo cấu hình của bạn.
* Tùy chọn, nếu `google-credentials.json` của bạn được lưu trữ ở một nơi khác, chẳng hạn như đường dẫn như `$HOME/.gc`,
sửa đổi các env-vars (`GOOGLE_APPLICATION_CREDENTIALS`, `AIRFLOW_CONN_GOOGLE_CLOUD_DEFAULT`) và đường dẫn `volumes` trong `docker-compose-nofrills.yml`

6. Đây là giao diện của phiên bản cuối cùng của [Dockerfile](./Dockerfile) và [docker-compose-nofrills](./docker-compose-nofrills.yml).


## Sự cố

### `no-frills setup does not work for me - WSL/Windows user `

Nếu bạn đang chạy Docker trong Windows/WSL/WSL2 và gặp phải một số vấn đề về `ModuleNotFoundError` hoặc hiệu suất thấp, hãy xem [Ý chính của Airflow & WSL2](https://gist.github.com/nervuzz/d1afe81116cbfa3c834634ebce7f11c5) tập trung hoàn toàn vào việc khắc phục các sự cố có thể xảy ra.

### `File /.google/credentials/google_credentials.json was not found`

Trước tiên, hãy đảm bảo bạn có thông tin xác thực trong `$HOME/.google/credentials` của mình.
Có thể bạn đã bỏ lỡ bước này và không sao chép JSON bằng thông tin xác thực ở đó?
Ngoài ra, hãy đảm bảo tên tệp là `google_credentials.json`.

Thứ hai, kiểm tra xem docker-compose có thể ánh xạ chính xác thư mục này tới nhân viên luồng không khí hay không.

Thực thi `docker ps` để xem danh sách các bộ chứa docker đang chạy trên máy chủ của bạn và tìm ID của nhân viên luồng khí.

Sau đó thực thi `bash` trên vùng chứa này:

```bash
docker exec -it <container-ID> bash
```

Bây giờ hãy kiểm tra xem tệp có thông tin xác thực có thực sự ở đó không:

```bash
ls -lh /.google/credentials/
```

Nếu nó trống, docker-compose không thể ánh xạ thư mục có thông tin xác thực.
Trong trường hợp này, hãy thử thay đổi nó thành đường dẫn tuyệt đối tới thư mục này:

```yaml
  volumes:
    - ./dags:/opt/airflow/dags
    - ./logs:/opt/airflow/logs
    - ./plugins:/opt/airflow/plugins
    # here: ----------------------------
    - c:/Users/alexe/.google/credentials/:/.google/credentials:ro
    # -----------------------------------
```
