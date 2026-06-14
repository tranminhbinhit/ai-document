FROM python:3.11-slim

WORKDIR /app

# Cài đặt system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    freetds-dev \
    freetds-bin \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements và cài đặt dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Tạo thư mục documents nếu chưa có
RUN mkdir -p /documents

CMD ["python", "watcher.py"]
