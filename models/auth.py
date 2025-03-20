# models.py

from database.db import Base
from sqlalchemy import Column, String, UUID, TIMESTAMP, func, ForeignKey, Integer, CheckConstraint
from uuid import uuid4
from sqlalchemy.orm import relationship



class CasbinRule(Base):
    __tablename__ = "casbin_rule"

    id = Column(Integer, primary_key=True, index=True)
    ptype = Column(String(10))
    v0 = Column(String(255))
    v1 = Column(String(255))
    v2 = Column(String(255))
    v3 = Column(String(255), nullable=True)
    v4 = Column(String(255), nullable=True)
    v5 = Column(String(255), nullable=True)


class BaseModel(Base):
    __abstract__ = True

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())


class User(Base):
    __tablename__ = "users"
    id = Column(UUID, default=uuid4, primary_key=True, unique=True, nullable=False)
    username = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)

    profile = relationship("Profile", back_populates="user", uselist=False, passive_deletes=True)
    addresses = relationship("Address", back_populates="user", passive_deletes=True)
    posts = relationship("Post", back_populates="user", cascade="all, delete")

    roles = relationship("Role", back_populates="users", secondary="user_roles", passive_deletes=True)

    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Profile(BaseModel):
    __tablename__ = "profiles"
    gender = Column(String(50), nullable=False)
    ethnicity = Column(String(50), nullable=False)
    country = Column(String(50), unique=True, nullable=False)
    language = Column(String, unique=True, nullable=False)

    user_id = Column(UUID, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    user = relationship("User", back_populates="profile")


class Address(BaseModel):
    __tablename__ = "addresses"
    street = Column(String, nullable=False)
    city = Column(String, nullable=False)
    country = Column(String, nullable=False)
    zip_code = Column(Integer, nullable=False)

    user_id = Column(UUID, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    user = relationship("User", back_populates="addresses")

    __table_args__ = (
        CheckConstraint("zip_code >=100000 AND zip_code <=10000000", name="check_zip_code_length"),
        CheckConstraint("LENGTH(country) BETWEEN 5 AND 8")
    )


class Role(BaseModel):
    __tablename__ = "roles"
    name = Column(String(80), nullable=False, unique=True)

    users = relationship("User", back_populates="roles", secondary="user_roles", passive_deletes=True)


class UserRole(BaseModel):
    __tablename__ = "user_roles"

    user_id = Column(UUID, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    role_id = Column(UUID, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True)

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

