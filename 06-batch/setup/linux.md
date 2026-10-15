
## Linux

Ở đây chúng tôi sẽ hướng dẫn bạn cách cài đặt Spark 4.x cho Linux.
Chúng tôi đã thử nghiệm nó trên Ubuntu 24.04 (cũng như WSL), nhưng nó cũng hoạt động
cho các bản phân phối Linux khác


### Cài đặt Java

Spark 4.x yêu cầu Java 17 hoặc 21. Cách đơn giản nhất là cài đặt nó thông qua trình quản lý gói của bạn:

```bash
sudo apt update
sudo apt install default-jdk
```

Kiểm tra xem nó có hoạt động không:

```bash
java --version
```

Đầu ra (ví dụ):

```
openjdk 21.0.10 2026-01-20
OpenJDK Runtime Environment (build 21.0.10+7-Ubuntu-124.04)
OpenJDK 64-Bit Server VM (build 21.0.10+7-Ubuntu-124.04, mixed mode, sharing)
```

Đặt `JAVA_HOME` (thêm vào `.bashrc` hoặc `.zshrc` của bạn):

```bash
export JAVA_HOME=$(dirname $(dirname $(readlink -f $(which java))))
export PATH="${JAVA_HOME}/bin:${PATH}"
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

Cả hai phương pháp đều cài đặt PySpark cùng với bản phân phối Spark đi kèm - không cần tải xuống Spark riêng.


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

