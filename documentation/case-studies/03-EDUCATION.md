# Case Study: Education Platform

**Domain:** Education
**Company Size:** Small Institution (50-100 students)
**Timeline:** 10 weeks MVP
**Budget:** Non-profit ($200-400/month)

---

## Scenario

**Organization:** BrightPath Academy
**Type:** After-school tutoring center
**Location:** San Jose, California
**Staff:**
- Director (Sarah)
- 5 Tutors (part-time)
- 2 Admin Staff
- 50-80 students (K-12)

**Goal:** Replace paper-based tracking with digital platform for student progress, scheduling, and parent communication.

---

## Domain-Specific Terminology

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    EDUCATION DOMAIN GLOSSARY                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  STUDENT TERMS:                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  Enrollment     Student registration for courses/sessions        │   │
│  │  Grade Level    K, 1-12, or subject-based level                 │   │
│  │  Learning Plan  Personalized goals and curriculum               │   │
│  │  Assessment     Test, quiz, or evaluation                        │   │
│  │  Progress       Skill advancement tracking                       │   │
│  │  Benchmark      Expected level at given point                    │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  SESSION TERMS:                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  Session        One tutoring appointment (typically 1 hour)      │   │
│  │  Subject        Math, Reading, Science, etc.                     │   │
│  │  Curriculum     Structured learning content                      │   │
│  │  Homework       Assigned practice work                           │   │
│  │  Attendance     Present, absent, late tracking                   │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  BUSINESS TERMS:                                                        │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  Package        Bundle of sessions (e.g., 10-pack)               │   │
│  │  Subscription   Monthly unlimited sessions                       │   │
│  │  Make-up        Rescheduled missed session                       │   │
│  │  Tutor:Student  Ratio (1:1, 1:3, etc.)                          │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## QUAD Methodology Application

### Phase Q: Question

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    PHASE Q: QUESTIONING                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Q1: What is this project?                                              │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  "BrightPath LMS - Digital platform for our tutoring center     │   │
│  │   to track student progress and communicate with parents"       │   │
│  │                                                                  │   │
│  │  Extracted:                                                      │   │
│  │  • Title: BrightPath Academy Platform                            │   │
│  │  • Type: Education / Tutoring Management                         │   │
│  │  • Scale: 50-100 students, 5-8 tutors                            │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  Q2: Who are the users?                                                 │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  User Personas:                                                  │   │
│  │  • Parent (books sessions, views progress, pays)                 │   │
│  │  • Student (sees schedule, completes homework)                   │   │
│  │  • Tutor (records progress, manages schedule)                    │   │
│  │  • Admin (manages enrollments, billing, reports)                 │   │
│  │  • Director (overview, analytics, staff management)              │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  Q3: What are the must-have features?                                   │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  MVP Features:                                                   │   │
│  │  ✓ Student enrollment & profiles                                 │   │
│  │  ✓ Session scheduling (parent books, tutor manages)              │   │
│  │  ✓ Attendance tracking                                           │   │
│  │  ✓ Progress notes per session                                    │   │
│  │  ✓ Parent dashboard (view progress)                              │   │
│  │  ✓ Simple billing (packages, invoices)                           │   │
│  │  ✓ Session reminders (SMS/email)                                 │   │
│  │                                                                  │   │
│  │  Phase 2:                                                        │   │
│  │  ✗ Online homework submission                                    │   │
│  │  ✗ Video tutoring                                                │   │
│  │  ✗ Assessment/quiz builder                                       │   │
│  │  ✗ Curriculum marketplace                                        │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  Q4: What are the constraints?                                          │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  • Budget: Non-profit, minimal monthly costs                     │   │
│  │  • Privacy: FERPA awareness (student data)                       │   │
│  │  • Accessibility: Parents may not be tech-savvy                  │   │
│  │  • Timeline: Ready before fall semester (10 weeks)               │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Phase U: Understand

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    PHASE U: UNDERSTANDING                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  System Architecture:                                                   │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                                                                  │   │
│  │   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐     │   │
│  │   │   Parent     │    │    Tutor     │    │    Admin     │     │   │
│  │   │   Portal     │    │  Dashboard   │    │   Console    │     │   │
│  │   │  (Next.js)   │    │  (Next.js)   │    │  (Next.js)   │     │   │
│  │   └──────┬───────┘    └──────┬───────┘    └──────┬───────┘     │   │
│  │          │                   │                   │              │   │
│  │          └───────────┬───────┴───────────────────┘              │   │
│  │                      │                                          │   │
│  │                      ▼                                          │   │
│  │           ┌──────────────────────┐                              │   │
│  │           │   Next.js API        │                              │   │
│  │           │  (App Router)        │                              │   │
│  │           └──────────┬───────────┘                              │   │
│  │                      │                                          │   │
│  │      ┌───────────────┼───────────────┐                          │   │
│  │      │               │               │                          │   │
│  │      ▼               ▼               ▼                          │   │
│  │  ┌────────┐    ┌──────────┐    ┌──────────┐                    │   │
│  │  │Supabase│    │  Stripe  │    │  Twilio  │                    │   │
│  │  │  (DB)  │    │(Payments)│    │  (SMS)   │                    │   │
│  │  └────────┘    └──────────┘    └──────────┘                    │   │
│  │                                                                  │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  Tech Stack:                                                            │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  Frontend:  Next.js 14 + Tailwind + shadcn/ui                   │   │
│  │  Backend:   Next.js API Routes                                  │   │
│  │  Database:  Supabase (PostgreSQL + Auth)                        │   │
│  │  Payments:  Stripe                                              │   │
│  │  SMS:       Twilio                                              │   │
│  │  Hosting:   Vercel (free tier)                                  │   │
│  │  Calendar:  react-big-calendar                                  │   │
│  │                                                                  │   │
│  │  Monthly Cost: ~$50-100 (Twilio SMS + minimal)                  │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Phase A: Allocate

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    PHASE A: ALLOCATION                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  EPIC 1: User Management (Week 1-2)                              │   │
│  │  ─────────────────────────────────                               │   │
│  │  • BP-001: Parent registration with email verification           │   │
│  │  • BP-002: Parent login + password reset                         │   │
│  │  • BP-003: Add student profiles (multiple per parent)            │   │
│  │  • BP-004: Tutor accounts (admin creates)                        │   │
│  │  • BP-005: Admin/Director accounts                               │   │
│  │                                                                  │   │
│  │  Traditional: 30h | AI-Assisted: 6h | Assigned: 10h             │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  EPIC 2: Scheduling System (Week 2-4)                            │   │
│  │  ───────────────────────────────────                             │   │
│  │  • BP-010: Tutor availability management                         │   │
│  │  • BP-011: Session booking by parent                             │   │
│  │  • BP-012: Calendar view (tutor daily/weekly)                    │   │
│  │  • BP-013: Recurring session support                             │   │
│  │  • BP-014: Cancellation/rescheduling                             │   │
│  │  • BP-015: Make-up session tracking                              │   │
│  │                                                                  │   │
│  │  Traditional: 50h | AI-Assisted: 10h | Assigned: 16h            │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  EPIC 3: Attendance & Progress (Week 4-6)                        │   │
│  │  ──────────────────────────────────────                          │   │
│  │  • BP-020: Session check-in (tutor marks attendance)             │   │
│  │  • BP-021: Progress notes form                                   │   │
│  │  • BP-022: Skill tracking (per subject)                          │   │
│  │  • BP-023: Parent progress view                                  │   │
│  │  • BP-024: Progress report generation (PDF)                      │   │
│  │                                                                  │   │
│  │  Traditional: 40h | AI-Assisted: 8h | Assigned: 14h             │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  EPIC 4: Billing & Packages (Week 6-7)                           │   │
│  │  ────────────────────────────────────                            │   │
│  │  • BP-030: Package creation (10-pack, 20-pack)                   │   │
│  │  • BP-031: Session balance tracking                              │   │
│  │  • BP-032: Invoice generation                                    │   │
│  │  • BP-033: Stripe payment integration                            │   │
│  │  • BP-034: Payment history                                       │   │
│  │                                                                  │   │
│  │  Traditional: 35h | AI-Assisted: 7h | Assigned: 12h             │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  EPIC 5: Notifications (Week 7-8)                                │   │
│  │  ─────────────────────────────                                   │   │
│  │  • BP-040: Session reminder (24h before)                         │   │
│  │  • BP-041: Low balance alert                                     │   │
│  │  • BP-042: Progress note notification                            │   │
│  │  • BP-043: Notification preferences                              │   │
│  │                                                                  │   │
│  │  Traditional: 25h | AI-Assisted: 5h | Assigned: 8h              │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  EPIC 6: Admin Dashboard (Week 8-9)                              │   │
│  │  ─────────────────────────────────                               │   │
│  │  • BP-050: Student roster management                             │   │
│  │  • BP-051: Tutor schedule overview                               │   │
│  │  • BP-052: Revenue reports                                       │   │
│  │  • BP-053: Attendance reports                                    │   │
│  │  • BP-054: Export data (CSV)                                     │   │
│  │                                                                  │   │
│  │  Traditional: 35h | AI-Assisted: 7h | Assigned: 12h             │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  EPIC 7: Testing & Launch (Week 9-10)                            │   │
│  │  ─────────────────────────────────────                           │   │
│  │  • BP-060: User acceptance testing                               │   │
│  │  • BP-061: Bug fixes                                             │   │
│  │  • BP-062: Data migration (existing students)                    │   │
│  │  • BP-063: Staff training                                        │   │
│  │  • BP-064: Go-live                                               │   │
│  │                                                                  │   │
│  │  Traditional: 25h | AI-Assisted: 5h | Assigned: 10h             │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  TOTAL:                                                                 │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  Traditional: 240 hours (15 weeks at 16h/week)                  │   │
│  │  AI-Assisted:  48 hours                                         │   │
│  │  With Buffer:  82 hours                                         │   │
│  │                                                                  │   │
│  │  QUAD Schedule: 82h ÷ 16h/week = 5 weeks (build)                │   │
│  │  + Testing/Training: 2 weeks                                     │   │
│  │  + Buffer: 3 weeks                                               │   │
│  │  Final: 10 weeks MVP ✓                                           │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Sample Education Tickets

### Ticket BP-021: Progress Notes Form

```
┌─────────────────────────────────────────────────────────────────────────┐
│  TICKET: BP-021                                                         │
│  EPIC: Attendance & Progress                                            │
│  STATUS: Backlog                                                        │
│  ASSIGNEE: Developer                                                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  TITLE: Create Session Progress Notes Form for Tutors                   │
│                                                                         │
│  DESCRIPTION:                                                           │
│  As a tutor, I need to quickly record session notes after each          │
│  tutoring session so parents can see what their child learned.          │
│                                                                         │
│  ACCEPTANCE CRITERIA:                                                   │
│  ✓ Form appears after marking attendance "present"                      │
│  ✓ Fields: Topics covered (multi-select), Notes (text), Homework        │
│  ✓ Skill rating (1-5 stars) for each topic                              │
│  ✓ Quick templates for common feedback                                  │
│  ✓ Auto-save draft every 30 seconds                                     │
│  ✓ Mobile-friendly for tablet use                                       │
│  ✓ Notifies parent when submitted                                       │
│                                                                         │
│  UI MOCKUP:                                                             │
│  ┌───────────────────────────────────────────────────────────────┐     │
│  │  SESSION NOTES - Emma Johnson (Grade 4 Math)                   │     │
│  │  Date: Jan 15, 2026 | 4:00 PM - 5:00 PM                       │     │
│  │  ─────────────────────────────────────────────────────────────│     │
│  │                                                               │     │
│  │  Topics Covered:                                              │     │
│  │  [x] Multiplication    ★★★★☆                                  │     │
│  │  [x] Division          ★★★☆☆                                  │     │
│  │  [ ] Fractions                                                │     │
│  │  [ ] Word Problems                                            │     │
│  │                                                               │     │
│  │  Session Notes:                                               │     │
│  │  ┌─────────────────────────────────────────────────────────┐ │     │
│  │  │ Emma showed great improvement in multiplication today!  │ │     │
│  │  │ She can now do 2-digit × 1-digit problems confidently.  │ │     │
│  │  │ Division still needs practice - recommend extra work... │ │     │
│  │  └─────────────────────────────────────────────────────────┘ │     │
│  │                                                               │     │
│  │  Homework Assigned:                                           │     │
│  │  ┌─────────────────────────────────────────────────────────┐ │     │
│  │  │ Worksheet 4.3 - Division practice (20 problems)         │ │     │
│  │  └─────────────────────────────────────────────────────────┘ │     │
│  │                                                               │     │
│  │  Quick Templates: [Great Session] [Needs Review] [Homework]   │     │
│  │                                                               │     │
│  │  [Save Draft]                         [Submit & Notify Parent]│     │
│  └───────────────────────────────────────────────────────────────┘     │
│                                                                         │
│  TIME ESTIMATES:                                                        │
│  ┌───────────────────────────────────────────────────────────────┐     │
│  │  Traditional:     6 hours                                      │     │
│  │  AI-Assisted:     1.5 hours                                    │     │
│  │  Assigned:        2.5 hours (65% buffer)                       │     │
│  │                                                                │     │
│  │  AI Trust Level:  4/5 (standard form, high trust)             │     │
│  └───────────────────────────────────────────────────────────────┘     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Ticket BP-022: Skill Tracking System

```
┌─────────────────────────────────────────────────────────────────────────┐
│  TICKET: BP-022                                                         │
│  EPIC: Attendance & Progress                                            │
│  STATUS: Backlog                                                        │
│  ASSIGNEE: Developer                                                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  TITLE: Implement Skill Progress Tracking by Subject                    │
│                                                                         │
│  DESCRIPTION:                                                           │
│  As a parent, I want to see my child's progress over time in            │
│  specific skills so I know where they're improving.                     │
│                                                                         │
│  ACCEPTANCE CRITERIA:                                                   │
│  ✓ Define skills per subject (Math: Addition, Subtraction, etc.)        │
│  ✓ Track skill ratings from session notes over time                     │
│  ✓ Show progress chart (line graph over sessions)                       │
│  ✓ Benchmark indicators (grade-level expectations)                      │
│  ✓ Color coding: Red (below), Yellow (at), Green (above) benchmark     │
│                                                                         │
│  SKILL HIERARCHY:                                                       │
│  ┌───────────────────────────────────────────────────────────────┐     │
│  │  Math (Grade 4):                                               │     │
│  │  ├── Addition & Subtraction (benchmark: 4/5 by Oct)           │     │
│  │  ├── Multiplication (benchmark: 3/5 by Dec)                   │     │
│  │  ├── Division (benchmark: 3/5 by Feb)                         │     │
│  │  ├── Fractions (benchmark: 2/5 by Apr)                        │     │
│  │  └── Word Problems (benchmark: 3/5 by Jun)                    │     │
│  │                                                                │     │
│  │  Reading (Grade 4):                                            │     │
│  │  ├── Fluency (benchmark: 4/5 by Oct)                          │     │
│  │  ├── Comprehension (benchmark: 3/5 by Dec)                    │     │
│  │  ├── Vocabulary (benchmark: 3/5 by Feb)                       │     │
│  │  └── Writing (benchmark: 3/5 by Apr)                          │     │
│  └───────────────────────────────────────────────────────────────┘     │
│                                                                         │
│  PROGRESS VISUALIZATION:                                                │
│  ┌───────────────────────────────────────────────────────────────┐     │
│  │  Emma's Math Progress - Multiplication                         │     │
│  │                                                                │     │
│  │  5 │                                    ●──●                   │     │
│  │  4 │                          ●────●──●                        │     │
│  │  3 │     ═══════════════════════════════════ Benchmark        │     │
│  │  2 │        ●────●                                             │     │
│  │  1 │  ●──●                                                     │     │
│  │    └──────────────────────────────────────────────────────    │     │
│  │       Sep  Oct   Nov   Dec   Jan   Feb                         │     │
│  │                                                                │     │
│  │  Status: ████ ABOVE BENCHMARK (+1 level)                       │     │
│  └───────────────────────────────────────────────────────────────┘     │
│                                                                         │
│  TIME ESTIMATES:                                                        │
│  ┌───────────────────────────────────────────────────────────────┐     │
│  │  Traditional:     8 hours                                      │     │
│  │  AI-Assisted:     2 hours                                      │     │
│  │  Assigned:        3 hours (50% buffer)                        │     │
│  └───────────────────────────────────────────────────────────────┘     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Education-Specific Workflows

### Student Journey

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    STUDENT LEARNING JOURNEY                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ENROLLMENT PHASE:                                                      │
│  ┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐          │
│  │ Parent  │────▶│ Create  │────▶│  Add    │────▶│Purchase │          │
│  │ Signup  │     │ Account │     │ Student │     │ Package │          │
│  └─────────┘     └─────────┘     └─────────┘     └─────────┘          │
│                                                                         │
│  LEARNING PHASE (Weekly Cycle):                                         │
│  ┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐          │
│  │ Parent  │────▶│ Session │────▶│ Tutor   │────▶│ Progress│          │
│  │ Books   │     │ Reminder│     │ Session │     │  Notes  │          │
│  │ Session │     │  (24h)  │     │         │     │         │          │
│  └─────────┘     └─────────┘     └─────────┘     └─────────┘          │
│       │                               │               │                │
│       │                               ▼               ▼                │
│       │                         ┌─────────┐     ┌─────────┐           │
│       │                         │Attendance│    │ Parent  │           │
│       │                         │ Marked   │    │ Notified│           │
│       │                         └─────────┘     └─────────┘           │
│       │                                                                │
│       └──────────── REPEAT WEEKLY ─────────────────────────────────   │
│                                                                         │
│  REVIEW PHASE (Monthly):                                                │
│  ┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐          │
│  │ Parent  │────▶│ View    │────▶│Download │────▶│ Renew   │          │
│  │ Reviews │     │ Progress│     │ Report  │     │ Package │          │
│  │ Progress│     │ Charts  │     │  (PDF)  │     │         │          │
│  └─────────┘     └─────────┘     └─────────┘     └─────────┘          │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Tutor Daily Workflow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    TUTOR DAILY WORKFLOW                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  START OF DAY:                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  1. Open Dashboard                                               │   │
│  │  2. View today's schedule (4 sessions)                           │   │
│  │  3. Review student notes from last session                       │   │
│  │  4. Prepare materials                                            │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  DURING SESSION:                                                        │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  1. Mark student as "Arrived" (check-in)                         │   │
│  │  2. Quick review of learning plan                                │   │
│  │  3. Conduct tutoring (use tablet for reference)                  │   │
│  │  4. Note observations mentally                                   │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  AFTER SESSION (5 min):                                                 │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  1. Open Progress Notes form                                     │   │
│  │  2. Select topics covered                                        │   │
│  │  3. Rate skills (star rating)                                    │   │
│  │  4. Add brief notes (use template if applicable)                 │   │
│  │  5. Assign homework                                              │   │
│  │  6. Submit (parent auto-notified)                                │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  END OF DAY:                                                            │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  1. Verify all sessions have notes                               │   │
│  │  2. Update availability for next week                            │   │
│  │  3. Review messages from parents                                 │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Tool Stack (Education Non-Profit)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    BRIGHTPATH TOOL STACK                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  INFRASTRUCTURE:                                                        │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  Vercel           FREE      Hosting (hobby tier)                 │   │
│  │  Supabase         FREE      Database + Auth (free tier)          │   │
│  │  Cloudinary       FREE      Image storage                        │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  COMMUNICATION:                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  Twilio           ~$30/mo   SMS reminders (~500 SMS)             │   │
│  │  SendGrid         FREE      Email notifications (100/day)        │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  PAYMENTS:                                                              │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  Stripe           2.9%+30¢  Package purchases                    │   │
│  │                   per txn   (non-profit rate available)          │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  PROJECT MANAGEMENT:                                                    │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  QUAD Platform    FREE      Project management                   │   │
│  │  Notion           FREE      Documentation                        │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  TOTAL MONTHLY COST:                                                    │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  Fixed:           ~$30/month (Twilio SMS)                        │   │
│  │  Variable:        2.9% + $0.30 per payment                       │   │
│  │                                                                  │   │
│  │  Typical month (50 students, 10 package purchases):              │   │
│  │  SMS: $30                                                        │   │
│  │  Stripe: 10 × ($8.70 + $0.30) = $90                              │   │
│  │  ─────────────────────────────────────                           │   │
│  │  Total: ~$120/month                                              │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Adoption Matrix Position (Education)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    BRIGHTPATH ADOPTION JOURNEY                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  STARTING POSITION: Zone E (Transition Sweet Spot)                      │
│  Education can adopt QUAD relatively quickly                            │
│                                                                         │
│  AI Trust                                                               │
│     +5  ┌───────────────┬───────────────┬───────────────┐               │
│         │    ZONE G     │    ZONE H     │    ZONE I     │               │
│   HIGH  │               │   (Week 12)   │   ★ GOAL      │               │
│         │               │               │   (Week 16+)  │               │
│         ├───────────────┼───────────────┼───────────────┤               │
│         │    ZONE D     │    ZONE E     │    ZONE F     │               │
│   MED   │               │  ★ START      │   (Week 6)    │               │
│         │               │  (Week 1)     │               │               │
│         ├───────────────┼───────────────┼───────────────┤               │
│         │    ZONE A     │    ZONE B     │    ZONE C     │               │
│   LOW   │               │               │               │               │
│         │               │               │               │               │
│      0  └───────────────┴───────────────┴───────────────┘               │
│              0              +3              +5                           │
│             40h            24h            16h                            │
│                                                                         │
│  EDUCATION-FRIENDLY FACTORS:                                            │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  ✓ Standard CRUD operations (forms, lists, reports)             │   │
│  │  ✓ No high-risk data (student data is sensitive but not PHI)   │   │
│  │  ✓ Well-defined workflows (booking, attendance, billing)        │   │
│  │  ✓ Clear user personas with distinct needs                      │   │
│  │  ✓ AI can generate most UI components confidently               │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  PROGRESSION:                                                           │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  Week 1-3:   Zone E (24h/week, 50% AI trust)                    │   │
│  │              Building foundation, learning tools                 │   │
│  │                                                                  │   │
│  │  Week 4-6:   Zone E→F (moving to 16h/week)                      │   │
│  │              Faster development, confident with AI               │   │
│  │                                                                  │   │
│  │  Week 7-10:  Zone F (16h/week, 60% AI trust)                    │   │
│  │              QUAD-Lite, rapid feature delivery                   │   │
│  │                                                                  │   │
│  │  Post-launch: Target Zone H→I                                    │   │
│  │               Maintenance mode, high AI trust                    │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## FERPA Considerations

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    FERPA AWARENESS (Not Full Compliance)                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Note: Private tutoring centers are NOT subject to FERPA                │
│  (FERPA applies to schools receiving federal funds)                     │
│                                                                         │
│  However, BEST PRACTICES for student data:                              │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  ✓ Only parents can view their own children's data              │   │
│  │  ✓ Tutors can only see students assigned to them                │   │
│  │  ✓ No sharing of student data without parent consent            │   │
│  │  ✓ Secure password requirements                                 │   │
│  │  ✓ Data retention policy (delete after 2 years inactive)        │   │
│  │  ✓ Clear privacy policy on website                              │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  If serving SCHOOLS (B2B):                                              │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  □ May need to sign data protection agreements                   │   │
│  │  □ Follow school's data handling requirements                    │   │
│  │  □ Consider SOC 2 compliance for larger contracts                │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

**Author:** QUAD Framework Team
**Template Version:** 1.0
**Last Updated:** January 1, 2026
