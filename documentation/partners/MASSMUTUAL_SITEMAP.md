# MassMutual Partner Pitch Site - Sitemap

**URL:** https://massmutual.quadframe.work
**Created:** January 7, 2026
**Status:** Active

---

## The QUAD Concept: Channelized AI Energy

**The Problem:**
> Today's AI coding assistants have incredible power - Agent Rules, Commands, Skills, RAG, AST, ADK - but it's scattered. Developers send raw HTTP requests to AI, hoping for the best. Result? Hallucinations. Wrong syntax. Made-up file paths.

**QUAD's Solution:**
Think of AI like electricity - raw electricity is dangerous and unpredictable, but through proper wiring it safely powers your home. **QUAD is the wiring.**

| Instead of... | QUAD provides... |
|---------------|------------------|
| Random AI responses | Predictable, validated output |
| Hallucinated paths | Real codebase references |
| Syntax errors | AST-verified code |
| Context confusion | Smart memory management |

**Pitch One-Liner:**
> *"QUAD channels AI's raw power into enterprise-grade software delivery - zero hallucinations, syntactically correct, every time."*

---

## Site Structure

```
massmutual.quadframe.work/
│
├── /massmutual                    ← Landing Page (Overview)
│   │
│   ├── /massmutual/pitch          ← Pitch Deck
│   │
│   ├── /massmutual/demo           ← Guided Demo Walkthrough
│   │   ├── Step 1: The Problem    → /concept
│   │   ├── Step 2: QUAD Solution  → /flow
│   │   ├── Step 3: How It Works   → /details
│   │   ├── Step 4: Set Up Org     → /dashboard (🔐 Password)
│   │   ├── Step 5: Assign Users   → /dashboard (🔐 Password)
│   │   └── Step 6: Role Dashboards→ /dashboard (🔐 Password)
│   │
│   ├── /massmutual/settings       ← Feature Toggle Settings
│   │   ├── Presets: FULL MATRIX, PILOT VECTOR, GROWTH PLANE, CUSTOM PATH
│   │   └── 103 Features (toggleable)
│   │
│   ├── /massmutual/roi            ← ROI Calculator
│   │
│   └── /massmutual/contact        ← Schedule Demo / Contact
│
└── Shared Pages (QUAD Framework)
    ├── /concept                   ← The Problem (6 weeks for 1 paragraph)
    ├── /flow                      ← Q → U → A → D Flow
    ├── /details                   ← AI Agents in Action
    └── /dashboard                 ← Live Dashboard Demo
```

---

## Page Details

### 1. Landing Page (`/massmutual`)

**Purpose:** Hero page for MassMutual partnership pitch

**Content:**
- Co-branded header (QUAD × MassMutual)
- Problem statement: "Why does 1 paragraph take 6 weeks?"
- QUAD value proposition
- CTA buttons to demo and contact

---

### 2. Pitch Deck (`/massmutual/pitch`)

**Purpose:** Slide-based pitch presentation

**Content:**
- Problem slides
- Solution overview
- QUAD methodology
- ROI projections
- Customer testimonials (if any)

---

### 3. Demo Walkthrough (`/massmutual/demo`)

**Purpose:** Guided step-by-step demo flow

**Password Protected:** Steps 4-6 require password "Ashrith"

**Steps:**
| Step | Title | Link | Protected |
|------|-------|------|-----------|
| 1 | The Problem | /concept | No |
| 2 | QUAD Solution | /flow | No |
| 3 | How It Works | /details | No |
| 4 | Set Up Organization | /dashboard | Yes 🔐 |
| 5 | Assign Users & Roles | /dashboard | Yes 🔐 |
| 6 | Role-Based Dashboards | /dashboard | Yes 🔐 |

---

### 4. Feature Settings (`/massmutual/settings`)

**Purpose:** Configure which features to show in demo

**Presets (QUAD Math Terminology):**
| Preset | Features | Use Case |
|--------|----------|----------|
| FULL MATRIX | 103 features | Show everything |
| PILOT VECTOR | ~40 features | Minimal pilot demo |
| GROWTH PLANE | ~70 features | Mid-tier demo |
| CUSTOM PATH | User-defined | Custom selection |

**Feature Categories:**
- PART 1: Core Concepts (Document-First, QUAD Model)
- PART 2: Organization (Hierarchy, Circles, Roles)
- PART 3: Project Management (Dashboards, Kanban)
- PART 4: Integrations (Jira, GitHub, Slack)
- PART 5: Technical (VS Code, QUAD Algorithms FLUX, QUAD ORBIT Cloud)
- PART 6: ROI (Cost Estimation, Time Tracking)

---

### 5. ROI Calculator (`/massmutual/roi`)

**Purpose:** Show financial impact of QUAD for MassMutual

**Inputs:**
- Number of developers
- Average developer salary
- Current sprint velocity
- Feature delivery time

**Outputs:**
- Time savings
- Cost savings
- Productivity improvement %

---

### 6. Contact (`/massmutual/contact`)

**Purpose:** Schedule personalized demo

**Content:**
- Email: contact@quadframe.work
- Calendar booking link (coming soon)
- Team members list

---

## Demo Data (Pre-populated)

### Organization Structure

```
MassMutual (Parent Org)
├── Digital Experience (Sub-Org)
│   └── Customer Portal (Project)
│       ├── Management Circle
│       ├── Development Circle
│       ├── QA Circle
│       └── Infrastructure Circle
│
└── Data Engineering (Sub-Org)
    └── Claims Pipeline (Project)
        ├── Management Circle
        ├── Development Circle
        ├── QA Circle
        └── Infrastructure Circle
```

### Demo Users

| Name | Role | Allocation |
|------|------|------------|
| Sarah Chen | Senior Director | 40% CP + 40% CLM |
| Mike Rodriguez | Team Lead | 80% CP + 20% CLM |
| Priya Sharma | Principal Engineer | 70% CLM + 30% CP |
| James Wilson | Senior Developer | 100% CP |
| Emma Thompson | QA Lead | 60% CP + 40% CLM |
| David Kim | Platform Engineer | 50% CP + 50% CLM |

### Demo Projects

**1. Customer Portal (CP)**
- Tech: Next.js 15 + Spring Boot 3.2 + PostgreSQL
- Cloud: AWS (ECS, RDS, S3)
- Sprint 12: "Document Upload"
- Health Score: 87%

**2. Claims Pipeline (CLM)**
- Tech: Spring Batch 5 + SageMaker + Redshift
- Cloud: AWS (Lambda, Glue, Step Functions)
- Sprint 8: "ML Improvements"
- Health Score: 92%

---

## Database Tables

| Table | Purpose |
|-------|---------|
| QUAD_organizations | Org hierarchy |
| quad_users | Demo users |
| quad_domains | Projects |
| quad_domain_members | User allocations |
| quad_circles | 4 circles per project |
| quad_cycles | Sprints |
| quad_tickets | Flows at QUAD stages |
| quad_demo_settings | Feature toggles |

**Seed File:** `quad-database/sql/seeds/800_massmutual_demo.dta.sql`

---

## Contact Information

### QUAD Team

| Email | Purpose |
|-------|---------|
| quad@quadframe.work | Main contact |
| contact@quadframe.work | General inquiries |
| support@quadframe.work | Technical support |
| sales@quadframe.work | Demo requests, pricing |
| suman@quadframe.work | CTO - Technical questions |
| madhuri@quadframe.work | CEO - Partnership |
| lokesh@quadframe.work | Team member |
| sharath@quadframe.work | Team member |
| mahesh@quadframe.work | Team member |

---

## Deployment

| Environment | URL | Status |
|-------------|-----|--------|
| DEV | https://dev.quadframe.work/massmutual | ✅ Active |
| PROD | https://massmutual.quadframe.work | ✅ DNS Active |

**DNS Records:**
| Type | Name | Target | Purpose |
|------|------|--------|---------|
| A | massmutual-dev | 96.240.97.243 | DEV (Mac Studio → Caddy) |
| CNAME | massmutual | ghs.googlehosted.com | PROD (GCP Cloud Run) |

---

## API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| /api/demo-settings | GET | Get org feature settings |
| /api/demo-settings | POST | Save org feature settings |
| /api/demo-settings/list | GET | List all configs for org |

---

**Last Updated:** January 7, 2026
**Maintained By:** Suman Addanki
