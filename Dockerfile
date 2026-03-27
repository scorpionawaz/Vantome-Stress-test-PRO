# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies if needed (e.g., for compiled packages)
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     gcc \
#     python3-dev \
#     && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to /app
COPY . .

# Expose port 8080 to the outside world
EXPOSE 8080

# Run the application when the container launches
# Using Gunicorn with explicit log redirection to stdout (-) for both access and error logs
CMD ["gunicorn", "--workers", "4", "--threads", "4", "--worker-class", "gthread", "--access-logfile", "-", "--error-logfile", "-", "--log-level", "info", "-b", "0.0.0.0:8080", "app:app"]
