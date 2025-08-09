from fastapi import APIRouter
from atletas.controller import router as atletas
from categorias.controller import router as categorias
from centro_treinamento.controller import router as centro_treinamento


api_router = APIRouter()
api_router.include_router(atletas, prefix='/atletas', tags=['atletas'])
api_router.include_router(categorias, prefix='/categorias', tags=['categorias'])
api_router.include_router(centro_treinamento, prefix='/centro_treinamento', tags=['centro_treinamento'])