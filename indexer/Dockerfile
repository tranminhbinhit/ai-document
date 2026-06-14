FROM python:3.12-slim

WORKDIR /app

# Install system dependencies for document processing and MS SQL ODBC driver
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    unixodbc-dev \
    unixodbc \
    curl \
    gnupg2 \
    && curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /usr/share/keyrings/microsoft-archive-keyring.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/microsoft-archive-keyring.gpg] https://packages.microsoft.com/debian/12/prod bookworm main" > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Run worker
CMD ["python", "worker.py"]
