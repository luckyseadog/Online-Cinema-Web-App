import uuid
from datetime import datetime

from typing import Annotated
from sqlalchemy import Boolean, Column, DateTime, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.orm import relationship, DeclarativeBase
from db.postgres import Base


class Base(DeclarativeBase):
    pass


class UserRole(Base):
    __tablename__ = 'users_roles'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id= Column(UUID(as_uuid=True), ForeignKey("users.id"))
    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id"))
    updated_at = Column(DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())


class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    login = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(Boolean, default=True)
    roles = relationship("Role", secondary='users_roles', back_populates='users', lazy='selectin')
    # history = relationship("History", secondary=)

    def __init__(self, login: str, password: str, first_name: str, last_name: str) -> None:
        self.login = login
        self.password = generate_password_hash(password)
        self.first_name = first_name
        self.last_name = last_name

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)


    def __repr__(self) -> str:
        return f'<User {self.login}>'


class Role(Base):
    __tablename__ = 'roles'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    title = Column(String(255), unique=True, nullable=False)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())
    users = relationship("User", secondary='users_roles', back_populates='roles', lazy='selectin')

    def __init__(self, title: str, description: str = None) -> None:
        self.title = title
        self.description = description

    def __repr__(self):
        return f'<Role {self.title}>'

class UserHistory(Base):
    __tablename__ = 'user_history'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    occured_at = Column(DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())
    action = Column(String(255), nullable=False)
    fingreprint = Column(String(255), nullable=False)

    def __init__(self):
        pass