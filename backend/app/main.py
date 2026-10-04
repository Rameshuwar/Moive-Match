from fastapi import FastAPI

from app.api.v1.search import router as search_router
from app.api.v1.movies import router as movies_router


app = FastAPI(
    title="MovieMatch API",
    description="Backend API for the MovieMatch application",
    version="0.1.0",
)


app.include_router(
    search_router,
    prefix="/api/v1",
)

app.include_router(
    movies_router,
    prefix="/api/v1",
)


@app.get("/")
async def root():
    return {
        "message": "MovieMatch API is running",
        "version": "0.1.0",
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
    }