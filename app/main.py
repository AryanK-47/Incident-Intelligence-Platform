from fastapi import FastAPI
from app.features.Incident.routers import router
from app.features.users.routers import router as user_router
app = FastAPI(title="Incident Management Platform")


app.include_router(router)
app.include_router(user_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}

