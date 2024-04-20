from fastapi import APIRouter, FastAPI
from routers.users import user_router

app = FastAPI()

main_api_router = APIRouter()
main_api_router.include_router(user_router, prefix="/user", tags=["user"])

app.include_router(main_api_router)
