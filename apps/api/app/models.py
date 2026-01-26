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


class ChartOfAccounts(Base):
    """Chart of accounts for an entity."""

    __tablename__ = "chart_of_accounts"

    id = Column(Integer, primary_key=True)
    entity_id = Column(Integer, ForeignKey("entities.id"), nullable=False)
    account_code = Column(String(50), nullable=False)
    account_name = Column(String(255), nullable=False)
    account_type = Column(String(50))  # asset, liability, equity, income, expense
    parent_code = Column(String(50))  # For hierarchical COA
    is_active = Column(Integer, default=1)

    __table_args__ = (
        sa.UniqueConstraint("entity_id", "account_code", name="uq_entity_account"),
    )


class AccountMapping(Base):
    """Maps GL accounts to tax categories and rules."""

    __tablename__ = "account_mappings"

    id = Column(Integer, primary_key=True)
    entity_id = Column(Integer, ForeignKey("entities.id"), nullable=False)
    account_code = Column(String(50), nullable=False)
    tax_category = Column(
        String(50), nullable=False
    )  # fixed_assets, provisions, inventory, leases, etc.
    tax_base_rule = Column(
        String(50), nullable=False
    )  # carrying_amount, tax_wdv, nil, etc.
    deductibility = Column(
        String(50), nullable=False
    )  # on_accrual, on_payment, non_deductible
    posting_route = Column(String(20), nullable=False)  # pnl, oci, equity
    description = Column(String(255))
    is_active = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    updated_by = Column(Integer, ForeignKey("users.id"))

    __table_args__ = (
        sa.UniqueConstraint("entity_id", "account_code", name="uq_entity_mapping"),
    )


class TaxRate(Base):
    """Tax rates by entity and effective date."""

    __tablename__ = "tax_rates"

    id = Column(Integer, primary_key=True)
    entity_id = Column(Integer, ForeignKey("entities.id"), nullable=False)
    effective_date = Column(String(10), nullable=False)  # YYYY-MM-DD
    rate = Column(sa.Numeric(5, 2), nullable=False)  # e.g., 29.00 for 29%
    surtax_rate = Column(
        sa.Numeric(5, 2), default=0
    )  # Additional super tax if applicable
    description = Column(String(255))
    is_enacted = Column(Integer, default=1)  # 1 = enacted, 0 = substantively enacted
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        sa.UniqueConstraint("entity_id", "effective_date", name="uq_entity_rate_date"),
    )


class ConfigVersion(Base):
    """Versioned snapshot of configuration (mappings, rates, rules)."""

    __tablename__ = "config_versions"

    id = Column(Integer, primary_key=True)
    entity_id = Column(Integer, ForeignKey("entities.id"), nullable=False)
    version_number = Column(Integer, nullable=False)
    description = Column(String(255))
    mappings_hash = Column(String(64))  # Hash of account_mappings at this version
    rates_hash = Column(String(64))  # Hash of tax_rates at this version
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(Integer, ForeignKey("users.id"))

    __table_args__ = (
        sa.UniqueConstraint("entity_id", "version_number", name="uq_entity_version"),
    )


class Run(Base):
    """A single deferred tax calculation run."""

    __tablename__ = "runs"

    id = Column(Integer, primary_key=True)
    entity_id = Column(Integer, ForeignKey("entities.id"), nullable=False)
    period_id = Column(Integer, ForeignKey("periods.id"), nullable=False)
    config_version_id = Column(
        Integer, ForeignKey("config_versions.id"), nullable=False
    )
    run_number = Column(Integer, nullable=False)  # v1, v2, v3 within a period
    status = Column(String(20), default="draft")  # draft, reviewed, approved, posted
    inputs_hash = Column(String(64))  # Hash of all source files used
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(Integer, ForeignKey("users.id"))
    approved_at = Column(DateTime)
    approved_by = Column(Integer, ForeignKey("users.id"))

    __table_args__ = (
        sa.UniqueConstraint("period_id", "run_number", name="uq_period_run"),
    )


class RunInput(Base):
    """Links a run to its source files."""

    __tablename__ = "run_inputs"

    id = Column(Integer, primary_key=True)
    run_id = Column(Integer, ForeignKey("runs.id"), nullable=False)
    source_file_id = Column(Integer, ForeignKey("source_files.id"), nullable=False)
    file_hash = Column(String(64), nullable=False)

    __table_args__ = (
        sa.UniqueConstraint("run_id", "source_file_id", name="uq_run_source"),
    )
