# QUAD Context Files Quick Reference

**Purpose:** Quick lookup for which files to read before making changes.

---

## Essential Files (Always Read First)

| Step | File | Purpose |
|------|------|---------|
| 1 | [../CLAUDE.md](../CLAUDE.md) | Project overview, tech stack, deployment |
| 2 | [AGENT_RULES.md](AGENT_RULES.md) | 10 core rules for Claude Code |
| 3 | [SESSION_HISTORY.md](SESSION_HISTORY.md) | Previous session context |
| 4 | This file | Quick reference for key files |

---

## By Area of Work

### Frontend (Next.js)

| File | Purpose |
|------|---------|
| `quad-web/src/app/` | App Router pages |
| `quad-web/src/components/` | Reusable components |
| `quad-web/src/lib/` | Utilities, API clients |
| `quad-web/src/context/` | React contexts |
| `quad-web/.env.local` | Environment variables |

### Backend (Java Spring Boot)

| File | Purpose |
|------|---------|
| `quad-services/src/main/java/.../controller/` | REST endpoints |
| `quad-services/src/main/java/.../service/` | Business logic |
| `quad-services/src/main/java/.../repository/` | JPA repositories |
| `quad-services/src/main/java/.../entity/` | JPA entities |
| `quad-services/pom.xml` | Maven dependencies |

### API Gateway

| File | Purpose |
|------|---------|
| `quad-api/src/index.js` | Express server |
| `quad-api/src/middleware/` | Auth, rate limiting |
| `quad-api/Dockerfile` | Container build |

### Database

| File | Purpose |
|------|---------|
| `prisma/schema.prisma` | Prisma schema (Next.js) |
| `quad-database/sql/` | SQL files (Java) |
| `documentation/database/` | Architecture docs |

### Authentication

| File | Purpose |
|------|---------|
| `quad-web/src/lib/authOptions.ts` | NextAuth config |
| `quad-services/.../config/SecurityConfig.java` | Spring Security |
| `documentation/OAUTH_IMPLEMENTATION.md` | OAuth flow docs |

### Deployment

| File | Purpose |
|------|---------|
| `deploy-studio.sh` | Mac Studio deploy script |
| `deployment/scripts/` | Deployment utilities |
| `docker-compose.yml` | Container orchestration |

---

## Before Making Changes

### Schema Changes (Prisma)
1. Read `prisma/schema.prisma`
2. Read [SESSION_HISTORY.md](SESSION_HISTORY.md) for recent changes
3. Run `npx prisma db push` after changes
4. Update [SESSION_HISTORY.md](SESSION_HISTORY.md)
5. Update [DATABASE_CHANGELOG.md](DATABASE_CHANGELOG.md)

### Schema Changes (Java)
1. Read entity in `quad-services/.../entity/`
2. Read repository in `quad-services/.../repository/`
3. Read service in `quad-services/.../service/`
4. Update all three together
5. Run tests: `mvn test`

### API Changes
1. Read controller file
2. Read corresponding service
3. Update Javadoc/comments
4. Add/update tests

### UI Changes
1. Read component file
2. Check for related components
3. Check contexts used
4. Test on DEV: https://dev.quadframe.work

---

## Secrets Location

| Secret | Location |
|--------|----------|
| Database credentials | Vaultwarden: QUAD org > dev |
| OAuth keys | Vaultwarden: QUAD org > dev |
| API keys | `.env.local` (from Vaultwarden) |

**CLI:** `bw list items --organizationid 579c22f3-4f13-447c-a861-9a4aa0ab7fbc`

---

## Quick Commands

```bash
# Frontend dev
cd quad-web && npm run dev

# Backend dev
cd quad-services && mvn spring-boot:run

# Database
npx prisma studio

# Deploy
./deploy-studio.sh dev

# Tests
cd quad-services && mvn test
```

---

**Version:** 1.0
**Last Updated:** January 4, 2026
