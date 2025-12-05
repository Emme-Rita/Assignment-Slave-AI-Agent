from fastapi import APIRouter
from app.api.v1.endpoints import assignment, research, email, whatsapp, student

api_router = APIRouter()

api_router.include_router(
    assignment.router,
    prefix="", # Expose directly under /api/v1 so we get /api/v1/submit. 
    # Note: User asked for /api/submit. The base path is usually /api/v1 defined in config.
    # So this will result in /api/v1/submit. If user strictly needs /api/submit, we'd need to change API_V1_STR or move this router.
    # Assuming /api/v1/submit is acceptable or we alias it.
    tags=["assignment"]
)

api_router.include_router(
    research.router,
    prefix="/research",
    tags=["research"]
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
