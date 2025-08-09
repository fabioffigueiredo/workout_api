from uuid import UUID, uuid4
from fastapi import APIRouter, Body, status, HTTPException
from pydantic import UUID4
from sqlalchemy.future import select
from datetime import datetime, timezone

from centro_treinamento.schema import CentroTreinamentoIn, CentroTreinamentoOut, CentroTreinamentoUpdate
from contrib.dependencies import DatabaseDependency
from centro_treinamento.models import CentroTreinamentoModels

router = APIRouter()

@router.post(
    '/',
    summary="Criar um novo centro de treinamento",
    status_code=status.HTTP_201_CREATED,
    response_model=CentroTreinamentoOut,
)
async def post(
    db_session: DatabaseDependency,
    centro_treinamento_in: CentroTreinamentoIn = Body(...)
) -> CentroTreinamentoOut:
    
    centro_treinamento_model = CentroTreinamentoModels(
        **centro_treinamento_in.model_dump(), 
        created_at=datetime.now(timezone.utc)
    )
    
    db_session.add(centro_treinamento_model)
    await db_session.commit()
    await db_session.refresh(centro_treinamento_model)

    return centro_treinamento_model

@router.get(
    '/',
    summary="Consultar todas os centros de treinamento",
    status_code=status.HTTP_200_OK,
    response_model=list[CentroTreinamentoOut],
)
async def get_all(
    db_session: DatabaseDependency
) -> list[CentroTreinamentoOut]:
    centros_treinamento: list[CentroTreinamentoOut] = (await db_session.execute(select(CentroTreinamentoModels))).scalars().all()
    return centros_treinamento

@router.get(
    '/{id}',
    summary="Consultar um centro de treinamento pelo ID",
    status_code=status.HTTP_200_OK,
    response_model=CentroTreinamentoOut,
)
async def get_by_id(
    id: str,
    db_session: DatabaseDependency) -> CentroTreinamentoOut:
    try:
        ct_id = UUID(id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Centro de treinamento não encontrado no id informado: {id}")

    centro_treinamento: CentroTreinamentoOut = (await db_session.execute(select(CentroTreinamentoModels).filter_by(id=ct_id))).scalars().first()
    
    if not centro_treinamento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Centro de treinamento não encontrado no id informado: {id}")
    
    return centro_treinamento

@router.get(
    "/nome/{nome}",
    summary="Consulta um centro de treinamento pelo nome",
    status_code=status.HTTP_200_OK,
    response_model=CentroTreinamentoOut,
)
async def get_by_name(nome: str, db_session: DatabaseDependency) -> CentroTreinamentoOut:
    centro_treinamento: CentroTreinamentoOut = (
        (await db_session.execute(select(CentroTreinamentoModels).filter_by(nome=nome)))
        .scalars()
        .first()
    )

    if not centro_treinamento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Centro de treinamento não encontrado com o nome: {nome}",
        )

    return centro_treinamento

@router.get(
    "/proprietario/{proprietario}",
    summary="Consulta centros de treinamento pelo proprietário",
    status_code=status.HTTP_200_OK,
    response_model=list[CentroTreinamentoOut],
)
async def get_by_proprietario(proprietario: str, db_session: DatabaseDependency) -> list[CentroTreinamentoOut]:
    centros_treinamento: list[CentroTreinamentoOut] = (
        (await db_session.execute(select(CentroTreinamentoModels).filter_by(proprietario=proprietario)))
        .scalars()
        .all()
    )

    if not centros_treinamento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nenhum centro de treinamento encontrado para o proprietário: {proprietario}",
        )

    return centros_treinamento

@router.patch(
    '/{id}',
    summary="Editar um centro de treinamento pelo ID",
    status_code=status.HTTP_200_OK,
    response_model=CentroTreinamentoOut,
)
async def patch(
    id: str, db_session: DatabaseDependency, ct_up: CentroTreinamentoUpdate = Body(...)
) -> CentroTreinamentoOut:
    try:
        ct_id = UUID(id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Centro de treinamento não encontrado no id informado: {id}")

    centro_treinamento: CentroTreinamentoModels = (await db_session.execute(select(CentroTreinamentoModels).filter_by(id=ct_id))).scalars().first()
    if not centro_treinamento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Centro de treinamento não encontrado no id informado: {id}")
    
    ct_update = ct_up.model_dump(exclude_unset=True)
    for key, value in ct_update.items():
        setattr(centro_treinamento, key, value)
    
    await db_session.commit()
    await db_session.refresh(centro_treinamento)
    return centro_treinamento

@router.delete(
    '/{id}',
    summary="Deletar um centro de treinamento pelo ID",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete(id: str, db_session: DatabaseDependency) -> None:
    try:
        ct_id = UUID(id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Centro de treinamento não encontrado no id informado: {id}")

    centro_treinamento: CentroTreinamentoModels = (await db_session.execute(select(CentroTreinamentoModels).filter_by(id=ct_id))).scalars().first()
    if not centro_treinamento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Centro de treinamento não encontrado no id informado: {id}")
    
    await db_session.delete(centro_treinamento)
    await db_session.commit()