from fastapi import APIRouter

from .routes.ofx_routes import router as ofx_router
from .routes.pdf_routes import router as pdf_router
from .routes.ocr_routes import router as ocr_router
from .routes.instituicao_financeira_routes import router as instituicao_financeira_router
from .routes.instituicao_financeira_alias_routes import router as instituicao_financeira_alias_router
from .routes.extrato_bancario_routes import router as extrato_bancario_router
from .routes.extrato_bancario_alias_routes import router as extrato_bancario_alias_routes
from .routes.prompt_routes import router as prompt_routes


router = APIRouter()
router.include_router(ofx_router)
router.include_router(pdf_router)
router.include_router(ocr_router)
router.include_router(instituicao_financeira_router)
router.include_router(instituicao_financeira_alias_router)
router.include_router(extrato_bancario_router)
router.include_router(extrato_bancario_alias_routes)
router.include_router(prompt_routes)
