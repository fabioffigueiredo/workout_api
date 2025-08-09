from typing import Annotated, Optional
from datetime import datetime

from pydantic import UUID4, Field
from contrib.schema import BaseSchema


class CategoriasIn(BaseSchema):
    nome: Annotated[str, Field(description='Nome da categoria', example='Scale', max_length=10)]
    
class CategoriasOut(CategoriasIn):
    id: Annotated[UUID4, Field(description='Identificador da categoria')]
    created_at: Annotated[datetime, Field(description='Data de criação')]

class CategoriasUpdate(BaseSchema):
    nome: Annotated[Optional[str], Field(None, description='Nome da categoria', example='Scale', max_length=10)]