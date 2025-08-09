from typing import Annotated, Optional

from pydantic import UUID4, Field
from contrib.schema import BaseSchema


class CentroTreinamentoIn(BaseSchema):
    nome: Annotated[str, Field(description='Nome da Centro Treinamento', example='Cross Curicica', max_length=20)]
    endereco: Annotated[str, Field(description='Endereco Centro Treinamento', example='Rua, numero', max_length=60)]
    proprietario: Annotated[str, Field(description='Proprietaio Centro Treinamento', example='Felipe', max_length=30)]

class CentroTreinamentoAtleta(BaseSchema):
    nome: Annotated[str, Field(description='Nome do Centro de Treinamento', example='Cross Curicica', max_length=20)]

class CentroTreinamentoOut(CentroTreinamentoIn):
    id: Annotated[UUID4, Field(description='ID do Centro de Treinamento')]

class CentroTreinamentoUpdate(BaseSchema):
    nome: Annotated[Optional[str], Field(None, description='Nome da Centro Treinamento', example='Cross Curicica', max_length=20)]
    endereco: Annotated[Optional[str], Field(None, description='Endereco Centro Treinamento', example='Rua, numero', max_length=60)]
    proprietario: Annotated[Optional[str], Field(None, description='Proprietaio Centro Treinamento', example='Felipe', max_length=30)]
