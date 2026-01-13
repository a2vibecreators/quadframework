# QUAD Organization Import Template

## Excel Structure (4 Tabs)

### Tab 1: Organization
| Column | Example | Maps To |
|--------|---------|---------|
| org_name | "Acme Corp" | quad_organizations.name |
| slug | "acme" | quad_organizations.slug |
| industry | "Technology" | quad_organizations.industry |
| team_size | "50-100" | quad_organizations.team_size |
| timezone | "America/New_York" | quad_organizations.timezone |
| contact_email | "admin@acme.com" | quad_organizations.contact_email |

### Tab 2: Team Members
| Column | Example | Maps To |
|--------|---------|---------|
| email | "alex@acme.com" | quad_users.email |
| name | "Alex Director" | quad_users.name |
| job_title | "Executive Director" | quad_users.job_title |
| department | "Engineering" | quad_users.department |
| reports_to_email | "" | (lookup user_id) |
| github_username | "alexdir" | quad_users.github_username |
| slack_user_id | "U12345" | quad_users.slack_user_id |

### Tab 3: Projects (Domains)
| Column | Example | Maps To |
|--------|---------|---------|
| project_name | "SUMA Platform" | quad_domains.name |
| slug | "suma" | quad_domains.slug |
| description | "AI Platform" | quad_domains.description |
| methodology | "quad" | quad_domains.methodology |
| git_repo_url | "github.com/..." | quad_domains.git_repo_url |
| owner_email | "dir1@acme.com" | quad_domains.created_by |

### Tab 4: Allocations
| Column | Example | Maps To |
|--------|---------|---------|
| user_email | "dev1@acme.com" | quad_domain_members.user_id (lookup) |
| project_slug | "suma" | quad_domain_members.domain_id (lookup) |
| role | "DEVELOPER" | quad_domain_members.role |
| allocation_pct | 40 | quad_domain_members.allocation_percentage |
| start_date | "2026-01-13" | effective_date |
| end_date | "" | end_date (optional) |

---

## Example Data

### Organization
| org_name | slug | industry | team_size |
|----------|------|----------|-----------|
| Acme Corp | acme | Technology | 10-50 |

### Team Members
| email | name | job_title | reports_to_email |
|-------|------|-----------|------------------|
| alex@acme.com | Alex Executive | Executive Director | |
| dir1@acme.com | Director One | Director | alex@acme.com |
| dir2@acme.com | Director Two | Director | alex@acme.com |
| ba1@acme.com | BA One | Business Analyst | dir1@acme.com |
| dev1@acme.com | Dev One | Developer | dir1@acme.com |
| dev2@acme.com | Dev Two | Developer | dir1@acme.com |
| qa1@acme.com | QA One | QA Engineer | dir1@acme.com |

### Projects
| project_name | slug | owner_email |
|--------------|------|-------------|
| SUMA Platform | suma | dir1@acme.com |
| NutriNine App | nutri | dir2@acme.com |

### Allocations
| user_email | project_slug | role | allocation_pct |
|------------|--------------|------|----------------|
| dir1@acme.com | suma | MANAGER | 100 |
| ba1@acme.com | suma | MANAGER | 50 |
| dev1@acme.com | suma | DEVELOPER | 40 |
| dev1@acme.com | nutri | DEVELOPER | 60 |
| dev2@acme.com | suma | DEVELOPER | 100 |
| qa1@acme.com | suma | QA | 80 |
| qa1@acme.com | nutri | QA | 20 |

---

## Allocation Logic

```
Weekly Hours = 40
Available Hours = 40 × (100 - allocation_pct) / 100

Example: dev1 is 40% on SUMA
- SUMA hours: 40 × 0.40 = 16 hours/week
- Available for new SUMA tickets: 16 hours max
```
