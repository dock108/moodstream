from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings

from .api.routes import router as api_router

app = FastAPI(title="MoodStream AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "Welcome to MoodStream AI"}


@app.get("/ping")
async def ping():
    return {"message": "pong"}
