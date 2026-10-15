Hack nhanh để tải file trực tiếp lên GCS mà không cần Airflow. Tải xuống các tệp csv từ https://nyc-tlc.s3.amazonaws.com/trip+data/ và tải chúng lên Tài khoản lưu trữ đám mây của bạn dưới dạng tệp gỗ.

1. Cài đặt các yêu cầu trước với `uv sync`
2. Chạy: `uv run python web_to_gcs_with_progress_bar.py`
2. hoặc Chạy: `uv run python web_to_gcs.py` để ít dài dòng hơn (nếu bạn có kết nối Internet nhanh khi tải lên)
