# QUAD Platform

**Complete end-to-end deployable solution for enterprise QUAD adoption**

---

## Overview

**QUAD Platform** is an enterprise-ready installation package that brings the QUAD methodology to your organization. It provides everything needed to implement AI-powered development workflows.

### Core Components

| Component | Description |
|-----------|-------------|
| **AI Agent Runtime** | Pluggable AI providers (Claude, OpenAI, Gemini, Local Ollama) |
| **Integration Hub** | Connect Jira, Slack, GitHub, Teams, Email |
| **Admin Dashboard** | Company/Director/Project management |
| **User Management** | Role-based access control with circle assignments |
| **Analytics** | Flow rate, cycle metrics, agent performance |
| **Enterprise Security** | SSO, audit logs, data encryption |

---

## Deployment Options

QUAD Platform supports two deployment models:

### Option 1: Self-Hosted (Docker)

**Requirements:**
- Docker & Docker Compose
- 8GB RAM minimum (16GB recommended)
- 50GB storage
- PostgreSQL 15+ (included in package)
- Your AI provider API key

**Quick Start:**
```bash
$ git clone quad-platform
$ cp .env.example .env
$ # Edit .env with your API keys
$ docker-compose up -d
# Access: http://localhost:3000
```

**Benefits:**
- Your data stays on your servers
- Full control over infrastructure
- No external dependencies after setup
- Customize as needed

### Option 2: SaaS (Cloud)

**Benefits:**
- No infrastructure to manage
- Automatic updates
- 99.9% uptime SLA
- SOC2 / HIPAA compliant
- Multi-region availability

**Getting Started:**
1. Sign up at quad.dev
2. Create your organization
3. Connect your AI provider
4. Invite your team

**Start in under 5 minutes**

---

## Company Hierarchy

QUAD Platform organizes your organization into a clear hierarchy:

```
COMPANY LEVEL (QUAD Platform Installation)
├── Company Admin (IT/CTO) - Installs QUAD, configures AI providers
│
├── DIRECTOR LEVEL (Portfolio Management)
│   ├── Director 1 (e.g., "Digital Products")
│   │   ├── Project A (NutriNine)
│   │   └── Project B (Inventory App)
│   └── Director 2 (e.g., "Internal Tools")
│       └── Project C (HR Portal)
│
└── PROJECT LEVEL (4 Circles per Project)
    ├── Circle 1: Management (BA, PM, Tech Lead)
    ├── Circle 2: Development (Devs)
    ├── Circle 3: QA (Testers)
    └── Circle 4: Infrastructure (DevOps)
```

### Hierarchy Levels

| Level | Description | Key Responsibility |
|-------|-------------|-------------------|
| **Company** | QUAD Platform Installation | Configure AI, manage directors |
| **Director** | Portfolio Management | Own multiple projects, assign circle leads, set budgets |
| **Project** | 4 Circles Per Project | Execute work within circles |
| **Team** | Operators + AI Agents | Execute circle functions, collaborate with AI |

---

## User Onboarding Journey

From joining a company to becoming a productive QUAD circle member:

| Step | Actor | Action | ACL Granted | Description |
|------|-------|--------|-------------|-------------|
| 1 | IT Admin | Installs QUAD Platform | `COMPANY_ADMIN` | Downloads package, runs Docker, configures AI provider API key |
| 2 | IT Admin | Creates Director Accounts | `DIRECTOR` | Invites department heads (Engineering VP, Product VP, etc.) |
| 3 | Director | Creates Projects | `PROJECT_OWNER` | Sets up projects under their portfolio with 4 circles each |
| 4 | Director | Assigns Circle Leads | `CIRCLE_LEAD` | Tech Lead → Management, Senior Dev → Development, QA Lead → QA, DevOps Lead → Infra |
| 5 | HR / Director | Invites New Employee | `EMPLOYEE` | Employee gets company SSO access, sees available projects |
| 6 | Circle Lead | Assigns to Circle | `CIRCLE_MEMBER` | Employee gains access to circle-specific agents and tools |
| 7 | Employee | Starts Contributing | `OPERATOR` | Works within circle, uses AI agents, follows QUAD flow |

---

## AI Provider Configuration

QUAD is a **generic methodology** - not locked to any single AI provider. Configure your preferred providers at the company level.

### Supported Providers

| Provider | Status | Notes |
|----------|--------|-------|
| **Claude** | Recommended | Best for complex reasoning, code generation |
| **OpenAI** | Supported | GPT-4o, GPT-4 Turbo |
| **Gemini** | Supported | Google's multimodal AI |
| **Ollama** | Self-hosted | Run models locally (Llama, Mistral, etc.) |

### Configuration Example

```yaml
# quad-config.yaml

ai_providers:
  primary:
    type: claude
    api_key: ${ANTHROPIC_API_KEY}
    model: claude-sonnet-4-20250514

  fallback:
    type: openai
    api_key: ${OPENAI_API_KEY}
    model: gpt-4o

  # Self-hosted option
  local:
    type: ollama
    endpoint: http://localhost:11434
    model: llama3.2

# Agent-specific provider overrides
agent_overrides:
  story-agent:
    provider: primary  # Use Claude for story expansion
  code-review-agent:
    provider: primary  # Use Claude for code review
  test-generator:
    provider: fallback  # Use OpenAI for test generation
```

---

## Installation Package Contents

```
quad-platform/
├── docker-compose.yml       # All services orchestration
├── .env.example             # Environment template
├── quad-config.yaml         # QUAD configuration
│
├── services/
│   ├── quad-api/            # Backend API (Node.js/TypeScript)
│   ├── quad-web/            # Admin Dashboard (Next.js)
│   ├── quad-agents/         # AI Agent Runtime
│   └── quad-db/             # PostgreSQL + migrations
│
├── integrations/
│   ├── jira-connector/      # Jira Cloud/Server webhooks
│   ├── slack-connector/     # Slack App integration
│   ├── github-connector/    # GitHub App (PRs, issues)
│   ├── teams-connector/     # Microsoft Teams
│   └── email-connector/     # SMTP/SendGrid
│
├── helm/                    # Kubernetes charts
│   ├── Chart.yaml
│   ├── values.yaml
│   └── templates/
│
└── docs/
    ├── INSTALLATION.md
    ├── CONFIGURATION.md
    └── UPGRADING.md
```

---

## ACL & Permissions Matrix

### Role Permissions

| Role | Company | Directors | Projects | Circles | Agents |
|------|---------|-----------|----------|---------|--------|
| **COMPANY_ADMIN** | Admin | Manage | View All | View All | Configure |
| **DIRECTOR** | View | Self | Manage Own | Assign Leads | View |
| **CIRCLE_LEAD** | — | View | View Assigned | Manage Own | Use |
| **OPERATOR** | — | — | View Assigned | Work In | Use |
| **VIEWER** | — | — | View Only | View Only | — |

### Default ACL (New Employee)

When a new employee joins:
- Can view company directory
- Can see available projects
- Cannot access any project until assigned
- Gets `OPERATOR` role when added to circle

### Inherited Permissions

Permissions flow down the hierarchy:
- Circle members inherit project view access
- Circle leads inherit operator permissions
- Directors inherit circle lead permissions
- Admins have full access to everything

---

## Integration Architecture

### Trigger Sources

QUAD Platform can receive requirements from multiple sources:

| Source | Webhook/Integration | Example Event |
|--------|---------------------|---------------|
| **Jira** | Jira Webhook | Issue created in PROJECT |
| **Slack** | Slack App | Message in #requirements channel |
| **GitHub** | GitHub App | Issue opened with label `feature` |
| **Email** | SMTP/Webhook | Email to requirements@company.com |
| **Teams** | Teams Bot | Adaptive card submitted |
| **Cron** | Internal scheduler | Daily backlog processing |

### Outbound Integrations

QUAD agents can push to:
- **Git**: Create branches, PRs, commits
- **Jira**: Update issues, add comments, transition status
- **Slack/Teams**: Send notifications, request approvals
- **CI/CD**: Trigger pipelines (GitHub Actions, Jenkins)

---

## Security & Compliance

### Authentication
- **SSO Support**: SAML 2.0, OAuth 2.0, OIDC
- **MFA**: TOTP, WebAuthn/FIDO2
- **API Keys**: Scoped tokens for integrations

### Data Protection
- **Encryption at Rest**: AES-256
- **Encryption in Transit**: TLS 1.3
- **Data Residency**: Choose region for SaaS

### Audit & Compliance
- **Audit Logs**: All agent actions logged
- **SOC2 Type II**: Available for SaaS
- **HIPAA**: BAA available for healthcare
- **GDPR**: Data export/deletion support

---

## Pricing (SaaS)

| Plan | Users | Projects | AI Calls/Month | Price |
|------|-------|----------|----------------|-------|
| **Starter** | Up to 10 | 2 | 10,000 | $99/mo |
| **Team** | Up to 50 | 10 | 100,000 | $499/mo |
| **Enterprise** | Unlimited | Unlimited | Custom | Contact us |

**Self-hosted**: One-time license fee + annual support

---

## Getting Started

### For Self-Hosted

1. **Download**: Clone the quad-platform repository
2. **Configure**: Copy `.env.example` to `.env`, add your API keys
3. **Deploy**: Run `docker-compose up -d`
4. **Access**: Open `http://localhost:3000`
5. **Setup**: Create your first Director account
6. **Invite**: Add your team members

### For SaaS

1. **Sign Up**: Create account at quad.dev
2. **Configure AI**: Add your Claude/OpenAI API key
3. **Create Org**: Set up your company structure
4. **Invite Team**: Send invitations to directors
5. **Start Using**: Create your first project

---

## Support & Resources

- **Documentation**: https://docs.quad.dev
- **Community**: https://community.quad.dev
- **GitHub**: https://github.com/quadframework
- **Support**: support@quad.dev

---

**Version**: 1.0.0
**Last Updated**: December 2025
**Author**: A2 Vibe Creators LLC
