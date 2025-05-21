from fastapi import FastAPI

from .api.routes import router as api_router

app = FastAPI(title="MoodStream AI")

app.include_router(api_router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "Welcome to MoodStream AI"}
