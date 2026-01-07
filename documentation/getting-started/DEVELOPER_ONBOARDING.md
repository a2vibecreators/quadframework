# QUAD Framework - Developer Onboarding Guide

**For New Developers (Sharath, Remote Team Members)**

This guide walks you through setting up the QUAD Framework development environment on a **new machine**.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Step 1: Clone the Repository](#step-1-clone-the-repository)
3. [Step 2: Initialize Git Submodules](#step-2-initialize-git-submodules)
4. [Step 3: Set Up Vaultwarden Access](#step-3-set-up-vaultwarden-access)
5. [Step 4: Run Setup Script](#step-4-run-setup-script)
6. [Step 5: Verify Database Connection](#step-5-verify-database-connection)
7. [Step 6: Install Dependencies](#step-6-install-dependencies)
8. [Step 7: Start Development Server](#step-7-start-development-server)
9. [Step 8: Test Login](#step-8-test-login)
10. [Troubleshooting](#troubleshooting)
11. [Deploying to DEV/QA](#deploying-to-devqa)
12. [Security Best Practices](#security-best-practices)
13. [Next Steps After Setup](#next-steps-after-setup)
14. [Quick Reference](#quick-reference)

---

## Prerequisites

Before starting, you need:

1. **Mac Studio or macOS machine** (for local DEV/QA)
2. **Vaultwarden Access** - Request from Suman
   - Organization: QUAD (id: `7548352c-4c18-45ab-ba58-cabceb58a25b`)
   - Collections: dev, qa (NOT prod - limited access)
3. **GitHub Access** - Added to a2Vibes organization
4. **Tools Installed:**
   - Git
   - Docker Desktop
   - Node.js 18+ and npm
   - Bitwarden CLI: `brew install bitwarden-cli`

---

## Step 1: Clone the Repository

```bash
# Clone from a2Vibes (active development)
git clone git@github.com:a2Vibes/QUAD.git
cd QUAD

# Checkout your personal branch
git checkout sumanMain  # or sharuMain
```

**✅ Check:** No `.env` files should exist - they're `.gitignored`

```bash
find . -name ".env*" -type f ! -name ".env.example"
# Should return nothing
```

---

## Step 2: Initialize Git Submodules

QUAD uses submodules for modular architecture:

```bash
git submodule update --init --recursive
```

**Expected output:**
```
Submodule 'quad-android' checked out
Submodule 'quad-database' checked out
Submodule 'quad-ios' checked out
Submodule 'quad-services' checked out
Submodule 'quad-vscode' checked out
Submodule 'quad-web' checked out
```

---

## Step 3: Set Up Vaultwarden Access

### 3.1 Configure Vaultwarden Server

```bash
bw config server https://vault.a2vibes.tech
```

### 3.2 Login to Vaultwarden

```bash
bw login
# Enter your email: <your-email>@<domain>
# Enter master password: <your-password>
```

### 3.3 Unlock Vault

```bash
export BW_SESSION=$(bw unlock --raw)
```

**💡 Tip:** Add to `~/.zshrc` or `~/.bashrc` to persist across sessions:
```bash
# Save session for convenience (optional)
bw unlock --raw > ~/.bw-session
export BW_SESSION=$(cat ~/.bw-session)
```

### 3.4 Verify Access to QUAD Organization

```bash
bw list organizations
# Should show: QUAD org with id 7548352c-4c18-45ab-ba58-cabceb58a25b
```

---

## Step 4: Run Setup Script

**This script pulls all secrets from Vaultwarden and creates `.env.local` files:**

```bash
chmod +x scripts/setup-dev-environment.sh
./scripts/setup-dev-environment.sh
```

**Expected Output:**
```
╔═══════════════════════════════════════════════════╗
║   QUAD Framework - Developer Environment Setup   ║
╚═══════════════════════════════════════════════════╝

✅ Vaultwarden connection verified
📥 Fetching credentials from Vaultwarden...
✅ quad-web/.env.local created
✅ .env.deploy created
✅ .gitignore updated

╔═══════════════════════════════════════════════════╗
║              Setup Complete! ✅                    ║
╚═══════════════════════════════════════════════════╝
```

**Files created (NOT committed to Git):**
- `quad-web/.env.local` - Local development secrets
- `.env.deploy` - Deployment secrets for deploy scripts

---

## Step 5: Verify Database Connection

QUAD databases run in Docker on Mac Studio:

```bash
# Check if QUAD databases are running
docker ps | grep postgres-quad

# Expected:
# postgres-quad-dev   (port 14201)
# postgres-quad-qa    (port 15201)
```

**If databases aren't running:**
```bash
# Start QUAD databases (ask Suman for startup script)
/Users/semostudio/scripts/startup-services.sh start
```

---

## Step 6: Install Dependencies

```bash
cd quad-web
npm install
```

---

## Step 7: Start Development Server

```bash
npm run dev
```

**Expected Output:**
```
ready - started server on 0.0.0.0:14001
  ▲ Next.js 15.1.3
  - Local:        http://localhost:14001
```

**🌐 Visit:** http://localhost:14001

---

## Step 8: Test Login

1. Go to http://localhost:14001
2. Click "Sign In"
3. Use test credentials (from Vaultwarden or ask Suman):
   - Email: `suman@a2vibecreators.com`
   - Password: `password123`

---

## Troubleshooting

### ❌ "Cannot connect to database"

**Check 1: Database is running**
```bash
docker ps | grep postgres-quad-dev
```

**Check 2: Verify credentials in Vaultwarden**
```bash
export BW_SESSION=$(bw unlock --raw)
bw get item "Database" --organizationid 7548352c-4c18-45ab-ba58-cabceb58a25b
```

**Check 3: Re-run setup script**
```bash
./scripts/setup-dev-environment.sh
```

**Check 4: Connect directly to verify**
```bash
docker exec postgres-quad-dev psql -U quad_user -d quad_dev_db -c "SELECT 1;"
# Should return: 1
```

---

### ❌ "OAuth credentials required"

**The `.env.local` is missing OAuth secrets.**

**Fix 1: Re-run setup script**
```bash
./scripts/setup-dev-environment.sh
```

**Fix 2: Manually check vault**
```bash
bw get item "Google OAuth" --organizationid 7548352c-4c18-45ab-ba58-cabceb58a25b
bw get item "GitHub OAuth" --organizationid 7548352c-4c18-45ab-ba58-cabceb58a25b
```

**Fix 3: If vault credentials are wrong, update them**
- Login to https://vault.a2vibes.tech
- Navigate to QUAD org → dev collection
- Update "Google OAuth" or "GitHub OAuth" item
- Re-run setup script

---

### ❌ "Vault session expired"

```bash
export BW_SESSION=$(bw unlock --raw)
```

---

### ❌ Port 14001 already in use

**Another process is using port 14001:**

```bash
# Find what's using it
lsof -i :14001

# Stop it if it's an old QUAD container
docker stop quad-web-dev
```

---

## Deploying to DEV/QA

**After local development works:**

```bash
# Deploy to DEV (port 14001)
./deployment/scripts/deploy-studio.sh dev

# Deploy to QA (port 15001)
./deployment/scripts/deploy-studio.sh qa

# Deploy to both
./deployment/scripts/deploy-studio.sh all
```

**Access via Caddy reverse proxy:**
- DEV: https://dev.quadframe.work
- QA: https://qa.quadframe.work

---

## Security Best Practices

### ✅ DO:
- Use Vaultwarden for ALL secrets
- Run `./scripts/setup-dev-environment.sh` on new machines
- Add new secrets to Vaultwarden (not `.env` files)
- Keep your Bitwarden vault unlocked during development

### ❌ DON'T:
- NEVER commit `.env`, `.env.local`, or `.env.deploy` files
- NEVER hardcode secrets in code
- NEVER share secrets via Slack/Email
- NEVER push secrets to GitHub (even in private repos)

---

## When Passwords Don't Work

**If any credential from Vaultwarden doesn't work:**

1. **Verify in vault UI:**
   - Go to https://vault.a2vibes.tech
   - Login and check QUAD org → dev collection
   - Compare credentials with what's in your `.env.local`

2. **Test the credential directly:**
   ```bash
   # Example: Test database password
   docker exec postgres-quad-dev psql -U quad_user -d quad_dev_db -c "SELECT 1;"
   ```

3. **Update in Vaultwarden if wrong:**
   - Update the item in https://vault.a2vibes.tech
   - Re-run `./scripts/setup-dev-environment.sh`
   - Restart your dev server

4. **Ask Suman:**
   - If credentials are completely wrong, ask Suman to verify and update vault

---

## Next Steps After Setup

1. **Read project documentation:**
   - [CLAUDE.md](../../CLAUDE.md) - Complete project guide
   - [README.md](../../README.md) - Quick start

2. **Join communication channels:**
   - GitHub Discussions (for code questions)
   - Slack #quad-dev (for daily coordination)

3. **Run tests:**
   ```bash
   cd quad-web
   npm test
   ```

4. **Make your first contribution:**
   - Create a feature branch from `sumanMain` or `sharuMain`
   - Make changes
   - Submit PR to `main`

---

## Quick Reference

**Vault Organization IDs:**
- QUAD Org: `7548352c-4c18-45ab-ba58-cabceb58a25b`
- DEV Collection: `bd26fd3e-b01f-47a9-80e9-9841b52fc1c6`
- QA Collection: `75fb3b57-9e84-4e2d-8b4f-447518e0a315`

**Ports:**
- QUAD DEV Web: 14001
- QUAD DEV API (Java): 14101
- QUAD DEV Database: 14201
- QUAD QA Web: 15001
- QUAD QA API (Java): 15101
- QUAD QA Database: 15201

**Key Commands:**
```bash
# Setup
./scripts/setup-dev-environment.sh

# Development
cd quad-web && npm run dev

# Deploy
./deployment/scripts/deploy-studio.sh {dev|qa|all}

# Database
docker exec postgres-quad-dev psql -U quad_user -d quad_dev_db

# Vault
export BW_SESSION=$(bw unlock --raw)
bw list items --organizationid 7548352c-4c18-45ab-ba58-cabceb58a25b
```

---

**Last Updated:** January 4, 2026
**Author:** QUAD Team
**Questions?** Ask Suman or check #quad-dev
