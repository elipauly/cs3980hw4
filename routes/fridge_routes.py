from fastapi import APIRouter, Depends, Header, HTTPException
from db import fridge_collection
from models import FridgeItemRequest
from auth import get_current_user
from bson import ObjectId

fridge_router = APIRouter()


def get_user(authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    return get_current_user(token)


@fridge_router.get("")
async def get_items(user_id: str = Depends(get_user)):
    items = []
    async for item in fridge_collection.find({"owner_id": user_id}):
        item["id"] = str(item["_id"])
        del item["_id"]
        items.append(item)
    return items


@fridge_router.post("")
async def add_item(
    item: FridgeItemRequest,
    user_id: str = Depends(get_user)
):
    doc = item.dict()
    doc["owner_id"] = user_id

    result = await fridge_collection.insert_one(doc)

    created = await fridge_collection.find_one({"_id": result.inserted_id})

    created["id"] = str(created["_id"])
    del created["_id"]

    return created


@fridge_router.delete("/{id}")
async def delete_item(
    id: str,
    user_id: str = Depends(get_user)
):
    result = await fridge_collection.delete_one({
        "_id": ObjectId(id),
        "owner_id": user_id
    })

    if result.deleted_count == 0:
        raise HTTPException(404, "Item not found")

    return {"msg": "Deleted"}

@fridge_router.put("/{id}")
async def update_item(
    id: str,
    item: FridgeItemRequest,
    user_id: str = Depends(get_user)
):
    result = await fridge_collection.update_one(
        {
            "_id": ObjectId(id),
            "owner_id": user_id
        },
        {"$set": item.dict()}
    )

    if result.matched_count == 0:
        raise HTTPException(404, "Item not found")

    updated = await fridge_collection.find_one({"_id": ObjectId(id)})

    updated["id"] = str(updated["_id"])
    del updated["_id"]

    return updated