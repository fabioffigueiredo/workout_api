from typing import Annotated

from pydantic import Field
from workout_api.contrib.schema import BaseSchema


class CentroTreinamento(BaseSchema):
    nome: Annotated[str, Field(description='Nome da Centro Treinamento', example='Cross Curicica', max_length=20)]
    endereco: Annotated[str, Field(description='Endereco Centro Treinamento', example='Rua, numero', max_length=60)]
    proprietario: Annotated[str, Field(description='Proprietaio Centro Treinamento', example='Felipe', max_length=30)]