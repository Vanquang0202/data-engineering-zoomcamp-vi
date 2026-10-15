---
prev_url: 10-sql-refresher.md
next_url: 12-terraform-overview.md
---
#Dọn dẹp

Khi bạn hoàn thành hội thảo, hãy dọn sạch tài nguyên Docker để giải phóng dung lượng ổ đĩa.


## Dừng tất cả các container đang chạy

```bash
docker-compose down
```

## Xóa các vùng chứa cụ thể

```bash
# List all containers
docker ps -a

# Remove specific container
docker rm <container_id>

# Remove all stopped containers
docker container prune
```

## Xóa hình ảnh Docker

```bash
# List all images
docker images

# Remove specific image
docker rmi taxi_ingest:v001

# Remove all unused images
docker image prune -a
```

## Xóa khối lượng Docker

```bash
# List volumes
docker volume ls

# Remove specific volumes
docker volume rm ny_taxi_postgres_data
docker volume rm pgadmin_data

# Remove all unused volumes
docker volume prune
```

## Xóa mạng Docker

```bash
# List networks
docker network ls

# Remove specific network
docker network rm pg-network

# Remove all unused networks
docker network prune
```

## Hoàn tất dọn dẹp

Loại bỏ TẤT CẢ tài nguyên Docker - hãy thận trọng khi sử dụng!

```bash
# ⚠️ Warning: This removes ALL Docker resources!
docker system prune -a --volumes
```

## Dọn dẹp các tập tin cục bộ

```bash
# Remove parquet files
rm *.parquet

# Remove Python cache
rm -rf __pycache__ .pytest_cache

# Remove virtual environment (if using venv)
rm -rf .venv
```

---

Đó là tất cả cho ngày hôm nay. Chúc bạn học tập vui vẻ! 🐳📊
