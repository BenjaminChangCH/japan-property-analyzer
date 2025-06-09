# Use the official Python image as a base image
FROM python:3.11-slim-buster

# 建置參數
ARG VERSION="unknown"
ARG BUILD_NUMBER="unknown"

# 設定環境變數
ENV APP_VERSION=$VERSION
ENV BUILD_NUMBER=$BUILD_NUMBER

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# 在容器中設定版本資訊
RUN echo "Building version: $VERSION.$BUILD_NUMBER" && \
    python3 -c "import os; version_file = 'version.py'; content = open(version_file, 'r').read(); content = content.replace('BUILD_NUMBER = None', f'BUILD_NUMBER = \\\'{os.environ.get(\\\"BUILD_NUMBER\\\", \\\"unknown\\\")}\\\''); open(version_file, 'w').write(content); print(f'Version info updated: {os.environ.get(\\\"APP_VERSION\\\", \\\"unknown\\\")}.{os.environ.get(\\\"BUILD_NUMBER\\\", \\\"unknown\\\")}')"

# Expose the port that the application will listen on
ENV PORT 8080
EXPOSE $PORT

# Run Gunicorn when the container starts.
# Use "shell form" to ensure the $PORT environment variable is substituted.
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 main:app 