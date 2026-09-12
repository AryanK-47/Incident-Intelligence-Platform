from fastapi import FastAPI
from app.features.Incident.routers import router
app = FastAPI(title="Incident Management Platform")


app.include_router(router)

@app.get("/health")
def health_check():
    return {"status": "ok"}


