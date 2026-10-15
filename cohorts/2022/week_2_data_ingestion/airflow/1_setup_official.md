## Cài đặt (Chính thức)

### Yêu cầu trước

1. Để tiêu chuẩn hóa cấu hình của hội thảo này,
đổi tên tệp gcp-service-accounts-credentials của bạn thành `google_credentials.json` và lưu trữ nó trong thư mục `$HOME`
    ``` bash
        cd ~ && mkdir -p ~/.google/credentials/
        mv <path/to/your/service-account-authkeys>.json ~/.google/credentials/google_credentials.json
    ```

2. Bạn có thể cần nâng cấp phiên bản docker-compose của mình lên v2.x+ và đặt bộ nhớ cho Docker Engine của bạn ở mức tối thiểu 5GB
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
    echo -e "AIRFLOW_UID=$(id -u)" > .env
    ```

Trên Windows có thể bạn cũng sẽ cần nó. Nếu bạn sử dụng MINGW/GitBash, hãy thực hiện lệnh tương tự.

Để loại bỏ cảnh báo ("AIRFLOW_UID chưa được đặt"), bạn có thể tạo tệp `.env` với
nội dung này:

    ```
    AIRFLOW_UID=50000
    ```

   
3. **Nhập tệp thiết lập docker chính thức** từ phiên bản Airflow mới nhất:
   ```shell
   curl -LfO 'https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml'
   ```
   
4. Có thể bạn sẽ choáng ngợp khi thấy có rất nhiều dịch vụ ở đây.
Nhưng đây chỉ là mẫu bắt đầu nhanh và khi tiếp tục, bạn sẽ tìm ra những dịch vụ không sử dụng nào có thể bị xóa.
Ví dụ. [Đây là](docker-compose-nofrills.yml) phiên bản đơn giản của mẫu đó.

5. **Bản dựng Docker**:

Khi muốn chạy Airflow cục bộ, bạn có thể muốn sử dụng hình ảnh mở rộng,
chứa một số phần phụ thuộc bổ sung - ví dụ: bạn có thể thêm gói python mới,
hoặc nâng cấp nhà cung cấp luồng khí lên phiên bản mới hơn.
    
Tạo `Dockerfile` trỏ đến phiên bản Airflow bạn vừa tải xuống,
chẳng hạn như `apache/airflow:2.2.3`, làm hình ảnh cơ sở,
       
Và tùy chỉnh `Dockerfile` này bằng cách:
* Thêm các gói tùy chỉnh của bạn sẽ được cài đặt. Thứ chúng ta cần nhất là `gcloud` để kết nối với nhóm GCS/Hồ dữ liệu.
* Ngoài ra, tích hợp `requirements.txt` để cài đặt thư viện qua `pip install`

6. **Soạn Docker**:

Quay lại `docker-compose.yaml` của bạn:
* Trong `x-airflow-common`:
* Xóa thẻ `image`, để thay thế nó bằng `build` từ Dockerfile của bạn, như được hiển thị
* Gắn `google_credentials` của bạn vào Phần `volumes` dưới dạng
chỉ đọc * Đặt các biến môi trường: `GCP_PROJECT_ID`, `GCP_GCS_BUCKET`, `GOOGLE_APPLICATION_CREDENTIALS` & `AIRFLOW_CONN_GOOGLE_CLOUD_DEFAULT`, theo cấu hình của bạn.
* Thay đổi `AIRFLOW__CORE__LOAD_EXAMPLES` thành `false` (tùy chọn)

7. Đây là giao diện của phiên bản cuối cùng của [Dockerfile](./Dockerfile) và [docker-compose.yml](./docker-compose.yaml).


## Sự cố

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
