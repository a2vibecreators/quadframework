# QUAD API Reference

## Base URL

```
http://localhost:3000  (Development)
https://api.quadframe.work  (Production - future)
```

## Authentication

All endpoints (except `/health`) require Bearer token authentication.

```bash
Authorization: Bearer <QUAD_API_KEY>
```

Default dev key: `quad_dev_key_abc123`

---

## Endpoints

### GET /health

Health check endpoint.

**Request:**
```bash
curl http://localhost:3000/health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "quad-api-poc"
}
```

---

### POST /context

Get organization context for a question. **NO AI processing** - only database lookup.

**Request:**
```bash
curl -X POST http://localhost:3000/context \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer quad_dev_key_abc123" \
  -d '{
    "question": "Who has availability?",
    "domain_slug": "suma"
  }'
```

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `question` | string | Yes | The question to analyze |
| `domain_slug` | string | No | Filter by specific domain |

**Response:**
```json
{
  "success": true,
  "context_type": "availability",
  "domain": "suma",
  "summary": "Team Availability (1 members with capacity):\n- Ashrith Addanke (DEVELOPER): 16 hrs available (60% allocated)",
  "data": [
    {
      "name": "Ashrith Addanke",
      "email": "madhuri.recherla@gmail.com",
      "role": "DEVELOPER",
      "allocation_pct": 60,
      "available_hrs": 16
    }
  ],
  "prompt_addition": "<quad-context>\nTeam Availability...\n</quad-context>\n\nBased on the above context, please answer: Who has availability?"
}
```

**Context Types:**

The API analyzes question keywords to determine context type:

| Keywords | Context Type | Data Returned |
|----------|--------------|---------------|
| available, hours, capacity, bandwidth | `availability` | Team capacity |
| team, who, members, people | `team` | Team roster |
| project, domain, working on | `project` | Project info |
| (default) | `full` | All context |

---

### GET /domains

List active domains (projects).

**Request:**
```bash
curl http://localhost:3000/domains \
  -H "Authorization: Bearer quad_dev_key_abc123"
```

**Response:**
```json
{
  "domains": [
    {
      "slug": "suma",
      "name": "SUMA Platform",
      "description": "SUMA AI Platform Development",
      "team_size": 2
    }
  ]
}
```

---

## Error Responses

### 401 Unauthorized

```json
{
  "detail": "Invalid API key"
}
```

### 500 Internal Server Error

```json
{
  "detail": "Database connection failed: ..."
}
```

---

## Database Schema

### quad_organizations

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| name | VARCHAR | Organization name |
| slug | VARCHAR | URL-friendly slug |
| timezone | VARCHAR | Timezone |
| created_at | TIMESTAMP | Created timestamp |

### quad_domains

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| name | VARCHAR | Project name |
| slug | VARCHAR | URL-friendly slug |
| description | TEXT | Project description |
| methodology | VARCHAR | 'quad' |
| company_id | UUID | FK to organization |
| is_active | BOOLEAN | Active flag |

### quad_team_members

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| name | VARCHAR | Member name |
| email | VARCHAR | Email |
| role | VARCHAR | Role (DIRECTOR, DEVELOPER, etc.) |
| domain_id | UUID | FK to domain |
| allocation_pct | INT | Allocation percentage (0-100) |

---

*Copyright © 2026 Gopi Suman Addanke. All Rights Reserved.*
