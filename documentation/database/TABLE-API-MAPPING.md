# QUAD Database - Table to API Mapping

**Total Tables:** 139 (after SUMA cleanup)
**Generated:** January 14, 2026

---

## 🎯 POC CORE (Must Have - 10 tables)

| Table | API Endpoint | Purpose |
|-------|--------------|---------|
| `quad_organizations` | `POST /api/orgs` | Create/manage organizations |
| `quad_org_members` | `POST /api/orgs/:id/members` | Add users to org |
| `quad_org_settings` | `GET/PUT /api/orgs/:id/settings` | Org configuration |
| `quad_users` | `POST /api/users` | User registration |
| `quad_user_sessions` | `POST /api/auth/login` | Authentication |
| `quad_domains` | `POST /api/domains` | Projects/domains |
| `quad_domain_members` | `POST /api/domains/:id/members` | Project team |
| `quad_companies` | `POST /api/companies` | Company info |
| `quad_flows` | `POST /api/flows` | Workflows |
| `quad_tickets` | `POST /api/tickets` | Tasks/tickets |

**quad init flow:**
```
~/.quad/config.json     → quad_organizations, quad_users
<project>/.quad/        → quad_domains, quad_flows
```

---

## 🧠 AI/Context (16 tables)

| Table | API Endpoint | Purpose |
|-------|--------------|---------|
| `quad_ai_contexts` | `POST /api/ai/contexts` | Store AI context |
| `quad_ai_conversations` | `POST /api/ai/conversations` | Chat history |
| `quad_ai_messages` | `POST /api/ai/messages` | Individual messages |
| `quad_ai_user_memories` | `GET /api/ai/memories` | User preferences |
| `quad_ai_configs` | `GET /api/ai/config` | AI provider settings |
| `quad_ai_provider_config` | `GET /api/ai/providers` | Claude/OpenAI config |
| `quad_ai_credit_balances` | `GET /api/ai/credits` | Usage credits |
| `quad_ai_credit_transactions` | `GET /api/ai/credits/history` | Credit history |
| `quad_ai_operations` | `POST /api/ai/operations` | AI operation logs |
| `quad_ai_code_reviews` | `POST /api/ai/reviews` | Code review results |
| `quad_ai_analysis_cache` | (internal) | Cache AI responses |
| `quad_ai_activity_routing` | (internal) | Route to correct AI |
| `quad_ai_context_relationships` | (internal) | Context links |
| `quad_memory_chunks` | (internal) | RAG chunks |
| `quad_memory_documents` | (internal) | RAG documents |
| `quad_memory_keywords` | (internal) | Search keywords |

---

## 👥 Teams & Circles (6 tables)

| Table | API Endpoint | Purpose |
|-------|--------------|---------|
| `quad_circles` | `POST /api/circles` | Team circles |
| `quad_circle_members` | `POST /api/circles/:id/members` | Circle membership |
| `quad_roles` | `GET /api/roles` | Role definitions |
| `quad_core_roles` | `GET /api/roles/core` | System roles |
| `quad_user_role_allocations` | `POST /api/users/:id/roles` | Assign roles |
| `quad_skills` | `GET /api/skills` | Skill definitions |

---

## 💻 Code & Git (10 tables)

| Table | API Endpoint | Purpose |
|-------|--------------|---------|
| `quad_git_repositories` | `POST /api/repos` | Git repos |
| `quad_git_integrations` | `POST /api/repos/:id/integrate` | GitHub/GitLab |
| `quad_git_operations` | `GET /api/repos/:id/operations` | Git history |
| `quad_pull_requests` | `GET /api/prs` | PR tracking |
| `quad_pr_reviewers` | `POST /api/prs/:id/reviewers` | PR reviewers |
| `quad_pr_approvals` | `POST /api/prs/:id/approve` | PR approvals |
| `quad_codebase_files` | (internal) | File index |
| `quad_codebase_indexes` | (internal) | Search index |
| `quad_code_cache` | (internal) | Code cache |
| `quad_release_notes` | `POST /api/releases` | Release notes |

---

## 🚀 Deployments (8 tables)

| Table | API Endpoint | Purpose |
|-------|--------------|---------|
| `quad_deployments` | `POST /api/deployments` | Deploy history |
| `quad_deployment_recipes` | `GET /api/deployments/recipes` | Deploy templates |
| `quad_environments` | `GET /api/environments` | Dev/QA/Prod |
| `quad_infrastructure_config` | `GET /api/infra/config` | Infra settings |
| `quad_rollback_operations` | `POST /api/deployments/:id/rollback` | Rollback |
| `quad_sandbox_instances` | `POST /api/sandbox` | Dev sandboxes |
| `quad_sandbox_usage` | `GET /api/sandbox/usage` | Sandbox metrics |
| `quad_database_connections` | `GET /api/databases` | DB connections |

---

## 🏠 Smart Home/Devices (5 tables)

| Table | API Endpoint | Purpose |
|-------|--------------|---------|
| `quad_devices` | `POST /api/devices` | Device registry |
| `quad_device_types` | `GET /api/devices/types` | Device types |
| `quad_device_commands` | `POST /api/devices/:id/command` | Send commands |
| `quad_command_wiring` | `GET /api/devices/wiring` | Command routing |
| `quad_known_persons` | `GET /api/persons` | Known people (voice) |

---

## 📅 Meetings & HR (8 tables)

| Table | API Endpoint | Purpose |
|-------|--------------|---------|
| `quad_meetings` | `POST /api/meetings` | Schedule meetings |
| `quad_meeting_action_items` | `POST /api/meetings/:id/actions` | Action items |
| `quad_meeting_follow_ups` | `GET /api/meetings/:id/followups` | Follow ups |
| `quad_meeting_integrations` | `POST /api/meetings/integrate` | Zoom/Teams |
| `quad_kudos` | `POST /api/kudos` | Team recognition |
| `quad_training_content` | `GET /api/training` | Training materials |
| `quad_training_completions` | `POST /api/training/:id/complete` | Track completion |
| `quad_work_sessions` | `POST /api/sessions` | Work tracking |

---

## 🔐 Auth & Security (10 tables)

| Table | API Endpoint | Purpose |
|-------|--------------|---------|
| `quad_sso_configs` | `POST /api/auth/sso` | SSO setup |
| `company_sso_configs` | `GET /api/companies/:id/sso` | Company SSO |
| `quad_email_verification_codes` | (internal) | Email verify |
| `quad_validated_credentials` | (internal) | Stored creds |
| `quad_secret_rotations` | `POST /api/secrets/rotate` | Secret rotation |
| `quad_secret_scans` | `GET /api/security/scans` | Security scans |
| `quad_portal_access` | `GET /api/portal/access` | Portal permissions |
| `quad_portal_audit_log` | `GET /api/portal/audit` | Audit trail |
| `quad_verification_requests` | (internal) | Verification |
| `quad_api_access_config` | `GET /api/access/config` | API access rules |

---

## ⚙️ System/Config (12 tables)

| Table | API Endpoint | Purpose |
|-------|--------------|---------|
| `quad_config_settings` | `GET /api/config` | System config |
| `quad_demo_settings` | `GET /api/demo/settings` | Demo mode |
| `quad_industry_defaults` | `GET /api/industry/:type` | Industry templates |
| `quad_notification_preferences` | `PUT /api/notifications/prefs` | Notification settings |
| `quad_notifications` | `GET /api/notifications` | User notifications |
| `quad_api_request_logs` | (internal) | API logging |
| `quad_cache_usage` | (internal) | Cache metrics |
| `quad_indexing_usage` | (internal) | Index metrics |
| `quad_anonymization_rules` | (internal) | Data anonymization |
| `quad_context_rules` | (internal) | Context rules |
| `quad_context_requests` | (internal) | Context requests |
| `quad_context_sessions` | (internal) | Context sessions |

---

## 📊 Metrics & Analytics (6 tables)

| Table | API Endpoint | Purpose |
|-------|--------------|---------|
| `quad_dora_metrics` | `GET /api/metrics/dora` | DORA metrics |
| `quad_workload_metrics` | `GET /api/metrics/workload` | Team workload |
| `quad_user_activity_summaries` | `GET /api/users/:id/activity` | User activity |
| `quad_user_rankings` | `GET /api/rankings` | Leaderboard |
| `quad_ranking_configs` | `GET /api/rankings/config` | Ranking rules |
| `quad_technical_debt_scores` | `GET /api/metrics/debt` | Tech debt |

---

## 🔄 Workflows & Approvals (10 tables)

| Table | API Endpoint | Purpose |
|-------|--------------|---------|
| `quad_flows` | `POST /api/flows` | Workflows |
| `quad_flow_branches` | `GET /api/flows/:id/branches` | Flow branches |
| `quad_flow_stage_history` | `GET /api/flows/:id/history` | Stage history |
| `quad_cycles` | `POST /api/cycles` | Sprint cycles |
| `quad_cycle_risk_predictions` | `GET /api/cycles/:id/risk` | Risk analysis |
| `quad_approvals` | `POST /api/approvals` | General approvals |
| `quad_database_approvals` | `POST /api/db/approvals` | DB change approvals |
| `quad_database_operations` | `GET /api/db/operations` | DB operations |
| `quad_milestones` | `POST /api/milestones` | Project milestones |
| `quad_requirements` | `POST /api/requirements` | Requirements |

---

## 📝 Tickets & Tasks (8 tables)

| Table | API Endpoint | Purpose |
|-------|--------------|---------|
| `quad_tickets` | `POST /api/tickets` | Create tickets |
| `quad_ticket_comments` | `POST /api/tickets/:id/comments` | Comments |
| `quad_ticket_time_logs` | `POST /api/tickets/:id/time` | Time tracking |
| `quad_ticket_skills` | `GET /api/tickets/:id/skills` | Required skills |
| `quad_ticket_sandbox_groups` | (internal) | Sandbox grouping |
| `quad_story_point_suggestions` | `GET /api/tickets/:id/estimate` | AI estimates |
| `quad_cost_estimates` | `GET /api/tickets/:id/cost` | Cost estimates |
| `quad_risk_factors` | `GET /api/tickets/:id/risk` | Risk factors |

---

## 👤 User Management (12 tables)

| Table | API Endpoint | Purpose |
|-------|--------------|---------|
| `quad_users` | `POST /api/users` | User CRUD |
| `quad_user_sessions` | `POST /api/auth/login` | Sessions |
| `quad_user_skills` | `PUT /api/users/:id/skills` | User skills |
| `quad_user_setup_journeys` | `GET /api/users/:id/journey` | Onboarding |
| `quad_user_resource_setups` | `POST /api/users/:id/setup` | Resource setup |
| `quad_org_invitations` | `POST /api/orgs/:id/invite` | Invite users |
| `quad_org_members` | `GET /api/orgs/:id/members` | Org members |
| `quad_org_setup_status` | `GET /api/orgs/:id/status` | Setup progress |
| `quad_org_tiers` | `GET /api/orgs/tiers` | Pricing tiers |
| `quad_assignment_scores` | (internal) | Task assignment AI |
| `quad_skill_feedback` | `POST /api/skills/:id/feedback` | Skill feedback |
| `quad_domain_members` | `GET /api/domains/:id/members` | Project members |

---

## 🔧 Other/Support (18 tables)

| Table | API Endpoint | Purpose |
|-------|--------------|---------|
| `quad_domain_operations` | (internal) | Domain ops |
| `quad_domain_resources` | `GET /api/domains/:id/resources` | Domain resources |
| `quad_file_imports` | `POST /api/import` | File imports |
| `quad_incident_runbooks` | `GET /api/incidents/runbooks` | Incident response |
| `quad_runbook_executions` | `POST /api/incidents/:id/run` | Execute runbook |
| `quad_integration_health_checks` | `GET /api/integrations/health` | Health checks |
| `quad_memory_templates` | `GET /api/memory/templates` | Memory templates |
| `quad_memory_update_queue` | (internal) | Memory updates |
| `quad_platform_credit_pool` | `GET /api/credits/pool` | Credit pool |
| `quad_platform_pool_transactions` | `GET /api/credits/pool/history` | Pool history |
| `quad_rag_indexes` | (internal) | RAG indexes |
| `quad_release_contributors` | `GET /api/releases/:id/contributors` | Contributors |
| `quad_resource_attributes` | `GET /api/resources/attributes` | Resource attrs |
| `quad_resource_attribute_requirements` | (internal) | Attr requirements |
| `quad_resource_setup_templates` | `GET /api/resources/templates` | Setup templates |
| `quad_setup_bundles` | `GET /api/setup/bundles` | Setup bundles |
| `quad_slack_bot_commands` | `POST /api/slack/commands` | Slack bot |
| `quad_slack_messages` | `GET /api/slack/messages` | Slack messages |
| `QUAD_adoption_matrix` | `GET /api/adoption` | Adoption tracking |
| `quad_adoption_matrix` | (duplicate - remove) | |
| `quad_developer_onboarding_progress` | `GET /api/onboarding/:id` | Onboarding |
| `quad_developer_onboarding_templates` | `GET /api/onboarding/templates` | Templates |

---

## 📊 Views (2)

| View | Purpose |
|------|---------|
| `v_sandbox_usage_daily` | Daily sandbox metrics |
| `v_sandbox_usage_hourly` | Hourly sandbox metrics |

---

## Summary

| Category | Tables | API Endpoints |
|----------|--------|---------------|
| POC Core | 10 | 10 |
| AI/Context | 16 | 8 |
| Teams/Circles | 6 | 6 |
| Code/Git | 10 | 6 |
| Deployments | 8 | 7 |
| Smart Home | 5 | 4 |
| Meetings/HR | 8 | 7 |
| Auth/Security | 10 | 5 |
| System/Config | 12 | 4 |
| Metrics | 6 | 5 |
| Workflows | 10 | 9 |
| Tickets | 8 | 5 |
| User Mgmt | 12 | 10 |
| Other | 18 | 10 |
| **Total** | **139** | **~96** |

---

**Copyright © 2026 Gopi Suman Addanke. All Rights Reserved.**
