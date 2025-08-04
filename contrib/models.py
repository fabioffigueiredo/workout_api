from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PD_UUID
from uuid import uuid4



class BaseModel(DeclarativeBase):
    id: Mapped[UUID] = mapped_column(PD_UUID(as_uuid=True), default=uuid4, nullable=False)
    