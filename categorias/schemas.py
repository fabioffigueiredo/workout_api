from typing import Annotated

from pydantic import Field
from workout_api.contrib.schema import BaseSchema


class categorias(BaseSchema):
    nome: Annotated[str, Field(description='Nome da categoria', example='Scale', max_length=10)]
    