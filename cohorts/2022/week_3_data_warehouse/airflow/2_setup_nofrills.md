## Thiết lập (Không rườm rà)

### Yêu cầu trước

1. Để tiêu chuẩn hóa cấu hình của hội thảo này,
    rename your gcp-service-accounts-credentials file to `google_credentials.json` & store it in your `$HOME` directory
    ``` bash
        cd ~ && mkdir -p ~/.google/credentials/
        mv <path/to/your/service-account-authkeys>.json ~/.google/credentials/google_credentials.json
    ```

2. Bạn có thể cần nâng cấp phiên bản soạn thảo docker của mình lên v2.x+ và đặt bộ nhớ cho Docker Engine của bạn ở mức tối thiểu 4GB
(lý tưởng nhất là 8GB). Nếu không phân bổ đủ bộ nhớ, điều này có thể khiến máy chủ web luồng khí liên tục khởi động lại.

3. Phiên bản Python: 3.7+


### Thiết lập luồng khí

1. Tạo thư mục con mới có tên `airflow` trong thư mục `project` của bạn (chẳng hạn như thư mục chúng tôi hiện đang sử dụng)
   
2. **Đặt người dùng luồng khí**:

    On Linux, the quick-start needs to know your host user-id and needs to have group id set to 0. 
    Otherwise the files created in `dags`, `logs` and `plugins` will be created with root user. 
    You have to make sure to configure them for the docker-compose:

    ```bash
    mkdir -p ./dags ./logs ./plugins
    echo -e "AIRFLOW_UID=$(id -u)" >> .env
    ```

    On Windows you will probably also need it. If you use MINGW/GitBash, execute the same command. 

    To get rid of the warning ("AIRFLOW_UID is not set"), you can create `.env` file with
    this content:

    ```
    AIRFLOW_UID=50000
    ```

3. **Docker Build**:

    When you want to run Airflow locally, you might want to use an extended image, 
    containing some additional dependencies - for example you might add new python packages, 
    or upgrade airflow providers to a later version.
    
    Create a `Dockerfile` pointing to the latest Airflow version such as `apache/airflow:2.2.3`, for the base image,
       
    And customize this `Dockerfile` by:
    * Adding your custom packages to be installed. The one we'll need the most is `gcloud` to connect with the GCS bucket (Data Lake).
    * Also, integrating `requirements.txt` to install libraries via  `pip install`

4. Sao chép [docker-compose-nofrills.yml](docker-compose-nofrills.yml), [.env_example](.env_example) & [entrypoint.sh](scripts/entrypoint.sh) từ kho lưu trữ này.
    The changes from the official setup are:
    * Removal of `redis` queue, `worker`, `triggerer`, `flower` & `airflow-init` services, 
    and changing from `CeleryExecutor` (multi-node) mode to `LocalExecutor` (single-node) mode 
    * Inclusion of `.env` for better parametrization & flexibility
    * Inclusion of simple `entrypoint.sh` to the `webserver` container, responsible to initialize the database and create login-user (admin).
    * Updated `Dockerfile` to grant permissions on executing `scripts/entrypoint.sh`
        
5. `.env`:
    * Rebuild your `.env` file by making a copy of `.env_example` (but make sure your `AIRFLOW_UID` remains):
        ```shell
        mv .env_example .env
        ```
    * Set environment variables `AIRFLOW_UID`, `GCP_PROJECT_ID` & `GCP_GCS_BUCKET`, as per your config.
    * Optionally, if your `google-credentials.json` is stored somewhere else, such as a path like `$HOME/.gc`, 
    modify the env-vars (`GOOGLE_APPLICATION_CREDENTIALS`, `AIRFLOW_CONN_GOOGLE_CLOUD_DEFAULT`) and `volumes` path in `docker-compose-nofrills.yml`

6. Đây là giao diện của phiên bản cuối cùng của [Dockerfile](./Dockerfile) và [docker-compose-nofrills](./docker-compose-nofrills.yml).


## Sự cố

### `no-frills setup does not work for me - WSL/Windows user `

Nếu bạn đang chạy Docker trong Windows/WSL/WSL2 và bạn đã gặp phải một số vấn đề về `ModuleNotFoundError` hoặc hiệu suất thấp, hãy xem [Ý chính của Airflow & WSL2](https://gist.github.com/nervuzz/d1afe81116cbfa3c834634ebce7f11c5) này tập trung hoàn toàn vào việc khắc phục các sự cố có thể xảy ra.

### `File /.google/credentials/google_credentials.json was not found`

Trước tiên, hãy đảm bảo bạn có thông tin xác thực trong `$HOME/.google/credentials` của mình. Có thể bạn đã bỏ lỡ bước này và không sao chép JSON bằng thông tin xác thực ở đó? Ngoài ra, hãy đảm bảo tên tệp là `google_credentials.json`.

Thứ hai, hãy kiểm tra xem docker-compose có thể ánh xạ chính xác thư mục này tới nhân viên luồng không khí hay không.

Thực thi `docker ps` để xem danh sách các thùng chứa docker đang chạy trên máy chủ của bạn và tìm ID của nhân viên luồng không khí.

Sau đó thực thi `bash` trên vùng chứa này:

```bash
docker exec -it <container-ID> bash
```

Bây giờ hãy kiểm tra xem tệp có thông tin xác thực có thực sự ở đó hay không:

```bash
ls -lh /.google/credentials/
```

Nếu nó trống, docker-compose không thể ánh xạ thư mục có thông tin xác thực. 
Trong trường hợp này, hãy thử thay đổi nó thành đường dẫn tuyệt đối đến thư mục này:

```yaml
  volumes:
    - ./dags:/opt/airflow/dags
    - ./logs:/opt/airflow/logs
    - ./plugins:/opt/airflow/plugins
    # here: ----------------------------
    - c:/Users/alexe/.google/credentials/:/.google/credentials:ro
    # -----------------------------------
```
