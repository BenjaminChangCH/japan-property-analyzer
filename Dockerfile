# Use the official Python image as a base image
FROM python:3.11-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port that the application will listen on
ENV PORT 8080
EXPOSE $PORT

# Run Gunicorn when the container starts.
# Use "shell form" to ensure the $PORT environment variable is substituted.
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 main:app 