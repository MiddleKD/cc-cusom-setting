from fastapi import APIRouter
from typing import Optional
from app.services.hello_service import HelloService
from app.models.user import MessageRequest, MessageResponse

router = APIRouter(prefix="/api/v1", tags=["hello"])
hello_service = HelloService()

@router.get("/", response_model=MessageResponse)
async def root():
    return hello_service.hello_world()

@router.get("/hello", response_model=MessageResponse)
async def hello(message: Optional[str] = "Hello World!"):
    return hello_service.hello_world(message)

@router.post("/hello", response_model=MessageResponse)
async def hello_post(request: MessageRequest):
    return hello_service.hello_world(request.message)