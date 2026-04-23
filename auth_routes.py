from fastapi import APIRouter, HTTPException
from models.user import User
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

router = APIRouter(prefix="/auth", tags=["auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "secret"
ALGORITHM = "HS256"


def hash_password(password):
    return pwd_context.hash(password)


def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)


def create_token(username: str):
    return jwt.encode(
        {"sub": username, "exp": datetime.utcnow() + timedelta(hours=1)},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


@router.post("/register")
async def register(data: dict):
    if await User.find_one(User.username == data["username"]):
        raise HTTPException(400, "User exists")

    user = User(
        username=data["username"],
        password=hash_password(data["password"])
    )
    await user.insert()

    return {"message": "created"}


@router.post("/login")
async def login(data: dict):
    user = await User.find_one(User.username == data["username"])

    if not user or not verify_password(data["password"], user.password):
        raise HTTPException(401, "Invalid credentials")

    return {"access_token": create_token(user.username)}