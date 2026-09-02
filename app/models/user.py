from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.database.connection import Base

from datetime import datetime, timezone

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(String, unique=True, nullable=False)

    username = Column(String, unique=True, nullable=False)

    first_name = Column(String, nullable=False)

    last_name = Column(String, nullable=True)

    password_hash = Column(String, nullable=True)

    is_active = Column(Boolean, default=True)

    role_id = Column(Integer, ForeignKey("roles.id"))

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    last_login = Column(DateTime, nullable=True)

    role = relationship("Role", back_populates="users")