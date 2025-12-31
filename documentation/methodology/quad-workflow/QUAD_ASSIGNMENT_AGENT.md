# QUAD Assignment Agent

**Intelligent Task Assignment with Learning from Human Behavior**

Part of QUAD™ (Quick Unified Agentic Development) Methodology
© 2025 Suman Addanke / A2 Vibe Creators LLC

---

## Table of Contents

1. [Overview](#overview)
2. [Assignment Flow](#assignment-flow)
3. [Trigger Sources (Complete Reference)](#trigger-sources-complete-reference)
4. [Circle Detection Methods](#circle-detection-methods)
5. [Within-Circle Assignment](#within-circle-assignment)
6. [Learning Mechanism (Detailed)](#learning-mechanism-detailed)
7. [QUAD Web Application Integration](#quad-web-application-integration)
8. [Configuration Reference](#configuration-reference)

---

## Overview

The Assignment Agent is responsible for:
1. **Detecting which Circle** a sub-task belongs to
2. **Assigning to specific person** within that circle
3. **Learning from reassignments** to improve over time

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    ASSIGNMENT AGENT OVERVIEW                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   SOURCE OF TRUTH (Requirement)                                              │
│          │                                                                   │
│          ▼                                                                   │
│   ┌──────────────┐                                                          │
│   │ Story Agent  │  Creates story with sub-tasks                            │
│   └──────────────┘                                                          │
│          │                                                                   │
│          │ event: "story.expanded"                                          │
│          ▼                                                                   │
│   ┌──────────────────────────────────────────────────────────────────────┐  │
│   │                     ASSIGNMENT AGENT                                  │  │
│   │                                                                       │  │
│   │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐               │  │
│   │  │   DETECT    │    │   ASSIGN    │    │   LEARN     │               │  │
│   │  │   CIRCLE    │ ──►│   PERSON    │ ──►│   FROM      │               │  │
│   │  │             │    │             │    │   FEEDBACK  │               │  │
│   │  └─────────────┘    └─────────────┘    └─────────────┘               │  │
│   │                                                                       │  │
│   └──────────────────────────────────────────────────────────────────────┘  │
│          │                                                                   │
│          ▼                                                                   │
│   ┌──────────────────────────────────────────────────────────────────────┐  │
│   │  QUAD WEB APP: Human reviews & approves (HYBRID mode)                 │  │
│   └──────────────────────────────────────────────────────────────────────┘  │
│          │                                                                   │
│          ▼                                                                   │
│   Sub-tasks assigned in Jira/GitHub/Azure DevOps                            │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Assignment Flow

### Complete Flow with All Steps

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    ASSIGNMENT FLOW (Detailed)                                │
├─────────────────────────────────────────────────────────────────────────────┤

STEP 1: TRIGGER RECEIVED
════════════════════════════════════════════════════════════════════════════════

Trigger sources (see full list below):
  • Jira webhook: issue.created
  • Slack message: #requirements channel
  • Email: from pm@company.com
  • Story Agent event: story.expanded

Trigger payload contains:
  {
    source: "story-agent",
    event: "story.expanded",
    payload: {
      story_id: "RETAIL-456",
      story_title: "User Wishlist Feature",
      sub_tasks: [
        { id: "ST-1", title: "Design DB schema for wishlists" },
        { id: "ST-2", title: "Build React wishlist component" },
        { id: "ST-3", title: "Create REST API endpoints" },
        { id: "ST-4", title: "Write integration tests" },
        { id: "ST-5", title: "Deploy to staging environment" }
      ]
    }
  }


STEP 2: DETECT CIRCLE FOR EACH SUB-TASK
════════════════════════════════════════════════════════════════════════════════

For each sub_task, Assignment Agent determines circle:

┌──────────────────────────────────────────────────────────────────────────────┐
│ Sub-Task                      │ Detection Method │ Circle │ Confidence      │
│──────────────────────────────────────────────────────────────────────────────│
│ "Design DB schema..."         │ AI analyzed      │   1    │ 94%             │
│ "Build React wishlist..."     │ AI analyzed      │   2    │ 91%             │
│ "Create REST API..."          │ AI analyzed      │   2    │ 88%             │
│ "Write integration tests..."  │ AI analyzed      │   3    │ 96%             │
│ "Deploy to staging..."        │ AI analyzed      │   4    │ 97%             │
└──────────────────────────────────────────────────────────────────────────────┘


STEP 3: ASSIGN PERSON WITHIN CIRCLE
════════════════════════════════════════════════════════════════════════════════

For each sub_task, select person from circle members:

Circle 1 (Management): [Alice, Frank]
Circle 2 (Development): [Bob, Carol, Greg]
Circle 3 (QA): [Dave, Helen]
Circle 4 (Infrastructure): [Eve, Ivan]

Assignment Logic:
┌──────────────────────────────────────────────────────────────────────────────┐
│ Sub-Task          │ Circle │ Method           │ Selected │ Why              │
│──────────────────────────────────────────────────────────────────────────────│
│ Design DB schema  │   1    │ Skill match      │ Alice    │ DB skill: 0.9    │
│ Build React       │   2    │ Round-robin      │ Bob      │ Next in rotation │
│ Create REST API   │   2    │ Learned affinity │ Carol    │ API affinity +3  │
│ Write tests       │   3    │ Round-robin      │ Dave     │ Next in rotation │
│ Deploy staging    │   4    │ Round-robin      │ Eve      │ Next in rotation │
└──────────────────────────────────────────────────────────────────────────────┘


STEP 4: PRESENT FOR APPROVAL (HYBRID MODE)
════════════════════════════════════════════════════════════════════════════════

QUAD Web App shows:

┌──────────────────────────────────────────────────────────────────────────────┐
│  ASSIGNMENT REVIEW                                    [Approve All] [Cancel] │
│──────────────────────────────────────────────────────────────────────────────│
│                                                                              │
│  Story: "User Wishlist Feature" [RETAIL-456]                                │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │ ☑ ST-1: Design DB schema       → Circle 1 → @Alice (94% conf) [Edit ▼]│ │
│  │ ☑ ST-2: Build React wishlist   → Circle 2 → @Bob   (91% conf) [Edit ▼]│ │
│  │ ☑ ST-3: Create REST API        → Circle 2 → @Carol (88% conf) [Edit ▼]│ │
│  │ ☑ ST-4: Write integration tests→ Circle 3 → @Dave  (96% conf) [Edit ▼]│ │
│  │ ☑ ST-5: Deploy to staging      → Circle 4 → @Eve   (97% conf) [Edit ▼]│ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
│  💡 Carol suggested for API task based on 3 previous reassignments          │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘


STEP 5: EXECUTE ASSIGNMENT
════════════════════════════════════════════════════════════════════════════════

After approval, Assignment Agent:
  1. Updates Jira/GitHub with assignee for each sub-task
  2. Notifies assignees via Slack/Email
  3. Records assignment for future learning


STEP 6: MONITOR FOR REASSIGNMENTS
════════════════════════════════════════════════════════════════════════════════

Assignment Agent watches for:
  • Jira webhook: issue.updated (assignee changed)
  • GitHub: issue reassigned
  • Manual changes in any tool

When reassignment detected → LEARN (see Learning Mechanism section)

└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Trigger Sources (Complete Reference)

### All Trigger Options with Context

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    TRIGGER SOURCES (COMPLETE)                                │
├─────────────────────────────────────────────────────────────────────────────┤

1. SLACK TRIGGERS
═══════════════════════════════════════════════════════════════════════════════

┌──────────────────────────────────────────────────────────────────────────────┐
│ Trigger Type         │ Context                │ Target Agent │ Example      │
│──────────────────────────────────────────────────────────────────────────────│
│ CHANNEL MESSAGE      │ Specific channel       │ Story Agent  │ #requirements│
│ CHANNEL MESSAGE      │ Any public channel     │ Story Agent  │ *            │
│ CHANNEL MESSAGE      │ Private channel        │ Story Agent  │ #core-team   │
│──────────────────────────────────────────────────────────────────────────────│
│ DIRECT MESSAGE       │ From specific person   │ Any agent    │ @PM-John     │
│ DIRECT MESSAGE       │ From any person        │ Any agent    │ *            │
│──────────────────────────────────────────────────────────────────────────────│
│ THREAD REPLY         │ In specific thread     │ Story Agent  │ Thread ID    │
│ THREAD REPLY         │ Any thread             │ Story Agent  │ *            │
│──────────────────────────────────────────────────────────────────────────────│
│ MENTION              │ @QUAD mentioned        │ Route by cmd │ @QUAD expand │
│ MENTION              │ @StoryAgent mentioned  │ Story Agent  │ @StoryAgent  │
│──────────────────────────────────────────────────────────────────────────────│
│ EMOJI REACTION       │ Specific emoji         │ Custom       │ :rocket:     │
│ EMOJI REACTION       │ On specific channel    │ Custom       │ :approve:    │
│──────────────────────────────────────────────────────────────────────────────│
│ FILE SHARED          │ In specific channel    │ Doc Agent    │ #docs        │
│ FILE SHARED          │ File type filter       │ Doc Agent    │ *.pdf, *.md  │
└──────────────────────────────────────────────────────────────────────────────┘

Configuration Example:
```yaml
slack:
  triggers:
    # Monitor specific channel for requirements
    requirements-channel:
      type: CHANNEL_MESSAGE
      channel: "#requirements"
      filter:
        contains_keywords: [requirement, story, feature, need]
      target_agent: story-agent
      context:
        project: auto-detect  # From channel topic or message
        priority: P2          # Default priority

    # Monitor PM direct messages
    pm-directs:
      type: DIRECT_MESSAGE
      from:
        - "@john.pm"
        - "@sarah.pm"
      target_agent: story-agent
      context:
        source: "PM Direct"
        priority: P1

    # React to approve emoji
    emoji-approval:
      type: EMOJI_REACTION
      emoji: ":white_check_mark:"
      channel: "#pr-reviews"
      target_agent: deploy-agent
      context:
        action: "approve-and-merge"

    # Any mention of @QUAD bot
    quad-mention:
      type: MENTION
      mention: "@QUAD"
      target_agent: router  # Routes based on command
```


2. EMAIL TRIGGERS
═══════════════════════════════════════════════════════════════════════════════

┌──────────────────────────────────────────────────────────────────────────────┐
│ Trigger Type         │ Context                │ Target Agent │ Example      │
│──────────────────────────────────────────────────────────────────────────────│
│ FROM SPECIFIC PERSON │ Exact email            │ Story Agent  │ pm@company   │
│ FROM DOMAIN          │ Wildcard domain        │ Story Agent  │ *@client.com │
│ FROM GROUP           │ Distribution list      │ Story Agent  │ pms@company  │
│──────────────────────────────────────────────────────────────────────────────│
│ TO SPECIFIC ADDRESS  │ Sent to this inbox     │ Any agent    │ req@company  │
│ TO GROUP             │ Sent to group          │ Any agent    │ dev@company  │
│ CC/BCC               │ Copied to address      │ Any agent    │ audit@       │
│──────────────────────────────────────────────────────────────────────────────│
│ SUBJECT CONTAINS     │ Keywords in subject    │ Story Agent  │ "REQ:", "CR:"│
│ SUBJECT PATTERN      │ Regex pattern          │ Story Agent  │ "^REQ-\d+"   │
│──────────────────────────────────────────────────────────────────────────────│
│ BODY CONTAINS        │ Keywords in body       │ Story Agent  │ "Please impl"│
│ ATTACHMENT TYPE      │ File type attached     │ Doc Agent    │ *.pdf, *.doc │
│ ATTACHMENT NAME      │ File name pattern      │ Doc Agent    │ "spec_*.pdf" │
│──────────────────────────────────────────────────────────────────────────────│
│ LABEL/FOLDER         │ Gmail label or folder  │ Any agent    │ "Inbox/Reqs" │
│ UNREAD ONLY          │ Only unread emails     │ Any agent    │ true/false   │
│ THREAD               │ Part of specific thread│ Same agent   │ Thread ID    │
└──────────────────────────────────────────────────────────────────────────────┘

Configuration Example:
```yaml
email:
  connection:
    type: IMAP  # or MS_GRAPH for Office 365
    host: imap.company.com
    credentials: $EMAIL_CREDENTIALS

  triggers:
    # From any PM in the company
    pm-requirements:
      type: FROM_GROUP
      group: "pm-team@company.com"
      subject_contains: ["requirement", "story", "feature"]
      target_agent: story-agent
      context:
        source: "PM Email"
        priority: auto-detect  # Parse from subject/body

    # From client domain
    client-requests:
      type: FROM_DOMAIN
      domain: "*.bigclient.com"
      target_agent: story-agent
      context:
        source: "Client Request"
        priority: P1
        notify: ["@pm-lead", "#client-requests"]

    # Emails to specific requirements inbox
    requirements-inbox:
      type: TO_ADDRESS
      address: "requirements@company.com"
      target_agent: story-agent
      context:
        auto_respond: true  # Send "We received your request"

    # Attachments containing specs
    spec-documents:
      type: ATTACHMENT_TYPE
      patterns: ["*.pdf", "*.docx"]
      attachment_name_contains: ["spec", "requirement", "prd"]
      target_agent: doc-agent
      context:
        action: "extract-and-create-stories"

    # Specific folder/label in Gmail/Outlook
    inbox-requirements-folder:
      type: LABEL
      label: "Inbox/Requirements"  # Gmail label or Outlook folder
      target_agent: story-agent
      context:
        mark_as_read: true
```


3. JIRA TRIGGERS
═══════════════════════════════════════════════════════════════════════════════

┌──────────────────────────────────────────────────────────────────────────────┐
│ Trigger Type         │ Context                │ Target Agent │ Example      │
│──────────────────────────────────────────────────────────────────────────────│
│ ISSUE CREATED        │ New issue              │ Story Agent  │ type: Story  │
│ ISSUE UPDATED        │ Issue modified         │ Story Agent  │ desc changed │
│ ISSUE TRANSITIONED   │ Status changed         │ Assignment   │ To: Ready    │
│──────────────────────────────────────────────────────────────────────────────│
│ ASSIGNEE CHANGED     │ Reassignment           │ Learn Agent  │ A → B        │
│ COMMENT ADDED        │ New comment            │ Any agent    │ @QUAD expand │
│ ATTACHMENT ADDED     │ File attached          │ Doc Agent    │ *.pdf        │
│──────────────────────────────────────────────────────────────────────────────│
│ SPRINT STARTED       │ Sprint begins          │ Assignment   │ Sprint 5     │
│ SPRINT ENDED         │ Sprint ends            │ Report Agent │ Sprint 5     │
│──────────────────────────────────────────────────────────────────────────────│
│ PROJECT SPECIFIC     │ Only this project      │ Any agent    │ RETAIL       │
│ ISSUE TYPE           │ Story, Bug, Task       │ Any agent    │ Story only   │
│ LABEL ADDED          │ Specific label         │ Any agent    │ "needs-ai"   │
└──────────────────────────────────────────────────────────────────────────────┘

Configuration Example:
```yaml
jira:
  webhook_url: "/api/webhooks/jira"

  triggers:
    # New story created
    story-created:
      event: issue.created
      filter:
        project: ["RETAIL", "PLATFORM"]
        issueType: ["Story", "Epic"]
      target_agent: story-agent
      context:
        action: "expand-story"

    # Issue transitioned to "Ready for Dev"
    ready-for-dev:
      event: issue.transitioned
      filter:
        to_status: "Ready for Dev"
      target_agent: assignment-agent
      context:
        action: "assign-to-circles"

    # Assignee changed (for learning)
    reassignment-detected:
      event: issue.updated
      filter:
        field_changed: "assignee"
      target_agent: learning-agent
      context:
        action: "record-reassignment"

    # Comment with @QUAD mention
    quad-comment:
      event: comment.created
      filter:
        body_contains: "@QUAD"
      target_agent: router
      context:
        action: "parse-command"
```


4. GITHUB TRIGGERS
═══════════════════════════════════════════════════════════════════════════════

┌──────────────────────────────────────────────────────────────────────────────┐
│ Trigger Type         │ Context                │ Target Agent │ Example      │
│──────────────────────────────────────────────────────────────────────────────│
│ PR OPENED            │ New pull request       │ Review Agent │ To main      │
│ PR UPDATED           │ New commits pushed     │ Review Agent │ Re-review    │
│ PR REVIEW            │ Review submitted       │ Deploy Agent │ Approved     │
│ PR MERGED            │ PR merged              │ Deploy Agent │ To main      │
│──────────────────────────────────────────────────────────────────────────────│
│ ISSUE CREATED        │ New issue              │ Story Agent  │ Bug report   │
│ ISSUE LABELED        │ Label added            │ Any agent    │ "needs-triage│
│ ISSUE ASSIGNED       │ Assignment changed     │ Learn Agent  │ A → B        │
│──────────────────────────────────────────────────────────────────────────────│
│ PUSH                 │ Code pushed            │ Build Agent  │ To develop   │
│ PUSH TO BRANCH       │ Specific branch        │ Deploy Agent │ To main      │
│──────────────────────────────────────────────────────────────────────────────│
│ DISCUSSION           │ Discussions feature    │ Doc Agent    │ RFC created  │
│ RELEASE              │ Release created        │ Deploy Agent │ v1.2.0       │
│ WORKFLOW RUN         │ CI/CD workflow         │ Monitor Agent│ Failed       │
└──────────────────────────────────────────────────────────────────────────────┘


5. MICROSOFT TEAMS TRIGGERS
═══════════════════════════════════════════════════════════════════════════════

┌──────────────────────────────────────────────────────────────────────────────┐
│ Trigger Type         │ Context                │ Target Agent │ Example      │
│──────────────────────────────────────────────────────────────────────────────│
│ CHANNEL MESSAGE      │ Specific channel       │ Story Agent  │ Requirements │
│ CHAT MESSAGE         │ 1:1 or group chat      │ Any agent    │ From PM      │
│ @MENTION             │ Bot mentioned          │ Router       │ @QUAD expand │
│ ADAPTIVE CARD        │ Card button clicked    │ Any agent    │ "Approve"    │
│ FILE SHARED          │ In channel             │ Doc Agent    │ *.pdf        │
└──────────────────────────────────────────────────────────────────────────────┘


6. SCHEDULED TRIGGERS (CRON)
═══════════════════════════════════════════════════════════════════════════════

┌──────────────────────────────────────────────────────────────────────────────┐
│ Trigger Type         │ Context                │ Target Agent │ Example      │
│──────────────────────────────────────────────────────────────────────────────│
│ DAILY                │ Every day at time      │ Report Agent │ 6:00 AM      │
│ WEEKLY               │ Every week on day      │ Review Agent │ Mon 9:00 AM  │
│ CUSTOM CRON          │ Cron expression        │ Any agent    │ */15 * * * * │
│──────────────────────────────────────────────────────────────────────────────│
│ STALE CHECK          │ Find stale items       │ Reminder Agt │ > 3 days old │
│ SPRINT START         │ When sprint begins     │ Assignment   │ Auto-assign  │
│ SPRINT END           │ Before sprint ends     │ Report Agent │ Generate rpt │
└──────────────────────────────────────────────────────────────────────────────┘

Configuration Example:
```yaml
scheduled:
  triggers:
    # Daily standup reminder
    daily-standup:
      cron: "0 9 * * 1-5"  # 9 AM Mon-Fri
      target_agent: reminder-agent
      context:
        action: "send-standup-reminder"
        channel: "#daily-standup"

    # Weekly stale story check
    stale-check:
      cron: "0 10 * * MON"  # 10 AM Monday
      target_agent: cleanup-agent
      context:
        action: "find-stale-stories"
        threshold_days: 7
        notify: ["@pm-lead"]

    # Re-assign unassigned tasks every 4 hours
    unassigned-check:
      cron: "0 */4 * * *"  # Every 4 hours
      target_agent: assignment-agent
      context:
        action: "assign-unassigned"
        filter: "status = 'Ready' AND assignee IS NULL"
```


7. MANUAL TRIGGERS
═══════════════════════════════════════════════════════════════════════════════

┌──────────────────────────────────────────────────────────────────────────────┐
│ Trigger Type         │ Context                │ Target Agent │ Example      │
│──────────────────────────────────────────────────────────────────────────────│
│ CLI COMMAND          │ Terminal               │ Any agent    │ quad invoke  │
│ IDE RIGHT-CLICK      │ VS Code context menu   │ Any agent    │ Expand story │
│ QUAD WEB APP         │ Button click           │ Any agent    │ "Assign All" │
│ KEYBOARD SHORTCUT    │ IDE hotkey             │ Any agent    │ Cmd+Shift+Q  │
│ CHAT COMMAND         │ Claude/Copilot         │ Any agent    │ /quad expand │
└──────────────────────────────────────────────────────────────────────────────┘

└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Circle Detection Methods

### All Options with Configuration

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CIRCLE DETECTION METHODS                                  │
├─────────────────────────────────────────────────────────────────────────────┤

METHOD 1: RULE-BASED (Simple, Fast)
═══════════════════════════════════════════════════════════════════════════════

How it works:
  1. Define keyword → circle mappings
  2. Scan sub-task title/description for keywords
  3. First match wins (or weighted scoring)

```yaml
circle_detection:
  method: RULE_BASED
  rules:
    circle_1:  # Management
      keywords: [database, schema, migration, requirement, spec, design]
      weight: 1.0
    circle_2:  # Development
      keywords: [UI, frontend, React, Angular, Vue, backend, API, REST, service]
      weight: 1.0
    circle_3:  # QA
      keywords: [test, QA, validation, verify, check, bug, defect]
      weight: 1.0
    circle_4:  # Infrastructure
      keywords: [deploy, kubernetes, docker, infra, CI, CD, pipeline, monitor]
      weight: 1.0

  fallback: circle_2  # Default if no match
```

Pros: Fast, predictable, easy to debug
Cons: Misses nuanced tasks, requires maintenance


METHOD 2: AI-BASED (Intelligent, Recommended)                          DEFAULT
═══════════════════════════════════════════════════════════════════════════════

How it works:
  1. Send sub-task to AI (Gemini/Claude/GPT)
  2. AI classifies based on understanding, not just keywords
  3. Returns circle + confidence score

```yaml
circle_detection:
  method: AI_BASED  # DEFAULT
  ai_provider: gemini  # or openai, anthropic

  prompt_template: |
    You are a QUAD methodology expert. Classify this sub-task into one of 4 circles:

    Circle 1 (Management): BA work, requirements, specifications, database design
    Circle 2 (Development): UI code, API code, frontend, backend implementation
    Circle 3 (QA): Testing, validation, quality assurance, bug verification
    Circle 4 (Infrastructure): Deployment, CI/CD, monitoring, operations

    Sub-task: "{sub_task_title}"
    Description: "{sub_task_description}"

    Respond with JSON:
    {
      "circle": 1-4,
      "confidence": 0.0-1.0,
      "reasoning": "brief explanation"
    }

  min_confidence: 0.7  # Below this, ask human
  fallback: RULE_BASED  # If AI fails
```

Pros: Understands context, handles edge cases
Cons: Slower, costs API calls, may need tuning


METHOD 3: EXPLICIT TAGS (Pre-labeled by Story Agent)
═══════════════════════════════════════════════════════════════════════════════

How it works:
  1. Story Agent adds circle hint when creating sub-tasks
  2. Assignment Agent just reads the hint
  3. No additional detection needed

```yaml
circle_detection:
  method: EXPLICIT_TAGS
  tag_field: "circle"  # Field name in sub-task

  # Story Agent config to add tags
  story_agent:
    add_circle_hints: true
    circle_hint_field: "circle"
```

Example sub-task from Story Agent:
```json
{
  "title": "Build React wishlist component",
  "circle": 2,
  "circle_confidence": 0.95
}
```

Pros: No duplicate processing, consistent
Cons: Requires Story Agent to be accurate

└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Within-Circle Assignment

### All Options with Configuration

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    WITHIN-CIRCLE ASSIGNMENT METHODS                          │
├─────────────────────────────────────────────────────────────────────────────┤

METHOD 1: ROUND-ROBIN (Simple, Fair)                                   DEFAULT
═══════════════════════════════════════════════════════════════════════════════

How it works:
  1. Maintain pointer to "next person" in each circle
  2. Assign to next person, advance pointer
  3. Wrap around when end reached

```yaml
within_circle:
  method: ROUND_ROBIN  # DEFAULT

  # State stored per circle
  state:
    circle_1:
      members: [alice, frank]
      next_index: 0
    circle_2:
      members: [bob, carol, greg]
      next_index: 1  # Carol is next
```

Example:
  Task 1 → Bob (index 0)
  Task 2 → Carol (index 1)
  Task 3 → Greg (index 2)
  Task 4 → Bob (index 0, wrapped)


METHOD 2: SKILLS MATCH (Smart, Complex)
═══════════════════════════════════════════════════════════════════════════════

How it works:
  1. Extract required skills from sub-task
  2. Match against person skill profiles
  3. Assign to best skill match

```yaml
within_circle:
  method: SKILLS_MATCH

  # Person skill profiles
  profiles:
    bob:
      skills:
        react: 0.9
        typescript: 0.8
        css: 0.6
      circle: 2
    carol:
      skills:
        nodejs: 0.9
        rest_api: 0.95
        postgresql: 0.8
      circle: 2
    greg:
      skills:
        react: 0.7
        angular: 0.9
        testing: 0.6
      circle: 2

  # How to extract skills from task
  skill_extraction:
    method: AI  # or KEYWORD
    ai_prompt: "Extract technical skills needed for: {task_title}"
```

Example:
  Task: "Build React wishlist component"
  Skills needed: [react, typescript]

  Scores:
    Bob:  react(0.9) + typescript(0.8) = 1.7 ← BEST
    Carol: react(0.0) + typescript(0.0) = 0.0
    Greg:  react(0.7) + typescript(0.0) = 0.7

  Assign to: Bob


METHOD 3: ROUND-ROBIN + SKILLS (Hybrid)
═══════════════════════════════════════════════════════════════════════════════

How it works:
  1. Filter circle members by minimum skill match
  2. Round-robin among filtered members
  3. If no skill match, fallback to pure round-robin

```yaml
within_circle:
  method: ROUND_ROBIN_SKILLS  # Hybrid

  min_skill_score: 0.5  # Need at least 50% skill match

  # If multiple people have skills, round-robin among them
  # If nobody has skills, round-robin among all
```

Example:
  Task: "Build React wishlist component"
  Skills needed: [react]

  Filtering:
    Bob:  react(0.9) >= 0.5 ✓ Include
    Carol: react(0.0) < 0.5  ✗ Exclude
    Greg:  react(0.7) >= 0.5 ✓ Include

  Round-robin pool: [Bob, Greg]
  Next in rotation: Bob
  Assign to: Bob


METHOD 4: LOAD BALANCE (Capacity-based)
═══════════════════════════════════════════════════════════════════════════════

How it works:
  1. Count current assigned tasks per person
  2. Assign to person with least tasks
  3. Optionally weight by task complexity

```yaml
within_circle:
  method: LOAD_BALANCE

  # How to count load
  load_calculation:
    method: TASK_COUNT  # or STORY_POINTS
    include_statuses: [TODO, IN_PROGRESS]  # Don't count Done
    max_load: 5  # Max tasks per person

  # If tie, use round-robin
  tiebreaker: ROUND_ROBIN
```

Example:
  Current load:
    Bob:   3 tasks
    Carol: 1 task  ← LEAST
    Greg:  2 tasks

  Assign to: Carol


METHOD 5: MANUAL (Circle Lead Decides)
═══════════════════════════════════════════════════════════════════════════════

How it works:
  1. Assign to circle (not person)
  2. Circle lead gets notified
  3. Circle lead manually assigns to person

```yaml
within_circle:
  method: MANUAL

  circle_leads:
    circle_1: alice
    circle_2: bob
    circle_3: dave
    circle_4: eve

  notification:
    channel: slack
    message: "New task for Circle {circle}: {task_title}"
```

└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Learning Mechanism (Detailed)

### EXACTLY How Learning Works

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    LEARNING MECHANISM (DETAILED)                             │
├─────────────────────────────────────────────────────────────────────────────┤

OVERVIEW
════════════════════════════════════════════════════════════════════════════════

The Assignment Agent learns from human behavior:
  • Reassignments (A → B means B is better for this type)
  • Completion times (fast = good match)
  • Explicit feedback (optional rating)

This improves future assignments without manual configuration.


STEP 1: DATA COLLECTION
════════════════════════════════════════════════════════════════════════════════

What we collect for each task:

┌──────────────────────────────────────────────────────────────────────────────┐
│                        TASK RECORD                                           │
│──────────────────────────────────────────────────────────────────────────────│
│ task_id:              "ST-123"                                               │
│ task_title:           "Create REST API for wishlist"                         │
│ task_description:     "Build endpoints for CRUD operations..."              │
│                                                                              │
│ # Extracted features (by AI or rules)                                        │
│ detected_skills:      ["rest_api", "nodejs", "postgresql"]                   │
│ detected_circle:      2                                                      │
│ detected_complexity:  "MEDIUM"                                               │
│ detected_type:        "IMPLEMENTATION"                                       │
│                                                                              │
│ # Assignment history                                                         │
│ original_assignee:    "bob"                                                  │
│ original_timestamp:   "2025-01-15T10:00:00Z"                                │
│ original_method:      "ROUND_ROBIN"                                          │
│                                                                              │
│ # Reassignment (if happened)                                                 │
│ reassigned_to:        "carol"                                                │
│ reassigned_timestamp: "2025-01-15T14:30:00Z"                                │
│ reassigned_by:        "bob"  # Self-reassigned                              │
│ reassignment_reason:  "Carol has more API experience"  # From comment       │
│                                                                              │
│ # Completion data                                                            │
│ completed_by:         "carol"                                                │
│ completed_timestamp:  "2025-01-16T16:00:00Z"                                │
│ completion_time_hrs:  25.5                                                   │
│ quality_rating:       null  # Optional                                       │
└──────────────────────────────────────────────────────────────────────────────┘

Storage:
```sql
CREATE TABLE assignment_learning_data (
  id UUID PRIMARY KEY,
  task_id VARCHAR NOT NULL,
  task_title TEXT,

  -- Feature extraction
  detected_skills JSONB,         -- ["rest_api", "nodejs"]
  detected_circle INTEGER,
  detected_complexity VARCHAR,   -- LOW, MEDIUM, HIGH
  detected_type VARCHAR,         -- IMPLEMENTATION, TEST, DEPLOY

  -- Original assignment
  original_assignee VARCHAR,
  original_timestamp TIMESTAMP,
  original_method VARCHAR,       -- ROUND_ROBIN, SKILLS_MATCH, etc.

  -- Reassignment (nullable)
  was_reassigned BOOLEAN DEFAULT FALSE,
  reassigned_to VARCHAR,
  reassigned_timestamp TIMESTAMP,
  reassigned_by VARCHAR,
  reassignment_reason TEXT,

  -- Completion
  completed_by VARCHAR,
  completed_timestamp TIMESTAMP,
  completion_time_hours DECIMAL,

  -- Metadata
  created_at TIMESTAMP DEFAULT NOW()
);
```


STEP 2: FEATURE EXTRACTION
════════════════════════════════════════════════════════════════════════════════

From each task, we extract:

┌──────────────────────────────────────────────────────────────────────────────┐
│ Feature Type     │ How Extracted        │ Example Values                    │
│──────────────────────────────────────────────────────────────────────────────│
│ Skills           │ AI analysis or       │ ["react", "typescript", "api"]    │
│                  │ keyword matching     │                                   │
│──────────────────────────────────────────────────────────────────────────────│
│ Task Type        │ AI classification    │ IMPLEMENTATION, TEST, CONFIG,     │
│                  │                      │ DOCUMENTATION, DEPLOY, REVIEW     │
│──────────────────────────────────────────────────────────────────────────────│
│ Complexity       │ AI analysis or       │ LOW, MEDIUM, HIGH                 │
│                  │ story points         │                                   │
│──────────────────────────────────────────────────────────────────────────────│
│ Keywords         │ TF-IDF extraction    │ ["wishlist", "crud", "rest"]      │
│──────────────────────────────────────────────────────────────────────────────│
│ Circle           │ Circle detection     │ 1, 2, 3, 4                        │
│                  │ method               │                                   │
└──────────────────────────────────────────────────────────────────────────────┘


STEP 3: BUILDING AFFINITY SCORES
════════════════════════════════════════════════════════════════════════════════

For each person, we maintain affinity scores:

┌──────────────────────────────────────────────────────────────────────────────┐
│                    PERSON AFFINITY MODEL                                     │
│──────────────────────────────────────────────────────────────────────────────│
│                                                                              │
│  person_id: "carol"                                                          │
│  circle: 2                                                                   │
│                                                                              │
│  skill_affinity:                                                             │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │ Skill        │ Score │ Data Points │ Last Updated │ Trend              ││
│  │─────────────────────────────────────────────────────────────────────────││
│  │ rest_api     │ +3.2  │ 12          │ 2025-01-15   │ ↑ (improving)      ││
│  │ nodejs       │ +2.1  │ 8           │ 2025-01-14   │ → (stable)         ││
│  │ postgresql   │ +1.5  │ 5           │ 2025-01-12   │ ↑ (improving)      ││
│  │ react        │ -0.8  │ 3           │ 2025-01-10   │ ↓ (declining)      ││
│  └─────────────────────────────────────────────────────────────────────────┘│
│                                                                              │
│  task_type_affinity:                                                         │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │ Type           │ Score │ Data Points │ Trend                           ││
│  │─────────────────────────────────────────────────────────────────────────││
│  │ IMPLEMENTATION │ +2.5  │ 15          │ → (stable)                      ││
│  │ TEST           │ -1.2  │ 4           │ ↓ (avoid)                       ││
│  │ DOCUMENTATION  │ +0.3  │ 2           │ → (neutral)                     ││
│  └─────────────────────────────────────────────────────────────────────────┘│
│                                                                              │
│  complexity_affinity:                                                        │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │ Complexity │ Avg Completion Time │ vs Expected │ Trend                 ││
│  │─────────────────────────────────────────────────────────────────────────││
│  │ HIGH       │ 18.5 hours          │ -20% faster │ ↑ Good at complex     ││
│  │ MEDIUM     │ 8.2 hours           │ On par      │ →                     ││
│  │ LOW        │ 3.1 hours           │ +10% slower │ ↓ Bored?              ││
│  └─────────────────────────────────────────────────────────────────────────┘│
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘

Storage:
```sql
CREATE TABLE person_affinity (
  person_id VARCHAR NOT NULL,
  affinity_type VARCHAR NOT NULL,  -- 'skill', 'task_type', 'complexity'
  affinity_key VARCHAR NOT NULL,   -- 'rest_api', 'IMPLEMENTATION', 'HIGH'

  score DECIMAL DEFAULT 0,         -- Positive = good, Negative = avoid
  data_points INTEGER DEFAULT 0,   -- How many samples
  last_updated TIMESTAMP,

  PRIMARY KEY (person_id, affinity_type, affinity_key)
);
```


STEP 4: UPDATE ALGORITHM
════════════════════════════════════════════════════════════════════════════════

When reassignment happens:

```
EVENT: Task "ST-123" reassigned from Bob to Carol
       Reason: "Carol has more API experience"

ALGORITHM:

1. Extract features from task:
   skills = ["rest_api", "nodejs"]
   type = "IMPLEMENTATION"
   complexity = "MEDIUM"

2. Update Bob's affinity (NEGATIVE signal):
   For each skill in ["rest_api", "nodejs"]:
     bob.skill_affinity[skill].score -= REASSIGN_PENALTY  # -1.0
     bob.skill_affinity[skill].data_points += 1

   bob.task_type_affinity["IMPLEMENTATION"].score -= REASSIGN_PENALTY

3. Update Carol's affinity (POSITIVE signal):
   For each skill in ["rest_api", "nodejs"]:
     carol.skill_affinity[skill].score += REASSIGN_BONUS  # +1.5
     carol.skill_affinity[skill].data_points += 1

   carol.task_type_affinity["IMPLEMENTATION"].score += REASSIGN_BONUS

4. Apply decay to old data:
   For all affinities older than 30 days:
     affinity.score *= DECAY_FACTOR  # 0.9
```

Constants (configurable):
```yaml
learning:
  reassign_penalty: 1.0      # Negative score when reassigned away
  reassign_bonus: 1.5        # Positive score when reassigned to
  completion_bonus: 0.5      # Bonus for completing assigned task
  fast_completion_bonus: 1.0 # Extra bonus for fast completion
  decay_factor: 0.9          # How much old data fades
  decay_period_days: 30      # Apply decay every N days
  min_data_points: 5         # Need N samples before using affinity
```


STEP 5: INFERENCE (USING LEARNED DATA)
════════════════════════════════════════════════════════════════════════════════

When assigning a new task:

```
NEW TASK: "Build GraphQL API for orders"
CIRCLE: 2 (Development)
MEMBERS: [bob, carol, greg]

1. Extract features:
   skills = ["graphql", "nodejs", "api"]
   type = "IMPLEMENTATION"
   complexity = "HIGH"

2. Calculate score for each person:

   Bob's Score:
   ┌─────────────────────────────────────────────────────────┐
   │ skill_affinity["graphql"]        = 0.0 (no data)        │
   │ skill_affinity["nodejs"]         = -0.5 (some negatives)│
   │ skill_affinity["api"]            = -1.2                 │
   │ task_type_affinity["IMPL"]       = +0.3                 │
   │ complexity_affinity["HIGH"]      = -0.8                 │
   │ ───────────────────────────────────────────────────────│
   │ TOTAL                            = -2.2                 │
   └─────────────────────────────────────────────────────────┘

   Carol's Score:
   ┌─────────────────────────────────────────────────────────┐
   │ skill_affinity["graphql"]        = +0.8                 │
   │ skill_affinity["nodejs"]         = +2.1                 │
   │ skill_affinity["api"]            = +3.2                 │
   │ task_type_affinity["IMPL"]       = +2.5                 │
   │ complexity_affinity["HIGH"]      = +1.2                 │
   │ ───────────────────────────────────────────────────────│
   │ TOTAL                            = +9.8  ← HIGHEST      │
   └─────────────────────────────────────────────────────────┘

   Greg's Score:
   ┌─────────────────────────────────────────────────────────┐
   │ skill_affinity["graphql"]        = +1.5                 │
   │ skill_affinity["nodejs"]         = +0.5                 │
   │ skill_affinity["api"]            = +0.8                 │
   │ task_type_affinity["IMPL"]       = +1.0                 │
   │ complexity_affinity["HIGH"]      = +0.2                 │
   │ ───────────────────────────────────────────────────────│
   │ TOTAL                            = +4.0                 │
   └─────────────────────────────────────────────────────────┘

3. Combine with base method:

   If method = ROUND_ROBIN:
     Next in rotation: Bob
     But Carol's score (+9.8) vs Bob's (-2.2) difference > THRESHOLD (5.0)
     OVERRIDE: Suggest Carol instead
     Confidence: 95% (large score difference)

   If method = SKILLS_MATCH:
     Base skill match would pick Carol anyway
     Learning confirms: Carol with +9.8

4. Return suggestion:
   {
     "suggested_assignee": "carol",
     "confidence": 0.95,
     "reasoning": "Based on 12 historical reassignments, Carol is highly
                   effective with API tasks. Last 5 similar tasks completed
                   20% faster than average.",
     "alternative": "greg",
     "round_robin_would_be": "bob"
   }
```


STEP 6: FEEDBACK LOOP
════════════════════════════════════════════════════════════════════════════════

After task completion:

```
TASK COMPLETED: "Build GraphQL API for orders"
ASSIGNEE: Carol
TIME: 12 hours (expected: 16 hours = 25% faster)

UPDATE AFFINITIES:

1. Carol completed (as assigned) - small positive:
   carol.skill_affinity["graphql"].score += COMPLETION_BONUS  # +0.5
   carol.skill_affinity["nodejs"].score += COMPLETION_BONUS
   carol.skill_affinity["api"].score += COMPLETION_BONUS

2. Fast completion - extra positive:
   time_ratio = 12/16 = 0.75 (25% faster)
   if time_ratio < 0.9:  # At least 10% faster
     carol.all_affinities += FAST_BONUS * (1 - time_ratio)  # +0.25

3. Update completion time stats:
   carol.complexity_affinity["HIGH"].avg_time =
     (old_avg * old_count + 12) / (old_count + 1)
```


VISUALIZATION: LEARNING DASHBOARD
════════════════════════════════════════════════════════════════════════════════

QUAD Web App shows learning insights:

┌──────────────────────────────────────────────────────────────────────────────┐
│  ASSIGNMENT LEARNING INSIGHTS                                                │
│──────────────────────────────────────────────────────────────────────────────│
│                                                                              │
│  Circle 2 (Development) - 3 members                                          │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │  SKILL HEATMAP (darker = stronger affinity)                            │ │
│  │  ──────────────────────────────────────────────────────────────────── │ │
│  │                React   Node.js   API   GraphQL   SQL   Testing        │ │
│  │  Bob          ███░░   ░░░░░     ░░░   ░░░░░     ███   ░░░░░           │ │
│  │  Carol        ░░░░░   █████     ███   ████░     ███   ░░░░░           │ │
│  │  Greg         ████░   ░░░░░     ██░   ░░░░░     ░░░   ████░           │ │
│  │                                                                        │ │
│  │  Legend: █████ = Strong positive  ░░░░░ = Neutral  ░░░░░ = Negative    │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │  RECENT LEARNINGS                                                      │ │
│  │  ──────────────────────────────────────────────────────────────────── │ │
│  │  • Carol reassigned 3 API tasks from Bob this month (+3.0 affinity)   │ │
│  │  • Greg excels at testing tasks, 30% faster than average              │ │
│  │  • Bob prefers React tasks, 2 self-reassigns from API tasks           │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │  RECOMMENDATIONS                                                       │ │
│  │  ──────────────────────────────────────────────────────────────────── │ │
│  │  • Consider updating Bob's skill profile to exclude "api"             │ │
│  │  • Carol may be overloaded with API tasks (80% of assignments)        │ │
│  │  • Greg has capacity for more complex tasks                            │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘

└─────────────────────────────────────────────────────────────────────────────┘
```

---

## QUAD Web Application Integration

### Central Hub for All Tools

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    QUAD WEB APPLICATION                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  INTEGRATIONS                                              [+ Add]  │    │
│  │                                                                      │    │
│  │  ┌─────────────────────────────────────────────────────────────────┐│    │
│  │  │ ┌────┐ Jira           Connected  ✓   Webhook: Active           ││    │
│  │  │ │JIRA│ RETAIL, PLATFORM projects                    [Configure]││    │
│  │  │ └────┘                                                          ││    │
│  │  │ ┌────┐ GitHub         Connected  ✓   Webhook: Active           ││    │
│  │  │ │ GH │ org/retail-app, org/platform                 [Configure]││    │
│  │  │ └────┘                                                          ││    │
│  │  │ ┌────┐ Slack          Connected  ✓   Bot: @QUAD                ││    │
│  │  │ │ SL │ #requirements, #pr-reviews               [Configure]    ││    │
│  │  │ └────┘                                                          ││    │
│  │  │ ┌────┐ Email (O365)   Connected  ✓   Polling: 5 min            ││    │
│  │  │ │ EM │ requirements@company.com                     [Configure]││    │
│  │  │ └────┘                                                          ││    │
│  │  │ ┌────┐ Confluence     Connected  ✓   Spaces: SPECS, DOCS       ││    │
│  │  │ │CONF│                                              [Configure]││    │
│  │  │ └────┘                                                          ││    │
│  │  └─────────────────────────────────────────────────────────────────┘│    │
│  └──────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  TRIGGER CONFIGURATION                                              │    │
│  │                                                                      │    │
│  │  Active Triggers: 12                              [+ Add Trigger]  │    │
│  │                                                                      │    │
│  │  ┌──────────────────────────────────────────────────────────────┐   │    │
│  │  │ Source    │ Event           │ Target Agent   │ Status │ Hits │   │    │
│  │  │──────────────────────────────────────────────────────────────│   │    │
│  │  │ Jira      │ issue.created   │ story-agent    │ ✓ On   │ 145  │   │    │
│  │  │ Slack     │ #requirements   │ story-agent    │ ✓ On   │ 52   │   │    │
│  │  │ Email     │ from:pm@...     │ story-agent    │ ✓ On   │ 23   │   │    │
│  │  │ GitHub    │ PR opened       │ review-agent   │ ✓ On   │ 89   │   │    │
│  │  │ Jira      │ assignee change │ learn-agent    │ ✓ On   │ 31   │   │    │
│  │  │ Cron      │ Daily 9AM       │ reminder-agent │ ✓ On   │ 45   │   │    │
│  │  └──────────────────────────────────────────────────────────────┘   │    │
│  └──────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  PENDING ASSIGNMENTS (Hybrid Mode)                    [Approve All] │    │
│  │                                                                      │    │
│  │  Story: "Order Management Enhancement" [RETAIL-789]                 │    │
│  │  ┌──────────────────────────────────────────────────────────────┐   │    │
│  │  │ ☑ Design order state machine    → C1 → @Alice (92%)  [Edit] │   │    │
│  │  │ ☑ Build order list UI           → C2 → @Bob   (88%)  [Edit] │   │    │
│  │  │ ☑ Create order API endpoints    → C2 → @Carol (95%)  [Edit] │   │    │
│  │  │ ☑ Write order validation tests  → C3 → @Dave  (90%)  [Edit] │   │    │
│  │  │ ☑ Deploy order service          → C4 → @Eve   (94%)  [Edit] │   │    │
│  │  └──────────────────────────────────────────────────────────────┘   │    │
│  │                                                                      │    │
│  │  💡 Carol recommended for API (3 reassignments, 95% confidence)     │    │
│  │                                                                      │    │
│  └──────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  LEARNING INSIGHTS                                     [View All]  │    │
│  │                                                                      │    │
│  │  📊 Total Reassignments Tracked: 31                                 │    │
│  │  📈 Assignment Accuracy: 87% (no reassignment)                      │    │
│  │  🎯 Top Learnings:                                                  │    │
│  │     • Carol: +3.2 API affinity (12 data points)                    │    │
│  │     • Greg: +2.1 Testing affinity (8 data points)                  │    │
│  │     • Bob: -1.2 API affinity (5 data points)                       │    │
│  │                                                                      │    │
│  └──────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Configuration Reference

### Complete Configuration File

```yaml
# quad.config.yaml - Assignment Agent Section

assignment_agent:
  enabled: true

  # ============================================================================
  # MODE: How assignments are handled
  # ============================================================================
  mode: HYBRID  # AUTO | MANUAL | HYBRID (default)
  # AUTO: Assign without human approval
  # MANUAL: Always require human to assign
  # HYBRID: Suggest assignments, human approves in QUAD Web App

  # ============================================================================
  # CIRCLE DETECTION: How to determine which circle
  # ============================================================================
  circle_detection:
    method: AI_BASED  # RULE_BASED | AI_BASED (default) | EXPLICIT_TAGS

    # AI-based config
    ai:
      provider: gemini  # gemini | openai | anthropic
      min_confidence: 0.7  # Below this, flag for human review
      fallback: RULE_BASED  # What to do if AI fails

    # Rule-based config (used as fallback or primary)
    rules:
      circle_1:
        keywords: [database, schema, migration, requirement, spec, design, BA]
      circle_2:
        keywords: [UI, frontend, React, backend, API, REST, service, component]
      circle_3:
        keywords: [test, QA, validation, verify, bug, defect, quality]
      circle_4:
        keywords: [deploy, kubernetes, docker, infra, CI, CD, monitor, ops]

    fallback_circle: 2  # Default if nothing matches

  # ============================================================================
  # WITHIN-CIRCLE ASSIGNMENT: How to pick person in circle
  # ============================================================================
  within_circle:
    method: ROUND_ROBIN  # ROUND_ROBIN (default) | SKILLS_MATCH |
                         # ROUND_ROBIN_SKILLS | LOAD_BALANCE | MANUAL

    # Skills matching config
    skills:
      enabled: true
      extraction_method: AI  # AI | KEYWORD
      min_match_score: 0.5  # Minimum skill match to consider

    # Load balancing config
    load_balance:
      include_statuses: [TODO, IN_PROGRESS]
      max_tasks_per_person: 5

    # Circle leads (for MANUAL mode)
    circle_leads:
      1: alice
      2: bob
      3: dave
      4: eve

  # ============================================================================
  # LEARNING: How to learn from reassignments
  # ============================================================================
  learning:
    enabled: true

    # What signals to learn from
    signals:
      reassignment: true        # Task moved to different person
      self_reassignment: true   # Person reassigns their own task
      completion_time: true     # Fast/slow completion
      explicit_feedback: false  # Optional rating (if you have this)

    # Scoring weights
    weights:
      reassign_penalty: 1.0      # Negative when reassigned away
      reassign_bonus: 1.5        # Positive when reassigned to
      completion_bonus: 0.5      # For completing assigned task
      fast_completion_bonus: 1.0 # Extra for completing early

    # Data management
    min_data_points: 5     # Need N samples before trusting affinity
    decay_factor: 0.9      # Old data fades over time
    decay_period_days: 30  # Apply decay every N days

    # Override threshold
    override_threshold: 5.0  # Score difference to override round-robin

  # ============================================================================
  # TRIGGERS: What events trigger assignment
  # ============================================================================
  triggers:
    - event: story.expanded
      source: story-agent
      action: assign_sub_tasks

    - event: issue.transitioned
      source: jira
      filter:
        to_status: "Ready for Dev"
      action: assign_if_unassigned

    - event: issue.updated
      source: jira
      filter:
        field_changed: assignee
      action: record_reassignment

  # ============================================================================
  # NOTIFICATIONS: How to notify about assignments
  # ============================================================================
  notifications:
    on_assignment:
      slack: true
      email: false
      jira_comment: true

    on_pending_approval:  # For HYBRID mode
      slack:
        channel: "#assignment-review"
        mention: "@pm-lead"
```

---

*Part of QUAD™ (Quick Unified Agentic Development) Methodology*
*© 2025 Suman Addanke / A2 Vibe Creators LLC*
