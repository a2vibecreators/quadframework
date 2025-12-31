# QUAD Custom Agent Development

## How to Create, Extend, and Customize QUAD Agents

Part of QUAD™ (Quick Unified Agentic Development) Methodology
© 2025 Suman Addanke / A2 Vibe Creators LLC

---

## Table of Contents

1. [Overview](#overview)
2. [Creating a Custom Agent from Scratch](#creating-a-custom-agent-from-scratch)
3. [Extending Existing Agents](#extending-existing-agents)
4. [Agent Rules & Constraints](#agent-rules--constraints)
5. [Permission Configuration](#permission-configuration)
6. [Testing Your Agent](#testing-your-agent)
7. [Registering with QAR](#registering-with-qar)
8. [Examples](#examples)

---

## Overview

### Three Ways to Add Agents

```
┌──────────────────────────────────────────────────────────────────────┐
│                    AGENT CUSTOMIZATION OPTIONS                       │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  OPTION A: CREATE FROM SCRATCH                                       │
│  ═════════════════════════════                                       │
│  • Build a completely new agent                                      │
│  • Implement QUADAgent interface                                     │
│  • Full control over behavior                                        │
│  • Use case: Company-specific logic                                  │
│                                                                      │
│  Example: "cobol-analyzer-agent" for GlobalRetail's COBOL system     │
│                                                                      │
│  ────────────────────────────────────────────────────────────────── │
│                                                                      │
│  OPTION B: EXTEND EXISTING AGENT                                     │
│  ═══════════════════════════════                                     │
│  • Inherit from built-in agent                                       │
│  • Override specific methods                                         │
│  • Add custom rules/constraints                                      │
│  • Use case: Customize story-agent for your workflow                 │
│                                                                      │
│  Example: "globalretail-story-agent" extends "story-agent"           │
│           + Adds COBOL impact analysis                               │
│           + Enforces GlobalRetail naming conventions                 │
│                                                                      │
│  ────────────────────────────────────────────────────────────────── │
│                                                                      │
│  OPTION C: CONFIGURE EXISTING AGENT                                  │
│  ══════════════════════════════════                                  │
│  • Use quad.config.yaml rules                                        │
│  • Add constraints without code                                      │
│  • Restrict permissions                                              │
│  • Use case: Tighten rules on stubborn agent                         │
│                                                                      │
│  Example: Force story-agent to always require BA approval            │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Creating a Custom Agent from Scratch

### Step 1: Define Agent Identity

Create a new agent file:

```typescript
// .quad/agents/cobol-analyzer-agent.ts

import {
  QUADAgent,
  Circle,
  PermissionLevel,
  AgentInput,
  AgentOutput,
  Permission
} from '@quad/agent-runtime';

export class CobolAnalyzerAgent implements QUADAgent {
  // =========================================================================
  // IDENTITY (Required)
  // =========================================================================

  readonly agentId = 'cobol-analyzer-agent';
  readonly circle = Circle.DEVELOPMENT;  // Circle 2
  readonly version = '1.0.0';
  readonly description = 'Analyzes COBOL batch jobs for GlobalRetail legacy system';

  // =========================================================================
  // CAPABILITIES (Required)
  // =========================================================================

  readonly capabilities = [
    'analyze-cobol-program',
    'generate-dependency-map',
    'estimate-modernization-effort',
    'document-business-logic'
  ];

  readonly requiredInputs = [
    'program_name',      // e.g., "GL01"
    'program_path'       // e.g., "/cobol/programs/GL01.cbl"
  ];

  readonly outputs = [
    'analysis_report',
    'dependency_graph',
    'modernization_estimate',
    'documentation'
  ];

  // =========================================================================
  // PERMISSIONS (Required)
  // =========================================================================

  readonly canRead: Permission[] = [
    { resource: 'cobol/**/*.cbl', level: PermissionLevel.READ },
    { resource: 'cobol/**/*.cpy', level: PermissionLevel.READ },  // Copybooks
    { resource: 'jcl/**/*.jcl', level: PermissionLevel.READ },     // JCL scripts
    { resource: 'confluence/BATCH/**', level: PermissionLevel.READ }
  ];

  readonly canWrite: Permission[] = [
    { resource: 'confluence/BATCH/analysis/**', level: PermissionLevel.WRITE },
    { resource: 'jira/BATCH-*', level: PermissionLevel.SUGGEST }  // Suggest, not write
  ];

  readonly canInvoke = ['estimation-agent', 'doc-agent'];
  readonly cannotInvoke = ['deploy-agent-prod'];  // Safety: no prod deploys

  readonly maxModifications = 10;     // Max resources per invocation
  readonly requiresApproval = false;  // Doesn't need human approval

  // =========================================================================
  // MAIN EXECUTION (Required)
  // =========================================================================

  async invoke(input: AgentInput): Promise<AgentOutput> {
    const startTime = Date.now();
    const { program_name, program_path } = input.data;

    try {
      // Step 1: Read COBOL source
      const cobolSource = await this.readCobolProgram(program_path as string);

      // Step 2: Parse and analyze
      const analysis = await this.analyzeProgram(cobolSource);

      // Step 3: Find dependencies
      const dependencies = await this.findDependencies(analysis);

      // Step 4: Estimate modernization
      const estimate = await this.estimateModernization(analysis, dependencies);

      // Step 5: Generate documentation
      const documentation = await this.generateDocumentation(analysis);

      // Step 6: Write to Confluence
      await this.writeToConfluence(program_name as string, documentation);

      return {
        requestId: input.requestId,
        agentId: this.agentId,
        success: true,
        data: {
          analysis_report: analysis,
          dependency_graph: dependencies,
          modernization_estimate: estimate,
          documentation: documentation
        },
        modifiedResources: [`confluence/BATCH/analysis/${program_name}`],
        readResources: [program_path as string],
        duration: Date.now() - startTime
      };

    } catch (error) {
      return {
        requestId: input.requestId,
        agentId: this.agentId,
        success: false,
        data: {},
        error: error.message,
        modifiedResources: [],
        readResources: [],
        duration: Date.now() - startTime
      };
    }
  }

  // =========================================================================
  // PRIVATE METHODS (Your custom logic)
  // =========================================================================

  private async readCobolProgram(path: string): Promise<string> {
    // Use MCP tool to read from mainframe or file system
    const fileContent = await this.useMCPTool('file-mcp', 'read', { path });
    return fileContent;
  }

  private async analyzeProgram(source: string): Promise<CobolAnalysis> {
    // Use AI to analyze COBOL
    const analysis = await this.useMCPTool('gemini', 'analyze', {
      prompt: `Analyze this COBOL program and identify:
        1. Main business logic
        2. Database operations (EXEC SQL)
        3. File I/O operations
        4. Called subprograms
        5. Data divisions and structures`,
      content: source
    });
    return JSON.parse(analysis);
  }

  private async findDependencies(analysis: CobolAnalysis): Promise<DependencyGraph> {
    // Find all copybooks, subprograms, JCL references
    const deps: DependencyGraph = {
      copybooks: analysis.copyStatements,
      subprograms: analysis.callStatements,
      files: analysis.fileDescriptions,
      databases: analysis.sqlOperations
    };
    return deps;
  }

  private async estimateModernization(
    analysis: CobolAnalysis,
    deps: DependencyGraph
  ): Promise<ModernizationEstimate> {
    // Call estimation-agent for complexity
    const estimationResult = await this.invokeAgent('estimation-agent', {
      source_type: 'COBOL',
      lines_of_code: analysis.lineCount,
      complexity_score: analysis.complexity,
      dependency_count: Object.keys(deps).length,
      database_operations: deps.databases.length
    });

    return {
      complexity: estimationResult.data.platonic_solid,
      effort_days: estimationResult.data.estimated_days,
      risk_level: analysis.complexity > 50 ? 'HIGH' : 'MEDIUM',
      recommended_approach: this.selectApproach(analysis)
    };
  }

  private selectApproach(analysis: CobolAnalysis): string {
    if (analysis.lineCount < 500 && analysis.complexity < 20) {
      return 'REWRITE: Simple enough to rewrite in Java/Python';
    } else if (analysis.complexity > 80) {
      return 'STRANGLER: Gradually replace with wrapper APIs';
    } else {
      return 'REFACTOR: Convert to modern COBOL with microservices interface';
    }
  }

  private async generateDocumentation(analysis: CobolAnalysis): Promise<string> {
    // Use doc-agent or AI to generate docs
    const docs = await this.useMCPTool('gemini', 'generate', {
      prompt: `Generate technical documentation for this COBOL analysis:
        - Purpose and business function
        - Input/Output description
        - Key algorithms
        - Database tables accessed
        - Modernization recommendations`,
      data: analysis
    });
    return docs;
  }

  private async writeToConfluence(programName: string, docs: string): Promise<void> {
    await this.useMCPTool('confluence', 'create_page', {
      space: 'BATCH',
      parent: 'analysis',
      title: `${programName} Analysis`,
      content: docs
    });
  }

  // Helper methods (provided by QAR runtime)
  private async useMCPTool(tool: string, action: string, params: any): Promise<any> {
    // QAR runtime provides this
    return await (this as any).runtime.useMCPTool(tool, action, params);
  }

  private async invokeAgent(agentId: string, data: any): Promise<AgentOutput> {
    // QAR runtime provides this
    return await (this as any).runtime.invokeAgent(agentId, data);
  }
}

// Type definitions
interface CobolAnalysis {
  lineCount: number;
  complexity: number;
  copyStatements: string[];
  callStatements: string[];
  fileDescriptions: any[];
  sqlOperations: any[];
}

interface DependencyGraph {
  copybooks: string[];
  subprograms: string[];
  files: any[];
  databases: any[];
}

interface ModernizationEstimate {
  complexity: string;
  effort_days: number;
  risk_level: string;
  recommended_approach: string;
}
```

### Step 2: Register Agent

```yaml
# .quad/agents.yaml

agents:
  # Register your custom agent
  cobol-analyzer-agent:
    path: ./agents/cobol-analyzer-agent.ts
    enabled: true

    # Trigger configuration
    triggers:
      human:
        enabled: true
        methods: [cli, chat, ide]
      auto:
        enabled: true
        events:
          - source: jira
            event: issue.created
            filter:
              labels: ["cobol-analysis"]

    # MCP tools this agent can use
    mcp_tools:
      - file-mcp      # Read COBOL files
      - gemini        # AI analysis
      - confluence    # Write documentation

    # Override default permissions
    permissions:
      canRead:
        - "cobol/**/*"
        - "jcl/**/*"
      canWrite:
        - "confluence/BATCH/**"
```

---

## Extending Existing Agents

### Extend Story Agent with Custom Rules

```typescript
// .quad/agents/globalretail-story-agent.ts

import { StoryAgent, AgentInput, AgentOutput } from '@quad/built-in-agents';

/**
 * GlobalRetail-specific Story Agent
 *
 * Extends the built-in story-agent with:
 * - COBOL impact analysis for any story touching batch
 * - Naming convention enforcement
 * - Required fields validation
 * - Custom acceptance criteria format
 */
export class GlobalRetailStoryAgent extends StoryAgent {

  readonly agentId = 'globalretail-story-agent';
  readonly version = '1.0.0';
  readonly description = 'Story agent customized for GlobalRetail conventions';

  // =========================================================================
  // CUSTOM RULES (Strict enforcement)
  // =========================================================================

  private readonly REQUIRED_FIELDS = [
    'business_justification',
    'affected_systems',
    'rollback_plan'
  ];

  private readonly NAMING_PATTERN = /^GR-[A-Z]{3}-\d{4}$/;  // GR-PRJ-0001

  private readonly FORBIDDEN_WORDS = [
    'ASAP',           // Must have specific date
    'simple',         // Underestimates complexity
    'just',           // Underestimates complexity
    'easy'            // Underestimates complexity
  ];

  // =========================================================================
  // OVERRIDE: Pre-processing validation
  // =========================================================================

  async invoke(input: AgentInput): Promise<AgentOutput> {
    // RULE 1: Validate required fields
    const missingFields = this.validateRequiredFields(input);
    if (missingFields.length > 0) {
      return this.rejectWithReason(input,
        `Missing required fields: ${missingFields.join(', ')}`);
    }

    // RULE 2: Check for forbidden words
    const forbiddenFound = this.checkForbiddenWords(input);
    if (forbiddenFound.length > 0) {
      return this.rejectWithReason(input,
        `Forbidden words found: ${forbiddenFound.join(', ')}. ` +
        `Please use specific, measurable language.`);
    }

    // RULE 3: Check naming convention (if story ID provided)
    if (input.data.story_id && !this.isValidStoryId(input.data.story_id as string)) {
      return this.rejectWithReason(input,
        `Invalid story ID format. Must match: GR-XXX-0000`);
    }

    // All rules pass → call parent implementation
    const result = await super.invoke(input);

    // RULE 4: Post-process - Add COBOL impact if touching batch
    if (result.success && this.touchesBatchSystem(input)) {
      result.data = await this.addCobolImpactAnalysis(result.data);
    }

    // RULE 5: Enforce acceptance criteria format
    if (result.success) {
      result.data = this.enforceAcceptanceCriteriaFormat(result.data);
    }

    return result;
  }

  // =========================================================================
  // RULE IMPLEMENTATIONS
  // =========================================================================

  private validateRequiredFields(input: AgentInput): string[] {
    const missing: string[] = [];
    for (const field of this.REQUIRED_FIELDS) {
      if (!input.data[field]) {
        missing.push(field);
      }
    }
    return missing;
  }

  private checkForbiddenWords(input: AgentInput): string[] {
    const text = JSON.stringify(input.data).toLowerCase();
    return this.FORBIDDEN_WORDS.filter(word => text.includes(word.toLowerCase()));
  }

  private isValidStoryId(storyId: string): boolean {
    return this.NAMING_PATTERN.test(storyId);
  }

  private touchesBatchSystem(input: AgentInput): boolean {
    const affectedSystems = input.data.affected_systems as string[] || [];
    return affectedSystems.some(sys =>
      sys.toLowerCase().includes('batch') ||
      sys.toLowerCase().includes('cobol') ||
      sys.toLowerCase().includes('mainframe')
    );
  }

  private async addCobolImpactAnalysis(data: any): Promise<any> {
    // Invoke COBOL analyzer for impact assessment
    const cobolImpact = await this.invokeAgent('cobol-analyzer-agent', {
      analysis_type: 'impact',
      affected_programs: data.affected_systems
    });

    return {
      ...data,
      cobol_impact: {
        affected_programs: cobolImpact.data.programs,
        risk_level: cobolImpact.data.risk,
        requires_batch_testing: true,
        recommended_testers: ['batch-qa-team']
      }
    };
  }

  private enforceAcceptanceCriteriaFormat(data: any): any {
    // Ensure all acceptance criteria follow Given/When/Then
    const criteria = data.acceptance_criteria || [];
    const formattedCriteria = criteria.map((ac: string) => {
      if (!ac.toUpperCase().startsWith('GIVEN')) {
        return `GIVEN the system is in normal state\nWHEN ${ac}\nTHEN the expected behavior occurs`;
      }
      return ac;
    });

    return {
      ...data,
      acceptance_criteria: formattedCriteria,
      format_enforced: true
    };
  }

  private rejectWithReason(input: AgentInput, reason: string): AgentOutput {
    return {
      requestId: input.requestId,
      agentId: this.agentId,
      success: false,
      data: {
        rejection_reason: reason,
        suggestions: this.getSuggestions(reason)
      },
      error: `Story rejected: ${reason}`,
      modifiedResources: [],
      readResources: [],
      duration: 0
    };
  }

  private getSuggestions(reason: string): string[] {
    if (reason.includes('Missing required fields')) {
      return [
        'Add business_justification: Why is this needed?',
        'Add affected_systems: Which systems will change?',
        'Add rollback_plan: How to revert if something goes wrong?'
      ];
    }
    if (reason.includes('Forbidden words')) {
      return [
        'Replace "ASAP" with a specific date',
        'Replace "simple/easy/just" with complexity estimate',
        'Use measurable criteria'
      ];
    }
    return [];
  }
}
```

---

## Agent Rules & Constraints

### Option C: Configure Without Code

For existing agents, add strict rules via configuration:

```yaml
# quad.config.yaml

agents:
  # =========================================================================
  # STORY AGENT - Strict Rules (No code changes)
  # =========================================================================
  story-agent:
    # Make this agent stricter
    rules:
      # RULE: Always require BA approval before creating stories
      require_approval:
        enabled: true
        approvers: [ba-team, pm-team]
        message: "Story must be approved by BA before creation"

      # RULE: Minimum acceptance criteria
      min_acceptance_criteria: 3

      # RULE: Required fields
      required_fields:
        - business_value        # Why is this important?
        - definition_of_done    # When is it complete?
        - test_approach         # How to test?

      # RULE: Forbidden patterns in story text
      forbidden_patterns:
        - pattern: "\\bASAP\\b"
          message: "Use specific dates instead of ASAP"
        - pattern: "\\beasy\\b|\\bsimple\\b|\\bjust\\b"
          message: "Avoid underestimating - use complexity estimate"
        - pattern: "TBD|TODO|FIXME"
          message: "All details must be filled in"

      # RULE: Max story size
      max_complexity: DODECAHEDRON  # Stories > 12 pts must be split

      # RULE: Platform coverage
      require_platform_tags: true   # Must specify platform/API, platform/WEB, etc.

      # RULE: Auto-label rules
      auto_labels:
        - when: "text contains 'security'"
          apply: [priority/P0, type/SECURITY]
        - when: "text contains 'batch' OR 'COBOL'"
          apply: [requires/batch-review]

    # Override permissions
    permissions:
      canWrite:
        - "jira/GR-*"             # Only GlobalRetail Jira projects
        - "confluence/SPECS/**"   # Only specs space
      cannotWrite:
        - "jira/GR-PROD-*"        # Cannot touch production stories directly

    # Rate limiting
    rate_limit:
      max_per_hour: 50            # Prevent runaway story generation
      max_per_day: 200

  # =========================================================================
  # DEV AGENT - Strict Rules
  # =========================================================================
  dev-agent-ui:
    rules:
      # RULE: Cannot modify backend files
      file_restrictions:
        allowed_patterns:
          - "src/ui/**"
          - "src/components/**"
          - "tests/ui/**"
        denied_patterns:
          - "src/api/**"
          - "src/services/**"
          - "database/**"

      # RULE: Must run tests before commit
      pre_commit_hooks:
        - command: "npm test"
          must_pass: true
        - command: "npm run lint"
          must_pass: true

      # RULE: Code review required
      require_review: true
      min_reviewers: 1

    permissions:
      canInvoke:
        - test-agent-ui
        - review-agent
      cannotInvoke:
        - deploy-agent-prod    # UI dev cannot deploy to prod
        - db-agent             # UI dev cannot modify database

  # =========================================================================
  # DEPLOY AGENT PROD - Maximum Strictness
  # =========================================================================
  deploy-agent-prod:
    rules:
      # RULE: Always requires human approval
      require_approval:
        enabled: true
        approvers: [devops-lead, tech-lead, cto]
        min_approvers: 2       # Need 2 people to approve
        message: "Production deployment requires 2 approvals"

      # RULE: Time restrictions
      deployment_windows:
        allowed_days: [tuesday, wednesday, thursday]
        allowed_hours: [9, 10, 11, 14, 15, 16]  # 9-11 AM, 2-4 PM
        blocked_dates:
          - "2025-01-15"   # Holiday
          - "2025-12-31"   # New Year's Eve

      # RULE: Prerequisites
      prerequisites:
        - agent: test-agent
          status: QA_PASS
        - agent: security-agent
          status: PASS
        - manual_checklist:
            - "Database backup completed"
            - "Rollback plan documented"
            - "On-call engineer notified"

      # RULE: Post-deployment
      post_deployment:
        - monitor_duration: 30  # minutes
        - alert_threshold: 5    # errors trigger rollback
        - auto_rollback: true

    permissions:
      requiresApproval: true
      maxModifications: 5        # Very limited scope
      canInvoke: []              # Cannot chain to other agents
```

### Rule Types Available

| Rule Type | Description | Example |
|-----------|-------------|---------|
| `require_approval` | Human must approve | `approvers: [ba-team]` |
| `required_fields` | Must have these fields | `[business_value, test_approach]` |
| `forbidden_patterns` | Regex patterns to reject | `["\\bASAP\\b"]` |
| `min_acceptance_criteria` | Minimum AC count | `3` |
| `max_complexity` | Split if larger | `DODECAHEDRON` |
| `file_restrictions` | Allowed/denied file paths | `allowed_patterns: [src/ui/**]` |
| `rate_limit` | Prevent abuse | `max_per_hour: 50` |
| `deployment_windows` | When can deploy | `allowed_days: [tue, wed, thu]` |
| `prerequisites` | What must pass first | `test-agent: QA_PASS` |
| `auto_labels` | Auto-apply labels | `when: "contains security"` |

---

## Permission Configuration

### Permission Levels Explained

```
┌──────────────────────────────────────────────────────────────────────┐
│                    PERMISSION LEVELS                                 │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Level 0: NONE                                                       │
│  ──────────────                                                      │
│  Cannot access the resource at all                                   │
│  Example: dev-agent-ui cannot access database/**                     │
│                                                                      │
│  Level 1: READ                                                       │
│  ──────────────                                                      │
│  Can read but not modify                                             │
│  Example: test-agent can READ src/** but not WRITE                   │
│                                                                      │
│  Level 2: SUGGEST                                                    │
│  ──────────────────                                                  │
│  Can propose changes, human must approve                             │
│  Example: code-review-agent SUGGESTS changes, dev approves           │
│                                                                      │
│  Level 3: WRITE                                                      │
│  ─────────────                                                       │
│  Can modify (with audit trail)                                       │
│  Example: dev-agent-ui can WRITE to src/ui/**                        │
│                                                                      │
│  Level 4: ADMIN                                                      │
│  ─────────────                                                       │
│  Full access (use sparingly!)                                        │
│  Example: Only infra-agent has ADMIN on infrastructure/**            │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

### Permission Matrix Example

```yaml
# Permission matrix for GlobalRetail
permissions:
  # Story Agent permissions
  story-agent:
    canRead:
      - resource: "jira/**"
        level: READ
      - resource: "confluence/**"
        level: READ
    canWrite:
      - resource: "jira/GR-*"
        level: WRITE
        conditions: [requires_ba_approval]
      - resource: "confluence/SPECS/**"
        level: WRITE
    canInvoke:
      - estimation-agent
      - doc-agent
    cannotInvoke:
      - deploy-agent-prod
      - db-agent

  # Dev Agent UI permissions
  dev-agent-ui:
    canRead:
      - resource: "src/**"
        level: READ
    canWrite:
      - resource: "src/ui/**"
        level: WRITE
      - resource: "src/components/**"
        level: WRITE
      - resource: "tests/ui/**"
        level: WRITE
    cannotWrite:
      - resource: "src/api/**"        # Backend off-limits
      - resource: "database/**"        # DB off-limits
      - resource: "infrastructure/**"  # Infra off-limits
```

---

## Testing Your Agent

### Unit Testing

```typescript
// .quad/agents/__tests__/cobol-analyzer-agent.test.ts

import { CobolAnalyzerAgent } from '../cobol-analyzer-agent';
import { AgentInput, InvocationMethod } from '@quad/agent-runtime';

describe('CobolAnalyzerAgent', () => {
  let agent: CobolAnalyzerAgent;

  beforeEach(() => {
    agent = new CobolAnalyzerAgent();
  });

  test('should have correct identity', () => {
    expect(agent.agentId).toBe('cobol-analyzer-agent');
    expect(agent.circle).toBe('DEVELOPMENT');
  });

  test('should analyze simple COBOL program', async () => {
    const input: AgentInput = {
      requestId: 'test-001',
      data: {
        program_name: 'GL01',
        program_path: '/cobol/programs/GL01.cbl'
      },
      invokedBy: 'user',
      invocationMethod: InvocationMethod.CLI,
      timestamp: new Date()
    };

    const output = await agent.invoke(input);

    expect(output.success).toBe(true);
    expect(output.data.analysis_report).toBeDefined();
    expect(output.data.dependency_graph).toBeDefined();
  });

  test('should respect permissions', async () => {
    // Try to write to forbidden resource
    // Should fail permission check
  });

  test('should not invoke forbidden agents', async () => {
    expect(agent.cannotInvoke).toContain('deploy-agent-prod');
  });
});
```

### Integration Testing

```bash
# Test agent invocation
quad agent test cobol-analyzer-agent \
  --input='{"program_name": "GL01", "program_path": "/test/GL01.cbl"}' \
  --mock-mcp
```

---

## Registering with QAR

### Registration Methods

```yaml
# Method 1: Auto-discovery (recommended)
# Place agent in .quad/agents/ directory
# QAR scans and registers on startup

# Method 2: Explicit registration in quad.config.yaml
agents:
  cobol-analyzer-agent:
    path: ./.quad/agents/cobol-analyzer-agent.ts
    enabled: true

# Method 3: Programmatic registration
# In your app's startup code:
```

```typescript
// Method 3: Programmatic
import { QARRuntime } from '@quad/agent-runtime';
import { CobolAnalyzerAgent } from './agents/cobol-analyzer-agent';

const runtime = new QARRuntime();
runtime.registerAgent(new CobolAnalyzerAgent());
```

### Verification

```bash
# List all registered agents
quad agent list

# Check specific agent
quad agent info cobol-analyzer-agent

# Test agent permissions
quad agent permissions cobol-analyzer-agent
```

---

## Examples

### Example 1: Security Scanner Agent (Custom)

```typescript
// Strict security agent with mandatory findings report
export class SecurityScannerAgent implements QUADAgent {
  readonly agentId = 'security-scanner-agent';
  readonly requiresApproval = false;  // Can run automatically

  readonly canRead = [
    { resource: 'src/**', level: PermissionLevel.READ },
    { resource: 'package*.json', level: PermissionLevel.READ }
  ];

  readonly canWrite = [
    { resource: 'security-reports/**', level: PermissionLevel.WRITE }
  ];

  // This agent ALWAYS generates a report, even if no issues
  async invoke(input: AgentInput): Promise<AgentOutput> {
    const findings = await this.scanForVulnerabilities(input.data.target);

    // STRICT RULE: Always write report
    await this.writeReport(findings);

    // STRICT RULE: Block if critical findings
    if (findings.critical > 0) {
      return {
        ...this.baseOutput(input),
        success: false,
        error: `BLOCKED: ${findings.critical} critical vulnerabilities found`,
        data: { findings, blocked: true }
      };
    }

    return {
      ...this.baseOutput(input),
      success: true,
      data: { findings, blocked: false }
    };
  }
}
```

### Example 2: Extending Estimation Agent

```typescript
// Add industry-specific complexity factors
export class GlobalRetailEstimationAgent extends EstimationAgent {

  // Add COBOL factor to estimates
  protected calculateComplexity(analysis: any): number {
    let baseComplexity = super.calculateComplexity(analysis);

    // GlobalRetail-specific: COBOL adds 50% complexity
    if (analysis.touches_cobol) {
      baseComplexity *= 1.5;
    }

    // GlobalRetail-specific: Oracle stored procs add 30%
    if (analysis.uses_stored_procedures) {
      baseComplexity *= 1.3;
    }

    return baseComplexity;
  }
}
```

---

## Summary

| Approach | Use Case | Effort |
|----------|----------|--------|
| **Create from scratch** | Completely new functionality | High |
| **Extend existing** | Add rules to built-in agent | Medium |
| **Configure via YAML** | Restrict/tighten existing agent | Low |

**Recommendation:**
1. Start with YAML configuration (Option C) for quick wins
2. Extend existing agents (Option B) for custom logic
3. Create from scratch (Option A) only for unique needs

---

*Part of QUAD™ (Quick Unified Agentic Development) Methodology*
*© 2025 Suman Addanke / A2 Vibe Creators LLC*
