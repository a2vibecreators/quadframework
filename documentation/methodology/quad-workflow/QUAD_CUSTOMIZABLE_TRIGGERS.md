# QUAD Customizable Trigger System

**Part of QUAD™ (Quick Unified Agentic Development) Methodology**
**© 2025 Suman Addanke / A2 Vibe Creators LLC**

---

## Table of Contents

1. [Overview](#overview)
2. [The Problem](#the-problem)
3. [QUAD's Solution: Pluggable Triggers](#quads-solution-pluggable-triggers)
4. [Trigger Source Types](#trigger-source-types)
5. [Configuration Reference](#configuration-reference)
6. [Example Configurations](#example-configurations)
7. [Building Custom Triggers](#building-custom-triggers)
8. [Trigger Flow Diagram](#trigger-flow-diagram)

---

## Overview

Not every organization uses the same tools or workflows. Some use Jira, others use Azure DevOps. Some teams prefer Slack notifications, others watch specific email inboxes. QUAD's **Customizable Trigger System** allows organizations to configure how agents get triggered without changing agent code.

### Key Principle

```
+------------------------------------------------------------------+
|                   QUAD TRIGGER PHILOSOPHY                         |
+------------------------------------------------------------------+
|                                                                   |
|  AGENTS are TOOL-AGNOSTIC                                         |
|  =========================                                         |
|                                                                   |
|  Story Agent doesn't know or care WHERE the trigger came from.    |
|  It receives standardized input, produces standardized output.    |
|                                                                   |
|  +-----------------+     +------------------+     +-------------+ |
|  |  Jira Webhook   |---->|                  |---->|             | |
|  +-----------------+     |   QUAD Trigger   |     |   Story     | |
|  |  Email Monitor  |---->|   Adapter Layer  |---->|   Agent     | |
|  +-----------------+     |                  |     |             | |
|  |  Slack Message  |---->|  (normalizes     |     | (same code  | |
|  +-----------------+     |   all inputs)    |     |  for all)   | |
|  |  Azure DevOps   |---->|                  |---->|             | |
|  +-----------------+     +------------------+     +-------------+ |
|                                                                   |
|  Organizations configure WHICH triggers they want.                |
|  Agents remain unchanged.                                         |
|                                                                   |
+------------------------------------------------------------------+
```

---

## The Problem

Different organizations have different preferences:

| Company Type | Pain Point | Preferred Trigger |
|--------------|------------|-------------------|
| **Traditional Enterprise** | "We don't want to change Jira workflow" | Email from specific mailbox |
| **Startup** | "We live in Slack, not Jira" | Slack messages in #requirements |
| **Government** | "Everything must go through ServiceNow" | ServiceNow webhook |
| **Agency** | "Clients email requirements" | Email from client domains |
| **Hybrid Team** | "Some use Jira, some use Confluence" | Multiple sources simultaneously |

### Common Objections to Jira-Only Triggers

1. **"We don't want to add Jira plugins"** - Security policy restriction
2. **"Our BAs don't use Jira, they email"** - Workflow mismatch
3. **"We need email audit trail"** - Compliance requirement
4. **"Some stakeholders don't have Jira access"** - External contributors
5. **"We use ServiceNow/Monday/Asana, not Jira"** - Different tooling

---

## QUAD's Solution: Pluggable Triggers

QUAD implements a **Trigger Adapter Pattern** where:

1. **Trigger Sources** are external systems (Jira, Email, Slack, etc.)
2. **Trigger Adapters** convert source-specific events to standard format
3. **QUAD Runtime** receives standardized trigger events
4. **Agents** process triggers without knowing the source

### Architecture

```
+========================================================================+
||                    QUAD CUSTOMIZABLE TRIGGER SYSTEM                   ||
+========================================================================+
||                                                                        ||
||  TRIGGER SOURCES                    TRIGGER ADAPTERS                   ||
||  ================                   ================                   ||
||                                                                        ||
||  +---------------+                  +-------------------+              ||
||  | Jira Webhook  |----------------->| JiraTriggerAdapter|              ||
||  +---------------+                  +-------------------+              ||
||                                              |                         ||
||  +---------------+                  +-------------------+              ||
||  | Email Monitor |----------------->| EmailTriggerAdapter|             ||
||  | (IMAP/Graph)  |                  +-------------------+              ||
||  +---------------+                          |                          ||
||                                              |                          ||
||  +---------------+                  +-------------------+              ||
||  | Slack Events  |----------------->| SlackTriggerAdapter|             ||
||  +---------------+                  +-------------------+              ||
||                                              |                          ||
||  +---------------+                  +-------------------+              ||
||  | Azure DevOps  |----------------->| AzureDevOpsTriggerAdapter|       ||
||  +---------------+                  +-------------------+              ||
||                                              |                          ||
||  +---------------+                  +-------------------+              ||
||  | Confluence    |----------------->| ConfluenceTriggerAdapter|        ||
||  +---------------+                  +-------------------+              ||
||                                              |                          ||
||  +---------------+                  +-------------------+              ||
||  | GitHub Issues |----------------->| GitHubTriggerAdapter|            ||
||  +---------------+                  +-------------------+              ||
||                                              |                          ||
||  +---------------+                  +-------------------+              ||
||  | Custom API    |----------------->| CustomTriggerAdapter|            ||
||  +---------------+                  +-------------------+              ||
||                                              |                          ||
||                                              v                          ||
||                                 +------------------------+             ||
||                                 |    QUAD RUNTIME (QAR)  |             ||
||                                 |    =================== |             ||
||                                 |  Receives standardized |             ||
||                                 |  TriggerEvent objects  |             ||
||                                 +------------------------+             ||
||                                              |                          ||
||                                              v                          ||
||                                      +--------------+                   ||
||                                      |    AGENT     |                   ||
||                                      | Story Agent  |                   ||
||                                      | Dev Agent    |                   ||
||                                      | Test Agent   |                   ||
||                                      +--------------+                   ||
||                                                                        ||
+========================================================================+
```

---

## Trigger Source Types

### 1. Webhook Triggers (Push-based)

External system pushes events to QUAD endpoint.

```
+---------------------------------------------------------------+
|                    WEBHOOK TRIGGERS                            |
+---------------------------------------------------------------+
|                                                                |
|  SOURCE → QUAD WEBHOOK ENDPOINT → ADAPTER → AGENT              |
|                                                                |
|  Supported Sources:                                            |
|  ==================                                            |
|                                                                |
|  +------------------+  Event Types:                            |
|  | Jira             |  issue.created, issue.updated, sprint.*  |
|  +------------------+                                          |
|                                                                |
|  +------------------+  Event Types:                            |
|  | GitHub           |  issues.opened, pull_request.*, push     |
|  +------------------+                                          |
|                                                                |
|  +------------------+  Event Types:                            |
|  | Azure DevOps     |  workitem.created, workitem.updated      |
|  +------------------+                                          |
|                                                                |
|  +------------------+  Event Types:                            |
|  | Confluence       |  page.created, page.updated              |
|  +------------------+                                          |
|                                                                |
|  +------------------+  Event Types:                            |
|  | ServiceNow       |  incident.created, change.created        |
|  +------------------+                                          |
|                                                                |
|  +------------------+  Event Types:                            |
|  | Custom           |  Any custom event structure              |
|  +------------------+                                          |
|                                                                |
+---------------------------------------------------------------+
```

### 2. Email Triggers (Poll-based)

QUAD monitors email inbox and triggers on matching messages.

```
+---------------------------------------------------------------+
|                    EMAIL TRIGGERS                              |
+---------------------------------------------------------------+
|                                                                |
|  QUAD EMAIL MONITOR polls → parses email → matches rules       |
|                          → creates trigger event               |
|                                                                |
|  Email Matching Options:                                       |
|  =======================                                       |
|                                                                |
|  By Sender:                                                    |
|  +----------------------------------------------------------+ |
|  | Match specific email:   requirements@company.com          | |
|  | Match domain:           *@client.com                       | |
|  | Match group/DL:         product-requests@company.com       | |
|  | Match multiple:         [pm@*, ba@*, stakeholder@*]        | |
|  +----------------------------------------------------------+ |
|                                                                |
|  By Subject:                                                   |
|  +----------------------------------------------------------+ |
|  | Contains keyword:       "REQUIREMENT:" in subject          | |
|  | Regex pattern:          /\[REQ-\d+\]/                       | |
|  | Prefix:                 "[STORY]" at start                  | |
|  +----------------------------------------------------------+ |
|                                                                |
|  By Recipients:                                                |
|  +----------------------------------------------------------+ |
|  | Sent to specific inbox: requirements@company.com           | |
|  | CC'd to team:           dev-team@company.com               | |
|  +----------------------------------------------------------+ |
|                                                                |
|  By Labels/Folders:                                            |
|  +----------------------------------------------------------+ |
|  | Gmail label:            "Requirements/New"                 | |
|  | Outlook folder:         "Inbox/Requirements"               | |
|  +----------------------------------------------------------+ |
|                                                                |
|  Email Providers Supported:                                    |
|  +----------------------------------------------------------+ |
|  | Gmail         | OAuth2 or App Password (IMAP)              | |
|  | Microsoft 365 | Microsoft Graph API                        | |
|  | Exchange      | EWS (Exchange Web Services)                | |
|  | Any IMAP      | Standard IMAP connection                   | |
|  +----------------------------------------------------------+ |
|                                                                |
+---------------------------------------------------------------+
```

### 3. Chat/Messaging Triggers

QUAD monitors chat channels for trigger messages.

```
+---------------------------------------------------------------+
|                    CHAT TRIGGERS                               |
+---------------------------------------------------------------+
|                                                                |
|  Slack:                                                        |
|  ======                                                        |
|  +----------------------------------------------------------+ |
|  | Channel watch:     #requirements, #product-requests       | |
|  | @mention:          @quad-bot expand this story            | |
|  | Emoji reaction:    Add 📝 emoji to message                | |
|  | Slash command:     /quad-expand @story-description        | |
|  +----------------------------------------------------------+ |
|                                                                |
|  Microsoft Teams:                                              |
|  ================                                              |
|  +----------------------------------------------------------+ |
|  | Channel watch:     "Requirements" channel                  | |
|  | @mention:          @QUAD Bot please expand                 | |
|  | Adaptive card:     Button click in card                    | |
|  +----------------------------------------------------------+ |
|                                                                |
|  Discord:                                                      |
|  ========                                                      |
|  +----------------------------------------------------------+ |
|  | Channel watch:     #requirements                           | |
|  | Bot command:       !expand <description>                   | |
|  +----------------------------------------------------------+ |
|                                                                |
+---------------------------------------------------------------+
```

### 4. Scheduled Triggers (Time-based)

QUAD executes agents on schedule.

```
+---------------------------------------------------------------+
|                    SCHEDULED TRIGGERS                          |
+---------------------------------------------------------------+
|                                                                |
|  Cron-style scheduling:                                        |
|  ======================                                        |
|                                                                |
|  +----------------------------------------------------------+ |
|  | Daily 6 AM:        "0 6 * * *"    Re-process drafts       | |
|  | Every 30 min:      "*/30 * * * *" Check for stale items   | |
|  | Monday 9 AM:       "0 9 * * 1"    Sprint planning refresh | |
|  | First of month:    "0 0 1 * *"    Monthly report          | |
|  +----------------------------------------------------------+ |
|                                                                |
|  Query-based triggers:                                         |
|  =====================                                         |
|                                                                |
|  +----------------------------------------------------------+ |
|  | "Run for all stories WHERE status = 'Draft' AND age > 2d" | |
|  | "Run for all PRs WHERE review_pending > 24h"              | |
|  | "Run for all tests WHERE last_run > 7d"                   | |
|  +----------------------------------------------------------+ |
|                                                                |
+---------------------------------------------------------------+
```

### 5. Manual Triggers (Human-initiated)

Direct human invocation through UI/CLI/Chat.

```
+---------------------------------------------------------------+
|                    MANUAL TRIGGERS                             |
+---------------------------------------------------------------+
|                                                                |
|  IDE (VS Code, Cursor):                                        |
|  +----------------------------------------------------------+ |
|  | Right-click → "Expand with Story Agent"                   | |
|  | Keyboard: Cmd+Shift+E                                     | |
|  | Command Palette: "QUAD: Expand Story"                     | |
|  +----------------------------------------------------------+ |
|                                                                |
|  CLI:                                                          |
|  +----------------------------------------------------------+ |
|  | $ quad agent invoke story-agent --story-id=123            | |
|  | $ quad expand "As a user, I want to..."                   | |
|  +----------------------------------------------------------+ |
|                                                                |
|  Web Dashboard:                                                |
|  +----------------------------------------------------------+ |
|  | "Expand Story" button on story detail page                | |
|  | Bulk action: Select stories → "Expand All"                | |
|  +----------------------------------------------------------+ |
|                                                                |
|  Jira/Azure DevOps Button:                                     |
|  +----------------------------------------------------------+ |
|  | Custom button in issue view: "🤖 AI Expand"               | |
|  +----------------------------------------------------------+ |
|                                                                |
+---------------------------------------------------------------+
```

---

## Configuration Reference

### Master Trigger Configuration

```yaml
# quad.config.yaml
# ==============================================================================
# TRIGGER CONFIGURATION
# ==============================================================================

triggers:
  # ==========================================================================
  # GLOBAL SETTINGS
  # ==========================================================================
  global:
    default_adapter: jira              # Fallback adapter if not specified
    deduplication:
      enabled: true
      window_seconds: 300              # Ignore duplicate triggers within 5 min
    rate_limiting:
      max_triggers_per_minute: 60
      max_triggers_per_agent: 10

  # ==========================================================================
  # WEBHOOK TRIGGERS
  # ==========================================================================
  webhooks:
    enabled: true
    endpoint: /api/triggers/webhook    # Base endpoint for all webhooks
    secret_header: X-QUAD-Secret       # HMAC signature header

    # --------------------------------------------------------------------------
    # JIRA
    # --------------------------------------------------------------------------
    jira:
      enabled: true
      secret: ${JIRA_WEBHOOK_SECRET}
      events:
        story-created:
          event_type: issue.created
          filter:
            project: ["PROJ", "DEMO"]
            issueType: ["Story", "Epic"]
          target_agent: story-agent

        story-updated:
          event_type: issue.updated
          filter:
            project: ["PROJ"]
            fields_changed: [description, summary]
            status_not: [Done, Closed]
          target_agent: story-agent
          skip_if:
            labels: ["no-ai-expand"]

    # --------------------------------------------------------------------------
    # GITHUB
    # --------------------------------------------------------------------------
    github:
      enabled: true
      secret: ${GITHUB_WEBHOOK_SECRET}
      events:
        pr-opened:
          event_type: pull_request.opened
          filter:
            base_branch: [main, develop]
          target_agent: review-agent

        issue-created:
          event_type: issues.opened
          filter:
            labels: ["requirement", "story"]
          target_agent: story-agent

    # --------------------------------------------------------------------------
    # CONFLUENCE
    # --------------------------------------------------------------------------
    confluence:
      enabled: true
      secret: ${CONFLUENCE_WEBHOOK_SECRET}
      events:
        page-created:
          event_type: page.created
          filter:
            space: ["SPECS", "REQS"]
            label: ["requirement"]
          target_agent: story-agent

    # --------------------------------------------------------------------------
    # AZURE DEVOPS
    # --------------------------------------------------------------------------
    azure_devops:
      enabled: false                   # Enable if using Azure DevOps
      secret: ${AZURE_WEBHOOK_SECRET}
      events:
        workitem-created:
          event_type: workitem.created
          filter:
            workItemType: ["User Story", "Product Backlog Item"]
          target_agent: story-agent

    # --------------------------------------------------------------------------
    # SERVICENOW
    # --------------------------------------------------------------------------
    servicenow:
      enabled: false
      secret: ${SERVICENOW_WEBHOOK_SECRET}
      events:
        change-created:
          event_type: change.created
          target_agent: story-agent

  # ==========================================================================
  # EMAIL TRIGGERS
  # ==========================================================================
  email:
    enabled: true

    # Email provider configuration
    provider: gmail                    # gmail | microsoft365 | exchange | imap

    # Gmail-specific
    gmail:
      client_id: ${GMAIL_CLIENT_ID}
      client_secret: ${GMAIL_CLIENT_SECRET}
      refresh_token: ${GMAIL_REFRESH_TOKEN}

    # Microsoft 365-specific
    microsoft365:
      tenant_id: ${MS_TENANT_ID}
      client_id: ${MS_CLIENT_ID}
      client_secret: ${MS_CLIENT_SECRET}

    # Generic IMAP
    imap:
      host: imap.company.com
      port: 993
      username: ${IMAP_USERNAME}
      password: ${IMAP_PASSWORD}
      tls: true

    # Polling settings
    poll_interval_seconds: 60
    max_emails_per_poll: 50
    mark_as_read: true

    # --------------------------------------------------------------------------
    # EMAIL RULES
    # --------------------------------------------------------------------------
    rules:
      # Rule 1: Emails from PM team
      pm-requirements:
        enabled: true
        match:
          from:
            - "pm@company.com"
            - "*@product-team.company.com"
            - "requirements@company.com"
          subject_contains: ["requirement", "story", "feature"]
        target_agent: story-agent
        extract:
          story_text: body               # Use email body as story text
          priority: subject_tag          # Extract [HIGH], [LOW] from subject

      # Rule 2: Emails from specific client domain
      client-requests:
        enabled: true
        match:
          from:
            - "*@clientcompany.com"
            - "*@partnerfirm.com"
          to:
            - "requirements@company.com"
        target_agent: story-agent
        extract:
          story_text: body
          source: "external-client"
        auto_reply: true                 # Send confirmation reply
        auto_reply_template: "Thanks! Your requirement has been received."

      # Rule 3: Emails with specific prefix
      prefixed-requirements:
        enabled: true
        match:
          subject_regex: "^\\[REQ\\].*"  # Subject starts with [REQ]
        target_agent: story-agent

      # Rule 4: Emails to specific mailbox
      requirements-inbox:
        enabled: true
        match:
          to:
            - "new-requirements@company.com"
        target_agent: story-agent
        folder: "Requirements/New"       # Only check this folder

  # ==========================================================================
  # CHAT TRIGGERS (SLACK)
  # ==========================================================================
  slack:
    enabled: true
    bot_token: ${SLACK_BOT_TOKEN}
    app_token: ${SLACK_APP_TOKEN}
    signing_secret: ${SLACK_SIGNING_SECRET}

    rules:
      # Rule 1: Watch specific channel
      requirements-channel:
        type: channel_watch
        channels: ["#requirements", "#product-requests"]
        target_agent: story-agent
        extract:
          story_text: message_text
          user: slack_user

      # Rule 2: @mention the bot
      bot-mention:
        type: mention
        target_agent: story-agent
        keywords: ["expand", "enhance", "analyze"]

      # Rule 3: Slash command
      slash-command:
        type: slash_command
        command: /quad-expand
        target_agent: story-agent

      # Rule 4: Emoji reaction
      emoji-trigger:
        type: reaction
        emoji: ["memo", "pencil", "page_facing_up"]
        target_agent: story-agent

  # ==========================================================================
  # CHAT TRIGGERS (MICROSOFT TEAMS)
  # ==========================================================================
  teams:
    enabled: false
    app_id: ${TEAMS_APP_ID}
    app_password: ${TEAMS_APP_PASSWORD}

    rules:
      requirements-channel:
        type: channel_watch
        team: "Product Team"
        channel: "Requirements"
        target_agent: story-agent

  # ==========================================================================
  # SCHEDULED TRIGGERS
  # ==========================================================================
  scheduled:
    enabled: true

    jobs:
      # Daily re-process drafts
      daily-draft-review:
        schedule: "0 6 * * *"            # 6 AM daily
        target_agent: story-agent
        query: "status = 'Draft' AND updated < now() - interval '24 hours'"

      # Weekly sprint planning refresh
      weekly-sprint-prep:
        schedule: "0 9 * * 1"            # Monday 9 AM
        target_pipeline: estimation-pipeline
        query: "sprint = nextSprint() AND estimated = false"

      # Hourly stale PR check
      stale-pr-check:
        schedule: "0 * * * *"            # Every hour
        target_agent: review-agent
        query: "pr.created < now() - interval '48 hours' AND pr.status = 'open'"

  # ==========================================================================
  # MANUAL TRIGGERS
  # ==========================================================================
  manual:
    enabled: true

    # IDE integration
    ide:
      vscode:
        enabled: true
        context_menu: true
        keyboard_shortcut: "Cmd+Shift+E"
      cursor:
        enabled: true
        context_menu: true

    # CLI commands
    cli:
      enabled: true

    # Web dashboard
    web:
      enabled: true
      require_authentication: true

  # ==========================================================================
  # CUSTOM TRIGGERS
  # ==========================================================================
  custom:
    enabled: true

    # Custom webhook with custom payload format
    my-custom-source:
      endpoint: /api/triggers/custom/my-source
      secret: ${CUSTOM_WEBHOOK_SECRET}

      # Payload mapping (JSON path expressions)
      mapping:
        story_id: "$.data.ticket_id"
        story_text: "$.data.description"
        priority: "$.data.urgency"
        source: "'custom-source'"        # Literal value

      target_agent: story-agent
```

---

## Example Configurations

### Example 1: Traditional Enterprise (Email-Only)

**Scenario:** Government contractor that cannot install Jira plugins. BAs email requirements.

```yaml
# quad.config.yaml - Email-Only Trigger Configuration
triggers:
  webhooks:
    enabled: false                     # No webhook access

  email:
    enabled: true
    provider: exchange
    exchange:
      server: https://outlook.office365.com/EWS/Exchange.asmx
      username: quad-bot@agency.gov
      password: ${EXCHANGE_PASSWORD}

    poll_interval_seconds: 30

    rules:
      # BA team sends requirements
      ba-team-requirements:
        enabled: true
        match:
          from:
            - "*@requirements-team.agency.gov"
            - "ba-lead@agency.gov"
            - "senior-analyst@agency.gov"
          subject_contains: ["[REQ]", "[STORY]", "[REQUIREMENT]"]
        target_agent: story-agent

      # Stakeholders from specific divisions
      division-requests:
        enabled: true
        match:
          from:
            - "*@finance-division.agency.gov"
            - "*@hr-division.agency.gov"
          to:
            - "system-requests@agency.gov"
        target_agent: story-agent

      # External contractor requests (higher scrutiny)
      contractor-requests:
        enabled: true
        match:
          from:
            - "*@approved-contractor.com"
          to:
            - "requirements@agency.gov"
        target_agent: story-agent
        require_approval: true          # Human must approve before processing
        auto_reply: true
        auto_reply_template: |
          Your requirement has been received and is pending review.
          Reference: {{trigger_id}}

  slack:
    enabled: false

  scheduled:
    enabled: true
    jobs:
      daily-pending-review:
        schedule: "0 8 * * *"
        target_agent: story-agent
        query: "status = 'PendingReview' AND age > 2d"
```

### Example 2: Startup (Slack-First)

**Scenario:** Small startup where team lives in Slack. No formal ticket system.

```yaml
# quad.config.yaml - Slack-First Configuration
triggers:
  webhooks:
    enabled: false                     # No Jira

  email:
    enabled: false                     # Don't use email

  slack:
    enabled: true
    bot_token: ${SLACK_BOT_TOKEN}
    app_token: ${SLACK_APP_TOKEN}

    rules:
      # Watch the product channel
      product-channel:
        type: channel_watch
        channels: ["#product-ideas", "#feature-requests"]
        target_agent: story-agent
        min_message_length: 50         # Ignore short messages

      # @mention the bot to expand
      mention-expand:
        type: mention
        keywords: ["expand", "detail", "spec out"]
        target_agent: story-agent

      # Slash command for quick stories
      slash-story:
        type: slash_command
        command: /story
        target_agent: story-agent

      # 📝 emoji = "this should be a story"
      story-emoji:
        type: reaction
        emoji: ["memo", "spiral_note_pad"]
        target_agent: story-agent

  scheduled:
    enabled: true
    jobs:
      # Daily standup prep
      standup-prep:
        schedule: "0 9 * * 1-5"        # 9 AM weekdays
        slack_channel: "#daily-standup"
        message: "Good morning! Here's the sprint status..."
```

### Example 3: Hybrid Enterprise (Multiple Sources)

**Scenario:** Large company with multiple teams using different tools.

```yaml
# quad.config.yaml - Multi-Source Configuration
triggers:
  webhooks:
    enabled: true

    jira:
      enabled: true
      events:
        story-created:
          event_type: issue.created
          filter:
            project: ["PLATFORM", "MOBILE"]
          target_agent: story-agent

    azure_devops:
      enabled: true
      events:
        workitem-created:
          event_type: workitem.created
          filter:
            project: "EnterpriseApps"
          target_agent: story-agent

    github:
      enabled: true
      events:
        issue-created:
          event_type: issues.opened
          filter:
            repo: ["company/api", "company/web"]
            labels: ["requirement"]
          target_agent: story-agent

  email:
    enabled: true
    provider: microsoft365

    rules:
      # External stakeholder requests
      external-requests:
        enabled: true
        match:
          from:
            - "*@client1.com"
            - "*@partner2.com"
          to:
            - "requirements@company.com"
        target_agent: story-agent
        auto_create_jira: true         # Create Jira ticket from email

      # Executive requests (high priority)
      exec-requests:
        enabled: true
        match:
          from:
            - "ceo@company.com"
            - "cto@company.com"
            - "vp-*@company.com"
        target_agent: story-agent
        priority_override: "CRITICAL"

  slack:
    enabled: true
    rules:
      engineering-requests:
        type: channel_watch
        channels: ["#engineering-requests"]
        target_agent: story-agent

  teams:
    enabled: true
    rules:
      business-requirements:
        type: channel_watch
        team: "Business Unit"
        channel: "Requirements"
        target_agent: story-agent

  # Source priority (which trigger takes precedence for same item)
  priority_order:
    - jira                             # Jira is source of truth
    - azure_devops
    - github
    - email
    - slack
    - teams
```

---

## Building Custom Triggers

### Custom Trigger Adapter Interface

```typescript
// src/triggers/TriggerAdapter.ts

/**
 * Standard trigger event that all adapters must produce
 */
export interface TriggerEvent {
  // Identity
  triggerId: string;                   // Unique trigger ID
  timestamp: Date;                     // When trigger occurred
  source: TriggerSource;               // Where it came from

  // Agent routing
  targetAgent: string;                 // Which agent to invoke
  targetPipeline?: string;             // Or which pipeline

  // Payload
  data: {
    storyId?: string;                  // External ID if known
    storyText: string;                 // The requirement text
    priority?: Priority;
    labels?: string[];
    metadata?: Record<string, any>;
  };

  // Provenance
  rawPayload: any;                     // Original payload for audit
  invoker: string;                     // Who/what triggered (email, user, etc.)
}

export type TriggerSource =
  | 'jira'
  | 'github'
  | 'azure_devops'
  | 'confluence'
  | 'email'
  | 'slack'
  | 'teams'
  | 'scheduled'
  | 'manual'
  | 'custom';

/**
 * All trigger adapters must implement this interface
 */
export interface TriggerAdapter {
  // Identity
  readonly name: string;
  readonly source: TriggerSource;

  // Lifecycle
  initialize(config: TriggerConfig): Promise<void>;
  shutdown(): Promise<void>;

  // For webhook-based: parse incoming request
  parseWebhook?(req: Request): Promise<TriggerEvent | null>;

  // For poll-based: check for new items
  poll?(): Promise<TriggerEvent[]>;

  // Validation
  validateConfig(config: TriggerConfig): ValidationResult;
}
```

### Example: Custom Email Trigger Adapter

```typescript
// src/triggers/adapters/EmailTriggerAdapter.ts

import Imap from 'imap-simple';
import { simpleParser } from 'mailparser';

export class EmailTriggerAdapter implements TriggerAdapter {
  readonly name = 'email-trigger';
  readonly source: TriggerSource = 'email';

  private connection: Imap.ImapSimple | null = null;
  private config: EmailTriggerConfig;
  private rules: EmailRule[];

  async initialize(config: TriggerConfig): Promise<void> {
    this.config = config as EmailTriggerConfig;
    this.rules = this.config.rules;

    // Connect to email provider
    this.connection = await Imap.connect({
      imap: {
        host: this.config.imap.host,
        port: this.config.imap.port,
        user: this.config.imap.username,
        password: this.config.imap.password,
        tls: this.config.imap.tls,
      }
    });

    console.log(`[EmailTrigger] Connected to ${this.config.imap.host}`);
  }

  async poll(): Promise<TriggerEvent[]> {
    const events: TriggerEvent[] = [];

    await this.connection!.openBox('INBOX');

    // Search for unread emails
    const searchCriteria = ['UNSEEN'];
    const fetchOptions = { bodies: ['HEADER', 'TEXT'], markSeen: true };

    const messages = await this.connection!.search(searchCriteria, fetchOptions);

    for (const message of messages) {
      const parsed = await simpleParser(message.parts[1].body);

      // Check each rule
      for (const rule of this.rules) {
        if (this.matchesRule(parsed, rule)) {
          const event = this.createTriggerEvent(parsed, rule);
          events.push(event);
          break; // First matching rule wins
        }
      }
    }

    return events;
  }

  private matchesRule(email: ParsedMail, rule: EmailRule): boolean {
    const match = rule.match;

    // Check sender
    if (match.from) {
      const senderEmail = email.from?.value[0]?.address || '';
      const fromMatches = match.from.some(pattern =>
        this.matchPattern(senderEmail, pattern)
      );
      if (!fromMatches) return false;
    }

    // Check recipient
    if (match.to) {
      const recipients = email.to?.value.map(r => r.address) || [];
      const toMatches = match.to.some(pattern =>
        recipients.some(r => this.matchPattern(r!, pattern))
      );
      if (!toMatches) return false;
    }

    // Check subject
    if (match.subject_contains) {
      const subject = email.subject || '';
      const subjectMatches = match.subject_contains.some(keyword =>
        subject.toLowerCase().includes(keyword.toLowerCase())
      );
      if (!subjectMatches) return false;
    }

    // Check subject regex
    if (match.subject_regex) {
      const regex = new RegExp(match.subject_regex);
      if (!regex.test(email.subject || '')) return false;
    }

    return true;
  }

  private matchPattern(value: string, pattern: string): boolean {
    if (pattern.startsWith('*')) {
      // Wildcard domain match: *@domain.com
      const domain = pattern.substring(1);
      return value.endsWith(domain);
    }
    return value.toLowerCase() === pattern.toLowerCase();
  }

  private createTriggerEvent(email: ParsedMail, rule: EmailRule): TriggerEvent {
    return {
      triggerId: `email-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
      timestamp: new Date(),
      source: 'email',
      targetAgent: rule.target_agent,
      data: {
        storyText: email.text || email.html || '',
        priority: this.extractPriority(email.subject || ''),
        labels: ['from-email'],
        metadata: {
          from: email.from?.value[0]?.address,
          subject: email.subject,
          date: email.date,
        }
      },
      rawPayload: { headers: email.headers, subject: email.subject },
      invoker: email.from?.value[0]?.address || 'unknown',
    };
  }

  private extractPriority(subject: string): Priority {
    if (subject.includes('[CRITICAL]') || subject.includes('[URGENT]')) {
      return 'CRITICAL';
    }
    if (subject.includes('[HIGH]')) return 'HIGH';
    if (subject.includes('[LOW]')) return 'LOW';
    return 'MEDIUM';
  }

  async shutdown(): Promise<void> {
    if (this.connection) {
      await this.connection.end();
      console.log('[EmailTrigger] Disconnected');
    }
  }

  validateConfig(config: TriggerConfig): ValidationResult {
    const errors: string[] = [];
    const emailConfig = config as EmailTriggerConfig;

    if (!emailConfig.imap?.host) {
      errors.push('IMAP host is required');
    }
    if (!emailConfig.rules || emailConfig.rules.length === 0) {
      errors.push('At least one email rule is required');
    }

    return { valid: errors.length === 0, errors };
  }
}
```

### Registering Custom Adapters

```typescript
// src/triggers/TriggerRegistry.ts

export class TriggerRegistry {
  private adapters: Map<TriggerSource, TriggerAdapter> = new Map();

  register(adapter: TriggerAdapter): void {
    this.adapters.set(adapter.source, adapter);
    console.log(`[TriggerRegistry] Registered adapter: ${adapter.name}`);
  }

  get(source: TriggerSource): TriggerAdapter | undefined {
    return this.adapters.get(source);
  }
}

// Initialize with all adapters
const registry = new TriggerRegistry();
registry.register(new JiraTriggerAdapter());
registry.register(new GitHubTriggerAdapter());
registry.register(new EmailTriggerAdapter());
registry.register(new SlackTriggerAdapter());
registry.register(new AzureDevOpsTriggerAdapter());
registry.register(new ConfluenceTriggerAdapter());
registry.register(new ScheduledTriggerAdapter());
// Add custom adapters
registry.register(new CustomTriggerAdapter());
```

---

## Trigger Flow Diagram

### Complete Flow: Email → Agent

```
+========================================================================+
||              EMAIL TRIGGER FLOW (Complete Example)                    ||
+========================================================================+
||                                                                        ||
||  1. PM sends email                                                    ||
||     From: pm@company.com                                              ||
||     To: requirements@company.com                                      ||
||     Subject: [REQ] User login with SSO                               ||
||     Body: "As a user, I want to login with company SSO..."           ||
||                                                                        ||
||            │                                                           ||
||            ▼                                                           ||
||                                                                        ||
||  2. Email Monitor polls inbox (every 60 seconds)                      ||
||     ┌──────────────────────────────────────────────────┐              ||
||     │ EmailTriggerAdapter.poll()                        │              ||
||     │ - Connect to IMAP                                │              ||
||     │ - Search UNSEEN emails                           │              ||
||     │ - Found 1 new email                              │              ||
||     └──────────────────────────────────────────────────┘              ||
||            │                                                           ||
||            ▼                                                           ||
||                                                                        ||
||  3. Match against rules                                               ||
||     ┌──────────────────────────────────────────────────┐              ||
||     │ Rule: pm-requirements                             │              ||
||     │ Match:                                            │              ||
||     │   from: ["pm@company.com"] ✓                     │              ||
||     │   subject_contains: ["[REQ]"] ✓                  │              ||
||     │ Target: story-agent                               │              ||
||     │ MATCH!                                            │              ||
||     └──────────────────────────────────────────────────┘              ||
||            │                                                           ||
||            ▼                                                           ||
||                                                                        ||
||  4. Create standardized TriggerEvent                                  ||
||     ┌──────────────────────────────────────────────────┐              ||
||     │ TriggerEvent {                                    │              ||
||     │   triggerId: "email-1735657200000-abc123",       │              ||
||     │   timestamp: "2025-12-31T10:00:00Z",             │              ||
||     │   source: "email",                                │              ||
||     │   targetAgent: "story-agent",                    │              ||
||     │   data: {                                         │              ||
||     │     storyText: "As a user, I want to...",        │              ||
||     │     priority: "MEDIUM",                          │              ||
||     │     metadata: {                                   │              ||
||     │       from: "pm@company.com",                    │              ||
||     │       subject: "[REQ] User login with SSO"       │              ||
||     │     }                                             │              ||
||     │   },                                              │              ||
||     │   invoker: "pm@company.com"                      │              ||
||     │ }                                                 │              ||
||     └──────────────────────────────────────────────────┘              ||
||            │                                                           ||
||            ▼                                                           ||
||                                                                        ||
||  5. Send to QUAD Agent Runtime                                        ||
||     ┌──────────────────────────────────────────────────┐              ||
||     │ QAR.handleTrigger(event)                          │              ||
||     │ - Validate trigger event                         │              ||
||     │ - Check deduplication (not a duplicate)          │              ||
||     │ - Check rate limits (under limit)                │              ||
||     │ - Route to target agent                          │              ||
||     └──────────────────────────────────────────────────┘              ||
||            │                                                           ||
||            ▼                                                           ||
||                                                                        ||
||  6. Invoke Story Agent                                                ||
||     ┌──────────────────────────────────────────────────┐              ||
||     │ runtime.invoke("story-agent", {                   │              ||
||     │   storyText: "As a user, I want to...",          │              ||
||     │   priority: "MEDIUM",                             │              ||
||     │   invocationMethod: "AUTO",                      │              ||
||     │   triggerSource: "email",                        │              ||
||     │   invoker: "pm@company.com"                      │              ||
||     │ })                                                │              ||
||     └──────────────────────────────────────────────────┘              ||
||            │                                                           ||
||            ▼                                                           ||
||                                                                        ||
||  7. Story Agent processes (same as any other trigger)                 ||
||     ┌──────────────────────────────────────────────────┐              ||
||     │ - Read project context                           │              ||
||     │ - Call Gemini for expansion                      │              ||
||     │ - Generate user stories, acceptance criteria     │              ||
||     │ - Create Jira tickets (via Jira MCP)            │              ||
||     │ - Create Confluence page (via Confluence MCP)   │              ||
||     └──────────────────────────────────────────────────┘              ||
||            │                                                           ||
||            ▼                                                           ||
||                                                                        ||
||  8. Output (same format regardless of trigger source)                 ||
||     ┌──────────────────────────────────────────────────┐              ||
||     │ AgentOutput {                                     │              ||
||     │   success: true,                                  │              ||
||     │   data: {                                         │              ||
||     │     stories_created: ["PROJ-101", "PROJ-102"],   │              ||
||     │     confluence_link: "wiki/PROJ/specs/..."       │              ||
||     │   }                                               │              ||
||     │ }                                                 │              ||
||     └──────────────────────────────────────────────────┘              ||
||            │                                                           ||
||            ▼                                                           ||
||                                                                        ||
||  9. (Optional) Reply to original email                                ||
||     ┌──────────────────────────────────────────────────┐              ||
||     │ To: pm@company.com                                │              ||
||     │ Subject: Re: [REQ] User login with SSO           │              ||
||     │ Body:                                             │              ||
||     │   Your requirement has been processed!           │              ||
||     │   Created stories: PROJ-101, PROJ-102            │              ||
||     │   View specs: wiki/PROJ/specs/...                │              ||
||     └──────────────────────────────────────────────────┘              ||
||                                                                        ||
+========================================================================+
```

---

## Summary

| Trigger Type | Push/Poll | Best For |
|--------------|-----------|----------|
| **Jira Webhook** | Push | Teams using Jira natively |
| **GitHub Webhook** | Push | Developer-centric teams |
| **Azure DevOps Webhook** | Push | Microsoft shops |
| **Email Monitor** | Poll | Traditional enterprises, external stakeholders |
| **Slack Bot** | Push | Startup/agile teams |
| **Teams Bot** | Push | Microsoft 365 organizations |
| **Scheduled** | Poll | Batch processing, stale item cleanup |
| **Manual** | N/A | Direct human invocation |
| **Custom** | Either | Integration with any system |

### Key Principles

1. **Agents don't care about trigger source** - They receive standardized input
2. **Organizations configure their preferred triggers** - No code changes
3. **Multiple triggers can coexist** - Jira + Email + Slack simultaneously
4. **Deduplication prevents double-processing** - Same requirement from multiple sources = one execution
5. **Full audit trail** - Every trigger is logged with source and invoker

---

**Author:** QUAD Methodology Team
**Version:** 1.0.0
**Last Updated:** December 31, 2025
**© 2025 Suman Addanke / A2 Vibe Creators LLC**
