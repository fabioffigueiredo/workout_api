from pydantic import BaseModel


class BaseSchema(BaseModel):
    class Config:
        extra = 'forbid' #Não vai aceitar campos extras
        from_attributes = True