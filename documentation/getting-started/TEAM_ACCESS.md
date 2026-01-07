# QUAD Team Access Guide

**Purpose:** Guide for team members to set up Vaultwarden access and deploy QUAD to dev/qa/prod environments.

**Last Updated:** January 5, 2026

---

## Table of Contents

1. [Overview](#overview)
2. [Vaultwarden Organization Structure](#vaultwarden-organization-structure)
3. [One-Time Setup](#one-time-setup)
4. [Daily Workflow](#daily-workflow)
5. [Deployment Guide](#deployment-guide)
6. [Troubleshooting](#troubleshooting)

---

## Overview

QUAD uses **Vaultwarden** (self-hosted Bitwarden) for secrets management. This ensures:
- ✅ Secure credential storage
- ✅ Role-based access control
- ✅ Audit trail (who accessed what)
- ✅ Easy credential rotation

**Vaultwarden Server:** https://vault.a2vibes.tech

---

## Vaultwarden Organization Structure

### QUAD Organization
```
QUAD Organization (579c22f3-4f13-447c-a861-9a4aa0ab7fbc)
├── Collections (Folder-Level Authorization)
│   ├── dev (e4f03d1a-b8ac-4186-a384-0fb62d431ddd)
│   │   ├── Google OAuth
│   │   ├── GitHub OAuth
│   │   ├── NextAuth Secret
│   │   ├── Database
│   │   └── Anthropic API Key
│   │
│   ├── qa (75fb3b57-9e84-4e2d-8b4f-447518e0a315)
│   │   ├── Google OAuth
│   │   ├── GitHub OAuth
│   │   ├── NextAuth Secret
│   │   ├── Database
│   │   └── Anthropic API Key
│   │
│   └── prod (cc4a16a2-9acc-459a-ad37-a8ef99592366)
│       ├── Google OAuth
│       ├── GitHub OAuth
│       ├── NextAuth Secret
│       ├── Database (GCP Cloud SQL)
│       └── Anthropic API Key
│
├── Members
│   ├── sumanaddanki (Owner)
│   │   └── Access: dev, qa, prod (all collections)
│   │
│   └── sharuuu (User)
│       └── Access: dev, qa only (no prod access)
```

### Access Levels

| Member | Role | Dev | QA | Prod | Notes |
|--------|------|-----|----|----|-------|
| **sumanaddanki** | Owner | ✅ | ✅ | ✅ | Full access to all environments |
| **sharuuu** | User | ✅ | ✅ | ❌ | Can deploy to dev/qa, must request prod deployments |

**Rationale:**
- **Dev/QA:** Open access for rapid iteration
- **Prod:** Restricted to prevent accidental deployments (requires code review)

---

## One-Time Setup

### Step 1: Install Bitwarden CLI

```bash
# Install globally via npm
npm install -g @bitwarden/cli

# Verify installation
bw --version
```

### Step 2: Configure Vaultwarden Server

```bash
# Point CLI to our self-hosted server
bw config server https://vault.a2vibes.tech

# Verify configuration
bw config server
# Output: https://vault.a2vibes.tech
```

### Step 3: Accept Organization Invitation

1. **Check your email** for Vaultwarden invitation from sumanaddanki
2. **Click the link** to accept invitation
3. **Create your account:**
   - Email: Your work email (e.g., sharuuu@example.com)
   - Master Password: **Create a strong password** (you'll need this daily)
   - Hint: Optional but recommended

### Step 4: Login via CLI

```bash
# Login (will prompt for master password)
bw login sharuuu@example.com

# Enter your master password when prompted
# Output: You are logged in!
```

### Step 5: Create Daily Unlock Alias (Optional but Recommended)

Add to your `~/.zshrc` or `~/.bashrc`:

```bash
# Vaultwarden quick unlock
alias bwu='export BW_SESSION=$(bw unlock --raw)'
```

Reload shell:
```bash
source ~/.zshrc  # or ~/.bashrc
```

---

## Daily Workflow

### Unlock Vault (Start of Day)

```bash
# Option 1: Manual unlock
export BW_SESSION=$(bw unlock --raw)
# Enter your master password

# Option 2: If you set up the alias
bwu
# Enter your master password
```

**Pro Tip:** Keep your session unlocked for the entire workday. It expires after a few hours of inactivity.

### Verify Access

```bash
# List all items you have access to
bw list items --organizationid 579c22f3-4f13-447c-a861-9a4aa0ab7fbc

# You should see secrets from dev and qa collections
# If you see prod secrets, contact Suman (you shouldn't have prod access yet)
```

### Lock Vault (End of Day)

```bash
# Lock your vault when done
bw lock

# Or just close terminal (session expires automatically)
```

---

## Deployment Guide

### Deploy to DEV

```bash
# 1. Unlock vault
export BW_SESSION=$(bw unlock --raw)

# 2. Fetch secrets from Vaultwarden
./deployment/scripts/fetch-secrets.sh dev

# 3. Deploy quad-web to DEV
cd quad-web
./deployment/dev/dev-deploy.sh

# 4. Verify deployment
curl -I https://dev.quadframe.work
# Should return HTTP/2 200
```

### Deploy to QA

```bash
# 1. Unlock vault (if not already unlocked)
export BW_SESSION=$(bw unlock --raw)

# 2. Fetch secrets
./deployment/scripts/fetch-secrets.sh qa

# 3. Deploy quad-web to QA
cd quad-web
./deployment/qa/qa-deploy.sh

# 4. Verify deployment
curl -I https://qa.quadframe.work
# Should return HTTP/2 200
```

### Deploy to PROD (Request-Based)

**⚠️ Production deployments require approval from Suman.**

**Process:**
1. **Test thoroughly on QA** - Ensure all features work
2. **Create deployment request** via Slack:
   ```
   @suman PROD deployment request:
   - Changes: [List what changed]
   - QA tested: ✅
   - Database migrations: [Yes/No]
   - Risks: [Any known risks]
   ```
3. **Suman reviews** code changes and QA testing
4. **Suman deploys** to production OR grants you temporary prod access

**If granted temporary prod access:**
```bash
# 1. Unlock vault
export BW_SESSION=$(bw unlock --raw)

# 2. Fetch prod secrets (you'll have access temporarily)
./deployment/scripts/fetch-secrets.sh prod

# 3. Deploy to GCP Cloud Run
cd quad-web
./deployment/prod/prod-deploy.sh

# 4. Verify deployment
curl -I https://quadframe.work
# Should return HTTP/2 200

# 5. Notify Suman deployment is complete
# Suman will revoke your prod access after deployment
```

---

## Troubleshooting

### Error: "BW_SESSION not set"

**Cause:** Vault is locked or session expired

**Fix:**
```bash
export BW_SESSION=$(bw unlock --raw)
# Enter your master password
```

### Error: "User does not have access to item"

**Cause:** Trying to access prod secrets without permission

**Fix:**
- For dev/qa: Contact Suman (you should have access)
- For prod: This is expected - request deployment via Slack

### Error: "Invalid master password"

**Cause:** Incorrect password or account locked

**Fix:**
1. Try password again (check caps lock)
2. If forgotten, use password hint: `bw login --help`
3. Last resort: Contact Suman to reset password (you'll lose access to personal vault items)

### Forgot Master Password?

**⚠️ Important:** Bitwarden/Vaultwarden cannot reset your master password. If you forget it:
1. **Organization secrets:** Suman can remove you and re-invite (you regain access)
2. **Personal vault items:** Lost forever (this is by design for security)

**Prevention:** Use a password manager for your master password or write it down securely.

### Session Keeps Expiring

**Cause:** Session timeout (default: 2 hours of inactivity)

**Fix:**
```bash
# Unlock again
export BW_SESSION=$(bw unlock --raw)

# Or set a longer timeout (30 days)
bw config sessionTimeout 43200  # 30 days in minutes
```

### Can't Access Vaultwarden Web Interface

**URL:** https://vault.a2vibes.tech

**Troubleshooting:**
1. Check VPN (if required)
2. Clear browser cache
3. Try incognito mode
4. Contact Suman if server is down

---

## Best Practices

### ✅ DO

- **Use unique master password** - Different from other accounts
- **Lock vault daily** - Run `bw lock` at end of day
- **Test on QA first** - Always test thoroughly before prod
- **Document deployments** - Note what changed in Slack
- **Keep CLI updated** - Run `npm update -g @bitwarden/cli` monthly

### ❌ DON'T

- **Don't share master password** - Each person should have their own
- **Don't commit secrets** - Never commit `.env` files to git
- **Don't deploy to prod without approval** - Always get Suman's review
- **Don't share BW_SESSION token** - It grants full access to your vault
- **Don't use same password as vault.a2vibes.tech login** - Master password should be unique

---

## Quick Reference

### Common Commands

```bash
# Unlock vault
export BW_SESSION=$(bw unlock --raw)

# Lock vault
bw lock

# List accessible secrets
bw list items --organizationid 579c22f3-4f13-447c-a861-9a4aa0ab7fbc

# Get specific secret
bw get item "Google OAuth" --organizationid 579c22f3-4f13-447c-a861-9a4aa0ab7fbc

# Fetch secrets for deployment
./deployment/scripts/fetch-secrets.sh dev   # DEV
./deployment/scripts/fetch-secrets.sh qa    # QA
./deployment/scripts/fetch-secrets.sh prod  # PROD (requires access)

# Deploy
cd quad-web
./deployment/dev/dev-deploy.sh     # DEV
./deployment/qa/qa-deploy.sh       # QA
./deployment/prod/prod-deploy.sh   # PROD (requires access)
```

### Deployment Checklist

**Before Deployment:**
- [ ] Code changes committed and pushed
- [ ] Vault unlocked (`bwu`)
- [ ] Secrets fetched (`./fetch-secrets.sh <env>`)
- [ ] QA tested (for prod deployments)

**After Deployment:**
- [ ] Verify site is accessible
- [ ] Check logs for errors
- [ ] Test critical features (login, signup)
- [ ] Notify team in Slack

---

## Getting Help

**For questions or issues:**
1. **Slack:** @suman in #quad-dev channel
2. **Email:** sumanaddanki@example.com
3. **Documentation:** This file + `/Users/semostudio/git/a2vibes/QUAD/CLAUDE.md`

---

## CI/CD Pipeline Setup (API Key Authentication)

**For automated deployments via GitHub Actions or Jenkins:**

### Step 1: Create API Key (Suman Only)

1. **Login to Vaultwarden web interface:** https://vault.a2vibes.tech
2. **Go to Settings → Security → Keys & APIs**
3. **Click "New API Key"**
4. **Name:** `QUAD CI/CD Pipeline`
5. **Copy the credentials:**
   - `client_id` (example: `organization.abc123...`)
   - `client_secret` (example: `xyz789...`) **⚠️ Save immediately, won't show again!**

### Step 2: Configure GitHub Secrets

Add to GitHub repository secrets (Settings → Secrets and variables → Actions):

```
BW_CLIENTID=organization.abc123...
BW_CLIENTSECRET=xyz789...
```

### Step 3: GitHub Actions Workflow

Create `.github/workflows/deploy-dev.yml`:

```yaml
name: Deploy to DEV

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Install Bitwarden CLI
        run: npm install -g @bitwarden/cli

      - name: Configure Vaultwarden
        run: bw config server https://vault.a2vibes.tech

      - name: Login with API Key
        run: |
          bw login --apikey
        env:
          BW_CLIENTID: ${{ secrets.BW_CLIENTID }}
          BW_CLIENTSECRET: ${{ secrets.BW_CLIENTSECRET }}

      - name: Unlock and Fetch Secrets
        run: |
          export BW_SESSION=$(bw unlock --passwordenv BW_CLIENTSECRET --raw)
          ./deployment/scripts/fetch-secrets.sh dev
        env:
          BW_CLIENTSECRET: ${{ secrets.BW_CLIENTSECRET }}

      - name: Deploy to DEV
        run: |
          cd quad-web
          ./deployment/dev/dev-deploy.sh
```

### Benefits of API Key for CI/CD

| Feature | Password Auth | API Key Auth |
|---------|---------------|--------------|
| **Human users** | ✅ Recommended | ❌ Not needed |
| **CI/CD pipelines** | ❌ Not ideal | ✅ Perfect |
| **Audit trail** | ✅ Per user | ✅ "CI/CD Pipeline" |
| **Rotation** | Change master password | Revoke & create new key |
| **Security** | Needs password vault | Stored in GitHub Secrets |

**Recommended Setup:**
- **Sharath:** Password-based auth (individual account)
- **CI/CD:** API key auth (automated deployments)

---

## Appendix: Collection IDs

| Environment | Collection ID |
|-------------|---------------|
| dev | `e4f03d1a-b8ac-4186-a384-0fb62d431ddd` |
| qa | `75fb3b57-9e84-4e2d-8b4f-447518e0a315` |
| prod | `cc4a16a2-9acc-459a-ad37-a8ef99592366` |

**Organization ID:** `579c22f3-4f13-447c-a861-9a4aa0ab7fbc`

---

## Authentication Summary

| Use Case | Method | Setup By | Access |
|----------|--------|----------|--------|
| **Sharath (dev/qa)** | Password | Sharath | dev, qa collections |
| **Suman (all envs)** | Password | Suman | dev, qa, prod collections |
| **CI/CD Pipeline** | API Key | Suman | dev, qa collections (configurable) |

---

**Last Updated:** January 5, 2026
**Maintainer:** Suman Addanki
**Version:** 1.0
