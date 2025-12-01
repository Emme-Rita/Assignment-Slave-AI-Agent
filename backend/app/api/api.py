from fastapi import APIRouter
from app.api.v1.endpoints import assignment, research, email, whatsapp, student

api_router = APIRouter()

api_router.include_router(
    assignment.router,
    prefix="/assignment",
    tags=["assignment"]
)

api_router.include_router(
    research.router,
    prefix="/research",
    tags=["research"]
)

api_router.include_router(
    email.router,
    prefix="/email",
    tags=["email"]
)

api_router.include_router(
    whatsapp.router,
    prefix="/whatsapp",
    tags=["whatsapp"]
)

api_router.include_router(
    student.router,
    prefix="/student",
    tags=["student"]
)
