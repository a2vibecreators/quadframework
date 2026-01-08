# Infrastructure Agent Specification

**Agent Type:** QUAD Server Agent (Service-Account)
**Version:** 1.0
**Status:** Planned for Phase 2 (Q2 2026)
**Last Updated:** January 8, 2026

---

## Overview

The **Infrastructure Agent** continuously monitors system health and performance, detecting slowdowns, failures, and inefficiencies. It transforms reactive troubleshooting into proactive optimization, automatically alerting teams before customers notice issues.

### Core Capabilities

1. **Real-time Performance Monitoring** - Track API response times, database queries, and deployment durations
2. **Anomaly Detection** - Identify unusual patterns (slow queries, memory spikes, CPU overload)
3. **Auto-Alerting** - Notify teams via Slack, email when thresholds crossed
4. **Root Cause Analysis** - Suggest fixes ("N+1 query pattern detected", "Container memory limit")
5. **Historical Trending** - Track performance over time to identify degradation

---

## Agent Triggers

### Automatic Triggers

| Trigger | Condition | Action |
|---------|-----------|--------|
| **Slow Response** | API response > threshold | Alert team + suggest optimization |
| **Query Performance** | Database query > threshold | Highlight slow query + execution plan |
| **Memory Spike** | Memory usage > 85% | Alert DevOps + suggest scaling |
| **Deployment Duration** | Deployment > expected time | Alert team + check for errors |
| **Error Rate Spike** | Errors > baseline + 10% | Investigate + identify root cause |
| **Daily Report** | Scheduled (e.g., 9 AM) | Send performance summary to team |

### Manual Triggers

```
📧 Email: "why is our API slow today?"
💬 Messenger: "@quad analyze slow API response"
🖥️ QUAD App: Dashboard > "Performance Analysis" button
📊 Datadog: Integration with existing monitoring tools
```

---

## Capabilities & Modes

### 1. Real-time Performance Monitoring

**Input:** Metrics from APM tools (Datadog, New Relic, Prometheus, CloudWatch)
**Output:** Performance dashboard, alerts, analysis

**Monitors:**

| Metric | Good | Warning | Critical |
|--------|------|---------|----------|
| **API P95 Response Time** | < 200ms | 200-500ms | > 500ms |
| **Database Query Time** | < 100ms | 100-500ms | > 500ms |
| **Deployment Duration** | < 5 min | 5-15 min | > 15 min |
| **Error Rate** | < 0.1% | 0.1-1% | > 1% |
| **Container Memory** | < 60% | 60-85% | > 85% |
| **CPU Usage** | < 70% | 70-90% | > 90% |

**Example - Slow API Endpoint:**

```
🚨 ALERT: API /api/users response time spike

Current Performance:
  ⏱️ P95: 1,250ms (was 120ms 1 hour ago)
  📊 Error rate: 0.5% (normal: 0.05%)
  📈 Traffic: 15K requests/min (was 5K)

Root Cause Analysis:
  • N+1 query pattern detected in getUserWithDomain()
  • SELECT user.* (OK)
  • SELECT domain.* for each user (500 queries per request!)

Quick Fixes:
  1. Add JOIN to getUserWithDomain() query
  2. Add caching for domain lookups
  3. Paginate response (show 10 users, not 100)

Manual Fix Time: ~1 hour
QUAD Code Agent can implement: ✅ Yes (~5 minutes)
```

**Features:**
- ✅ Real-time dashboard with live metrics
- ✅ Comparison to historical baseline
- ✅ Identifies outlier API endpoints
- ✅ Cross-correlation (slow API + high memory = OOM risk)
- ✅ Anomaly detection (statistical deviation from norm)

---

### 2. Slow Query Detection

**Input:** Database query logs (PostgreSQL `pg_stat_statements`, MySQL slow log)
**Output:** Slow query report, optimization suggestions

**Process:**

```
1. Query Execution
   → PostgreSQL logs slow query (> 1 second)
   ↓
2. Analysis
   → Fetch query execution plan (EXPLAIN ANALYZE)
   → Identify sequential scans, missing indexes
   → Check for N+1 patterns
   ↓
3. Root Cause
   → "Missing index on users.email"
   → "Sequential scan on 100K rows"
   → "Cartesian product in JOIN"
   ↓
4. Recommendation
   → "CREATE INDEX idx_users_email ON users(email)"
   → Estimated improvement: 10x faster
   ↓
5. Action
   → Alert DBA or Code Agent
   → Execute fix (if approved)
   → Verify improvement with benchmarks
```

**Example Report:**

```markdown
# Slow Queries (Last 24 hours)

## Top 3 Slowest Queries

### 1. getUserWithDomain - 2,150ms average
```sql
SELECT u.*, d.* FROM users u
  LEFT JOIN domains d ON u.id = d.owner_id
  WHERE u.org_id = $1
```
**Issue:** Cartesian product (100 users × 50 domains each = 5,000 rows)
**Fix:** Use window function or separate queries
**Estimated Time Saved:** 8 seconds per request

### 2. findRecentFlows - 850ms average
```sql
SELECT f.* FROM flows f
  WHERE f.created_at > NOW() - INTERVAL '7 days'
```
**Issue:** No index on `created_at`
**Fix:** `CREATE INDEX idx_flows_created_at ON flows(created_at DESC)`
**Estimated Impact:** 50x faster

### 3. getOrganizationStats - 620ms average
**Issue:** Multiple subqueries (could use aggregation)
**Fix:** Consolidate into single query or add materialized view
```

---

### 3. Deployment Monitoring

**Tracks:** CI/CD pipeline health, deployment duration, rollback frequency

**Workflow:**

```
1. Deploy starts
   → Infrastructure Agent begins monitoring
   → Track build time, test time, deploy time
   ↓
2. During deployment
   → Monitor error rate, latency
   → Check new container health
   → Verify database migrations
   ↓
3. Deployment completes
   → Compare pre/post metrics
   → Alert if performance degraded
   → Send completion notification
   ↓
4. Post-deployment analysis
   → "Deployment took 18 min (usually 5 min)"
   → "Error rate increased from 0.05% to 0.5%"
   → Suggest rollback if needed
```

**Example:**

```
✅ Deployment Succeeded: quadframework-web v1.2.3

Timeline:
  🏗️  Build: 2 min 30 sec ✅
  🧪 Tests: 3 min 15 sec ✅
  🚀 Deploy: 4 min 45 sec ✅
  ✔️  Health Check: PASS ✅

Performance Impact:
  API Response Time: 120ms → 125ms (small increase)
  Error Rate: 0.05% → 0.08% (within tolerance)
  Memory Usage: Stable

🎉 All checks passed! Production healthy.
```

---

### 4. Error Rate & Anomaly Detection

**Input:** Application logs, error tracking (Sentry, Rollbar)
**Output:** Root cause analysis, alert

**Detects:**

| Anomaly | Detection | Action |
|---------|-----------|--------|
| **Error Rate Spike** | Errors > baseline + 10% | Identify affected endpoint + suggest fix |
| **Specific Error Trending Up** | Same error recurring | Link to similar past issues |
| **Memory Leak** | Memory gradually increasing over days | Alert DevOps to restart container |
| **Cascading Failures** | Service A fails → Service B fails | Identify dependency chain |
| **Silent Failures** | No errors logged but response empty | Detect via assertion checks |

**Example - Error Analysis:**

```
🚨 ALERT: Error rate spike detected

Error Rate: 2.5% (normal: 0.05%) - 50x increase!

Top Errors:
  1. "Database connection refused" (68% of errors)
     → postgres-quad-dev unavailable?
     → Check container status: docker ps | grep postgres

  2. "Timeout contacting java-backend:8080" (22% of errors)
     → quad-services-dev not responding
     → Check logs: docker logs quad-services-dev

  3. "Invalid JWT token" (10% of errors)
     → JWT_SECRET mismatch or expired?

Quick Diagnosis:
  • postgres-quad-dev: NOT RUNNING ❌
  • quad-services-dev: Running but logs show connection errors
  • Caddy routing: Healthy ✅

Root Cause: PostgreSQL container crashed
Suggested Fix: `docker start postgres-quad-dev`
Estimated Fix Time: 30 seconds
```

---

### 5. Daily Performance Reports

**Sent:** Every morning at 9 AM (customizable)
**Recipients:** Engineering lead, DevOps team

**Report Contents:**

```markdown
# Daily Infrastructure Report
**Date:** January 8, 2026

## Summary
✅ 99.95% uptime (SLA: 99.9%)
⚠️ 2 performance issues detected & fixed
📈 Traffic: 2.3M requests (↑12% vs yesterday)

## Performance Metrics

| Metric | Yesterday | Today | Trend |
|--------|-----------|-------|-------|
| API P95 | 145ms | 152ms | ↑ +5% |
| DB Query P95 | 85ms | 91ms | ↑ +7% |
| Error Rate | 0.04% | 0.06% | ↑ +50% |
| Deployment Duration | 5m 30s | 6m 15s | ↑ +14% |

## Detected Issues
1. ✅ Slow query on users.email lookup (FIXED: added index)
2. ✅ Memory spike at 2 PM (container restarted)

## Upcoming
📅 Database maintenance scheduled for 2/15
🔄 Node upgrades planned for next week

## Team Actions
- [ ] Review slow query fixes
- [ ] Monitor memory usage trend
- [ ] Plan capacity upgrade for Q1
```

---

## Configuration & Customization

### Agent Settings

```yaml
# .quad/infrastructure-agent.yml
enabled: true

monitoring:
  enabled: true
  apm_provider: "datadog"  # or "new-relic", "prometheus", "cloudwatch"
  check_interval_secs: 30  # How often to check metrics

  thresholds:
    api_response_time_ms: 500      # Alert if P95 > 500ms
    database_query_ms: 500         # Alert if query > 500ms
    error_rate_percent: 1.0        # Alert if > 1%
    memory_usage_percent: 85       # Alert if > 85%
    cpu_usage_percent: 90          # Alert if > 90%
    deployment_duration_mins: 15   # Alert if deploy > 15 min

alerts:
  slack_enabled: true
  email_enabled: true
  slack_channel: "#infrastructure"
  daily_report_time: "09:00"  # 9 AM daily

database:
  enabled: true
  slow_query_threshold_ms: 1000   # Alert if query > 1 second
  analyze_execution_plans: true   # Run EXPLAIN ANALYZE
  check_interval_secs: 300        # Check every 5 minutes

deployments:
  enabled: true
  monitor_ci_cd: true
  track_error_rate_changes: true
  auto_rollback_on_spike: false   # Manual approval required
  rollback_threshold: 5           # Rollback if errors > 5x baseline

ignore:
  - "SELECT 1"  # Skip health checks
  - "SELECT now()"  # Skip time queries
```

### Custom Thresholds by Environment

```yaml
# Different SLAs for different environments
dev:
  api_response_time_ms: 1000      # More lenient in dev
  error_rate_percent: 5.0

qa:
  api_response_time_ms: 500
  error_rate_percent: 1.0

prod:
  api_response_time_ms: 200       # Strict in production
  error_rate_percent: 0.1
  escalate_to_oncall: true        # Page on-call engineer
```

---

## Integration Points

### Datadog Integration
- ✅ Fetch metrics from Datadog API
- ✅ Set up monitors and alerts
- ✅ Send events to Datadog timeline
- ✅ Link to Datadog dashboards in alerts

### New Relic Integration
- ✅ Query APM data
- ✅ Analyze trace data
- ✅ Get transaction performance

### Prometheus Integration
- ✅ Query Prometheus for metrics
- ✅ Use PromQL to identify anomalies
- ✅ Set up recording rules

### Slack Integration
- ✅ Send performance alerts
- ✅ Daily/weekly reports
- ✅ Post-deployment summaries
- ✅ Root cause analysis in threads

### PagerDuty Integration
- ✅ Trigger incidents on critical alerts
- ✅ Auto-escalate after 15 minutes
- ✅ Link to runbooks

### GitHub Integration
- ✅ Auto-create issue for slow query fixes
- ✅ Link to related PRs
- ✅ Track performance improvements

---

## Example: Infrastructure Agent in Action

### Scenario: Detecting Memory Leak

**Hour 1: Deployment Complete**
```
✅ Container deployed: quadframework-web:v1.3.0
Memory usage: 256 MB (normal for this container)
Infrastructure Agent begins baseline monitoring
```

**Hour 3: First Alert**
```
⚠️ WARNING: Memory trending upward
Memory usage: 380 MB (↑48% in 2 hours)

Trend line suggests OOM in ~4 hours
Suggested action: Monitor or restart container
```

**Hour 5: Critical Alert**
```
🚨 CRITICAL: Memory near limit
Memory usage: 512 MB of 512 MB limit (100%)!

Container about to be OOM-killed
Immediate action: Restart container OR scale up

Automatic Actions Taken:
1. Scaled from 1 → 2 containers (load balanced)
2. Restarted original container (freed memory)
3. Alerted DevOps: "Memory leak detected - investigate PR #1234"
```

**Hour 6: Analysis Report**
```
📊 Memory Leak Analysis

Suspected Cause: PR #1234 "Add caching layer"
- New Redis cache but forgot to evict old entries
- Cache size grows: 1MB/min × 360 min = 360MB

Solution: Add cache TTL (time-to-live)
Code Agent can fix: ✅ Yes
Fix PR created: github.com/QUAD/quad-web/pull/5678
Estimated time: 5 minutes

Action Items:
1. ✅ Scale containers (temporary fix)
2. ⏳ Merge cache TTL fix
3. ⏳ Monitor memory for 24 hours
4. ⏳ Write regression test for memory leaks
```

---

## Success Metrics

| Metric | Target | How Measured |
|--------|--------|--------------|
| Mean Time to Detection | < 5 min | From spike to first alert |
| Mean Time to Resolution | < 30 min | From alert to fix deployed |
| False Positive Rate | < 5% | Alerts that don't indicate real issues |
| Uptime Improvement | 99.95%+ | Year-over-year improvement |
| Team Satisfaction | 4.5/5 | Quarterly survey on tool usefulness |
| Incidents Prevented | 90%+ | Issues detected before customer impact |

---

## Limitations & Scope

### What Infrastructure Agent Does NOT Do

- ❌ Fix issues automatically (alerts team first, suggests fixes)
- ❌ Scale infrastructure (recommends scaling, doesn't auto-execute)
- ❌ Manage DNS or networking
- ❌ Handle security incidents (requires human review)
- ❌ Predict failures weeks in advance (trend analysis only)

### Privacy Considerations

- 🔒 Metrics collected: Response times, error rates, resource usage
- 🔒 Personal data: NOT stored (only aggregated metrics)
- 🔒 Retention: Keep detailed metrics for 30 days, summaries for 1 year
- 🔒 Access control: Only team members with "DevOps" role can view infrastructure alerts

---

## Roadmap

**Phase 1 (Q2 2026):** MVP
- ✅ Real-time performance monitoring (APM integration)
- ✅ Slow query detection
- ✅ Error rate spike alerts
- ✅ Slack notifications

**Phase 2 (Q3 2026):** Advanced
- Predictive alerting (forecast issues before they happen)
- Root cause analysis with code suggestions
- Auto-remediation for common issues (restart container, scale up)
- Historical trend analysis

**Phase 3 (Q4 2026):** Enhancement
- Machine learning anomaly detection
- Multi-region performance comparison
- SLA dashboards
- Capacity planning recommendations

---

## Data Model

### Metrics Record

```json
{
  "id": "uuid",
  "orgId": "uuid",
  "timestamp": "2026-01-08T10:30:00Z",
  "metric_type": "api_response_time",
  "value": 245.5,
  "unit": "milliseconds",
  "endpoint": "/api/users",
  "method": "GET",
  "status_code": 200,
  "host": "quad-services-dev:8080",
  "environment": "dev",
  "percentile": 95,
  "comparison_to_baseline": 1.22  // 1.22x baseline
}
```

### Alert Record

```json
{
  "id": "uuid",
  "orgId": "uuid",
  "alert_type": "memory_spike",
  "severity": "critical",
  "timestamp": "2026-01-08T14:45:00Z",
  "message": "Memory usage 512MB of 512MB limit (100%)",
  "root_cause": "Possible cache memory leak in PR #1234",
  "suggested_actions": [
    "Scale containers from 1 to 2",
    "Restart container to free memory",
    "Review cache TTL configuration"
  ],
  "status": "acknowledged",
  "acknowledged_by": "alice@example.com",
  "resolved_at": "2026-01-08T15:20:00Z",
  "resolution": "Restarted container + deployed cache TTL fix"
}
```

---

**Next Steps:**
- [ ] Design APM data collection pipeline
- [ ] Integrate with Datadog API
- [ ] Implement slow query analyzer
- [ ] Create Slack notification system
- [ ] Build infrastructure dashboard
- [ ] Write test suite

---

**Maintained By:** QUAD Platform Team
**Contact:** Infrastructure Agent Maintainer
