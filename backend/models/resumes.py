import uuid
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import (
    String, Uuid, DateTime, ForeignKey,
    Integer, func
)
from click.types import UUID

class Resumes(Base):
    __tablename__ = "resumes"
    id:Mapped[uuid.UUID]=mapped_column(UUID,primary_key=True,unique=True,nullable=False)
    user_id : Mapped[uuid:UUID] = mapped_column(UUID,unique=True, ForeignKey("users.id"))
    