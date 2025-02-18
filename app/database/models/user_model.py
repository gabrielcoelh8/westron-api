import uuid
from sqlalchemy import String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, validates
from sqlalchemy.dialects.postgresql import UUID

from app.database.meta.declarative import Base
from app.database.meta.schema import schema


class User(Base):
    __tablename__ = 'user'
    __table_args__ = (
        UniqueConstraint('username', name='uq_user_username'),
        UniqueConstraint('email', name='uq_user_email'),
        {'schema': schema}
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(100), nullable=False)
    disabled: Mapped[bool] = mapped_column(nullable=False, default=False)
    
    @validates('email')
    def validate_email(self, key, value):
        if not '@' in value:
            raise ValueError("Email inválido")
        return value.lower()
    
    @validates('username')
    def validate_username(self, key, value):
        if len(value) < 3:
            raise ValueError("Username deve ter pelo menos 3 caracteres")
        return value.lower()