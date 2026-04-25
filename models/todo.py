from pydantic import BaseModel
from beanie import Document
from pydantic import BaseModel
from typing import Optional


class Todo(Document):
    id: int
    title: str
    desc: str
    category: str
    owner: str


class TodoRequest(Document):
    title: str
    desc: str
    category: str