FROM python:3.12.8-slim-bookworm
RUN apt-get update && apt-get install -y --no-install-recommends openjdk-17-jre-headless make && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV SPARK_LOCAL_IP=127.0.0.1
CMD ["python", "scripts/run_all.py", "--sf", "1"]
