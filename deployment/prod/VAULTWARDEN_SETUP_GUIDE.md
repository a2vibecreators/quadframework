# Vaultwarden Setup Guide for QUAD Production Deployment

**Purpose:** Step-by-step guide to set up Vaultwarden secrets for QUAD production deployment

**Date:** January 5, 2026

---

## Overview

QUAD production deployment reads ALL secrets from Vaultwarden (no hardcoded secrets in code/scripts).

**Architecture:**
```
Vaultwarden (vault.a2vibes.tech)
└── QUAD Organization
    ├── dev Collection    → DEV secrets (Mac Studio Docker)
    ├── qa Collection     → QA secrets (Mac Studio Docker)
    └── prod Collection   → PROD secrets (GCP Cloud Run)
```

---

## Step 1: Create Collections in QUAD Organization

1. Go to: https://vault.a2vibes.tech
2. Log in with: `suman.addanki@gmail.com`
3. Click on **"QUAD"** organization (left sidebar)
4. Click **"Collections"** tab
5. Click **"+ New Collection"**
6. Create 3 collections:
   - Name: `dev` → Save
   - Name: `qa` → Save
   - Name: `prod` → Save

---

## Step 2: Add Secrets to prod Collection

### Secret 1: NextAuth Secret

**Type:** Login
- **Name:** `NextAuth Secret`
- **Username:** `(leave empty)`
- **Password:** Generate random 32-character string OR use: `41hKCOZcnWggq2cG9oBietUYljvN0ZkUqjyFnKdgTEM=`
- **Collection:** `prod`

**How to generate:**
```bash
openssl rand -base64 32
```

---

### Secret 2: Google OAuth

**Type:** Login
- **Name:** `Google OAuth`
- **Username:** `(leave empty)`
- **Password:** `(leave empty)`
- **Collection:** `prod`

**Custom Fields (click "+ New custom field"):**
- Field name: `client_id`, Value: `805817782076-b6975p184nj0kqcs9l0hurjj2bv6gkev.apps.googleusercontent.com`
- Field name: `client_secret`, Value: `(get from Google Cloud Console)`

**Where to get values:**
1. Go to: https://console.cloud.google.com/apis/credentials
2. Project: "QUAD Platform"
3. OAuth 2.0 Client: "QUAD Platform Prod"
4. Copy Client ID and Client Secret

---

### Secret 3: Database

**Type:** Login
- **Name:** `Database`
- **Username:** `quad_user`
- **Password:** `(database password)`
- **Collection:** `prod`

**Custom Fields:**
- Field name: `host`, Value: `(Cloud SQL instance IP or connection name)`
- Field name: `database`, Value: `quad_prod_db`
- Field name: `url`, Value: `postgresql://quad_user:{password}@{host}:5432/quad_prod_db`

**For Cloud SQL:**
```
url: postgresql://quad_user:PASSWORD@/quad_prod_db?host=/cloudsql/PROJECT:REGION:INSTANCE
host: /cloudsql/nutrinine-prod:us-east1:nutrinine-db
database: quad_prod_db
```

---

### Secret 4: Anthropic API Key (Optional)

**Type:** Login
- **Name:** `Anthropic API Key`
- **Username:** `(leave empty)`
- **Password:** `sk-ant-...` (your Anthropic API key)
- **Collection:** `prod`

**Where to get:**
https://console.anthropic.com/settings/keys

---

### Secret 5: GitHub OAuth (Future)

**Type:** Login
- **Name:** `GitHub OAuth`
- **Username:** `(leave empty)`
- **Password:** `(leave empty)`
- **Collection:** `prod`

**Custom Fields:**
- Field name: `client_id`, Value: `(GitHub OAuth App Client ID)`
- Field name: `client_secret`, Value: `(GitHub OAuth App Client Secret)`

*Not required for initial deployment*

---

## Step 3: Verify Secrets via bw CLI

```bash
# Unlock vault
export BW_SESSION=$(bw unlock --raw)

# Get QUAD organization ID
bw list organizations | jq -r '.[] | select(.name=="QUAD") | {id, name}'

# Get prod collection ID
ORG_ID="..." # from above
bw list org-collections --organizationid "$ORG_ID" | jq -r '.[] | select(.name=="prod") | {id, name}'

# List all secrets in prod collection
COLLECTION_ID="..." # from above
bw list items --organizationid "$ORG_ID" --collectionid "$COLLECTION_ID" | jq -r '.[] | {name, id}'

# View specific secret (without password)
bw get item "NextAuth Secret" --organizationid "$ORG_ID" | jq 'del(.login.password)'
```

---

## Step 4: Run Deployment Script

```bash
# Navigate to quad-web directory
cd /Users/semostudio/git/a2vibes/QUAD/quad-web

# Unlock vault (if not already)
export BW_SESSION=$(bw unlock --raw)

# Run deployment
./deployment/scripts/deploy.sh prod
```

**What the script does:**
1. ✅ Validates BW_SESSION is set
2. ✅ Fetches all secrets from Vaultwarden (QUAD → prod collection)
3. ✅ Builds Docker image (quad-web)
4. ✅ Pushes to Google Container Registry
5. ✅ Deploys to Cloud Run with secrets as environment variables
6. ✅ Configures Cloud SQL connection
7. ✅ Returns deployment URL

---

## Troubleshooting

### Error: "Organization 'QUAD' not found"

**Solution:** Create QUAD organization in Vaultwarden
```bash
# Check existing organizations
bw list organizations | jq -r '.[] | .name'
```

---

### Error: "Collection 'prod' not found"

**Solution:** Create prod collection in QUAD organization via web UI

---

### Error: "Secret 'NextAuth Secret' not found"

**Solution:** Add the secret to the prod collection via web UI

---

### Error: "BW_SESSION not set"

**Solution:**
```bash
# Check current session
bw status

# If locked, unlock
export BW_SESSION=$(bw unlock --raw)

# Verify
echo $BW_SESSION
```

---

## Secret Schema Reference

For automation scripts, here's the expected schema:

```json
{
  "organizationId": "QUAD_ORG_ID",
  "collectionIds": ["PROD_COLLECTION_ID"],
  "type": 1,
  "name": "NextAuth Secret",
  "login": {
    "password": "41hKCOZcnWggq2cG9oBietUYljvN0ZkUqjyFnKdgTEM="
  }
}
```

```json
{
  "organizationId": "QUAD_ORG_ID",
  "collectionIds": ["PROD_COLLECTION_ID"],
  "type": 1,
  "name": "Google OAuth",
  "fields": [
    {"name": "client_id", "value": "805817782076-..."},
    {"name": "client_secret", "value": "GOCSPX-..."}
  ]
}
```

```json
{
  "organizationId": "QUAD_ORG_ID",
  "collectionIds": ["PROD_COLLECTION_ID"],
  "type": 1,
  "name": "Database",
  "login": {
    "username": "quad_user",
    "password": "quad_prod_pass"
  },
  "fields": [
    {"name": "host", "value": "/cloudsql/..."},
    {"name": "database", "value": "quad_prod_db"},
    {"name": "url", "value": "postgresql://..."}
  ]
}
```

---

## Next Steps

After deployment:

1. **Verify deployment:**
   ```bash
   curl -s https://quadframe-prod-...run.app | head -20
   ```

2. **Check logs:**
   ```bash
   gcloud run services logs read quadframework-prod --region=us-east1 --limit=50
   ```

3. **Configure custom domain:**
   ```bash
   gcloud run domain-mappings create \
     --service=quadframework-prod \
     --domain=quadframe.work \
     --region=us-east1
   ```

4. **Update DNS:**
   - Add CNAME: `quadframe.work` → `ghs.googlehosted.com`

---

**Version:** 1.0
**Last Updated:** January 5, 2026
