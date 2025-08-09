from datetime import datetime
from typing import Annotated
from pydantic import UUID4, BaseModel, Field



class BaseSchema(BaseModel):
    class Config:
        from_attributes = True
class OutMixin(BaseSchema):
    id: Annotated[UUID4, Field(description='Identicador')]
    created_at: Annotated[datetime, Field(description='Data de criação')]