from datetime import datetime, timezone
from uuid import UUID, uuid4
from fastapi import APIRouter, Body, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from atletas.models import AtletasModels
from atletas.schema import AtletasIn, AtletasOut, AtletasUpdate, AtletaResumido
from categorias.models import CategoriasModels
from centro_treinamento.models import CentroTreinamentoModels
from contrib.dependencies import DatabaseDependency
from fastapi_pagination import LimitOffsetPage, add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate

router = APIRouter()


@router.post(
    "/",
    summary="Criar novo atleta",
    status_code=status.HTTP_201_CREATED,
    response_model=AtletasOut,
)
async def post(db_session: DatabaseDependency, atleta_in: AtletasIn = Body(...)):
    categoria_nome = atleta_in.categoria.nome
    centro_treinamento_nome = atleta_in.categoria.nome

    categoria = (
        (await db_session.execute(select(CategoriasModels).filter_by(nome=categoria_nome)))
        .scalars()
        .first()
    )

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"A categoria {categoria_nome} não foi encontrada.",
        )

    centro_treinamento = (
        (
            await db_session.execute(
                select(CentroTreinamentoModels).filter_by(nome=centro_treinamento_nome)
            )
        )
        .scalars()
        .first()
    )

    if not centro_treinamento:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"O centro de treinamento {centro_treinamento_nome} não foi encontrado.",
        )
    try:
        atleta_out = AtletasOut(id=uuid4(), created_at=datetime.now(timezone.utc), **atleta_in.model_dump())
        atleta_model = AtletasModels(
            **atleta_out.model_dump(exclude={"categoria", "centro_treinamento"})
        )
        atleta_model.categoria_id = categoria.pk_id
        atleta_model.centro_treinamento_id = centro_treinamento.pk_id

        db_session.add(atleta_model)
        await db_session.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=f"Atleta já cadastrado com o cpf: {atleta_in.cpf}",
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocorreu um erro ao inserir os dados no banco",
        )

    return atleta_out

@router.get(
    "/",
    summary="Consultar todos os Atletas ",
    status_code=status.HTTP_200_OK,
    response_model=LimitOffsetPage[AtletaResumido],
)
async def query(
    db_session: DatabaseDependency,
) -> LimitOffsetPage[AtletaResumido]:
    return await paginate(db_session, select(AtletasModels))

@router.get(
    "/{id}",
    summary="Consulta um atleta pelo id",
    status_code=status.HTTP_200_OK,
    response_model=AtletasOut,
)
async def get(id: str, db_session: DatabaseDependency) -> AtletasOut:
    try:
        atleta_id = UUID(id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Atleta não encontrado no id: {id}",
        )
    atleta: AtletasOut = (
        (await db_session.execute(select(AtletasModels).filter_by(id=atleta_id)))
        .scalars()
        .first()
    )

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Atleta não encontrado no id: {id}",
        )

    return atleta

@router.get(
    "/nome/{nome}",
    summary="Consulta um atleta pelo nome",
    status_code=status.HTTP_200_OK,
    response_model=AtletasOut,
)
async def get_by_name(nome: str, db_session: DatabaseDependency) -> AtletasOut:
    atleta: AtletasOut = (
        (await db_session.execute(select(AtletasModels).filter_by(nome=nome)))
        .scalars()
        .first()
    )

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Atleta não encontrado com o nome: {nome}",
        )

    return atleta

@router.get(
    "/cpf/{cpf}",
    summary="Consulta um atleta pelo CPF",
    status_code=status.HTTP_200_OK,
    response_model=AtletasOut,
)
async def get_by_cpf(cpf: str, db_session: DatabaseDependency) -> AtletasOut:
    atleta: AtletasOut = (
        (await db_session.execute(select(AtletasModels).filter_by(cpf=cpf)))
        .scalars()
        .first()
    )

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Atleta não encontrado com o CPF: {cpf}",
        )

    return atleta

@router.patch(
    "/{id}",
    summary="Editar um atleta pelo id",
    status_code=status.HTTP_200_OK,
    response_model=AtletasOut,
)
async def patch(
    id: str, db_session: DatabaseDependency, atleta_up: AtletasUpdate = Body(...)
) -> AtletasOut:
    try:
        atleta_id = UUID(id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Atleta não encontrado no id: {id}",
        )
    atleta: AtletasOut = (
        (await db_session.execute(select(AtletasModels).filter_by(id=atleta_id)))
        .scalars()
        .first()
    )

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Atleta não encontrado no id: {id}",
        )

    atleta_update = atleta_up.model_dump(exclude_unset=True)
    for key, value in atleta_update.items():
        setattr(atleta, key, value)

    await db_session.commit()
    await db_session.refresh(atleta)

    return atleta

@router.delete(
    "/{id}",
    summary="Deletar um atleta pelo id",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete(id: str, db_session: DatabaseDependency) -> None:
    try:
        atleta_id = UUID(id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Atleta não encontrado no id: {id}",
        )
    atleta: AtletasOut = (
        (await db_session.execute(select(AtletasModels).filter_by(id=atleta_id)))
        .scalars()
        .first()
    )

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Atleta não encontrado no id: {id}",
        )

    await db_session.delete(atleta)
    await db_session.commit()

add_pagination(router)
