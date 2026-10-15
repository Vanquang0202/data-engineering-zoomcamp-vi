# Lời giải bài tập Module 6

Bộ dữ liệu: [Dữ liệu chuyến đi taxi Yellow - tháng 11/2025](https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2025-11.parquet)


## Câu hỏi 1: Cài đặt Spark và PySpark

```python
import pyspark
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .master("local[*]") \
    .appName('homework') \
    .getOrCreate()

spark.version
```

**Đáp án: `4.1.1`**

(Đáp án phụ thuộc vào phiên bản bạn đã cài đặt)


## Câu hỏi 2: Dữ liệu taxi Yellow tháng 11/2025

```python
df = spark.read.parquet("yellow_tripdata_2025-11.parquet")
df = df.repartition(4)
df.write.parquet("yellow_tripdata_2025-11_partitioned")
```

Sau đó kiểm tra kích thước các file:

```python
import os, glob

parquet_files = glob.glob("yellow_tripdata_2025-11_partitioned/*.parquet")
for f in parquet_files:
    size_mb = os.path.getsize(f) / (1024 * 1024)
    print(f"{os.path.basename(f)}: {size_mb:.1f} MB")
```

Mỗi file có kích thước khoảng 24,4 MB.

**Đáp án: 25MB**


## Câu hỏi 3: Đếm số bản ghi

```python
from pyspark.sql import functions as F

count_15 = df.filter(
    F.to_date(F.col("tpep_pickup_datetime")) == "2025-11-15"
).count()

print(count_15)
# 162604
```

**Đáp án: 162,604**


## Câu hỏi 4: Chuyến đi dài nhất

```python
df_with_duration = df.withColumn(
    "duration_hours",
    (F.unix_timestamp(F.col("tpep_dropoff_datetime")) - F.unix_timestamp(F.col("tpep_pickup_datetime"))) / 3600
)

longest = df_with_duration.agg(F.max("duration_hours")).collect()[0][0]
print(f"{longest:.1f}")
# 90.6
```

**Đáp án: 90.6**


## Câu hỏi 5: Giao diện người dùng

Theo mặc định, giao diện Spark chạy trên cổng 4040.

**Đáp án: 4040**


## Câu hỏi 6: Khu vực đón khách ít xuất hiện nhất

```python
zones = spark.read.option("header", "true").csv("taxi_zone_lookup.csv")
zones.createOrReplaceTempView("zones")
df.createOrReplaceTempView("trips")

spark.sql("""
    SELECT z.Zone, COUNT(*) as cnt
    FROM trips t
    JOIN zones z ON t.PULocationID = z.LocationID
    GROUP BY z.Zone
    ORDER BY cnt ASC
    LIMIT 5
""").show(truncate=False)
```

```
+---------------------------------------------+---+
|Zone                                         |cnt|
+---------------------------------------------+---+
|Governor's Island/Ellis Island/Liberty Island|1  |
|Eltingville/Annadale/Prince's Bay            |1  |
|Arden Heights                                |1  |
|Port Richmond                                |3  |
|Rikers Island                                |4  |
+---------------------------------------------+---+
```

Ba khu vực cùng có số chuyến bằng 1. Trong các lựa chọn của đề bài, Governor's Island/Ellis Island/Liberty Island là khu vực ít xuất hiện nhất.

**Đáp án: Governor's Island/Ellis Island/Liberty Island**
