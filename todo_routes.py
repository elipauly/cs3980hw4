from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, status, Depends
from dependencies import get_current_user

from models.todo import Todo, TodoRequest

from beanie import PydanticObjectId


todo_router = APIRouter()


@todo_router.get("/")
async def get_all_todos(user=Depends(get_current_user)):
    return await Todo.find(Todo.owner == user.username).to_list()


@todo_router.post("", status_code=status.HTTP_201_CREATED)
async def create_new_todo(todo: TodoRequest, user=Depends(get_current_user)):
    new_todo = Todo(
        title=todo.title, desc=todo.desc, category=todo.category, owner=user.username)
    await new_todo.insert()
    return new_todo

@todo_router.get("/{todo_id}")
async def get_todo_by_id(todo_id: PydanticObjectId, user=Depends(get_current_user)):
    todo = await Todo.get(todo_id)

    if not todo or todo.owner != user.username:
        raise HTTPException(status_code=404, detail=f"Item not found.")
    return todo


@todo_router.delete("/{todo_id}")
async def delete_todo_by_id(todo_id:PydanticObjectId, user=Depends(get_current_user)):
    todo = await Todo.get(todo_id)

    if not todo or todo.owner != user.username:
        raise HTTPException(status_code=404, detail=f"Item not found.")
    
    await todo.delete()
    return {"message": "Deleted successfully."}

@todo_router.put("/{todo_id}")
async def update_todo_by_id(todo_id: PydanticObjectId, todo_data: TodoRequest, user=Depends(get_current_user)):
    todo = await Todo.get(todo_id)

    if not todo or todo.owner != user.username:
        raise HTTPException(status_code=404, detail=f"Item not found.")
    
    todo.title = todo_data.title
    todo.desc = todo_data.desc
    todo.category = todo_data.category

    await todo.save()
    return todo