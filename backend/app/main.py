from fastapi import FastAPI
from app.core.config import settings
from app.core.security import setup_cors
from app.api.api import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="AI-powered Assignment Helper API",
    version="1.0.0"
)

# Setup CORS
setup_cors(app)

# Create database tables
from app.db.session import engine, Base
from app.models import conversation # Import models to register them
Base.metadata.create_all(bind=engine)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {
        "message": "Welcome to Assignment Helper API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Force reload for schema update
