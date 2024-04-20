from fastapi import APIRouter, FastAPI

from routers.note import note_router, basket_router

app = FastAPI()

main_api_router = APIRouter()

main_api_router.include_router(note_router, prefix="/note", tags=["note"])
main_api_router.include_router(basket_router, prefix="/basket", tags=["basket"])
app.include_router(main_api_router)
