from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.db.main import init_db
from src.api.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("server is starting")
    await init_db()
    yield
    print("server is shutting down")


app = FastAPI(
    title="Profile Creation System",
    version="0.1.0",
    description="A simple system that allows the creation of student profiles while enforcing password policies",
    lifespan=lifespan,
)


app.include_router(router, tags=["profiles"])
