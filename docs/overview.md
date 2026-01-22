# IAS 12 Deferred Tax Automation Platform

## What This System Does

A configurable IAS 12 (Income Taxes) engine that:

- Extracts book balances from GL and subledgers
- Determines tax bases via rule-mapping
- Computes temporary differences (Carrying Amount − Tax Base)
- Generates a deferred tax register and period-to-period roll-forward
- Produces journals with correct P&L / OCI / Equity routing
- Outputs disclosure packs for financial statement notes

## Who Uses It

| Role         | Responsibilities                                             |
| ------------ | ------------------------------------------------------------ |
| Preparer     | Runs extracts, reviews unmapped exceptions, drafts register  |
| Reviewer     | Validates mappings, unusual movements, DTA probability flags |
| CFO Approver | Approves journals and key assumptions                        |
| Admin        | Maintains master data (rates, mappings) with logged changes  |

## Key Benefits

- Faster close: System-driven computation vs. manual Excel
- Fewer errors: Automated sign handling, rate application, reversals
- Stronger controls: Audit trail, approvals, versioning
- Full traceability: Every DTA/DTL line links back to source transactions

## Architecture

```
React Web App (UI)
       │
       ▼
Python API (FastAPI)
       │
       ▼
PostgreSQL Database
```

## Scope

### In Scope (Phase 1)

- Deferred tax (DTA/DTL) using temporary differences method
- Automated deferred tax register and roll-forward
- Journal automation with P&L / OCI / Equity routing
- Disclosure support and movement reconciliations
- Governance, audit trail, and approvals

### Out of Scope

- Full corporate tax return preparation
- Transfer pricing computations
- Consolidation module (only inputs supported)
