# Step Journal

Tracks progress on each step of the build plan.

---

## Entry Format

### Step X: Title
**Date**: YYYY-MM-DD  
**Status**: ✅ Complete / 🟡 In Progress / ⬜ Not Started

**What Changed**:
- Files created/modified

**Commands Run**:
```bash
# commands here
```

**Evidence**:
- Test results or screenshots

**Notes**:
- Decisions or issues encountered

---

## Phase 0 — Foundations (Steps 1–20)

### Step 1: Create monorepo folder structure
**Date**: 2025-01-22  
**Status**: ✅ Complete

**What Changed**:
- Created /apps/web, /apps/api
- Created /docs (5 markdown files)
- Created /infra
- Created /packages/testdata/raw

**Commands Run**:
```bash
mkdir -p ias12-automation/apps/web
mkdir -p ias12-automation/apps/api
mkdir -p ias12-automation/docs
mkdir -p ias12-automation/infra
mkdir -p ias12-automation/packages/testdata/raw
```

**Evidence**:
- Folder structure verified

**Notes**:
- Monorepo allows shared test data between API and Web

---

### Step 2: Initialize git + .gitignore
**Date**: 2025-01-22  
**Status**: ✅ Complete

**What Changed**:
- Initialized git repo on main branch
- Created .gitignore (Python + React patterns)
- Populated all 5 doc files

**Commands Run**:
```bash
git init
git branch -M main
```

**Evidence**:
- Pending: initial commit

**Notes**:
- Branch protections configured on GitHub after push

---

### Step 3: Add .editorconfig + formatting rules
**Date**:  
**Status**: ⬜ Not Started

---

### Step 4: Choose stack versions
**Date**:  
**Status**: ⬜ Not Started

---

### Step 5: Add Docker Compose
**Date**:  
**Status**: ⬜ Not Started