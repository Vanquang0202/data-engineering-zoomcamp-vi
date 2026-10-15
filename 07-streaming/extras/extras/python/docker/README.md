
# Chạy cụm Spark và Kafka trên Docker

### 1. Xây dựng hình ảnh cần thiết để chạy Spark

Bạn có thể đọc chi tiết về cách tạo hình ảnh tia lửa ở các lớp khác nhau qua
, bài đăng trên blog do André Perez viết trên [Medium blog -Towards Data Science](https://towardsdatascience.com/apache-spark-cluster-on-docker-ft-a-juyterlab-interface-418383c95445)

```bash
# Build Spark Images
./build.sh 
```

### 2. Tạo Docker Network & Volume

```bash
# Create Network
docker network  create kafka-spark-network

# Create Volume
docker volume create --name=hadoop-distributed-file-system
```

### 3. Chạy Services trên Docker
```bash
# Start Docker-Compose (within for kafka and spark folders)
docker compose up -d
```
Giải thích chuyên sâu về [Người nghe Kafka](https://www.confluent.io/blog/kafka-listeners-explained/)

Giải thích về [Người nghe Kafka](https://www.confluent.io/blog/kafka-listeners-explained/)

### 4. Dừng dịch vụ trên Docker
```bash
# Stop Docker-Compose (within for kafka and spark folders)
docker compose down
```

### 5. Các lệnh hữu ích
```bash
# Delete all Containers
docker rm -f $(docker ps -a -q)

# Delete all volumes
docker volume rm $(docker volume ls -q)
```

