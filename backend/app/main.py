from fastapi import FastAPI

app = FastAPI(
    title="MovieMatch API",
    description="Backend API for the MovieMatch application",
    version="0.1.0",
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