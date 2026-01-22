# Traceability Matrix

Maps requirements to features, tests, and evidence.

---

## Status Legend

| Symbol | Meaning |
|--------|---------|
| ⬜ | Not started |
| 🟡 | In progress |
| ✅ | Complete |

---

## Core Requirements

| Req ID | Requirement | Module | Test File | Status |
|--------|-------------|--------|-----------|--------|
| REQ-001 | Deferred tax register by period/entity | Calculation Engine | test_register.py | ⬜ |
| REQ-002 | Automatic balance extraction from TB | Ingestion Pipeline | test_ingestion.py | ⬜ |
| REQ-003 | Tax base computation via mapping | Rules Engine | test_rules.py | ⬜ |
| REQ-004 | Temporary difference calculation | Calculation Engine | test_calc.py | ⬜ |
| REQ-005 | Movement schedule (roll-forward) | Calculation Engine | test_movements.py | ⬜ |
| REQ-006 | Book vs tax depreciation (FA) | Fixed Assets | test_fa.py | ⬜ |
| REQ-007 | Provisions deductible on payment | Provisions | test_provisions.py | ⬜ |
| REQ-008 | Inventory/NRV adjustments | Inventory | test_inventory.py | ⬜ |
| REQ-009 | IFRS adjustments layer | IFRS Module | test_ifrs.py | ⬜ |
| REQ-010 | Tax losses tracking | Losses Module | test_losses.py | ⬜ |
| REQ-011 | Journal automation (P&L/OCI/Equity) | Journals | test_journals.py | ⬜ |
| REQ-012 | Disclosure pack outputs | Disclosures | test_disclosures.py | ⬜ |
| REQ-013 | Approval workflow | Workflow | test_workflow.py | ⬜ |
| REQ-014 | Audit trail | Governance | test_audit.py | ⬜ |

---

## Test Datasets

| Dataset | Purpose | Used By |
|---------|---------|---------|
| DATASET_A_MINIMAL | Fast unit tests (10 lines) | All unit tests |
| DATASET_B_REALISTIC | Common scenarios | Integration tests |
| DATASET_C_EDGE_CASES | Negatives, FX, errors | Edge case tests |

---

## UAT Scenarios (from requirements doc)

| Scenario | Req IDs | Status |
|----------|---------|--------|
| FA accelerated depreciation → DTL | REQ-004, REQ-006 | ⬜ |
| Provision deductible on payment → DTA, then reversal | REQ-004, REQ-007 | ⬜ |
| IFRS 16 lease creates temp diff with correct routing | REQ-009, REQ-011 | ⬜ |
| Land revaluation → deferred tax through OCI | REQ-006, REQ-011 | ⬜ |
| Loss carryforward → DTA, then impairment | REQ-010 | ⬜ |
| DTA/DTL offsetting (same tax authority) | REQ-001 | ⬜ |