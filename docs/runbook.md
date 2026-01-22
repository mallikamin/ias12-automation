# IAS 12 Automation — Runbook

## Environment Setup

### Prerequisites

- Docker & Docker Compose
- Node.js 18+
- Python 3.11+
- Git

### Local Development Setup

```bash
# Clone repository
git clone <repo-url>
cd ias12-automation

# Start database
docker compose up -d db

# Setup API
cd apps/api
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head       # Run migrations

# Setup Web
cd ../web
npm install

# Start services
# Terminal 1: API
cd apps/api && source venv/bin/activate && uvicorn app.main:app --reload

# Terminal 2: Web
cd apps/web && npm run dev
```

---

## Period Close Process

### Step 1: Extract Balances

- Upload trial balance (Excel/CSV)
- System validates: required columns, data types, period match
- Review and resolve mapping gaps

### Step 2: Compute IAS 12

- Create new Run (freezes inputs + config)
- Engine computes temporary differences
- Register generated with DTA/DTL amounts

### Step 3: Review

- Check register for unusual items
- Validate DTA probability flags
- Add overrides with justification if needed

### Step 4: Approve

- Reviewer approves register
- CFO approves journals

### Step 5: Post Journals

- Preview journal entries
- Export to ERP format
- Mark as posted

### Step 6: Lock Period

- Lock to prevent changes
- Export evidence pack for audit

---

## Common Commands

```bash
# Run all tests
cd apps/api && pytest

# Run specific test
pytest tests/unit/test_rules.py -v

# Check API logs
docker compose logs -f api

# Reset database (dev only)
docker compose down -v
docker compose up -d db
cd apps/api && alembic upgrade head
```

---

## Troubleshooting

| Issue                | Solution                                        |
| -------------------- | ----------------------------------------------- |
| DB connection failed | Check Docker is running: `docker compose ps`    |
| Migration fails      | Reset DB: `docker compose down -v` then restart |
| API not responding   | Check logs: `docker compose logs api`           |
