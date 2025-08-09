from datetime import datetime
from contrib.models import BaseModel
from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class CategoriasModels(BaseModel):
    __tablename__='categorias'

    pk_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    atletas: Mapped[list['AtletasModels']] = relationship(back_populates='categoria')
    
