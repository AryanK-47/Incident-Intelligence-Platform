from fastapi import FastAPI
from app.features.users.models import User
from app.features.roles.models import Role
from app.features.user_roles.models import UserRole

#Load and register models in SQLAlchemy registry

# routers...
from app.core import models
from app.features.ai_analysis.routers import router as analysis_router
from app.features.auth.routers import router as auth_router
from app.features.Incident.routers import router as incident_router
from app.features.roles.routers import router as role_router
from app.features.users.routers import router as user_router
from app.features.Incident_Events.routers import router as incident_event_router


app = FastAPI(title="Incident Management Platform")

app.include_router(incident_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(analysis_router)
app.include_router(role_router)
app.include_router(incident_event_router)
