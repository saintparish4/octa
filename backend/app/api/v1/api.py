from fastapi import APIRouter
from app.api.v1.endpoints import spatial, network, tasks

api_router = APIRouter()

api_router.include_router(spatial.router, prefix="/spatial", tags=["spatial"])
api_router.include_router(network.router, prefix="/network", tags=["network"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])

@api_router.get("/")
async def root():
    return {"message": "OCTA API", "version": "1.0"}

@api_router.get("/health")
async def health_check():
    return {"status": "healthy", "service": "OCTA API"} 