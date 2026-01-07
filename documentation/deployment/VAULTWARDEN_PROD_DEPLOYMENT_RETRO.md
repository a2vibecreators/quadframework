# Vaultwarden Production Deployment - Retrospective

**Date:** January 6, 2026
**Duration:** ~8 hours
**Outcome:** ✅ Successful deployment to GCP Cloud Run with Vaultwarden secrets

---

## Summary

Successfully deployed quad-web to GCP Cloud Run production with ALL secrets managed centrally in Vaultwarden. This eliminates hardcoded secrets from deployment scripts and GCP Console.

**Key Achievement:**
Zero hardcoded secrets in production deployment - all secrets fetched dynamically from Vaultwarden at deploy time.

---

## Issues Encountered & Resolutions

### 1. Wrong Organization ID in fetch-secrets.sh

**Issue:**
Script had hardcoded organization ID `579c22f3-4f13-447c-a861-9a4aa0ab7fbc` but actual QUAD org is `7548352c-4c18-45ab-ba58-cabceb58a25b`

**Impact:**
`bw list items --organizationid` returned 0 items

**Root Cause:**
Copy-paste error from initial script draft

**Resolution:**
- Created `deployment/vault.config.sh` to centralize organization and collection IDs
- Updated fetch-secrets.sh to source vault.config.sh
- Verified with `bw list organizations` command

**Lesson Learned:**
Always verify IDs with `bw list organizations` before hardcoding

---

### 2. jq Filter Syntax for Array Membership

**Issue:**
jq filter `.collectionIds[]?=="$COLLECTION_ID"` returned empty results

**Impact:**
Secrets not found in collections

**Root Cause:**
Array expansion syntax doesn't work correctly for checking if value exists in array

**Resolution:**
Changed to `contains()` function:
```bash
# OLD (didn't work):
.collectionIds[]?=="$COLLECTION_ID"

# NEW (works):
.collectionIds | contains(["$COLLECTION_ID"])
```

**Applied to:**
All 6 secret fetch blocks (NextAuth, Google OAuth, GitHub OAuth, Database, Anthropic API, Gemini API)

**Lesson Learned:**
Use `contains()` for array membership checks in jq

---

### 3. OAuth Credentials Stored in Wrong Fields

**Issue:**
GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET coming back empty

**Impact:**
No Google sign-in button on login page

**Root Cause:**
Migration script stored OAuth credentials in custom fields (`client_id`, `client_secret`), but fetch-secrets.sh was looking in `login.username` and `login.password`

**Resolution:**
Updated fetch-secrets.sh to read from custom fields:
```bash
# OLD (wrong):
export GOOGLE_CLIENT_ID=$(echo "$GOOGLE_OAUTH" | jq -r '.login.username')
export GOOGLE_CLIENT_SECRET=$(echo "$GOOGLE_OAUTH" | jq -r '.login.password')

# NEW (correct):
export GOOGLE_CLIENT_ID=$(echo "$GOOGLE_OAUTH" | jq -r '.fields[] | select(.name=="client_id") | .value')
export GOOGLE_CLIENT_SECRET=$(echo "$GOOGLE_OAUTH" | jq -r '.fields[] | select(.name=="client_secret") | .value')
```

**Lesson Learned:**
Always inspect Vaultwarden item structure with `bw get item` before writing extraction code

---

### 4. Docker Platform Mismatch

**Issue:**
```
ERROR: Cloud Run does not support image 'gcr.io/nutrinine-prod/quad-web:latest':
Container manifest type 'application/vnd.oci.image.index.v1+json' must support amd64/linux.
```

**Impact:**
Deployment failed

**Root Cause:**
Docker build on Mac Studio (ARM64) creates ARM64 image, but Cloud Run requires linux/amd64

**Resolution:**
Added `--platform linux/amd64` flag to docker build command in deploy.sh:
```bash
# OLD:
docker build -t $GCP_IMAGE .

# NEW:
docker build --platform linux/amd64 -t $GCP_IMAGE .
```

**Lesson Learned:**
Always specify `--platform linux/amd64` when building for Cloud Run on ARM64 machines

---

### 5. Two Production Services Exist (Domain Mapping Confusion)

**Issue:**
User confused about which service quadframe.work should point to:
- `quadframework-prod` (old, deployed Jan 2, has hardcoded secrets)
- `quad-web-prod` (new, deployed Jan 6, uses Vaultwarden)

**Impact:**
Unclear which service is "production"

**Root Cause:**
Previous deployment created service with different naming convention

**Resolution:**
1. Deleted old domain mapping: `gcloud beta run domain-mappings delete --domain=quadframe.work`
2. Created new mapping: `gcloud beta run domain-mappings create --service=quad-web-prod --domain=quadframe.work`
3. Deleted old service: `gcloud run services delete quadframework-prod`

**Lesson Learned:**
- Use consistent naming (quad-web-dev, quad-web-qa, quad-web-prod)
- Clean up old services immediately after migration
- Document which service is "production" in CLAUDE.md

---

### 6. SSL Certificate Provisioning Delay

**Issue:**
User saw old content and no Google sign-in immediately after domain mapping

**Impact:**
User thought deployment failed

**Root Cause:**
SSL certificate takes 15-30 minutes to provision after domain mapping creation

**Resolution:**
- Explained certificate provisioning is normal
- Checked certificate status: `gcloud beta run domain-mappings describe --domain=quadframe.work`
- Certificate provisioned successfully after ~7 minutes

**Status Check:**
```bash
gcloud beta run domain-mappings describe --domain=quadframe.work --format="get(status.conditions)"
# Result:
# - CertificateProvisioned: True
# - Ready: True
# - DomainRoutable: True
```

**Lesson Learned:**
- SSL certificate provisioning is expected to take 15-30 minutes
- Always check certificate status before troubleshooting other issues
- Add certificate status check to deployment script

**User Education:**
Domain mapping is **ONCE**. Future deployments update the service, not the domain mapping. SSL certificate persists.

---

### 7. jq Parsing Multi-line JSON with `head -1` (CRITICAL BUG)

**Issue:**
Google OAuth credentials still empty even after deployment with fixed script

**Impact:**
No Google sign-in button on production site

**Root Cause:**
The `| head -1` command was truncating multi-line JSON objects to just the first line `{`, which is invalid JSON:

```bash
# This command:
GOOGLE_OAUTH=$(bw list items ... | jq -r ".[] | select(...)" | head -1)

# Outputs:
{
# (truncated - invalid JSON!)

# Later extraction fails:
echo "$GOOGLE_OAUTH" | jq -r '.fields[] | select(.name=="client_id") | .value'
# jq: parse error: Unfinished JSON term at EOF
```

**Why it happened:**
Developer assumed `| head -1` would select the first item from an array, but jq's `.[] | select(...)` already selects a single item. The JSON object spans multiple lines, and `head -1` only keeps the first line.

**Resolution:**
Removed `| head -1` from ALL commands that fetch full JSON objects:
```bash
# Fixed in fetch-secrets.sh (lines 82, 98, 115):
GOOGLE_OAUTH=$(bw list items ... | jq -r ".[] | select(...)" 2>/dev/null)  # No head -1
GITHUB_OAUTH=$(bw list items ... | jq -r ".[] | select(...)" 2>/dev/null)  # No head -1
DB_CREDS=$(bw list items ... | jq -r ".[] | select(...)" 2>/dev/null)      # No head -1
```

**Why NextAuth Secret didn't fail:**
The NextAuth Secret command also had `| head -1`, but it was harmless because the jq command ends with `| .login.password`, which outputs a single string value (not multi-line JSON).

**Testing:**
```bash
# Before fix:
GOOGLE_OAUTH=$(bw list items ... | jq -r ".[] | select(...)" | head -1)
echo "$GOOGLE_OAUTH"
# Output: {

# After fix:
GOOGLE_OAUTH=$(bw list items ... | jq -r ".[] | select(...)")
echo "$GOOGLE_OAUTH"
# Output: { "name": "Google OAuth", "organizationId": "...", "fields": [...] }
```

**Lesson Learned:**
- **NEVER use `| head -1` with JSON objects** - it truncates to first line only
- Use `jq -s '.[0]'` if you truly need to select the first item from an array
- Test jq commands manually before using in scripts
- Always inspect variable contents with `echo "$VAR" | head -20` during debugging

**Impact:**
This bug caused 3+ hours of debugging and 2 additional deployments. It was the hardest bug to find because:
1. The script said "✓ Google OAuth credentials loaded" (misleading success message)
2. The error only appeared when trying to parse the truncated JSON later
3. The `head -1` pattern was copied from online examples that didn't account for multi-line JSON

---

## What Worked Well

### 1. Vaultwarden Organization Structure

- QUAD organization with Dev/Qa/Prod collections (capitalized)
- Separate collections per environment
- Custom fields for OAuth credentials (client_id, client_secret)

### 2. vault.config.sh Centralized Configuration

Created `/Users/semostudio/git/a2vibes/QUAD/quad-web/deployment/vault.config.sh`:
```bash
export VAULT_QUAD_ORG_ID="7548352c-4c18-45ab-ba58-cabceb58a25b"
export VAULT_COLLECTION_DEV="bd26fd3e-b01f-47a9-80e9-9841b52fc1c6"
export VAULT_COLLECTION_QA="5b3ffa64-ee2e-41e2-a05a-11d4603f5496"
export VAULT_COLLECTION_PROD="0dc1c5d4-0b3d-49fc-8ab9-2322e1e2db67"
```

**Benefits:**
- Single source of truth for IDs
- Easy to update if collections change
- Can be committed to git (no secrets)

### 3. Migration Scripts for All Environments

Created 3 migration scripts:
- `/tmp/migrate-prod-secrets-to-vault.sh` - Migrated from GCP Cloud Run
- `/tmp/migrate-dev-secrets-to-vault.sh` - Migrated from Docker container
- `/tmp/migrate-qa-secrets-to-vault.sh` - Migrated from Docker with DEV fallback

### 4. QA Fallback to DEV Logic

Per user requirement: "see if qu value is empty use the same value as dev esp fro these secredt."

```bash
if [ -z "$QA_NEXTAUTH_SECRET" ] || [ "$QA_NEXTAUTH_SECRET" == "changeme" ]; then
    NEXTAUTH_SECRET="$DEV_NEXTAUTH_SECRET"
    print_warning "QA NEXTAUTH_SECRET is empty/placeholder → using DEV value"
else
    NEXTAUTH_SECRET="$QA_NEXTAUTH_SECRET"
fi
```

### 5. fetch-secrets.sh Export Pattern

Script exports environment variables for use in deployment scripts:
```bash
source deployment/scripts/fetch-secrets.sh prod
# Now GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, etc. are available
```

---

## Deployment Flow (Final Working Version)

```bash
# 1. Unlock vault
export BW_SESSION=$(bw unlock --raw)

# 2. Deploy to production
cd /Users/semostudio/git/a2vibes/QUAD/quad-web
./deployment/scripts/deploy.sh prod

# Steps performed by deploy.sh:
# - Check BW_SESSION is set
# - Source vault.config.sh (load org/collection IDs)
# - Source fetch-secrets.sh prod (fetch all secrets from Vaultwarden)
# - Build Docker image (linux/amd64)
# - Push to GCR (gcr.io/nutrinine-prod/quad-web)
# - Deploy to Cloud Run (quad-web-prod)
# - Set all environment variables from exported secrets
```

---

## File Changes

### Created Files:
1. `/Users/semostudio/git/a2vibes/QUAD/quad-web/deployment/vault.config.sh`
   - Centralized Vaultwarden configuration

2. `/tmp/migrate-prod-secrets-to-vault.sh` (later deleted)
   - Migrated production secrets from GCP to Vaultwarden

3. `/tmp/migrate-dev-secrets-to-vault.sh` (later deleted)
   - Migrated DEV secrets from Docker to Vaultwarden

4. `/tmp/migrate-qa-secrets-to-vault.sh` (later deleted)
   - Migrated QA secrets from Docker to Vaultwarden (with DEV fallback)

### Modified Files:
1. `/Users/semostudio/git/a2vibes/QUAD/quad-web/deployment/scripts/fetch-secrets.sh`
   - Fixed organization ID (now sourced from vault.config.sh)
   - Fixed jq filter syntax (uses `contains()`)
   - Fixed OAuth field mapping (reads from custom fields)
   - **CRITICAL FIX:** Removed `| head -1` from JSON object commands

2. `/Users/semostudio/git/a2vibes/QUAD/quad-web/deployment/scripts/deploy.sh`
   - Added `--platform linux/amd64` for Cloud Run compatibility

---

## Secrets Stored in Vaultwarden (PROD Collection)

| Secret Name | Type | Fields | Usage |
|-------------|------|--------|-------|
| NextAuth Secret | Login | password | NEXTAUTH_SECRET |
| Google OAuth | Login + Fields | client_id, client_secret | GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET |
| GitHub OAuth | Login + Fields | client_id, client_secret | GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET (optional) |
| Database | Login + Fields | username, password, host, database | DB_USER, DB_PASSWORD, DB_HOST, DB_NAME |
| Anthropic API Key | Login | password | ANTHROPIC_API_KEY (optional) |
| Google Gemini API Key | Login | password | GEMINI_API_KEY (fallback to shared NutriNine key) |

---

## GCP Cloud Run Production Configuration

**Service:** quad-web-prod
**Region:** us-east1
**Project:** nutrinine-prod
**Image:** gcr.io/nutrinine-prod/quad-web:latest
**Domain:** quadframe.work
**SSL Certificate:** Auto-provisioned (15-30 minutes)

**Environment Variables (from Vaultwarden):**
- DATABASE_URL
- NEXTAUTH_URL
- NEXTAUTH_SECRET
- GOOGLE_CLIENT_ID
- GOOGLE_CLIENT_SECRET
- GITHUB_CLIENT_ID (empty if not configured)
- GITHUB_CLIENT_SECRET (empty if not configured)
- ANTHROPIC_API_KEY (empty if not configured)
- GEMINI_API_KEY (shared NutriNine key)
- QUAD_API_URL
- SPRING_PROFILES_ACTIVE=prod

---

## Testing Checklist

After deployment, verify:

1. **Service Health**
   ```bash
   curl -sI https://quad-web-prod-605414080358.us-east1.run.app
   # Should return HTTP/2 200
   ```

2. **Domain Mapping**
   ```bash
   curl -sI https://quadframe.work
   # Should return HTTP/2 200
   ```

3. **SSL Certificate**
   ```bash
   gcloud beta run domain-mappings describe --domain=quadframe.work --format="get(status.conditions)"
   # Should show CertificateProvisioned: True
   ```

4. **Environment Variables**
   ```bash
   gcloud run services describe quad-web-prod --format="yaml(spec.template.spec.containers[0].env)" | grep -A1 GOOGLE_CLIENT_ID
   # Should show actual client ID value, not empty
   ```

5. **Google Sign-In Button**
   - Visit https://quadframe.work/auth/login
   - Should see "Sign in with Google" button
   - Click it, should redirect to Google OAuth

---

## Improvements for Next Time

### 1. Add Certificate Status Check to Deployment Script

Add to `deploy.sh` after domain mapping:
```bash
echo "Checking SSL certificate status..."
CERT_STATUS=$(gcloud beta run domain-mappings describe --domain=$DOMAIN --format="get(status.conditions[1].status)")
if [ "$CERT_STATUS" = "True" ]; then
    echo "✓ SSL certificate provisioned"
else
    echo "⏳ SSL certificate provisioning (15-30 minutes)..."
    echo "   Check status: gcloud beta run domain-mappings describe --domain=$DOMAIN"
fi
```

### 2. Add Environment Variable Validation

Add to `deploy.sh` after `source fetch-secrets.sh`:
```bash
echo "Validating required secrets..."
[ -z "$GOOGLE_CLIENT_ID" ] && echo "❌ GOOGLE_CLIENT_ID is empty" && exit 1
[ -z "$GOOGLE_CLIENT_SECRET" ] && echo "❌ GOOGLE_CLIENT_SECRET is empty" && exit 1
[ -z "$NEXTAUTH_SECRET" ] && echo "❌ NEXTAUTH_SECRET is empty" && exit 1
echo "✓ All required secrets loaded"
```

### 3. Add Deployment Health Check

Add to `deploy.sh` after Cloud Run deployment:
```bash
echo "Running post-deployment health check..."
SERVICE_URL=$(gcloud run services describe $GCP_SERVICE --format='value(status.url)')
HTTP_STATUS=$(curl -sI $SERVICE_URL | head -1 | awk '{print $2}')
if [ "$HTTP_STATUS" = "200" ]; then
    echo "✓ Service is healthy (HTTP $HTTP_STATUS)"
else
    echo "❌ Service health check failed (HTTP $HTTP_STATUS)"
    exit 1
fi
```

### 4. Test jq Commands Before Scripting

Always test jq extraction commands manually:
```bash
# Test fetching item
bw list items --organizationid "$ORG_ID" | jq -r ".[] | select(.name==\"Google OAuth\")"

# Test field extraction
GOOGLE_OAUTH=$(bw list items ... | jq -r ".[] | select(...)")
echo "$GOOGLE_OAUTH" | jq -r '.fields[] | select(.name=="client_id") | .value'
```

### 5. Document Domain Mapping Persistence

Add to CLAUDE.md:
```markdown
**Domain Mapping:** ONCE only. Future deployments update the service, not the domain mapping.

Domain mapping lifecycle:
1. First deployment: Map domain to service
2. SSL certificate provisions (15-30 minutes)
3. Future deployments: Service updates, domain stays mapped, SSL persists
```

---

## Metrics

| Metric | Value |
|--------|-------|
| **Total Time** | ~8 hours |
| **Deployments** | 4 (2 failed, 2 succeeded) |
| **Critical Bugs** | 7 |
| **Scripts Created** | 4 (1 config, 3 migrations) |
| **Files Modified** | 2 (fetch-secrets.sh, deploy.sh) |
| **Secrets Migrated** | 6 per environment (18 total) |
| **SSL Certificate Time** | ~7 minutes |

---

## Conclusion

Successfully deployed quad-web to GCP Cloud Run production with 100% Vaultwarden-managed secrets. Zero hardcoded secrets remain in deployment scripts or GCP Console.

**Key Takeaways:**
1. **Always test jq commands manually** before using in scripts
2. **Never use `| head -1` with multi-line JSON** - it truncates to first line only
3. **Verify SSL certificate status** before troubleshooting other issues
4. **Domain mapping is once** - future deployments update service, not domain
5. **Validate environment variables** after sourcing secrets before deploying

**Next Steps:**
1. Test Google sign-in on production (https://quadframe.work/auth/login)
2. Commit vault.config.sh and modified scripts to git
3. Document Vaultwarden setup in CLAUDE.md
4. Apply same pattern to quad-services (Java API) deployment

---

**Retrospective Created:** January 6, 2026
**Author:** Claude Sonnet 4.5 + Suman Addanki
