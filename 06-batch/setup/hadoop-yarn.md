## Tia lửa trên YARN

Đối với mô-đun Spark và Docker, chúng tôi cần YARN,
đi kèm với Hadoop. Vì vậy chúng ta cần cài đặt Hadoop

Trong tài liệu này, chúng tôi giả sử bạn sử dụng Linux. Đối với Windows, hãy sử dụng WSL. Nó cũng sẽ hoạt động (được cho là) ​​trên MacOS.

Chúng ta sẽ cần chạy nó ở chế độ phân phối giả.


### Cấu hình ssh

Bạn cần chạy `ssh` vào localhost của mình mà không cần phải nhập bất kỳ mật khẩu nào. Nói cách khác, bạn thực thi

```bash
ssh localhost
```

Và bạn có quyền truy cập ssh.

Nếu bạn không có nó, hãy thêm khóa `id_rsa.pub` của bạn vào danh sách các khóa được phép truy cập vào máy tính của bạn:

```bash
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
chmod 0600 ~/.ssh/authorized_keys
```

(Điều này giả sử bạn đã có `id_rsa.pub` trong `~/.ssh`)

Trên WSL, bạn có thể cần khởi động dịch vụ ssh:

```bash
sudo service ssh start
```

### Tải xuống các tệp nhị phân Hadoop

Chúng tôi sử dụng Spark mong đợi phiên bản Hadoop 3.2. Vì vậy, chúng tôi sẽ cài đặt nó.

Truy cập [trang web của Hadoop](https://www.apache.org/dyn/closer.cgi/hadoop/common/hadoop-3.2.3/hadoop-3.2.3.tar.gz) để lấy chiếc gương gần nhất. Và sau đó tải xuống:

```bash
wget https://dlcdn.apache.org/hadoop/common/hadoop-3.2.3/hadoop-3.2.3.tar.gz
```

Giải nén nó và vào thư mục này

```bash
tar xzfv hadoop-3.2.3.tar.gz
cd hadoop-3.2.3/
```


### YARN trên một nút

Đặt `JAVA_HOME` trong `etc/hadoop/hadoop-env.sh`:

```bash
echo "export JAVA_HOME=${JAVA_HOME}" >> etc/hadoop/hadoop-env.sh
```

Bắt đầu SỢI

```bash
./sbin/start-yarn.sh
```

YARN sẽ hoạt động trên cổng 8088: http://localhost:8088/


### Chạy Spark trên YARN

Để gửi công việc tia lửa, chúng tôi sẽ cần sử dụng `master="yarn"`.

Spark cần biết nơi tìm tệp cấu hình YARN, vì vậy chúng ta cần đặt nó:


```bash
export HADOOP_HOME="${HOME}/spark/hadoop-3.2.3"
export YARN_CONF_DIR="${HADOOP_HOME}/etc/hadoop"
```

Sau đó chạy Jupyter hoặc sử dụng spark-submit.


### Kết nối Spark và YARN với GCS

Tải xuống trình kết nối GCS:

```bash
gsutil cp gs://hadoop-lib/gcs/gcs-connector-hadoop3-2.2.5.jar .
```

Thay đổi cấu hình:

* Thay đổi `${SPARK_HOME}/conf/spark-defaults.conf` (xem [tại đây]())
* Thay đổi `${YARN_CONF_DIR}/core-site.xml` (xem [tại đây](config/core-site.xml))

Mẫu cho thuộc tính hadoop:

```xml
  <property>
    <name></name>
    <value></value>
  </property>
```

### Spark và YARN với Docker

Sao chép cấu hình từ [tại đây](https://hadoop.apache.org/docs/r3.2.3/hadoop-yarn/hadoop-yarn-site/DockerContainers.html)

Chạy spark-submit:

```bash
MOUNTS="$HADOOP_HOME:$HADOOP_HOME:ro,/etc/passwd:/etc/passwd:ro,/etc/group:/etc/group:ro"
IMAGE_ID="pyspark-docker:test"

spark-submit \
    --master yarn \
    --conf spark.yarn.appMasterEnv.YARN_CONTAINER_RUNTIME_TYPE=docker \
    --conf spark.yarn.appMasterEnv.YARN_CONTAINER_RUNTIME_DOCKER_IMAGE=${IMAGE_ID} \
    --conf spark.executorEnv.YARN_CONTAINER_RUNTIME_TYPE=docker \
    --conf spark.executorEnv.YARN_CONTAINER_RUNTIME_DOCKER_IMAGE=${IMAGE_ID} \
    06_spark_sql.py \
        --input_green=gs://dtc_data_lake_de-zoomcamp-nytaxi/pq/green/2021/*/ \
        --input_yellow=gs://dtc_data_lake_de-zoomcamp-nytaxi/pq/yellow/2021/*/ \
        --output=gs://dtc_data_lake_de-zoomcamp-nytaxi/report-2021
```



### Nguồn

* https://hadoop.apache.org/docs/r3.2.3/hadoop-project-dist/hadoop-common/SingleCluster.html
* https://spark.apache.org/docs/latest/configuration.html#custom-hadoophive-configuration
