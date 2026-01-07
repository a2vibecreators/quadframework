# Vaultwarden Troubleshooting Guide - Lessons Learned

**Date:** January 5, 2026
**Incident:** Organization creation failures in Vaultwarden
**Duration:** ~4 hours of troubleshooting
**Resolution:** Successful setup with PostgreSQL backend

---

## Executive Summary

**Problem:** Unable to create organizations in Vaultwarden despite multiple deployment attempts.

**Root Causes:**
1. **Version 1.35.1 has a critical bug** preventing organization creation
2. **Traffic routing not switched** to correct Cloud Run revision
3. **ORG_CREATION_USERS setting mismatch** (email vs "all")

**Solution:** Downgrade to v1.34.0 + `ORG_CREATION_USERS=all` + verify traffic routing

---

## Retrospective

### What Went Wrong

1. **Assumed latest = stable**
   - Deployed `vaultwarden/server:latest` (v1.35.1)
   - This version had a known JavaScript bug: `Cannot read properties of undefined (reading 'find')`
   - **Lesson:** Always check GitHub issues before using latest tag

2. **Didn't verify traffic routing**
   - Deployed revision 00014-clj (v1.34.0) but traffic stayed on 00012-5r2 (v1.35.1)
   - Tested against wrong revision for 30+ minutes
   - **Lesson:** Always verify `gcloud run services describe` shows correct serving revision

3. **Misleading error messages**
   - Frontend showed: "Data provided to an operation does not meet requirements"
   - Backend showed: `401 Unauthorized - Invalid claim`
   - Real issue: Session expired + wrong version
   - **Lesson:** Always check backend logs, not just frontend errors

4. **ORG_CREATION_USERS format confusion**
   - Tried `suman.addanki@gmail.com` (specific email)
   - Should have used `all` (allow all users)
   - **Lesson:** Check Vaultwarden docs for correct env var formats

### What Went Right

1. **Systematic version testing table** (SESSION_HISTORY.md)
   - Documented 6 deployment attempts
   - Tracked: version, config, revision, outcome
   - Made it easy to see patterns

2. **PostgreSQL backend from start**
   - Correct DATABASE_URL format: `postgresql://user:pass@/db?host=/cloudsql/instance`
   - Data persists across container restarts
   - No need to recreate organizations

3. **GitHub issue research**
   - Found exact bug report (#6638) with workaround
   - Confirmed v1.34.0 works, v1.35.1 broken
   - Saved hours of debugging

### Key Learnings

| Issue | What We Learned | How to Prevent |
|-------|-----------------|----------------|
| Version bug | Check GitHub issues BEFORE deploying | Add pre-deployment checklist |
| Traffic routing | Verify serving revision after deploy | Add `--no-traffic` flag, test first |
| Error messages | Backend logs > Frontend errors | Always check Cloud Run logs |
| Env var format | `all` != specific email | Read Vaultwarden wiki docs |

---

## Step-by-Step Troubleshooting Guide

### Problem: "Cannot read properties of undefined (reading 'find')"

**Symptoms:**
- Organization creation form loads
- Clicking Submit shows JavaScript error
- Browser console: `TypeError: Cannot read properties of undefined (reading 'find')`

**Solution:**
```bash
# Downgrade to v1.34.0
gcloud run services update vaultwarden-prod \
  --region=us-east1 \
  --image=vaultwarden/server:1.34.0 \
  --quiet

# Verify traffic switched
gcloud run services describe vaultwarden-prod \
  --region=us-east1 \
  --format="value(status.traffic[0].revisionName)"
```

**Why it works:** v1.35.1 has bug in `passwordManagerPlans.find()`, v1.34.0 doesn't.

---

### Problem: "401 Unauthorized - Invalid claim"

**Symptoms:**
- Form submits but shows generic error
- Backend logs: `Request guard 'Headers' failed: "Invalid claim"`
- Can create items but not organizations

**Root Causes:**
1. **Session expired** - Log out and log back in
2. **Wrong revision serving** - Traffic not switched to new revision
3. **ORG_CREATION_USERS not set** - Env var missing or wrong format

**Solution:**
```bash
# Check current serving revision and env vars
gcloud run services describe vaultwarden-prod \
  --region=us-east1 \
  --format="value(status.traffic[0].revisionName,spec.template.spec.containers[0].env)"

# Should see: ORG_CREATION_USERS=all

# If wrong revision is serving, force traffic switch:
gcloud run services update-traffic vaultwarden-prod \
  --region=us-east1 \
  --to-revisions=CORRECT_REVISION=100
```

---

### Problem: "Data provided to an operation does not meet requirements"

**This is a misleading error!** Real issues:
- Session expired → Log out and log back in
- Form fields empty → Fill in Name and Email
- Wrong version → Check logs for real error

**Check backend logs:**
```bash
gcloud logging read \
  "resource.type=cloud_run_revision AND resource.labels.service_name=vaultwarden-prod" \
  --limit=20 \
  --format="value(textPayload)" \
  | grep -i "organization\|error"
```

---

## Correct Configuration (Working Setup)

### Cloud Run Environment Variables

```bash
DATABASE_URL=postgresql://vaultwarden_user:vaultwarden_secure_pass_2026@/vaultwarden_prod_db?host=/cloudsql/nutrinine-prod:us-east1:nutrinine-db
ORG_CREATION_USERS=all  # Allow all users (NOT specific email)
DOMAIN=https://vault.a2vibes.tech
SIGNUPS_ALLOWED=true
WEBSOCKET_ENABLED=true
LOG_LEVEL=info
ADMIN_TOKEN=ts/GNXE9mXmz13WxS6Q4PYUYsXi7ntvHNfNFqDpjNtfJR7hY4lvegLuzVPUutu4k
ROCKET_PORT=80
ROCKET_ADDRESS=0.0.0.0
```

### Working Version

```bash
Image: vaultwarden/server:1.34.0
Revision: vaultwarden-prod-00015-cdb
```

### Database Connection (PostgreSQL)

```bash
Instance: nutrinine-prod:us-east1:nutrinine-db
Database: vaultwarden_prod_db
User: vaultwarden_user
Password: vaultwarden_secure_pass_2026
```

**Connection Format:** Cloud SQL Unix Socket (NOT TCP)
```
postgresql://USER:PASS@/DATABASE?host=/cloudsql/PROJECT:REGION:INSTANCE
```

---

## Pre-Deployment Checklist

Before deploying Vaultwarden:

- [ ] Check GitHub issues for version-specific bugs
- [ ] Use specific version tag (NOT `latest`)
- [ ] Set `ORG_CREATION_USERS=all` (NOT specific email)
- [ ] Use correct DATABASE_URL format for Cloud SQL
- [ ] Deploy with `--no-traffic` first (test before switching)
- [ ] Verify serving revision: `gcloud run services describe`
- [ ] Test organization creation in browser
- [ ] Check backend logs for errors
- [ ] Switch traffic only after successful test

---

## Post-Deployment Verification

```bash
# 1. Check serving revision
gcloud run services describe vaultwarden-prod \
  --region=us-east1 \
  --format="value(status.traffic[0].revisionName,spec.template.spec.containers[0].image)"

# 2. Verify env vars
gcloud run services describe vaultwarden-prod \
  --region=us-east1 \
  --format="value(spec.template.spec.containers[0].env)" \
  | grep ORG_CREATION

# 3. Check database connection
cloud-sql-proxy --port=5434 nutrinine-prod:us-east1:nutrinine-db &
PGPASSWORD='vaultwarden_secure_pass_2026' psql \
  -h localhost -p 5434 \
  -U vaultwarden_user \
  -d vaultwarden_prod_db \
  -c "SELECT count(*) FROM organizations;"

# 4. Test organization creation via web UI
# https://vault.a2vibes.tech → New Organisation

# 5. Check logs for errors
gcloud logging read \
  "resource.type=cloud_run_revision AND resource.labels.service_name=vaultwarden-prod" \
  --limit=20 \
  --format="value(textPayload)"
```

---

## Known Issues & Workarounds

### Issue: v1.35.0 and v1.35.1 Organization Creation Bug

**Symptoms:** `TypeError: Cannot read properties of undefined (reading 'find')`

**Affected Versions:** 1.35.0, 1.35.1, latest (as of Jan 5, 2026)

**GitHub Issues:** #6638, #6644, #6645, #6648, #6659

**Workaround:** Use v1.34.0
```bash
gcloud run services update vaultwarden-prod \
  --region=us-east1 \
  --image=vaultwarden/server:1.34.0
```

**Upgrade Path:** After creating organizations, can upgrade back to v1.35.1 (bug only affects creation, not usage)

---

### Issue: Session Expiration During Troubleshooting

**Symptoms:** 401 Unauthorized after long debugging session

**Solution:** Log out and log back in to get fresh JWT token

---

### Issue: Traffic Not Switching to New Revision

**Symptoms:** Changes not visible after deployment

**Root Cause:** Cloud Run sometimes keeps traffic on old revision

**Solution:**
```bash
# Force traffic switch
gcloud run services update-traffic vaultwarden-prod \
  --region=us-east1 \
  --to-revisions=NEW_REVISION_NAME=100
```

---

## Monitoring & Alerts

### Key Metrics to Watch

1. **Organization Creation Success Rate**
   - Log filter: `POST /api/organizations => 200 OK`
   - Alert if < 90%

2. **Session Token Errors**
   - Log filter: `Invalid claim`
   - Alert if > 5 per hour

3. **Database Connection Errors**
   - Log filter: `connection to server on socket`
   - Alert immediately

### Log Queries

```bash
# Organization creation attempts
gcloud logging read \
  "resource.labels.service_name=vaultwarden-prod AND textPayload:'POST /api/organizations'" \
  --limit=50

# Failed authentication
gcloud logging read \
  "resource.labels.service_name=vaultwarden-prod AND textPayload:'Invalid claim'" \
  --limit=20

# Database errors
gcloud logging read \
  "resource.labels.service_name=vaultwarden-prod AND textPayload:'connection to server'" \
  --limit=10
```

---

## Next Steps

### Immediate (Completed)
- [x] Create QUAD organization
- [ ] Create NutriNine organization
- [ ] Add collections (dev/qa/prod) to both orgs

### Short-term
- [ ] Document bw CLI workflow for managing secrets
- [ ] Create backup/restore procedures
- [ ] Set up monitoring alerts

### Long-term
- [ ] Monitor v1.35.2+ releases for bug fix
- [ ] Plan upgrade path back to latest version
- [ ] Consider Vaultwarden alternatives if bugs persist

---

## Related Documentation

- [Vaultwarden Setup Guide](../security/VAULTWARDEN_SETUP.md)
- [Session History](../../.claude/rules/SESSION_HISTORY.md)
- [GitHub Issue #6638](https://github.com/dani-garcia/vaultwarden/issues/6638)

---

**Version:** 1.0
**Last Updated:** January 5, 2026
**Author:** Claude Code + Suman Addanki
