from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from routes.fridge_routes import fridge_router
from routes.auth_routes import auth_router

app = FastAPI(title="Fridge App")


@app.get("/")
async def home():
    return FileResponse("./frontend/index.html")


app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(fridge_router, prefix="/fridge", tags=["Fridge"])

app.mount("/", StaticFiles(directory="frontend"), name="static")