from fastapi import APIRouter, HTTPException, status
from typing import List
from app.services.user_service import UserService
from app.models.user import User, UserCreate, UserUpdate

router = APIRouter(prefix="/api/v1/users", tags=["users"])
user_service = UserService()

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    return user_service.create_user(user)

@router.get("/", response_model=List[User])
async def read_users(skip: int = 0, limit: int = 100):
    return user_service.get_users(skip=skip, limit=limit)

@router.get("/{user_id}", response_model=User)
async def read_user(user_id: int):
    user = user_service.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=User)
async def update_user(user_id: int, user_update: UserUpdate):
    user = user_service.update_user(user_id, user_update)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/{user_id}")
async def delete_user(user_id: int):
    success = user_service.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}