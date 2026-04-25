from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId


class User(BaseModel):
    username: str
    password: str


class FridgeItem(BaseModel):
    name: str
    quantity: int
    category: str
    owner_id: str

class FridgeItemRequest(BaseModel):
    name: str
    quantity: int
    category: str