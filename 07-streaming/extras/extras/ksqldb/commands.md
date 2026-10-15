## Ví dụ về KSQL DB
### Tạo luồng
```sql
CREATE STREAM ride_streams (
    VendorId varchar, 
    trip_distance double,
    payment_type varchar
)  WITH (KAFKA_TOPIC='rides',
        VALUE_FORMAT='JSON');
```

### Luồng truy vấn
```sql
select * from RIDE_STREAMS 
EMIT CHANGES;
```

### Số luồng truy vấn
```sql
SELECT VENDORID, count(*) FROM RIDE_STREAMS 
GROUP BY VENDORID
EMIT CHANGES;
```

### Luồng truy vấn có bộ lọc
```sql
SELECT payment_type, count(*) FROM RIDE_STREAMS 
WHERE payment_type IN ('1', '2')
GROUP BY payment_type
EMIT CHANGES;
```

### Luồng truy vấn có chức năng cửa sổ
```sql
CREATE TABLE payment_type_sessions AS
  SELECT payment_type,
         count(*)
  FROM  RIDE_STREAMS 
  WINDOW SESSION (60 SECONDS)
  GROUP BY payment_type
  EMIT CHANGES;
```

## Tài liệu KSQL để biết chi tiết
[Tài liệu KSQL DB](https://docs.ksqldb.io/en/latest/developer-guide/ksqldb-reference/quick-reference/)

[Máy khách Java KSQL DB](https://docs.ksqldb.io/en/latest/developer-guide/ksqldb-clients/java-client/)