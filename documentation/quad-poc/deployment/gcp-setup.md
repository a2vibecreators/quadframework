# QUAD GCP Deployment Guide

## Overview

QUAD uses GCP (Google Cloud Platform) for:
- **Secret Manager** - Store secrets (DB passwords, API keys)
- **Cloud Run** - Deploy containerized services
- **Container Registry** - Store Docker images

## Prerequisites

1. GCP Account with billing enabled
2. `gcloud` CLI installed
3. Docker installed (for building images)

## GCP Project Setup

### 1. Create GCP Projects

Create separate projects for each environment:

```bash
# Development
gcloud projects create suma-dev --name="SUMA Development"

# Production
gcloud projects create suma-prod --name="SUMA Production"
```

### 2. Enable Required APIs

```bash
# Enable APIs for each project
for PROJECT in suma-dev suma-prod; do
  gcloud services enable secretmanager.googleapis.com --project=$PROJECT
  gcloud services enable run.googleapis.com --project=$PROJECT
  gcloud services enable containerregistry.googleapis.com --project=$PROJECT
done
```

### 3. Set Up Secret Manager

#### Using QUAD CLI

```bash
quad setup suma-dev
```

This interactively creates secrets:
- `DB_PASSWORD`
- `API_KEY`
- `JWT_SECRET`
- `QUAD_API_KEY`

#### Manual Setup

```bash
# Create a secret
echo -n "your-password" | gcloud secrets create DB_PASSWORD \
  --project=suma-dev \
  --data-file=-

# View secret
gcloud secrets versions access latest --secret=DB_PASSWORD --project=suma-dev
```

### 4. IAM Permissions

Grant Cloud Run service account access to secrets:

```bash
PROJECT_NUMBER=$(gcloud projects describe suma-dev --format='value(projectNumber)')

gcloud secrets add-iam-policy-binding DB_PASSWORD \
  --project=suma-dev \
  --member="serviceAccount:$PROJECT_NUMBER-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

---

## Deployment Flow

### Using QUAD CLI

```bash
# Deploy to dev
quad dev deploy suma

# Deploy to prod (requires confirmation)
quad prod deploy suma
```

### What Happens

1. **Read Config** - From Excel/database
2. **Fetch Secrets** - From GCP Secret Manager
3. **Build Image** - Docker build
4. **Push to GCR** - Push to Container Registry
5. **Deploy to Cloud Run** - With secrets mounted

---

## Cloud Run Configuration

### Service Configuration

```yaml
# Example Cloud Run service config
service:
  name: suma-api
  region: us-central1
  memory: 512Mi
  cpu: 1
  minInstances: 0
  maxInstances: 10
  timeout: 300s

secrets:
  - DB_PASSWORD:latest
  - API_KEY:latest
  - JWT_SECRET:latest
```

### Environment Variables

Secrets are mounted as environment variables:

```bash
# In your code
DB_PASSWORD = os.getenv("DB_PASSWORD")
API_KEY = os.getenv("API_KEY")
```

---

## Excel Deployment Tab

Configure deployment in Excel:

| Project | Environment | GCP Project ID | Region | Git Repo | Service Name |
|---------|-------------|----------------|--------|----------|--------------|
| SUMA Platform | dev | suma-dev | us-central1 | github.com/a2vibes/quad-suma-api | suma-api |
| SUMA Platform | prod | suma-prod | us-central1 | github.com/a2vibes/quad-suma-api | suma-api |
| NutriNine | dev | nutrinne-dev | us-central1 | github.com/a2vibes/nutrinne-api | nutrinne-api |

---

## Secrets Management

### What Goes in Secret Manager

| Secret | Description | Required |
|--------|-------------|----------|
| `DB_PASSWORD` | Database password | Yes |
| `API_KEY` | External API keys | As needed |
| `JWT_SECRET` | JWT signing key | Yes |
| `QUAD_API_KEY` | QUAD API authentication | Yes |

### What Stays in Excel (Plain Text)

| Config | Example |
|--------|---------|
| GCP Project ID | suma-dev |
| Region | us-central1 |
| Git Repo URL | github.com/a2vibes/... |
| Service Name | suma-api |

**Rule:** If it's a password, key, or credential → Secret Manager. Everything else → Excel.

---

## Troubleshooting

### API Not Enabled

```
ERROR: Secret Manager API has not been used in project...
```

**Fix:**
```bash
gcloud services enable secretmanager.googleapis.com --project=suma-dev
```

### Permission Denied

```
ERROR: Permission denied accessing secret...
```

**Fix:**
```bash
# Check IAM permissions
gcloud secrets get-iam-policy DB_PASSWORD --project=suma-dev

# Grant access
gcloud secrets add-iam-policy-binding DB_PASSWORD \
  --member="user:your-email@gmail.com" \
  --role="roles/secretmanager.secretAccessor"
```

### Not Authenticated

```
ERROR: gcloud auth not configured
```

**Fix:**
```bash
gcloud auth login
gcloud config set project suma-dev
```

---

## Cost Optimization

1. **Secret Manager:** $0.06 per 10,000 access operations
2. **Cloud Run:** Pay per request (dev can use 0 min instances)
3. **Container Registry:** Standard storage costs

### Recommendations

- Use `minInstances: 0` for dev (cold starts OK)
- Use `minInstances: 1` for prod (faster response)
- Clean up old container images monthly

---

*Copyright © 2026 Gopi Suman Addanke. All Rights Reserved.*
