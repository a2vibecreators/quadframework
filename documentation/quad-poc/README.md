# QUAD Documentation

> Quick Unified Agentic Development - Patent Pending (63/956,810)

## Documentation Structure

```
docs/
├── README.md                    # This file - Overview
├── architecture/
│   ├── overview.md              # System architecture
│   ├── scenario-1-rag.md        # RAG-based context injection
│   └── agent-hierarchy.md       # QUAD Agent structure
├── cli/
│   ├── commands.md              # CLI command reference
│   ├── installation.md          # Setup guide
│   └── examples.md              # Usage examples
├── api/
│   ├── endpoints.md             # API reference
│   ├── authentication.md        # Auth flow
│   └── context-types.md         # Context query types
├── excel/
│   ├── template-guide.md        # Excel template usage
│   └── field-reference.md       # Field descriptions
└── deployment/
    ├── gcp-setup.md             # GCP configuration
    ├── secrets.md               # Secret Manager setup
    └── cloud-run.md             # Cloud Run deployment
```

## Quick Links

| Topic | Document |
|-------|----------|
| **Getting Started** | [CLI Installation](cli/installation.md) |
| **Architecture** | [System Overview](architecture/overview.md) |
| **CLI Reference** | [Commands](cli/commands.md) |
| **API Reference** | [Endpoints](api/endpoints.md) |
| **Excel Template** | [Template Guide](excel/template-guide.md) |
| **Deployment** | [GCP Setup](deployment/gcp-setup.md) |

## What is QUAD?

QUAD (Quick Unified Agentic Development) is a methodology for compliance-aware AI code generation with zero hallucination. The QUAD CLI provides tools to:

1. **Initialize projects** from Excel templates
2. **Query context** about team, availability, projects
3. **Deploy** to GCP Cloud Run with secrets management
4. **Integrate** with Claude Code via hooks

## Architecture at a Glance

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Claude Code    │────▶│  QUAD API       │────▶│  PostgreSQL     │
│  (quad-* cmds)  │     │  (localhost:3000)│     │  (port 14201)   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
         │                       │
         │                       │ NO AI on our side
         ▼                       ▼
   AI processing          DB lookup only
   (Claude CLI)           (context fetch)
```

**Key Principle:** QUAD API does NO AI calls - only database lookups. Claude CLI handles all AI processing.

## Quick Start

```bash
# 1. Create Excel template
quad template my-org.xlsx

# 2. Fill in Excel (team, projects, deployment config)
# 3. Initialize from Excel
quad init @my-org.xlsx

# 4. Start API server
quad serve

# 5. Query with context
quad question "Who has availability?"

# 6. Deploy to GCP
quad dev deploy suma
```

---

*Copyright © 2026 Gopi Suman Addanke. All Rights Reserved.*
