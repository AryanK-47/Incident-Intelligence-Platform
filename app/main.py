from fastapi import FastAPI

#Load and register models in SQLAlchemy registry
from app.core import models

# routers...
from app.features.Incident.routers import router as incident_router
from app.features.users.routers import router as user_router
from app.features.auth.routers import router as auth_router
from app.features.ai_analysis.routers import router as analysis_router

app = FastAPI(title="Incident Management Platform")

app.include_router(incident_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(analysis_router)