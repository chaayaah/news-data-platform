from fastapi import FastAPI

app = FastAPI(title="News Data Platform")

@app.get("/")
def root():
    return {
        "message": "News Data Platform is running!"
    }