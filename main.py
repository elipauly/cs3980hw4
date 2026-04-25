from typing import Annotated

from fastapi import APIRouter, FastAPI, HTTPException, Path
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from todo_routes import todo_router
from auth_routes import router as auth_router

import asyncio

from motor.motor_asyncio import AsyncIOMotorClient


from contextlib import asynccontextmanager

from models.user import User
from models.food import Food
from models.todo import Todo

import certifi

from db import init_mongo

@asynccontextmanager
async def lifespan(app: FastAPI):
    client = await init_mongo()
    yield
    client.close()


app = FastAPI(title="Todo Items App", version="1.0.0", lifespan=lifespan)

@app.get("/")
async def home():
    return FileResponse("./frontend/index.html")


app.include_router(auth_router)
app.include_router(todo_router, tags=["Todos"], prefix="/todos")

# the router needs to be before the mount.
# otherwise, the routes cannot be found.
app.mount("/", StaticFiles(directory="frontend"), name="static")