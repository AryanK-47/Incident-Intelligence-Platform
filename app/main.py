from fastapi import FastAPI
from app.core.database import engine

app = FastAPI(title="Incident Management Platform")


@app.get("/health")
def health_check():
    return {"status": "ok"}



