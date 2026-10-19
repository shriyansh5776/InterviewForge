import uuid
from sqlalchemy import String,Uuid, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
from datetime import datetime


class User(Base):
    __tablename__ ="users"
    
    id:Mapped[uuid.UUID] = mapped_column(Uuid,primary_key =True,index=True,default=uuid.uuid4)
    email:Mapped[str] = mapped_column(String(255),unique=True,nullable=False)
    password_hash:Mapped[str] = mapped_column(String(255),nullable=False)
    full_name:Mapped[str] = mapped_column(String(255),nullable=False)
    created_at:Mapped[datetime]= mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
        )
    updated_at:Mapped[datetime]= mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
        )