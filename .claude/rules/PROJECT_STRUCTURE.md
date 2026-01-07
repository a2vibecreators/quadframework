# QUAD Project Structure Reference

**Purpose:** Know where to look BEFORE creating new files
**Last Updated:** January 5, 2026

---

## Critical Rule: Always Consult Sitemap First

**BEFORE creating ANY new file:**
1. **⭐ READ THE SITEMAP:** `documentation/sitemap/sitemap_documentation.md` (Suman's research - use this index!)
2. **⚠️ Verify sitemap is current:** Check last updated date, cross-reference with actual files
3. Use `Glob` to find similar files: `Glob pattern="**/*deployment*.md"`
4. Use `Grep` to search for keywords: `Grep pattern="deploy.*prod"`
5. Read existing files to understand structure
6. **Only create new files if they truly don't exist**

**Why sitemap first?**
- Suman already did extensive research and documentation
- Sitemap shows what exists and where it lives
- Prevents duplicate work
- May be outdated - always verify with Glob/Grep

---

## Project Root Structure

```
QUAD/
├── .claude/                    # Claude Code configuration
│   ├── commands/               # Slash commands (/quad-init)
│   └── rules/                  # Agent rules, session history, context
│
├── documentation/              # MAIN documentation folder
│   ├── architecture/           # System architecture docs
│   ├── deployment/             # Deployment strategies (READ HERE FIRST!)
│   ├── guides/                 # User guides, how-tos
│   ├── integration/            # Integration guides (OAuth, etc.)
│   ├── methodology/            # QUAD methodology docs
│   └── testing/                # Test plans, strategies
│
├── quad-web/                   # Next.js frontend (main web app)
│   ├── deployment/             # ⚠️ DEPLOYMENT SCRIPTS LIVE HERE!
│   │   ├── dev/                # DEV environment (.env, dev-deploy.sh)
│   │   ├── qa/                 # QA environment (.env, qa-deploy.sh)
│   │   ├── prod/               # PROD environment (Vaultwarden guide only)
│   │   ├── scripts/            # MAIN deployment scripts (deploy.sh, fetch-secrets.sh)
│   │   └── README.md           # ⭐ DEPLOYMENT DOCUMENTATION (READ THIS FIRST!)
│   ├── src/                    # Next.js source code
│   ├── prisma/                 # Prisma schema (frontend ORM)
│   ├── Dockerfile              # Docker build for web app
│   └── package.json            # NPM dependencies
│
├── quad-services/              # Java Spring Boot backend (JPA/Hibernate)
│   ├── src/main/               # Java source code
│   │   ├── java/               # Java packages
│   │   └── resources/          # application.properties, migrations
│   ├── pom.xml                 # Maven dependencies
│   └── Dockerfile              # Docker build for Java backend
│
├── quad-database/              # Database SQL files (submodule)
│   ├── sql/                    # Raw SQL CREATE TABLE scripts
│   ├── migrations/             # Migration history
│   └── deployment/             # Database deployment scripts
│
├── quad-api/                   # API Gateway (rate limiting, auth) (submodule)
│   ├── src/                    # Express.js server
│   └── Dockerfile              # Docker build for API gateway
│
├── quad-vscode/                # VS Code extension (submodule - future)
├── quad-ios/                   # iOS app (submodule - future)
├── quad-android/               # Android app (submodule - future)
│
├── deployment/                 # ⚠️ AVOID CREATING FILES HERE (use quad-web/deployment/)
│   └── prod/                   # Only Vaultwarden setup guide lives here
│
├── CLAUDE.md                   # Main project README for Claude
└── README.md                   # Public README

```

---

## Where Files Live (Lookup Table)

### Deployment

| File Type | Where It Lives | Example |
|-----------|---------------|---------|
| **Deployment scripts** | `quad-web/deployment/scripts/` | `deploy.sh`, `fetch-secrets.sh` |
| **DEV/QA environment files** | `quad-web/deployment/dev/` or `qa/` | `.env`, `dev-deploy.sh`, `qa-deploy.sh` |
| **Deployment documentation** | `quad-web/deployment/README.md` | Main deployment guide |
| **PROD setup guides** | `deployment/prod/` | Vaultwarden setup only |
| **High-level deployment strategy** | `documentation/deployment/` | Deployment modes, strategies |

**Rule:** If it's about deploying quad-web, it lives in `quad-web/deployment/`, NOT `deployment/prod/`

---

### Documentation

| Topic | Where It Lives | Example |
|-------|---------------|---------|
| **Architecture** | `documentation/architecture/` | System design, tech stack |
| **Deployment strategy** | `documentation/deployment/` | Multi-cloud, self-hosted |
| **User guides** | `documentation/guides/` | How-tos, walkthroughs |
| **OAuth/Integration** | `documentation/integration/` | OAuth setup, API integration |
| **QUAD methodology** | `documentation/methodology/` | QUAD concepts, flows |
| **Testing** | `documentation/testing/` | Test plans, QA strategy |
| **Claude-specific** | `.claude/rules/` | Agent rules, session history |

**Rule:** If it's high-level strategy/planning, it goes in `documentation/`. If it's hands-on deployment steps, it goes in `quad-web/deployment/README.md`.

---

### Source Code

| Component | Where It Lives | Language/Framework |
|-----------|---------------|-------------------|
| **Frontend (web UI)** | `quad-web/src/` | Next.js 15, TypeScript, Tailwind |
| **Backend (API)** | `quad-services/src/main/java/` | Java 17, Spring Boot 3.2.1 |
| **Database schema** | `quad-database/sql/` | Raw SQL CREATE TABLE scripts |
| **API Gateway** | `quad-api/src/` | Node.js, Express |
| **VS Code Extension** | `quad-vscode/` | TypeScript (future) |
| **Mobile apps** | `quad-ios/`, `quad-android/` | Swift, Kotlin (future) |

---

### Configuration

| Config Type | Where It Lives | Format |
|-------------|---------------|--------|
| **Frontend env** | `quad-web/.env.local`, `quad-web/deployment/{env}/.env` | Dotenv |
| **Backend config** | `quad-services/src/main/resources/application*.properties` | Java properties |
| **Database connection** | Vaultwarden (QUAD org → {env} collection) | Bitwarden items |
| **Secrets** | Vaultwarden (QUAD org → dev/qa/prod) | Bitwarden items |
| **Docker compose** | (Not used - manual docker commands) | N/A |
| **Claude rules** | `.claude/rules/` | Markdown |

---

## Deployment Script Hierarchy

```
quad-web/deployment/
├── scripts/
│   ├── deploy.sh              ⭐ MAIN SCRIPT (supports dev/qa/prod)
│   └── fetch-secrets.sh       ⭐ Vaultwarden secret fetcher
├── dev/
│   ├── .env                   (DEV secrets - not in git)
│   ├── .env.example           (Template - in git)
│   └── dev-deploy.sh          (Calls ../scripts/deploy.sh dev)
├── qa/
│   ├── .env                   (QA secrets - not in git)
│   ├── .env.example           (Template - in git)
│   └── qa-deploy.sh           (Calls ../scripts/deploy.sh qa)
└── README.md                  ⭐ DEPLOYMENT DOCUMENTATION
```

**Key Points:**
- `deploy.sh` handles ALL environments (dev/qa/prod)
- DEV/QA use `.env` files
- PROD uses Vaultwarden secrets (fetched by `fetch-secrets.sh`)
- README.md has complete deployment instructions

---

## Common Mistakes to Avoid

### ❌ Mistake 1: Creating duplicate deployment scripts

**Wrong:**
```
deployment/prod/deploy-gcp-with-vault.sh  # DUPLICATE!
```

**Right:**
```
quad-web/deployment/scripts/deploy.sh prod  # ALREADY EXISTS!
```

### ❌ Mistake 2: Creating duplicate documentation

**Wrong:**
```
deployment/prod/PRODUCTION_DEPLOYMENT_WORKFLOW.md  # DUPLICATE!
```

**Right:**
```
quad-web/deployment/README.md  # ALREADY HAS PROD SECTION!
```

### ❌ Mistake 3: Not searching before creating

**Wrong workflow:**
1. User asks for production deployment
2. Create new script immediately

**Right workflow:**
1. User asks for production deployment
2. Search: `Glob pattern="**/deploy*.sh"`
3. Read: `quad-web/deployment/scripts/deploy.sh`
4. Check if it already supports prod (it does!)
5. Only enhance if needed, don't duplicate

---

## Search Patterns (Before Creating Files)

### Before creating deployment script:
```
Glob pattern="**/deploy*.sh"
Glob pattern="**/deployment/**/*.sh"
```

### Before creating deployment documentation:
```
Glob pattern="**/deployment/**/*.md"
Glob pattern="**/README.md"
```

### Before creating OAuth guide:
```
Glob pattern="**/OAUTH*.md"
Glob pattern="**/integration/**/*.md"
```

### Before creating architecture docs:
```
Glob pattern="**/architecture/**/*.md"
Glob pattern="**/ARCHITECTURE*.md"
```

---

## Quick Decision Tree

**User asks for deployment help:**
1. Is it about deploying quad-web?
   - YES → Check `quad-web/deployment/README.md` first
   - NO → Check `quad-services/` or relevant submodule
2. Does documentation already exist?
   - YES → Update existing, don't create new
   - NO → Create in appropriate location
3. Is it a script?
   - YES → Check if `deploy.sh` already supports it
   - NO → Create only if truly needed

**User asks for documentation:**
1. Is it hands-on steps (how to deploy)?
   - YES → `quad-web/deployment/README.md`
2. Is it high-level strategy?
   - YES → `documentation/deployment/`
3. Is it about architecture?
   - YES → `documentation/architecture/`

---

## File Naming Conventions

### Scripts
- Environment-specific: `{env}-deploy.sh` (e.g., `dev-deploy.sh`)
- Generic: `deploy.sh` (handles all environments)
- Helpers: `fetch-secrets.sh`, `verify-dns.sh`

### Documentation
- Guides: `HOW_TO_{TOPIC}.md` (e.g., `HOW_TO_DEPLOY.md`)
- Reference: `{TOPIC}_REFERENCE.md` (e.g., `OAUTH_REFERENCE.md`)
- Architecture: `{COMPONENT}_ARCHITECTURE.md`
- READMEs: Always `README.md` (never `QUICK_START.md`, `WORKFLOW.md`)

---

## Reminders

1. **Always `Glob` before creating**
2. **Read existing files to understand structure**
3. **Update existing docs instead of creating new ones**
4. **quad-web/deployment/ is for deployment, NOT deployment/prod/**
5. **Documentation goes in documentation/, NOT scattered everywhere**

---

**Version:** 1.0
**Maintained By:** Claude Code + Suman Addanki
