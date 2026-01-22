from app.database import Base, engine
from sqlalchemy import inspect, text


def test_database_connection():
    """Verify database connection works."""
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        assert result.scalar() == 1


def test_tables_exist():
    """Verify all expected tables exist."""
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    expected_tables = ["roles", "users", "audit_log", "entities", "periods"]
    for table in expected_tables:
        assert table in tables, f"Table '{table}' not found"
