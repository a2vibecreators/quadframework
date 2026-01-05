# QUAD Database Changelog

**Purpose:** Track database schema changes with reasoning.

**Tech Stack:**
- Frontend: Prisma ORM → PostgreSQL
- Backend: JPA/Hibernate → PostgreSQL

---

## Changelog

### January 4, 2026

**Initial Schema (Prisma)**

Tables created with QUAD_ prefix:
- `QUAD_companies` - Organization accounts
- `QUAD_roles` - Role definitions
- `QUAD_users` - User accounts
- `QUAD_adoption_matrix` - Skill/Trust levels
- `QUAD_domains` - Product/project domains
- `QUAD_domain_members` - User assignments
- `QUAD_circles` - 4 Circles per domain
- `QUAD_circle_members` - User assignments to circles
- `QUAD_flows` - Work items (Q-U-A-D stages)
- `QUAD_flow_stage_history` - Stage transition audit
- `QUAD_domain_resources` - Git repos, databases, cloud projects
- `QUAD_resource_attributes` - Key-value attributes
- `QUAD_work_sessions` - Time tracking
- `QUAD_domain_blueprints` - UI blueprints
- `QUAD_blueprint_agent_sessions` - AI interview sessions

**Total:** 15 tables

---

## Schema Files

| Location | Purpose |
|----------|---------|
| `prisma/schema.prisma` | Prisma schema (Next.js frontend) |
| `quad-database/sql/` | SQL files (Java backend) |

---

## Change Log Format

When adding entries, use this format:

```markdown
### [Date]

**Change:** [Brief description]
**Reason:** [Why this change was needed]
**Tables Affected:** [List tables]
**Migration:** [If migration script needed]
**Approved By:** [User name if architectural change]
```

---

## Design Decisions

### UUID Primary Keys
- All tables use UUID primary keys
- Enables distributed ID generation
- Compatible with both Prisma and JPA

### QUAD_ Prefix
- All tables prefixed with QUAD_
- Prevents conflicts with NutriNine tables
- Same PostgreSQL instance, different databases

### Timestamps
- All tables have `created_at`, `updated_at`
- Managed by Prisma/JPA (not database triggers)

---

**Version:** 1.0
**Last Updated:** January 4, 2026
