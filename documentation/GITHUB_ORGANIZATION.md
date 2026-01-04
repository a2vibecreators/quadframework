# GitHub Organization Structure

This document describes the GitHub organization structure, repositories, and user access for the QUAD Framework project.

## Organizations

| Organization | Purpose | Visibility | URL |
|-------------|---------|------------|-----|
| **a2Vibes** | Active Development | Private | https://github.com/a2Vibes |
| **a2vibecreators** | Backup/Production | Private (NutriNine), Public (QUAD) | https://github.com/a2vibecreators |

## Development Workflow

```
a2Vibes (Development)                    a2vibecreators (Backup)
       |                                          |
       |  Daily automatic sync                    |
       |  (GitHub Actions)                        |
       | ───────────────────────────────────────> |
       |                                          |
   main branch                              backup branch
   sumanMain branch
   SharuMain branch
```

## Repositories

### QUAD Repositories (a2Vibes - Private)

| Repository | Description | Type |
|------------|-------------|------|
| [QUAD](https://github.com/a2Vibes/QUAD) | Parent monorepo | Parent |
| [QUAD-web](https://github.com/a2Vibes/QUAD-web) | Next.js website (quadframe.work) | Submodule |
| [QUAD-services](https://github.com/a2Vibes/QUAD-services) | Java Spring Boot backend | Submodule |
| [QUAD-database](https://github.com/a2Vibes/QUAD-database) | PostgreSQL schemas | Submodule |
| [QUAD-vscode](https://github.com/a2Vibes/QUAD-vscode) | VS Code extension | Submodule |
| [QUAD-ios](https://github.com/a2Vibes/QUAD-ios) | iOS app (future) | Submodule |
| [QUAD-android](https://github.com/a2Vibes/QUAD-android) | Android app (future) | Submodule |

### NutriNine Repositories (a2Vibes - Private)

| Repository | Description | Type |
|------------|-------------|------|
| [NutriNine](https://github.com/a2Vibes/NutriNine) | Parent monorepo | Parent |
| [NutriNine-services](https://github.com/a2Vibes/NutriNine-services) | Java Spring Boot backend API | Submodule |
| [NutriNine-web](https://github.com/a2Vibes/NutriNine-web) | Next.js web application | Submodule |
| [NutriNine-ios](https://github.com/a2Vibes/NutriNine-ios) | iOS SwiftUI app | Submodule |
| [NutriNine-android](https://github.com/a2Vibes/NutriNine-android) | Android Kotlin app | Submodule |
| [NutriNine-database](https://github.com/a2Vibes/NutriNine-database) | PostgreSQL schemas | Submodule |
| [NutriNine-voice](https://github.com/a2Vibes/NutriNine-voice) | Voice assistant (Chinna) | Submodule |
| [NutriNine-docs](https://github.com/a2Vibes/NutriNine-docs) | Codebase documentation RAG | Submodule |
| [NutriNine-models](https://github.com/a2Vibes/NutriNine-models) | AI/ML models | Submodule |
| [NutriNine-windows](https://github.com/a2Vibes/NutriNine-windows) | Windows desktop app (future) | Submodule |

### Backup Repositories (a2vibecreators)

| Repository | Visibility | Syncs From |
|------------|------------|------------|
| QUAD | **Public** | a2Vibes/QUAD |
| QUAD-* (6 repos) | **Public** | a2Vibes/QUAD-* |
| NutriNine | Private | a2Vibes/NutriNine |
| NutriNine-* (9 repos) | Private | a2Vibes/NutriNine-* |
| a2vibecreators-web | Private | Company website |

**Note:** QUAD repos in a2vibecreators are PUBLIC for open-source visibility. NutriNine repos remain private.

## User Access

### a2Vibes Organization (Development)

| Username | Role | Access Level | Working Branch |
|----------|------|--------------|----------------|
| **sumanaddanki** | Admin/Owner | Full access to all repos | `sumanMain` |
| **sharuuu** | Member | Read/Write to all repos | `SharuMain` |
| **lokesh.chowdary@gmail.com** | Member | Read-only | N/A |

**Note:** sharuuu and lokesh.chowdary@gmail.com have pending invitations.

### a2vibecreators Organization (Backup)

| Username | Role | Access Level | Notes |
|----------|------|--------------|-------|
| **sumanaddanki** | Admin/Owner | Full access | Only member - backup org |

**Important:** Only sumanaddanki has access to a2vibecreators. This is intentional for backup security.

## Branch Strategy

```
main ─────────────────────── Protected (production-ready code)
  │
  ├── sumanMain ──────────── Suman's development branch
  │
  └── SharuMain ──────────── Sharath's development branch
```

### Branch Rules

1. **Never push directly to `main`** - Always work on personal branches
2. **Merge via Pull Request** - Code review required
3. **After testing** - Sync to a2vibecreators backup branch

## Automatic Backup Sync

A GitHub Actions workflow runs daily at midnight UTC to sync from a2Vibes to a2vibecreators:

```yaml
# .github/workflows/backup-sync.yml
name: Daily Backup Sync

on:
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight UTC
  workflow_dispatch:      # Manual trigger

jobs:
  sync-to-backup:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: Push to backup
        run: |
          git remote add backup https://${{ secrets.BACKUP_PAT }}@github.com/a2vibecreators/[REPO].git
          git push backup main:backup --force
```

**Required Secret:** `BACKUP_PAT` - Classic Personal Access Token with `repo` scope

## Local Setup

### Clone with Submodules

```bash
# Clone QUAD with all submodules
git clone --recurse-submodules git@github.com:a2Vibes/QUAD.git

# Clone NutriNine with all submodules
git clone --recurse-submodules git@github.com:a2Vibes/NutriNine.git
```

### Add Backup Remote

```bash
# Add upstream remote for backup sync
git remote add upstream git@github.com:a2vibecreators/QUAD.git

# Push to backup after testing
git push upstream sumanMain:main
```

### VS Code Workspace

Open the monorepo workspace file:
```
~/git/a2vibes/a2vibes.code-workspace
```

This workspace includes both QUAD and NutriNine as root folders with submodule detection enabled.

---

**Last Updated:** January 4, 2026
