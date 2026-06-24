FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y default-jdk && \
    rm -rf /var/lib/apt/lists/*

RUN pip install pyspark

CMD ["tail", "-f", "/dev/null"]