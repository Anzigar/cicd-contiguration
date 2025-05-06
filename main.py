import os
from fastapi import FastAPI

app = FastAPI(
    title="CI/CD Configuration API",
    description="API for CI/CD configuration service",
    version="0.1.0",
)


@app.get("/")
async def root():
    return {
        "message": "Hello World",
        "status": "Running",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "port": os.getenv("PORT", "8000"),
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    reload_enabled = os.getenv("ENVIRONMENT", "development").lower() == "development"
    uvicorn.run(app, host=host, port=port, reload=reload_enabled)
