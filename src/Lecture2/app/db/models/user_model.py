from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.db.models.role_model import Role, association_table

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    legal_name = Column(String, nullable=False)
    preferred_name = Column(String, nullable=True)

    roles = relationship('Role', secondary=association_table, back_populates='users')

    def get_display_name(self) -> str:
        return self.preferred_name if self.preferred_name else self.legal_name
