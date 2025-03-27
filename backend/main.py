from fastapi import FastAPI
from database import get_session, engine, SessionDep
import uvicorn

app = FastAPI(
    title="FastAPI SQLAlchemy Async",
    description="FastAPI + SQLAlchemy Async = ❤️",
    version="0.1.0"
)

