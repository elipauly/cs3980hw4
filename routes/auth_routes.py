from fastapi import APIRouter, HTTPException
from db import users_collection
from models import User
from auth import create_token

auth_router = APIRouter()

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


@auth_router.post("/signup")
async def signup(user: User):
    # check if user exists
    existing = await users_collection.find_one({"username": user.username})
    if existing:
        raise HTTPException(400, "Username already taken")

    # hash password
    hashed_pw = hash_password(user.password)

    # store in DB
    result = await users_collection.insert_one({
        "username": user.username,
        "password": hashed_pw
    })

    # create token
    token = create_token(str(result.inserted_id))

    return {"token": token}

@auth_router.post("/login")
async def login(user: User):
    db_user = await users_collection.find_one({
        "username": user.username
    })

    if not db_user:
        raise HTTPException(401, "Invalid credentials")

    # verify password
    if not verify_password(user.password, db_user["password"]):
        raise HTTPException(401, "Invalid credentials")

    token = create_token(str(db_user["_id"]))

    return {"token": token}