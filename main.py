from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from app.routers import hello, users
from app.core.exceptions import http_exception_handler, general_exception_handler
from app.core.logger import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application starting up...")
    yield
    logger.info("Application shutting down...")

app = FastAPI(
    title="Hello World API", 
    description="FastAPI를 사용한 Hello World 서비스",
    version="1.0.0",
    lifespan=lifespan
)

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

@app.get("/")
async def root():
    return {"message": "Hello World API", "docs": "/docs", "redoc": "/redoc"}

app.include_router(hello.router)
app.include_router(users.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)