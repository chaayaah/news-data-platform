from fastapi import FastAPI
import psycopg2

app = FastAPI(title="News Data Platform")


@app.get("/")
def root():
    return {
        "message": "News Data Platform is running!"
    }


@app.get("/article-summary")
def article_summary():

    conn = psycopg2.connect(
        host="news-postgres",
        database="newsdb",
        user="postgres",
        password="postgres"
    )

    cur = conn.cursor()

    cur.execute("""
        SELECT country, article_count
        FROM article_summary
        ORDER BY country
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return [
        {
            "country": row[0],
            "article_count": row[1]
        }
        for row in rows
    ]