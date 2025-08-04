from pydantic import Field, PositiveFloat
from typing import Annotated

from workout_api.contrib.schema import BaseSchema   

class Atletas(BaseSchema):
    nome:   Annotated[str, Field(description='Nome do atleta', example='João da Silva', max_length=50, min_length=3)]
    cpf:    Annotated[str, Field(description="CPF do atleta", example='12345678901', max_length=11)]
    idade:  Annotated[int, Field(description='Idade do atleta', example=20)]
    peso:   Annotated[PositiveFloat, Field(description='Peso do atleta', example=70.5)]
    altura: Annotated[PositiveFloat, Field(description='Altura do atleta', example=1.75)]
    sexo: Annotated[str, Field(description='Gênero do atleta', example='M', max_length=1)]
   
    