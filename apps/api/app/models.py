from datetime import datetime

import sqlalchemy as sa
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


class Entity(Base):
    """Legal entity for tax purposes."""

    __tablename__ = "entities"

    id = Column(Integer, primary_key=True)
    code = Column(String(20), unique=True, nullable=False)  # e.g., "ABC-PK"
    name = Column(String(255), nullable=False)  # e.g., "ABC Ltd Pakistan"
    jurisdiction = Column(String(100), nullable=False)  # e.g., "Pakistan"
    currency = Column(String(3), nullable=False)  # e.g., "PKR"
    tax_authority = Column(String(100))  # e.g., "FBR"
    fiscal_year_end = Column(String(5), nullable=False)  # e.g., "12-31" or "06-30"
    is_active = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)

    periods = relationship("Period", back_populates="entity")


class Period(Base):
    """Fiscal period for deferred tax calculation."""

    __tablename__ = "periods"

    id = Column(Integer, primary_key=True)
    entity_id = Column(Integer, ForeignKey("entities.id"), nullable=False)
    period_end = Column(String(10), nullable=False)  # e.g., "2024-12-31"
    period_name = Column(String(50), nullable=False)  # e.g., "Dec 2024"
    status = Column(String(20), default="open")  # open, draft, approved, locked
    created_at = Column(DateTime, default=datetime.utcnow)
    locked_at = Column(DateTime, nullable=True)
    locked_by = Column(Integer, ForeignKey("users.id"), nullable=True)

    entity = relationship("Entity", back_populates="periods")


class SourceFile(Base):
    """Uploaded source file (trial balance, FA register, etc.)."""

    __tablename__ = "source_files"

    id = Column(Integer, primary_key=True)
    entity_id = Column(Integer, ForeignKey("entities.id"), nullable=False)
    period_id = Column(Integer, ForeignKey("periods.id"), nullable=False)
    file_type = Column(String(50), nullable=False)  # trial_balance, fixed_assets, etc.
    file_name = Column(String(255), nullable=False)
    file_hash = Column(String(64))  # SHA256 for reproducibility
    row_count = Column(Integer)
    uploaded_by = Column(Integer, ForeignKey("users.id"))
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    rows = relationship("SourceRow", back_populates="source_file")


class SourceRow(Base):
    """Individual row from source file."""

    __tablename__ = "source_rows"

    id = Column(Integer, primary_key=True)
    source_file_id = Column(Integer, ForeignKey("source_files.id"), nullable=False)
    row_number = Column(Integer, nullable=False)
    account_code = Column(String(50))
    account_name = Column(String(255))
    balance = Column(sa.Numeric(18, 2))  # Book value / carrying amount
    additional_data = Column(Text)  # JSON for extra columns

    source_file = relationship("SourceFile", back_populates="rows")
