# Bank Demo - QUAD Workflow Test

Step-by-step test of QUAD commands.

---

## Step 1: quad-init

**Command:**
```bash
cd /Users/semostudio/git/a2vibes/QUAD/quad-api-poc
./bin/quad init @../quad-projects/bank-demo/bank-demo-setup.xlsx
```

**Expected:**
- Reads Excel file
- Confirms org details
- Confirms resources/team
- Walks through project setup
- Saves to `.quad/project.json`

**Status:** [ ] Not Started

---

## Step 2: quad-plan

**Command:**
```bash
./bin/quad plan bank-demo
```

**Expected:**
- Reads Features tab from Excel
- Calculates PGCE priority for each feature
- Creates `.quad/features/` with ordered features
- Shows build order based on dependencies

**PGCE Formula:** `P = (D × 0.5) + (I × 0.3) + (C' × 0.2)`
- D = Dependency score
- I = Impact (Business Value / 10)
- C' = Complexity inverse (1 - Complexity/10)

**Status:** [ ] Not Started

---

## Step 3: quad-story

**Command:**
```bash
./bin/quad story bank-demo
```

**Expected:**
- Reads features from `.quad/features/`
- Generates user stories for each feature
- Creates `.quad/stories/`
- Interactive: confirm/edit each story

**Status:** [ ] Not Started

---

## Step 4: quad-ticket

**Command:**
```bash
./bin/quad ticket bank-demo
```

**Expected:**
- Reads stories from `.quad/stories/`
- Creates tickets with assignments
- Matches team skills to ticket requirements
- Creates `.quad/tickets/`

**Status:** [ ] Not Started

---

## Step 5: quad-write

**Command:**
```bash
./bin/quad write bank-demo --ticket BANK-001
```

**Expected:**
- Reads ticket details
- Generates code based on tech stack
- Creates `src/` structure
- Spring Boot + PostgreSQL for Bank Demo

**Status:** [ ] Not Started

---

## Step 6: quad-doc

**Command:**
```bash
./bin/quad doc bank-demo
```

**Expected:**
- Reads generated code
- Creates `docs/` with:
  - README.md
  - architecture.md
  - API documentation

**Status:** [ ] Not Started

---

## Step 7: quad-deploy

**Command:**
```bash
./bin/quad deploy bank-demo dev
```

**Expected:**
- Reads Deployment tab from Excel
- Reads Secrets tab
- Deploys to GCP Cloud Run (dev)

**Status:** [ ] Not Started

---

## Notes

_Add observations here as we test each step_

---

## Current Step: 1 (quad-init)

Start with:
```bash
cd /Users/semostudio/git/a2vibes/QUAD/quad-api-poc
./bin/quad init @../quad-projects/bank-demo/bank-demo-setup.xlsx
```
