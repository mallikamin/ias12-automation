from datetime import datetime

from app.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship


class Role(Base):
    """User roles: preparer, reviewer, approver, admin."""

    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(255))

    users = relationship("User", back_populates="role")


class User(Base):
    """System users."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    is_active = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)

    role = relationship("Role", back_populates="users")


class AuditLog(Base):
    """Tracks all changes for governance."""

    __tablename__ = "audit_log"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action = Column(String(50), nullable=False)  # CREATE, UPDATE, DELETE
    table_name = Column(String(100), nullable=False)
    record_id = Column(Integer)
    old_values = Column(Text)  # JSON string
    new_values = Column(Text)  # JSON string
    reason = Column(String(500))
    timestamp = Column(DateTime, default=datetime.utcnow)
