# Decision Log

Records architectural and design decisions made during development.

---

## Template

### [DECISION-XXX] Title

**Date**: YYYY-MM-DD
**Status**: Proposed / Accepted / Deprecated
**Context**: What is the background?
**Decision**: What was decided?
**Consequences**: What are the implications?

---

## Decisions

### [DECISION-001] Monorepo Structure

**Date**: 2025-01-22
**Status**: Accepted
**Context**: Need to organize frontend, backend, and shared resources.
**Decision**: Use a monorepo with `/apps/web`, `/apps/api`, `/packages`, `/docs`, `/infra`.
**Consequences**:

- Single repo to manage
- Shared test data accessible to both apps
- Coordinated versioning

### [DECISION-002] Technology Stack

**Date**: 2025-01-22
**Status**: Accepted
**Context**: Need to select technologies for frontend, backend, and database.
**Decision**:

- Frontend: React + Vite
- Backend: Python 3.11+ with FastAPI
- Database: PostgreSQL
- Migrations: Alembic
  **Consequences**:
- Python chosen for calculation engine (finance teams familiar with Python)
- React for modern, responsive UI
- PostgreSQL for robust relational data and audit requirements

### [DECISION-003] Configurable Rules over Hardcoded Logic

**Date**: 2025-01-22
**Status**: Accepted
**Context**: Tax base rules vary by account type and jurisdiction (e.g., Pakistan vs UAE).
**Decision**: Implement a rules engine with UI-configurable parameters stored in database, not in code.
**Consequences**:

- Finance team can adjust mappings without developer involvement
- Every config change is versioned and auditable
- Slightly more complex initial build, but much easier long-term maintenance
