FROM python:3.12-slim

WORKDIR /app

RUN pip install fastapi uvicorn psycopg2-binary

COPY app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]