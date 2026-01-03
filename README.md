# QUAD Framework

**Quick Unified Agentic Development** - A modern software development methodology for the AI era.

Website: [quadframe.work](https://quadframe.work)

---

## About QUAD

QUAD is a software development methodology that replaces traditional Agile/Scrum with:
- **AI-powered automation** - AI agents handle repetitive tasks
- **Documentation-first practices** - Docs written before code
- **Four functional circles** - Management, Development, QA, Infrastructure

### The 1-2-3-4 Hierarchy

- **1 Method** → QUAD (Quick Unified Agentic Development)
- **2 Dimensions** → Business + Technical
- **3 Axioms** → Operators, AI Agents, Docs-First
- **4 Circles** → Management, Development, QA, Infrastructure

---

## Repository Structure

**Git Organization:** Parent repo with git submodules (same pattern as NutriNine)

```
a2vibecreators/                       # GitHub Organization
│
├── quadframework/                    # Parent repo (THIS REPO)
│   ├── .gitmodules                   # Submodule definitions
│   ├── quad-database/                # ← Git Submodule (Prisma schema)
│   ├── quad-services/                # ← Git Submodule (Core business logic)
│   ├── quad-web/                     # ← Git Submodule (Next.js web app)
│   ├── quad-ios/                     # ← Git Submodule (iOS native app)
│   ├── quad-android/                 # ← Git Submodule (Android native app)
│   ├── quad-vscode/                  # ← Git Submodule (VS Code extension)
│   ├── documentation/                # Keep in parent (shared docs)
│   └── scripts/                      # Deploy scripts
│
├── quad-database/                    # Standalone repo
├── quad-services/                    # Standalone repo
├── quad-web/                         # Standalone repo
├── quad-ios/                         # Standalone repo
├── quad-android/                     # Standalone repo
└── quad-vscode/                      # Standalone repo
```

### GitHub Repositories

| Repository | Type | Description |
|------------|------|-------------|
| [a2vibecreators/quadframework](https://github.com/a2vibecreators/quadframework) | Parent | Parent repo with submodules |
| [a2vibecreators/quad-database](https://github.com/a2vibecreators/quad-database) | Submodule | Prisma schema & migrations |
| [a2vibecreators/quad-services](https://github.com/a2vibecreators/quad-services) | Submodule | Core business logic |
| [a2vibecreators/quad-web](https://github.com/a2vibecreators/quad-web) | Submodule | Next.js web application |
| [a2vibecreators/quad-ios](https://github.com/a2vibecreators/quad-ios) | Submodule | iOS native app (SwiftUI) |
| [a2vibecreators/quad-android](https://github.com/a2vibecreators/quad-android) | Submodule | Android native app (Kotlin) |
| [a2vibecreators/quad-vscode](https://github.com/a2vibecreators/quad-vscode) | Submodule | VS Code extension |

---

## Working with Submodules

### Clone with All Submodules

```bash
# Clone with all submodules (recommended for new developers)
git clone --recurse-submodules git@github.com:a2vibecreators/quadframework.git

# If already cloned, initialize submodules
git submodule update --init --recursive
```

### Pull Latest Changes (Including Submodules)

```bash
# Pull parent repo and update all submodules
git pull --recurse-submodules

# Or update all submodules to latest
git submodule update --remote --merge
```

### Make Changes to a Submodule

```bash
# 1. Navigate to submodule directory
cd quadframework-web

# 2. Make changes, commit, and push IN THE SUBMODULE
git add .
git commit -m "Your commit message"
git push

# 3. Go back to parent and update submodule reference
cd ..
git add quadframework-web
git commit -m "Update quadframework-web submodule"
git push
```

### Creating Submodule Repositories

To set up submodules from scratch (admin only):

```bash
# 1. Create repo on GitHub
gh repo create a2vibecreators/quadframework-database --public

# 2. Add as submodule in parent repo
cd quadframework
git submodule add git@github.com:a2vibecreators/quadframework-database.git

# 3. Commit the .gitmodules file
git add .gitmodules quadframework-database
git commit -m "Add quadframework-database submodule"
git push
```

---

## Submodule Descriptions

### quadframework-database

**Purpose:** Database schema, migrations, and SQL files

```
quadframework-database/
├── prisma/
│   ├── schema.prisma             # Full Prisma schema
│   ├── migrations/               # Migration history
│   └── sql/
│       ├── tables/               # Modular table definitions
│       ├── functions/            # PostgreSQL functions
│       ├── triggers/             # Triggers
│       └── views/                # Database views
├── scripts/
│   ├── db-push.sh                # Push schema to database
│   ├── db-seed.sh                # Seed data
│   └── db-reset.sh               # Reset database
└── package.json
```

### quadframework-services

**Purpose:** Reusable business logic shared by web app AND VS Code extension

```
quadframework-services/
├── src/
│   ├── index.ts                  # Main exports
│   ├── ai/                       # AI provider routing
│   ├── memory/                   # Memory system
│   ├── codebase/                 # Code indexing
│   ├── documentation/            # Doc generation
│   ├── tickets/                  # Ticket operations
│   └── agents/                   # Agent system
└── package.json
```

### quadframework-web

**Purpose:** Next.js web application (marketing + dashboard)

```
quadframework-web/
├── src/
│   ├── app/                      # Next.js pages + API routes
│   │   ├── api/                  # REST API endpoints
│   │   └── (pages)/              # Web pages
│   ├── components/               # React components
│   └── lib/                      # Utilities
└── package.json
```

### quad-ios

**Purpose:** Native iOS app for QUAD dashboard access

```
quad-ios/
├── QUAD/
│   ├── Views/                    # SwiftUI views
│   ├── ViewModels/               # MVVM ViewModels
│   └── Services/                 # API client
└── QUAD.xcodeproj
```

### quad-android

**Purpose:** Native Android app for QUAD dashboard access

```
quad-android/
├── app/
│   ├── src/main/java/com/quad/
│   │   ├── ui/                   # Jetpack Compose screens
│   │   ├── viewmodel/            # MVVM ViewModels
│   │   └── data/                 # API + Repository
│   └── build.gradle.kts
└── build.gradle.kts
```

### quad-vscode

**Purpose:** VS Code extension for IDE integration

```
quad-vscode/
├── src/
│   ├── extension.ts              # Entry point
│   ├── commands/                 # VS Code commands
│   ├── providers/                # Completion, hover, etc.
│   └── views/                    # Webview panels
└── package.json
```

---

## Architecture Flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        QUAD Architecture                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐             │
│   │   quad-ios   │    │quad-android  │    │  quad-vscode │             │
│   │   (Swift)    │    │  (Kotlin)    │    │     (TS)     │             │
│   └──────┬───────┘    └──────┬───────┘    └──────┬───────┘             │
│          │                   │                   │                      │
│          │ REST API          │ REST API          │ REST API            │
│          │                   │                   │                      │
│          └───────────────────┼───────────────────┘                      │
│                              │                                          │
│                    ┌─────────▼─────────┐                                │
│                    │  quadframework-web│                                │
│                    │   (Next.js API)   │ ← API Routes                   │
│                    └─────────┬─────────┘                                │
│                              │                                          │
│                    ┌─────────▼─────────┐                                │
│                    │quadframework-svcs │                                │
│                    │ (Business Logic)  │ ← Uses Prisma Client           │
│                    └─────────┬─────────┘                                │
│                              │                                          │
│                    ┌─────────▼─────────┐                                │
│                    │quadframework-db   │                                │
│                    │     (Prisma)      │ ← Schema & Migrations          │
│                    └───────────────────┘                                │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Key Point:** Mobile apps (iOS/Android) do NOT include Prisma. They consume REST APIs.

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| **Web Framework** | Next.js 15 with App Router |
| **Styling** | Tailwind CSS |
| **Language** | TypeScript |
| **Database** | PostgreSQL with Prisma ORM |
| **iOS** | SwiftUI (iOS 16+) |
| **Android** | Kotlin + Jetpack Compose |
| **VS Code** | TypeScript Extension API |
| **Deployment** | Docker + nginx (static export) |

---

## Development

```bash
# Install dependencies
npm install

# Run development server
npm run dev
# Open http://localhost:3003

# Build for production
npm run build
```

---

## Deployment

```bash
# Deploy to DEV (dev.quadframe.work) - Mac Studio
./deploy-studio.sh dev

# Deploy to QA (qa.quadframe.work) - Mac Studio
./deploy-studio.sh qa

# Deploy to PROD (quadframe.work) - GCP Cloud Run
./deploy-gcp.sh

# Deploy to both DEV and QA
./deploy-studio.sh all
```

---

## Project Structure (Current - Before Submodule Migration)

```
quadframework/
├── prisma/                   # Database schema (will become quadframework-database)
│   ├── schema.prisma
│   └── sql/
├── src/
│   ├── app/                  # Next.js pages + API (will become quadframework-web)
│   │   ├── api/              # REST API endpoints
│   │   └── (pages)/          # Marketing + dashboard pages
│   ├── components/           # React components
│   └── lib/
│       └── services/         # Business logic (will become quadframework-services)
├── quad-vscode-plugin/       # VS Code extension (will become quad-vscode)
├── documentation/            # Stays in parent repo
├── Dockerfile
├── deploy-studio.sh
└── package.json
```

---

## DNS Configuration (Cloudflare)

| Type | Name | Content | Purpose |
|------|------|---------|---------|
| A | `@` | Mac Studio IP | quadframe.work |
| A | `dev` | Mac Studio IP | dev.quadframe.work |
| A | `qa` | Mac Studio IP | qa.quadframe.work |

---

## Related Documentation

- [QUAD_SUBMODULES.md](documentation/architecture/QUAD_SUBMODULES.md) - Detailed submodule architecture
- [QUAD_SERVICES_SPEC.md](documentation/architecture/QUAD_SERVICES_SPEC.md) - Services package specification
- [DISCUSSIONS_LOG.md](documentation/internal/DISCUSSIONS_LOG.md) - Development discussions archive

---

## License

Copyright 2025 A2 Vibe Creators LLC. All rights reserved.

QUAD™ is a trademark of A2 Vibe Creators LLC.
