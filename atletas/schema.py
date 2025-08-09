from pydantic import Field, PositiveFloat, ConfigDict
from typing import Annotated, Optional

# Update the import path below to the correct location of BaseSchema, for example:
from categorias.schema import CategoriasIn
from centro_treinamento.schema import CentroTreinamentoAtleta  
from contrib.schema import BaseSchema, OutMixin
# or
# from ..contrib.schema import BaseSchema
# Uncomment the correct line below and remove this comment.

# from contrib.schema import BaseSchema
# from ..contrib.schema import BaseSchema

class Atletas(BaseSchema):
    nome:   Annotated[str, Field(description='Nome do atleta', example='João da Silva', max_length=50, min_length=3)]
    cpf:    Annotated[str, Field(description="CPF do atleta", example='12345678901', max_length=11)]
    idade:  Annotated[int, Field(description='Idade do atleta', example=20)]
    peso:   Annotated[PositiveFloat, Field(description='Peso do atleta', example=70.5)]
    altura: Annotated[PositiveFloat, Field(description='Altura do atleta', example=1.75)]
    sexo: Annotated[str, Field(description='Gênero do atleta', example='M', max_length=1)]
    categoria: Annotated[CategoriasIn, Field(description='Categoria do atleta')]
    centro_treinamento: Annotated[CentroTreinamentoAtleta, Field(description='Centro de treinamento do atleta')]

class AtletasIn(Atletas):
    pass
   
class AtletasOut(Atletas, OutMixin):
    pass

class AtletasUpdate(BaseSchema):
    nome:   Annotated[Optional[str], Field(None,description='Nome do atleta', example='João da Silva', max_length=50, min_length=3)]
    idade:  Annotated[Optional[int], Field(None, description='Idade do atleta', example=20)]
    pass

class CategoriaOutResumido(BaseSchema):
    nome: Annotated[str, Field(description='Nome da categoria', example='Scale')]

class CentroTreinamentoOutResumido(BaseSchema):
    nome: Annotated[str, Field(description='Nome do centro de treinamento', example='CrossFit Curicica')]

class AtletaResumido(BaseSchema):
    nome: Annotated[str, Field(description='Nome do atleta', example='João da Silva', max_length=50)]
    categoria: CategoriaOutResumido
    centro_treinamento: CentroTreinamentoOutResumido

    model_config = ConfigDict(from_attributes=True)