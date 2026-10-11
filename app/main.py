from fastapi import FastAPI
#Load and register models in SQLAlchemy registry
from app.core import models
from fastapi.middleware.cors import CORSMiddleware
# routers...
from app.features.Incident_Assignee.routers import router as assignee_router
from app.features.ai_analysis.routers import router as analysis_router
from app.features.auth.routers import router as auth_router
from app.features.comments.routers import router as comments_router
from app.features.Incident.routers import router as incident_router
from app.features.roles.routers import router as role_router
from app.features.users.routers import router as user_router
from app.features.Incident_Events.routers import router as incident_event_router
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="Incident Management Platform")
Instrumentator().instrument(app).expose(app)

app.include_router(incident_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(analysis_router)
app.include_router(role_router)
app.include_router(comments_router)
app.include_router(assignee_router)
app.include_router(incident_event_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://172.20.10.2:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
