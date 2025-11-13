# Sử dụng Python base image nhẹ
FROM python:3.10-slim

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Copy toàn bộ project vào container
COPY . .

# (Tùy chọn) Nếu có requirements.txt, cài đặt các dependency
# Nếu chưa có, bạn có thể tạo thủ công hoặc bỏ qua dòng này
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi

# Chạy chương trình chính
CMD ["python", "src/main.py"]
