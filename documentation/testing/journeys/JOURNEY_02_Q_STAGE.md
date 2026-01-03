# QUAD Framework - Test Scenarios: Journey 2 - Q-Stage (Requirements Analysis)

**Author:** Suman Addanke
**Version:** 1.0
**Last Updated:** January 2, 2026

---

## Overview

This document contains end-to-end test scenarios for **Journey 2: Q-Stage (Question/Requirements Analysis)**.

**Q-U-A-D Stage:** Q = Question (Analyze requirements, estimate complexity)

**Features Covered:**
- Document Upload (URLs → Phase 1)
- AI Requirement Analysis
- Confidence Scoring
- Flow Generation from Requirements
- Stream/Milestone Creation
- Trajectory Prediction

**Flow Accelerators Tested:**
- **Magnitude Estimator** - Estimates Flow complexity
- **Trajectory Predictor** - Predicts Cycle outcomes

---

## Prerequisites

Before testing, ensure:

- [ ] Journey 1 completed (User, Org, Circle, Domain created)
- [ ] AI tier configured (Quality recommended for testing)
- [ ] Anthropic API key configured in `.env`
- [ ] Sample PRD document available for upload

---

## SECTION A: DOCUMENT UPLOAD

---

## Scenario 1A: Upload Requirement Document (URL)

**User Type:** Business Analyst / Circle Lead
**Features Tested:** Document Import (Phase 1 = URL only)

### Steps:

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 1A.1 | Navigate to Domain "Mobile App v2" | See Domain dashboard | [ ] |
| 1A.2 | Click "Import Requirements" | See import modal | [ ] |
| 1A.3 | Select "From URL" tab | URL input shown | [ ] |
| 1A.4 | Enter URL: `https://docs.google.com/doc/PRD` | URL field accepts input | [ ] |
| 1A.5 | Click "Import" | Loading indicator | [ ] |
| 1A.6 | Wait for processing | Document imported | [ ] |
| 1A.7 | Verify document in list | "PRD" document shown | [ ] |
| 1A.8 | Click on document | See document preview | [ ] |

### API Endpoints Tested:
- `POST /api/documents/import`
- `GET /api/domains/{id}/documents`

### Expected Database State:
```sql
-- QUAD_file_imports
SELECT * FROM "QUAD_file_imports" WHERE domain_id = '<domain_id>';
-- Should have 1 row with source_url, import_status = 'completed'
```

---

## Scenario 1B: Upload Multiple Documents

**User Type:** Business Analyst
**Features Tested:** Bulk Document Import

### Steps:

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 1B.1 | Click "Import Requirements" again | See import modal | [ ] |
| 1B.2 | Add URL: Confluence page | URL accepted | [ ] |
| 1B.3 | Add another URL: Figma spec | Second URL accepted | [ ] |
| 1B.4 | Click "Import All" | Bulk import starts | [ ] |
| 1B.5 | See progress indicator | Shows "Importing 2 of 3" | [ ] |
| 1B.6 | Verify all documents imported | 3 documents in list | [ ] |

### API Endpoints Tested:
- `POST /api/documents/import/bulk`

---

## SECTION B: AI REQUIREMENT ANALYSIS

---

## Scenario 2A: Analyze Document with AI

**User Type:** Business Analyst
**Features Tested:** AI Requirement Extraction

### Steps:

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 2A.1 | From document list, click "Analyze" on PRD | Analysis modal opens | [ ] |
| 2A.2 | See AI options | "Extract Requirements" shown | [ ] |
| 2A.3 | Click "Extract Requirements" | Loading: "AI analyzing..." | [ ] |
| 2A.4 | Wait for AI response | Analysis complete | [ ] |
| 2A.5 | See extracted requirements list | Multiple requirements shown | [ ] |
| 2A.6 | Each requirement has title | Titles displayed | [ ] |
| 2A.7 | Each requirement has description | Descriptions shown | [ ] |
| 2A.8 | Each requirement has AI confidence | Percentage shown (e.g., 92%) | [ ] |

### API Endpoints Tested:
- `POST /api/ai/analyze-document`
- `GET /api/requirements?documentId={id}`

### AI Response Format:
```json
{
  "requirements": [
    {
      "title": "User Authentication",
      "description": "Implement OAuth2 login with Google/Apple",
      "priority": "HIGH",
      "category": "SECURITY",
      "aiConfidence": 94,
      "suggestedEffort": "M"
    }
  ],
  "summary": "PRD contains 12 requirements across 4 categories",
  "overallConfidence": 89
}
```

---

## Scenario 2B: Review AI Confidence Scoring

**User Type:** Business Analyst
**Features Tested:** Confidence Display & Human Override

### Steps:

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 2B.1 | View extracted requirements | Confidence scores visible | [ ] |
| 2B.2 | Find requirement with 90%+ confidence | Shows "Recommended" badge | [ ] |
| 2B.3 | Find requirement with 70-89% confidence | Shows "Review Carefully" warning | [ ] |
| 2B.4 | Find requirement with <70% confidence | Shows "Manual Review Required" | [ ] |
| 2B.5 | Click on low-confidence requirement | See details modal | [ ] |
| 2B.6 | See "AI reasoning" section | Explains why confidence is low | [ ] |
| 2B.7 | Option to approve anyway | "Override" button available | [ ] |
| 2B.8 | Option to edit | "Edit" button available | [ ] |

### Confidence Levels:

| Score | Badge | Color | Action Required |
|-------|-------|-------|-----------------|
| 90%+ | Recommended | Green | Can auto-approve |
| 70-89% | Review Carefully | Yellow | Manual review |
| <70% | Manual Review Required | Red | Must override |

---

## Scenario 2C: Edit AI-Generated Requirement

**User Type:** Business Analyst
**Features Tested:** Human Override

### Steps:

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 2C.1 | Click "Edit" on a requirement | Edit form opens | [ ] |
| 2C.2 | Modify title | Title field editable | [ ] |
| 2C.3 | Modify description | Description field editable | [ ] |
| 2C.4 | Change priority from HIGH to MEDIUM | Priority dropdown works | [ ] |
| 2C.5 | Click "Save Changes" | Success message | [ ] |
| 2C.6 | Verify "Human Edited" badge | Shows edited indicator | [ ] |
| 2C.7 | AI confidence now shows "N/A - Human Edited" | Override logged | [ ] |

### API Endpoints Tested:
- `PATCH /api/requirements/{id}`

---

## SECTION C: FLOW GENERATION

---

## Scenario 3A: Generate Flows from Requirements

**User Type:** Circle Lead
**Features Tested:** Requirement → Flow Conversion

### Steps:

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 3A.1 | From requirements list, select multiple | Checkboxes work | [ ] |
| 3A.2 | Click "Generate Flows" | AI generation modal | [ ] |
| 3A.3 | See AI suggestion preview | Draft Flows shown | [ ] |
| 3A.4 | Each Flow has title, description | Content displayed | [ ] |
| 3A.5 | Each Flow has effort estimate | S/M/L/XL shown | [ ] |
| 3A.6 | Each Flow linked to requirement | Source requirement visible | [ ] |
| 3A.7 | Click "Create Flows" | Loading indicator | [ ] |
| 3A.8 | Success message | "5 Flows created" | [ ] |
| 3A.9 | Navigate to Domain Canvas | Flows visible in backlog | [ ] |

### API Endpoints Tested:
- `POST /api/ai/generate-flows`
- `POST /api/flows/bulk`
- `GET /api/domains/{id}/flows`

### Expected Flow Structure:
```json
{
  "title": "Implement Google OAuth",
  "description": "Add Google Sign-In button, handle OAuth callback...",
  "priority": "HIGH",
  "effort": "M",
  "sourceRequirementId": "<requirement_id>",
  "aiGenerated": true,
  "aiConfidence": 88
}
```

---

## Scenario 3B: Magnitude Estimation (Complexity)

**User Type:** Circle Lead
**Features Tested:** Magnitude Estimator Flow Accelerator

### Steps:

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 3B.1 | From Flow details, click "Estimate Complexity" | AI modal opens | [ ] |
| 3B.2 | AI analyzes Flow | Loading indicator | [ ] |
| 3B.3 | See complexity breakdown | Multiple factors shown | [ ] |
| 3B.4 | See "Technical Complexity" score | 1-10 scale | [ ] |
| 3B.5 | See "Domain Knowledge" score | 1-10 scale | [ ] |
| 3B.6 | See "Integration Points" count | Number shown | [ ] |
| 3B.7 | See "Risk Factors" | List of risks | [ ] |
| 3B.8 | See overall "Magnitude" | S/M/L/XL recommendation | [ ] |
| 3B.9 | Click "Accept Estimate" | Flow updated with estimate | [ ] |

### API Endpoints Tested:
- `POST /api/ai/estimate-magnitude`

### Magnitude Output:
```json
{
  "flowId": "<flow_id>",
  "magnitude": "M",
  "confidence": 85,
  "breakdown": {
    "technicalComplexity": 6,
    "domainKnowledge": 4,
    "integrationPoints": 3,
    "riskFactors": ["Third-party API dependency", "Security implications"]
  },
  "reasoning": "OAuth implementation requires moderate technical skill..."
}
```

---

## SECTION D: STREAM MANAGEMENT

---

## Scenario 4A: Create Stream from Flows

**User Type:** Circle Lead
**Features Tested:** Stream (Epic) Creation

### Steps:

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 4A.1 | From Domain Canvas, select related Flows | Multiple Flows selected | [ ] |
| 4A.2 | Click "Create Stream" | Stream creation modal | [ ] |
| 4A.3 | Enter name: "Authentication Epic" | Name field accepts input | [ ] |
| 4A.4 | Enter description | Description accepts input | [ ] |
| 4A.5 | See auto-added Flows | Selected Flows shown | [ ] |
| 4A.6 | Click "Create Stream" | Success message | [ ] |
| 4A.7 | Verify Stream in sidebar | "Authentication Epic" visible | [ ] |
| 4A.8 | Click on Stream | See Stream details with child Flows | [ ] |

### API Endpoints Tested:
- `POST /api/streams`
- `POST /api/streams/{id}/flows`
- `GET /api/domains/{id}/streams`

---

## Scenario 4B: View Stream Progress

**User Type:** Any Circle Member
**Features Tested:** Stream Progress Tracking

### Steps:

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 4B.1 | From Stream details, see progress bar | Visual progress shown | [ ] |
| 4B.2 | See "X of Y Flows completed" | Count displayed | [ ] |
| 4B.3 | See effort breakdown | Total effort vs completed | [ ] |
| 4B.4 | See child Flow list | All Flows in Stream visible | [ ] |
| 4B.5 | Filter by status | Status filter works | [ ] |

### API Endpoints Tested:
- `GET /api/streams/{id}`
- `GET /api/streams/{id}/progress`

---

## SECTION E: TRAJECTORY PREDICTION

---

## Scenario 5A: Predict Cycle Outcome

**User Type:** Circle Lead
**Features Tested:** Trajectory Predictor Flow Accelerator

### Precondition:
- At least one Cycle exists with some Flows

### Steps:

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 5A.1 | Navigate to active Cycle | Cycle dashboard shown | [ ] |
| 5A.2 | Click "Predict Trajectory" | AI prediction modal | [ ] |
| 5A.3 | AI analyzes Cycle | Loading indicator | [ ] |
| 5A.4 | See prediction result | Trajectory displayed | [ ] |
| 5A.5 | See "On Track" / "At Risk" / "Behind" | Status indicator | [ ] |
| 5A.6 | See velocity trend | Graph or number | [ ] |
| 5A.7 | See completion prediction | "Expected: 85% complete" | [ ] |
| 5A.8 | See risk factors | List of concerns | [ ] |
| 5A.9 | See AI recommendations | Suggested actions | [ ] |

### API Endpoints Tested:
- `POST /api/ai/predict-trajectory`
- `GET /api/cycles/{id}/predictions`

### Trajectory Output:
```json
{
  "cycleId": "<cycle_id>",
  "status": "AT_RISK",
  "confidence": 78,
  "predictedCompletion": 75,
  "velocityTrend": "DECLINING",
  "riskFactors": [
    "2 blocked Flows for >3 days",
    "Key developer on PTO next week"
  ],
  "recommendations": [
    "Consider moving FLOW-123 to next Cycle",
    "Pair junior dev with blocked Flow"
  ]
}
```

---

## API Endpoint Coverage Matrix

### Documents

| Endpoint | Method | Scenario(s) |
|----------|--------|-------------|
| `/api/documents/import` | POST | 1A |
| `/api/documents/import/bulk` | POST | 1B |
| `/api/domains/{id}/documents` | GET | 1A, 1B |

### AI Analysis

| Endpoint | Method | Scenario(s) |
|----------|--------|-------------|
| `/api/ai/analyze-document` | POST | 2A |
| `/api/ai/generate-flows` | POST | 3A |
| `/api/ai/estimate-magnitude` | POST | 3B |
| `/api/ai/predict-trajectory` | POST | 5A |

### Requirements

| Endpoint | Method | Scenario(s) |
|----------|--------|-------------|
| `/api/requirements` | GET | 2A |
| `/api/requirements/{id}` | PATCH | 2C |

### Flows

| Endpoint | Method | Scenario(s) |
|----------|--------|-------------|
| `/api/flows/bulk` | POST | 3A |
| `/api/domains/{id}/flows` | GET | 3A |

### Streams

| Endpoint | Method | Scenario(s) |
|----------|--------|-------------|
| `/api/streams` | POST | 4A |
| `/api/streams/{id}` | GET | 4B |
| `/api/streams/{id}/flows` | POST | 4A |
| `/api/streams/{id}/progress` | GET | 4B |
| `/api/domains/{id}/streams` | GET | 4A |

### Predictions

| Endpoint | Method | Scenario(s) |
|----------|--------|-------------|
| `/api/cycles/{id}/predictions` | GET | 5A |

---

## Test Results Summary

| Scenario | Description | Status | Notes |
|----------|-------------|--------|-------|
| 1A | Upload Requirement Document (URL) | [ ] Pending | |
| 1B | Upload Multiple Documents | [ ] Pending | |
| 2A | Analyze Document with AI | [ ] Pending | |
| 2B | Review AI Confidence Scoring | [ ] Pending | |
| 2C | Edit AI-Generated Requirement | [ ] Pending | |
| 3A | Generate Flows from Requirements | [ ] Pending | |
| 3B | Magnitude Estimation (Complexity) | [ ] Pending | |
| 4A | Create Stream from Flows | [ ] Pending | |
| 4B | View Stream Progress | [ ] Pending | |
| 5A | Predict Cycle Outcome | [ ] Pending | |

**Total Scenarios:** 10
**Passed:** ___ / 10
**Failed:** ___ / 10

---

## Implementation Status (Gap Analysis)

| Feature | Table | API | UI | Status |
|---------|-------|-----|----|----|
| Document Upload | QUAD_file_imports | Partial | Yes | 60% |
| AI Requirement Analysis | QUAD_requirements | Partial | Partial | 40% |
| Confidence Scoring | Fields exist | Yes | Yes | 80% |
| Flow Generation | QUAD_flows | Partial | Yes | 50% |
| Magnitude Estimation | Fields exist | No | No | 10% |
| Stream Management | QUAD_milestones | Yes | Partial | 60% |
| Trajectory Prediction | QUAD_cycle_risk_predictions | No | No | 5% |

**Overall Q-Stage: ~50% Complete**

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Jan 2, 2026 | Initial version - 10 scenarios |

---
