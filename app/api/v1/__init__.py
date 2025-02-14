from fastapi import APIRouter

from app.api.v1.routers.auth_routes import router as auth_router
from app.api.v1.routers.positivity_routes import router as positivity_router
from app.api.v1.routers.translator_routes import router as translator_router
from app.api.v1.routers.user_routes import router as user_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(positivity_router)
router.include_router(translator_router)
router.include_router(user_router)

# cmd: uvicorn app.main:app --host 0.0.0.0 --port "8000" 
# docs: http://localhost:8000/docs/