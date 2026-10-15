
##MacOS

Ở đây chúng tôi sẽ hướng dẫn bạn cách cài đặt Spark 4.x cho macOS.
Chúng tôi đã thử nghiệm nó trên macOS 15 (Sequoia), nhưng nó cũng sẽ hoạt động
cho các phiên bản khác.


### Cài đặt Java

Spark 4.x yêu cầu Java 17. Đảm bảo [Homebrew](https://brew.sh/) đã được cài đặt, sau đó cài đặt OpenJDK 17:

```bash
brew install openjdk@17
```

Thêm các biến môi trường sau vào `.zshrc` (hoặc `.bash_profile`):
của bạn
```bash
export JAVA_HOME=$(brew --prefix openjdk@17)
export PATH="$JAVA_HOME/bin:$PATH"
```

Kiểm tra xem Java có hoạt động chính xác không:

```bash
java --version
```

Đầu ra (ví dụ):

```
openjdk 17.0.14 2026-01-21
OpenJDK Runtime Environment Homebrew (build 17.0.14+0)
OpenJDK 64-Bit Server VM Homebrew (build 17.0.14+0, mixed mode, sharing)
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

> Nếu trước đây bạn đã cài đặt Spark 3.x và đã đặt `SPARK_HOME` trong `.zshrc` hoặc `.bash_profile` (ví dụ: trỏ đến thư mục Spark cục bộ), hãy xóa dòng đó. PySpark 4.x tích hợp Spark riêng nên `SPARK_HOME` không còn cần thiết nữa. Nếu `SPARK_HOME` cũ vẫn được đặt, PySpark 4.x sẽ tải các JAR cũ và không thành công.


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

Bạn có thể thấy cảnh báo như `WARNING: Using incubator modules: jdk.incubator.vector` — bạn có thể yên tâm bỏ qua cảnh báo đó.
