FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y default-jdk wget && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /opt/jars

RUN wget -O /opt/jars/postgresql.jar \
    https://jdbc.postgresql.org/download/postgresql-42.7.7.jar

RUN pip install \
    pyspark \
    psycopg2-binary

CMD ["tail", "-f", "/dev/null"]