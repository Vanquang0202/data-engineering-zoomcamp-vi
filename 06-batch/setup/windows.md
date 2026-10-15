## Windows

Ở đây chúng tôi sẽ hướng dẫn bạn cách cài đặt Spark 4.x cho Windows.
Chúng tôi đã thử nghiệm nó trên Windows 10 và 11, nhưng nó cũng sẽ hoạt động
cho các phiên bản khác.

Trong hướng dẫn này, chúng ta sẽ sử dụng [MINGW](https://www.mingw-w64.org/)/[Git Bash](https://gitforwindows.org/) cho dòng lệnh.

Nếu bạn sử dụng WSL, hãy làm theo hướng dẫn từ [linux.md](linux.md).


### Cài đặt Java

Spark 4.x yêu cầu Java 17. Tải xuống và giải nén Adoptium JDK 17:

```bash
wget https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.18%2B8/OpenJDK17U-jdk_x64_windows_hotspot_17.0.18_8.zip
unzip OpenJDK17U-jdk_x64_windows_hotspot_17.0.18_8.zip -d /c/tools/
```

Đường dẫn đầy đủ tới JDK sẽ là `/c/tools/jdk-17.0.18+8`.

Bây giờ, hãy định cấu hình nó và thêm nó vào `PATH` (thêm vào `.bashrc` của bạn):

```bash
export JAVA_HOME="/c/tools/jdk-17.0.18+8"
export PATH="${JAVA_HOME}/bin:${PATH}"
```

Kiểm tra xem Java có hoạt động chính xác không:

```bash
java --version
```

Đầu ra:

```
openjdk 17.0.18 2026-01-20 LTS
OpenJDK Runtime Environment Temurin-17.0.18+8 (build 17.0.18+8-LTS)
OpenJDK 64-Bit Server VM Temurin-17.0.18+8 (build 17.0.18+8-LTS, mixed mode, sharing)
```


### PySpark

Chúng tôi khuyên bạn nên sử dụng [uv](https://docs.astral.sh/uv/) để quản lý các gói Python:

```bash
uv init
uv add pyspark
```

Sau đó chạy tập lệnh của bạn với `uv run`:

```bash
uv run python your_script.py
```

Ngoài ra, bạn có thể sử dụng pip:

```bash
pip install pyspark
```

Cả hai phương pháp đều cài đặt PySpark cùng với bản phân phối Spark đi kèm - không cần tải xuống Spark hoặc Hadoop riêng.

> Nếu trước đây bạn đã cài đặt Spark 3.x và đã đặt `SPARK_HOME` trong `.bashrc` của bạn (ví dụ: trỏ tới `C:/tools/spark-3.3.2-bin-hadoop3`), hãy xóa dòng đó. PySpark 4.x tích hợp Spark riêng nên `SPARK_HOME` không còn cần thiết nữa. Nếu `SPARK_HOME` cũ vẫn được đặt, PySpark 4.x sẽ tải các JAR cũ và không thành công.


### Đang thử nghiệm

Tạo tập lệnh thử nghiệm `test_spark.py`:

```python
import pyspark
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .master("local[*]") \
    .appName('test') \
    .getOrCreate()

print(f"Spark version: {spark.version}")

df = spark.range(10)
df.show()

spark.stop()
```

Chạy nó:

```bash
uv run python test_spark.py
```

Tại thời điểm này, bạn có thể nhận được thông báo từ Tường lửa Windows - hãy cho phép nó.

Bạn có thể thấy cảnh báo như `WARNING: Using incubator modules: jdk.incubator.vector` — bạn có thể yên tâm bỏ qua cảnh báo đó.

