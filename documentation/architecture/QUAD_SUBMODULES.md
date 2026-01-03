# QUAD Framework - Submodules Architecture

**Last Updated:** January 3, 2026
**Status:** Planning

---

## Table of Contents

1. [Current State](#1-current-state)
2. [Proposed Structure](#2-proposed-structure)
3. [Submodule Breakdown](#3-submodule-breakdown)
4. [Migration Plan](#4-migration-plan)
5. [Services Project](#5-services-project)
6. [Benefits](#6-benefits)

---

## 1. Current State

### Current Monorepo Structure

```
quadframework/                    # Single Next.js repo
├── prisma/                       # Database schema
│   ├── schema.prisma
│   └── sql/                      # Modular SQL files
├── src/
│   ├── app/                      # Next.js pages + API routes
│   │   ├── api/                  # REST API endpoints
│   │   └── (pages)/              # Web app pages
│   ├── components/               # React components
│   └── lib/                      # Shared libraries
│       ├── services/             # Business logic
│       └── db.ts                 # Database connection
├── documentation/                # All documentation
└── quad-vscode-plugin/           # VS Code extension (excluded from build)
```

### Problems with Current Structure

| Problem | Impact |
|---------|--------|
| Everything coupled | Can't deploy API without web app |
| Large builds | Changes to docs trigger full rebuild |
| VS Code plugin in wrong place | Needs separate repo |
| No reusable services | API and VS Code duplicate logic |
| Hard to scale team | Everyone works in same repo |

---

## 2. Proposed Structure

### New Multi-Repo with Submodules

```
a2vibecreators/                   # GitHub Organization
│
├── quadframework/                # Parent repo (orchestrator)
│   ├── .gitmodules               # Submodule definitions
│   ├── quad-database/            # ← Submodule (Prisma schema)
│   ├── quad-services/            # ← Submodule (Core business logic)
│   ├── quad-ui/                  # ← Submodule (Next.js web app)
│   ├── quad-ios/                 # ← Submodule (iOS native app)
│   ├── quad-android/             # ← Submodule (Android native app)
│   ├── quad-vscode/              # ← Submodule (VS Code extension)
│   ├── documentation/            # Keep in parent (shared docs)
│   └── scripts/                  # Deploy scripts
│
├── quad-database/                # Standalone repo
│   ├── prisma/
│   │   ├── schema.prisma
│   │   ├── migrations/
│   │   └── sql/
│   └── package.json
│
├── quad-services/                # Standalone repo
│   ├── src/
│   │   ├── services/             # Core business logic
│   │   ├── ai/                   # AI routing, providers
│   │   ├── memory/               # Memory system
│   │   └── index.ts              # Exports
│   └── package.json
│
├── quad-ui/                      # Standalone repo (Web App)
│   ├── src/
│   │   ├── app/                  # Next.js pages + API
│   │   └── components/
│   └── package.json              # Depends on services
│
├── quad-ios/                     # Standalone repo (iOS App)
│   ├── QUAD/
│   │   ├── Views/                # SwiftUI views
│   │   ├── ViewModels/           # MVVM ViewModels
│   │   └── Services/             # API client
│   └── QUAD.xcodeproj
│
├── quad-android/                 # Standalone repo (Android App)
│   ├── app/
│   │   ├── src/main/java/        # Kotlin source
│   │   └── src/main/res/         # Resources
│   └── build.gradle.kts
│
└── quad-vscode/                  # Standalone repo (VS Code Extension)
    ├── src/
    │   └── extension.ts
    └── package.json              # Depends on services
```

---

## 3. Submodule Breakdown

### quadframework-database

**Purpose:** Database schema and migrations only

```
quadframework-database/
├── prisma/
│   ├── schema.prisma             # Full schema
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
├── package.json
└── README.md
```

**Dependencies:** None (standalone)

**Consumers:**
- quadframework-web (imports Prisma client)
- quadframework-services (imports Prisma client)

---

### quadframework-services (NEW)

**Purpose:** Reusable business logic for web app AND VS Code extension

```
quadframework-services/
├── src/
│   ├── index.ts                  # Main exports
│   │
│   ├── ai/                       # AI Provider Layer
│   │   ├── router.ts             # Intelligent routing
│   │   ├── providers/
│   │   │   ├── claude.ts
│   │   │   ├── gemini.ts
│   │   │   ├── groq.ts
│   │   │   └── deepseek.ts
│   │   ├── classifier.ts         # Hybrid classification
│   │   └── types.ts
│   │
│   ├── memory/                   # Memory System
│   │   ├── memory-service.ts     # Hierarchical memory
│   │   ├── chunk-service.ts      # Document chunking
│   │   ├── keyword-service.ts    # Keyword extraction
│   │   └── types.ts
│   │
│   ├── codebase/                 # Codebase Indexing
│   │   ├── indexer.ts            # Code indexer
│   │   ├── parser.ts             # tree-sitter parsing
│   │   └── types.ts
│   │
│   ├── documentation/            # Doc Generation
│   │   ├── generator.ts          # AI doc generation
│   │   ├── templates/            # Doc templates
│   │   └── types.ts
│   │
│   ├── tickets/                  # Ticket Operations
│   │   ├── ticket-service.ts
│   │   ├── sprint-service.ts
│   │   └── types.ts
│   │
│   ├── agents/                   # Agent System
│   │   ├── base-agent.ts
│   │   ├── dev-agent.ts
│   │   ├── review-agent.ts
│   │   ├── ba-agent.ts
│   │   └── types.ts
│   │
│   └── utils/                    # Shared utilities
│       ├── token-counter.ts
│       └── cost-calculator.ts
│
├── package.json
├── tsconfig.json
└── README.md
```

**Dependencies:**
- `@prisma/client` (from quadframework-database)
- `@anthropic-ai/sdk`
- `@google/generative-ai`
- `groq-sdk`

**Consumers:**
- quadframework-web (API routes use services)
- quadframework-vscode (Extension uses services)

**Key Insight:** This is the "glue" that both web and VS Code share!

---

### quadframework-web

**Purpose:** Next.js web application (pages + API)

```
quadframework-web/
├── src/
│   ├── app/
│   │   ├── api/                  # REST API (thin layer)
│   │   │   ├── ai/               # AI endpoints
│   │   │   ├── memory/           # Memory endpoints
│   │   │   ├── tickets/          # Ticket endpoints
│   │   │   └── ...
│   │   ├── (pages)/              # Web pages
│   │   │   ├── dashboard/
│   │   │   ├── configure/
│   │   │   └── ...
│   │   └── layout.tsx
│   │
│   ├── components/               # React components
│   │   ├── ui/
│   │   └── ...
│   │
│   └── lib/
│       ├── auth.ts               # NextAuth
│       └── db.ts                 # Prisma client
│
├── package.json                  # Depends on services
├── next.config.ts
└── README.md
```

**Dependencies:**
- `quadframework-services` (npm link or workspace)
- `quadframework-database` (Prisma client)
- `next`, `react`, etc.

**API Routes Pattern:**
```typescript
// src/app/api/ai/route.ts
import { AIRouter } from 'quadframework-services';

export async function POST(request: NextRequest) {
  const { prompt, task_type } = await request.json();

  // Use shared service
  const response = await AIRouter.route({
    prompt,
    taskType: task_type,
    orgId: session.orgId,
  });

  return NextResponse.json(response);
}
```

---

### quadframework-vscode

**Purpose:** VS Code extension

```
quadframework-vscode/
├── src/
│   ├── extension.ts              # Entry point
│   │
│   ├── commands/                 # VS Code commands
│   │   ├── generate-docs.ts
│   │   ├── explain-code.ts
│   │   └── chat.ts
│   │
│   ├── providers/                # VS Code providers
│   │   ├── completion.ts
│   │   └── hover.ts
│   │
│   ├── views/                    # Webview panels
│   │   ├── chat-panel.ts
│   │   └── ticket-panel.ts
│   │
│   └── services/                 # Service wrappers
│       └── quad-client.ts        # Wraps quadframework-services
│
├── package.json
├── tsconfig.json
└── README.md
```

**Dependencies:**
- `quadframework-services` (bundled)
- `vscode` (VS Code API)

**Service Usage:**
```typescript
// src/services/quad-client.ts
import { DocumentationService, AIRouter } from 'quadframework-services';

export class QuadClient {
  async generateDocs(code: string, language: string) {
    return DocumentationService.generate({
      code,
      language,
      // Uses user's Gemini key (BYOK)
      apiKey: this.config.geminiKey,
    });
  }
}
```

---

### quad-ios

**Purpose:** Native iOS app for QUAD platform access on iPhone/iPad

```
quad-ios/
├── QUAD/
│   ├── App/
│   │   ├── QUADApp.swift           # App entry point
│   │   └── ContentView.swift       # Main container
│   │
│   ├── Views/                      # SwiftUI Views
│   │   ├── Dashboard/
│   │   │   ├── DashboardView.swift
│   │   │   └── WidgetViews/
│   │   ├── IDE/
│   │   │   ├── IDETabView.swift    # IDE experience
│   │   │   └── CodeEditorView.swift
│   │   ├── Tickets/
│   │   │   ├── TicketListView.swift
│   │   │   └── TicketDetailView.swift
│   │   └── Chat/
│   │       └── AIChatView.swift
│   │
│   ├── ViewModels/                 # MVVM ViewModels
│   │   ├── DashboardViewModel.swift
│   │   ├── TicketViewModel.swift
│   │   └── ChatViewModel.swift
│   │
│   ├── Services/                   # API & Services
│   │   ├── APIClient.swift         # REST API calls
│   │   ├── AuthService.swift       # Authentication
│   │   └── WebSocketService.swift  # Real-time updates
│   │
│   ├── Models/                     # Data Models
│   │   ├── Ticket.swift
│   │   ├── Project.swift
│   │   └── User.swift
│   │
│   └── Resources/
│       └── Assets.xcassets
│
├── QUAD.xcodeproj
├── QUADTests/
└── README.md
```

**Tech Stack:**
- SwiftUI (iOS 16+)
- Combine for reactive programming
- URLSession for networking
- Keychain for secure storage

**Key Features:**
- Role-based dashboard (same as web)
- Ticket management on the go
- AI chat for quick queries
- Push notifications for agent updates
- Offline support for viewing tickets

---

### quad-android

**Purpose:** Native Android app for QUAD platform access

```
quad-android/
├── app/
│   ├── src/main/
│   │   ├── java/com/quad/
│   │   │   ├── QUADApplication.kt
│   │   │   │
│   │   │   ├── ui/                 # Jetpack Compose UI
│   │   │   │   ├── dashboard/
│   │   │   │   │   ├── DashboardScreen.kt
│   │   │   │   │   └── WidgetComponents.kt
│   │   │   │   ├── ide/
│   │   │   │   │   ├── IDEScreen.kt
│   │   │   │   │   └── CodeEditorView.kt
│   │   │   │   ├── tickets/
│   │   │   │   │   ├── TicketListScreen.kt
│   │   │   │   │   └── TicketDetailScreen.kt
│   │   │   │   └── chat/
│   │   │   │       └── AIChatScreen.kt
│   │   │   │
│   │   │   ├── viewmodel/          # MVVM ViewModels
│   │   │   │   ├── DashboardViewModel.kt
│   │   │   │   ├── TicketViewModel.kt
│   │   │   │   └── ChatViewModel.kt
│   │   │   │
│   │   │   ├── data/               # Data Layer
│   │   │   │   ├── api/
│   │   │   │   │   ├── QUADApiService.kt  # Retrofit
│   │   │   │   │   └── AuthInterceptor.kt
│   │   │   │   ├── repository/
│   │   │   │   └── model/
│   │   │   │
│   │   │   └── di/                 # Hilt DI
│   │   │       └── AppModule.kt
│   │   │
│   │   └── res/
│   │       ├── values/
│   │       └── drawable/
│   │
│   └── build.gradle.kts
│
├── build.gradle.kts
├── settings.gradle.kts
└── README.md
```

**Tech Stack:**
- Jetpack Compose (Material 3)
- Kotlin Coroutines + Flow
- Retrofit + OkHttp
- Hilt for DI
- DataStore for preferences

**Key Features:**
- Same role-based dashboard as iOS/Web
- Ticket management
- AI chat interface
- FCM push notifications
- Offline-first with Room database

---

## Prisma Concern: Mobile Apps Don't Use Prisma

> **Important:** Mobile apps (iOS/Android) do NOT include Prisma. They consume the REST API exposed by `quad-ui` (Next.js).

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
│                    │     quad-ui       │                                │
│                    │   (Next.js API)   │ ← API Routes                   │
│                    └─────────┬─────────┘                                │
│                              │                                          │
│                    ┌─────────▼─────────┐                                │
│                    │   quad-services   │                                │
│                    │ (Business Logic)  │ ← Uses Prisma Client           │
│                    └─────────┬─────────┘                                │
│                              │                                          │
│                    ┌─────────▼─────────┐                                │
│                    │   quad-database   │                                │
│                    │     (Prisma)      │ ← Schema & Migrations          │
│                    └───────────────────┘                                │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Why this works:**
- Mobile apps are **thin clients** - just UI
- Business logic stays in `quad-services`
- Prisma only runs server-side in `quad-ui` and `quad-services`
- Mobile apps call REST APIs, not database directly
- This is the same pattern as NutriNine (Java API + iOS/Android clients)

---

## 4. Migration Plan

### Phase 1: Extract Database (1 day)

```bash
# 1. Create new repo
gh repo create a2vibecreators/quadframework-database --public

# 2. Copy prisma folder
cp -r quadframework/prisma quadframework-database/

# 3. Add as submodule to parent
cd quadframework
git submodule add git@github.com:a2vibecreators/quadframework-database.git
```

### Phase 2: Create Services Package (2 days)

```bash
# 1. Create new repo
gh repo create a2vibecreators/quadframework-services --public

# 2. Move service files from lib/services/
# 3. Set up npm package
# 4. Add as submodule
```

### Phase 3: Update Web App (1 day)

```bash
# 1. Create new repo
gh repo create a2vibecreators/quadframework-web --public

# 2. Move remaining Next.js code
# 3. Update imports to use services package
# 4. Add as submodule
```

### Phase 4: Move VS Code Plugin (1 day)

```bash
# 1. Create new repo
gh repo create a2vibecreators/quad-vscode --public

# 2. Move quad-vscode-plugin contents
# 3. Update to use services package
# 4. Add as submodule
```

### Phase 5: Create iOS App (Phase 2 - 2-3 weeks)

```bash
# 1. Create new repo
gh repo create a2vibecreators/quad-ios --private

# 2. Initialize Xcode project with SwiftUI
# 3. Set up API client to call quad-ui endpoints
# 4. Implement role-based dashboard
# 5. Add as submodule
```

### Phase 6: Create Android App (Phase 2 - 2-3 weeks)

```bash
# 1. Create new repo
gh repo create a2vibecreators/quad-android --private

# 2. Initialize Android project with Compose
# 3. Set up Retrofit to call quad-ui endpoints
# 4. Implement role-based dashboard
# 5. Add as submodule
```

### Migration Timeline

| Phase | Component | Effort | Priority |
|-------|-----------|--------|----------|
| 1 | quad-database | 1 day | P0 (Now) |
| 2 | quad-services | 2 days | P0 (Now) |
| 3 | quad-ui (web) | 1 day | P0 (Now) |
| 4 | quad-vscode | 1 day | P1 (Next) |
| 5 | quad-ios | 2-3 weeks | P2 (Later) |
| 6 | quad-android | 2-3 weeks | P2 (Later) |

**Note:** iOS and Android are Phase 2 priorities. Focus on web platform first.

---

## 5. Services Project - Key Design

### Why a Separate Services Package?

```
WITHOUT services package:
  ┌─────────────────┐     ┌─────────────────┐
  │   Web App       │     │   VS Code       │
  │                 │     │                 │
  │  ┌───────────┐  │     │  ┌───────────┐  │
  │  │ AI Logic  │  │     │  │ AI Logic  │  │  ← DUPLICATE!
  │  │ Memory    │  │     │  │ Memory    │  │  ← DUPLICATE!
  │  │ Indexing  │  │     │  │ Indexing  │  │  ← DUPLICATE!
  │  └───────────┘  │     │  └───────────┘  │
  └─────────────────┘     └─────────────────┘

WITH services package:
  ┌─────────────────┐     ┌─────────────────┐
  │   Web App       │     │   VS Code       │
  │                 │     │                 │
  │  Uses services  │     │  Uses services  │
  └────────┬────────┘     └────────┬────────┘
           │                       │
           └───────────┬───────────┘
                       │
              ┌────────▼────────┐
              │ QUAD Services   │
              │                 │
              │  • AI Router    │
              │  • Memory       │
              │  • Indexing     │
              │  • Agents       │
              └─────────────────┘
```

### Services Package API

```typescript
// quadframework-services/src/index.ts

// AI
export { AIRouter } from './ai/router';
export { ClaudeProvider, GeminiProvider, GroqProvider } from './ai/providers';
export { HybridClassifier } from './ai/classifier';

// Memory
export { MemoryService } from './memory/memory-service';
export { ChunkService } from './memory/chunk-service';

// Codebase
export { CodebaseIndexer } from './codebase/indexer';
export { TreeSitterParser } from './codebase/parser';

// Documentation
export { DocumentationService } from './documentation/generator';

// Tickets
export { TicketService } from './tickets/ticket-service';
export { SprintService } from './tickets/sprint-service';

// Agents
export { DevAgent, ReviewAgent, BAAgent, QAAgent } from './agents';

// Types
export * from './types';
```

### Usage in Web App

```typescript
// quadframework-web/src/app/api/memory/route.ts
import { MemoryService } from 'quadframework-services';
import { prisma } from '@/lib/db';

export async function POST(request: NextRequest) {
  const memoryService = new MemoryService(prisma);
  const result = await memoryService.retrieve({
    orgId: session.orgId,
    level: 'project',
    keywords: ['authentication'],
  });
  return NextResponse.json(result);
}
```

### Usage in VS Code Extension

```typescript
// quadframework-vscode/src/commands/generate-docs.ts
import { DocumentationService } from 'quadframework-services';
import * as vscode from 'vscode';

export async function generateDocs() {
  const editor = vscode.window.activeTextEditor;
  const code = editor?.document.getText(editor.selection);

  const docs = await DocumentationService.generate({
    code,
    language: editor?.document.languageId,
    apiKey: getConfig('geminiKey'), // User's BYOK key
  });

  // Insert docs above selection
  editor?.edit(builder => {
    builder.insert(editor.selection.start, docs + '\n');
  });
}
```

---

## 6. Benefits

### For Development

| Benefit | Description |
|---------|-------------|
| **Faster builds** | Only rebuild what changed |
| **Clear ownership** | Database team, services team, UI team |
| **Parallel work** | Teams work on different repos |
| **Smaller PRs** | Changes scoped to one area |
| **Reusable logic** | Write once, use in web + VS Code |

### For Deployment

| Benefit | Description |
|---------|-------------|
| **Independent deploys** | Update API without touching web |
| **Version control** | Pin submodule versions |
| **Rollback** | Rollback one component |
| **Scaling** | Scale services independently |

### For VS Code Extension

| Benefit | Description |
|---------|-------------|
| **Shared logic** | Same AI router as web app |
| **Consistent behavior** | Memory works same everywhere |
| **Smaller bundle** | Only import what's needed |
| **BYOK works** | Services support user API keys |

---

## Next Steps

1. ✅ Document structure (this file)
2. [ ] Create quadframework-database repo
3. [ ] Create quadframework-services repo
4. [ ] Migrate existing services
5. [ ] Update quadframework-web to use services
6. [ ] Move VS Code plugin to separate repo

---

*This architecture enables QUAD to scale from 1 developer to 100+ while keeping code reusable and maintainable.*
