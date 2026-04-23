from typing import Annotated

from fastapi import APIRouter, FastAPI, HTTPException, Path
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from todo_routes import todo_router
from auth_routes import router as auth_router

import asyncio

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from beanie.operators import Set

from contextlib import asynccontextmanager

from models.user import User
from models.food import Food
from models.todo import Todo

import certifi

@asynccontextmanager
async def lifespan(app: FastAPI):
    ca = certifi.where()
    client = AsyncIOMotorClient("mongodb://localhost:27017")

    await init_beanie(
        database=client.todo_app,
        document_models=[Food, User, Todo]
    )

    print("MongoDB connected")
    yield
    print("Shutting down")

app = FastAPI(title="Todo Items App", version="1.0.0", lifespan=lifespan)

@app.get("/")
async def home():
    return FileResponse("./frontend/index.html")


app.include_router(auth_router)
app.include_router(todo_router, tags=["Todos"], prefix="/todos")

# the router needs to be before the mount.
# otherwise, the routes cannot be found.
app.mount("/", StaticFiles(directory="frontend"), name="static")