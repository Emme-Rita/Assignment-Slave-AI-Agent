from fastapi import APIRouter
from app.api.v1.endpoints import assignment, research, email, whatsapp, student, history

api_router = APIRouter()

api_router.include_router(
    assignment.router,
    prefix="", 
    tags=["assignment"]
)

api_router.include_router(
    research.router,
    prefix="/research",
    tags=["research"]
)

api_router.include_router(
    history.router,
    prefix="",
    tags=["history"]
)

api_router.include_router(
    email.router,
    prefix="/send",
    tags=["email"]
)

api_router.include_router(
    whatsapp.router,
    prefix="/send",
    tags=["whatsapp"]
)

api_router.include_router(
    student.router,
    prefix="/student",
    tags=["student"]
)

api_router.include_router(
    history.router,
    prefix="/history",
    tags=["history"]
)

from app.api.v1.endpoints import download
api_router.include_router(
    download.router,
    prefix="",
    tags=["download"]
)
