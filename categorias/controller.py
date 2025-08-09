from datetime import datetime, timezone
from uuid import UUID, uuid4
from fastapi import APIRouter, Body, status, HTTPException
from sqlalchemy.future import select
from fastapi_pagination import Page, paginate
from categorias.models import CategoriasModels
from categorias.schema import CategoriasIn, CategoriasOut, CategoriasUpdate
from contrib.dependencies import DatabaseDependency

router = APIRouter()

@router.post(
    '/',
    summary="Criar nova categoria",
    status_code=status.HTTP_201_CREATED,
    response_model=CategoriasOut,
)
async def post(
    db_session: DatabaseDependency,
    categoria_in: CategoriasIn = Body(...)
) -> CategoriasOut:
    categoria_model = CategoriasModels(**categoria_in.model_dump(), created_at=datetime.now(timezone.utc))
    
    db_session.add(categoria_model)
    await db_session.commit()
    await db_session.refresh(categoria_model)

    return categoria_model

@router.get(
    '/',
    summary="Consultar todas as categorias",
    status_code=status.HTTP_200_OK,
    response_model=Page[CategoriasOut],
)
async def get_all(
    db_session: DatabaseDependency
) -> Page[CategoriasOut]:
    categorias: list[CategoriasModels] = (await db_session.execute(select(CategoriasModels))).scalars().all()
    return paginate(categorias)

@router.get(
    '/{id}',
    summary="Consultar uma categoria pelo ID",
    status_code=status.HTTP_200_OK,
    response_model=CategoriasOut,
)
async def get_by_id(
    id: str,
    db_session: DatabaseDependency) -> CategoriasOut:
    try:
        categoria_id = UUID(id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Categoria não encontrada no id informado: {id}")

    categoria: CategoriasOut = (await db_session.execute(select(CategoriasModels).filter_by(id=categoria_id))).scalars().first()
    if not categoria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Categoria não encontrada no id informado: {id}")
    return categoria

@router.get(
    "/nome/{nome}",
    summary="Consulta uma categoria pelo nome",
    status_code=status.HTTP_200_OK,
    response_model=CategoriasOut,
)
async def get_by_name(nome: str, db_session: DatabaseDependency) -> CategoriasOut:
    categoria: CategoriasOut = (
        (await db_session.execute(select(CategoriasModels).filter_by(nome=nome)))
        .scalars()
        .first()
    )

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoria não encontrada com o nome: {nome}",
        )

    return categoria

@router.patch(
    '/{id}',
    summary="Editar uma categoria pelo ID",
    status_code=status.HTTP_200_OK,
    response_model=CategoriasOut,
)
async def patch(
    id: str, db_session: DatabaseDependency, categoria_up: CategoriasUpdate = Body(...)
) -> CategoriasOut:
    try:
        categoria_id = UUID(id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Categoria não encontrada no id informado: {id}")

    categoria: CategoriasModels = (await db_session.execute(select(CategoriasModels).filter_by(id=categoria_id))).scalars().first()
    if not categoria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Categoria não encontrada no id informado: {id}")
    
    categoria_update = categoria_up.model_dump(exclude_unset=True)
    for key, value in categoria_update.items():
        setattr(categoria, key, value)
    
    await db_session.commit()
    await db_session.refresh(categoria)
    return categoria

@router.delete(
    '/{id}',
    summary="Deletar uma categoria pelo ID",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete(id: str, db_session: DatabaseDependency) -> None:
    try:
        categoria_id = UUID(id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Categoria não encontrada no id informado: {id}")

    categoria: CategoriasModels = (await db_session.execute(select(CategoriasModels).filter_by(id=categoria_id))).scalars().first()
    if not categoria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Categoria não encontrada no id informado: {id}")
    
    await db_session.delete(categoria)
    await db_session.commit()
