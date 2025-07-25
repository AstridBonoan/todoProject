from datetime import datetime
from app.extensions import db, bcrypt
from enum import Enum
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Enum as PgEnum, Table, JSON
from sqlalchemy.orm import relationship

# Enum for Todo status
class TodoStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    ARCHIVED = "archived"

# Association tables for many-to-many relationships
todo_tag = Table(
    'todo_tag',
    db.Model.metadata,
    Column('todo_id', Integer, ForeignKey('todos.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)

user_roles = Table(
    'user_roles',
    db.Model.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True)
)

role_permissions = Table(
    'role_permissions',
    db.Model.metadata,
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True),
    Column('permission_id', Integer, ForeignKey('permissions.id'), primary_key=True)
)

class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    name = Column(String(120), nullable=True)
    preferences = Column(JSON, nullable=True)
    password_hash = Column(String(128), nullable=True)
    is_verified = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    todos = relationship('Todo', back_populates='user', cascade='all, delete-orphan')

    # Roles (many-to-many)
    roles = relationship('Role', secondary=user_roles, back_populates='users')

    def set_password(self, password: str) -> None:
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password: str) -> bool:
        return bcrypt.check_password_hash(self.password_hash, password)

class Todo(db.Model):
    __tablename__ = 'todos'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    task = Column(String(256), nullable=False)
    status = Column(PgEnum(TodoStatus), default=TodoStatus.PENDING, nullable=False)
    category = Column(String(80))
    due_date = Column(DateTime, nullable=True)
    is_deleted = Column(Boolean, default=False, nullable=False)  # soft delete

    user = relationship('User', back_populates='todos')
    tags = relationship('Tag', secondary=todo_tag, back_populates='todos')
    completion_history = relationship('CompletionHistory', back_populates='todo', cascade='all, delete-orphan')

class Tag(db.Model):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    todos = relationship('Todo', secondary=todo_tag, back_populates='tags')

class CompletionHistory(db.Model):
    __tablename__ = 'completion_history'
    id = Column(Integer, primary_key=True)
    todo_id = Column(Integer, ForeignKey('todos.id'), nullable=False)
    completed_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    todo = relationship('Todo', back_populates='completion_history')

class Role(db.Model):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(255))

    users = relationship('User', secondary=user_roles, back_populates='roles')
    permissions = relationship('Permission', secondary=role_permissions, back_populates='roles')

class Permission(db.Model):
    __tablename__ = 'permissions'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(255))

    roles = relationship('Role', secondary=role_permissions, back_populates='permissions')
