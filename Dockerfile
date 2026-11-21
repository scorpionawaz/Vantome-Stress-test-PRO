FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["sh", "-c", "exec gunicorn --workers 2 --threads 8 --worker-class gthread --worker-tmp-dir /dev/shm --timeout 120 --graceful-timeout 30 --keep-alive 5 --access-logfile - --error-logfile - --log-level info -b 0.0.0.0:${PORT:-8080} app:app"]
