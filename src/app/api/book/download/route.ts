import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from 'next-auth/next';
import { authOptions } from '@/lib/auth';
import fs from 'fs';
import path from 'path';

// Book content - chapters from the book
const bookContent = `
================================================================================
                        JAVA FOR THE AI ERA
                            Version 3.0

                  Includes QUAD Framework Chapters

                        A2Vibe Creators
================================================================================

Table of Contents

Part I: Java Fundamentals (Chapters 1-8)
  Chapter 1: The AI Paradox
  Chapter 2: Java Types
  Chapter 3: Control Flow
  Chapter 4: OOP Foundations
  Chapter 5: OOP Pillars
  Chapter 6: Error Handling
  Chapter 7: Collections
  Chapter 8: Modern Java

Part II: Working with AI (Chapters 9-10)
  Chapter 9: Prompting AI for Java
  Chapter 10: Reviewing Java Output

Part III: QUAD Framework (Chapters 11-12)
  Chapter 11: The QUAD Framework
  Chapter 12: Practical QUAD Workflows

================================================================================

CHAPTER 1: THE AI PARADOX
================================================================================

> "You don't need to memorize syntax. But you absolutely need to understand
> concepts—because AI doesn't."

The Paradox

AI can generate thousands of lines of Java code in seconds. Yet that same AI:
- Creates NullPointerException landmines
- Ignores your existing class hierarchies
- Picks wrong collection types for your use case
- Misses thread safety issues entirely

The paradox: The faster AI generates code, the more you need to understand Java.

Real Disasters

DISASTER #1: The Healthcare App Crash
A startup used AI to generate patient data processing. The AI created code that
worked perfectly in tests. In production with 10,000 concurrent users:
- Memory leaks from unclosed database connections
- Race conditions corrupting patient records
- The app crashed during a critical procedure

DISASTER #2: The Financial Calculation
An AI generated BigDecimal calculations for a trading platform:
  double price = 19.99;
  double quantity = 3;
  double total = price * quantity; // AI used double, not BigDecimal

Result: Off by fractions of cents. Over millions of transactions = millions lost.

The Core Truth

AI is a powerful amplifier. It amplifies both your productivity AND your mistakes.
- Know Java deeply → AI makes you 10x faster
- Don't know Java → AI makes you 10x more dangerous

================================================================================

CHAPTER 11: THE QUAD FRAMEWORK — Organizing Teams Around AI
================================================================================

> "You can generate code with AI. But who decides WHAT to build? Who REVIEWS
> the output? Who DELIVERS it? That's where most teams fail."

The Missing Piece

Chapters 1-10 taught you how to think about Java, prompt AI effectively, and
review its output. But here's what we didn't cover:

How do teams actually work with AI at scale?

You're not a lone developer anymore. You're part of a team where:
- Product managers define requirements
- Tech leads make architectural decisions
- Developers implement features
- QA validates output
- DevOps deploys to production

The QUAD Framework

QUAD stands for the four stages every work item passes through:

  Q → U → A → D
  Question → Understand → Allocate → Deliver

| Stage | What Happens                    | Key Question                    |
|-------|---------------------------------|---------------------------------|
| Q     | Receive and clarify requirements| "What are we building and why?" |
| U     | Analyze and design solutions    | "How should we build it?"       |
| A     | Assign work to teams/circles    | "Who will build it?"            |
| D     | Implement and deliver           | "Is it done correctly?"         |

The AI Adoption Matrix

Not everyone should use AI the same way. QUAD includes an Adoption Matrix:

                    SKILL LEVEL
                Low      Medium     High
           ┌─────────┬─────────┬─────────┐
      High │Supervised│Collab   │Delegated│
           │Autonomy  │AI       │AI       │
TRUST ─────┼─────────┼─────────┼─────────┤
LEVEL Med  │Cautious │Balanced │Enhanced │
           │AI       │AI       │AI       │
      ─────┼─────────┼─────────┼─────────┤
      Low  │Restricted│Assisted │Expert   │
           │AI       │AI       │Review   │
           └─────────┴─────────┴─────────┘

The 4 Circles

QUAD organizes teams into 4 functional circles:

1. Management Circle - Product owners, scrum masters (Q and A stages)
2. Development Circle - Engineers, architects (U and D stages)
3. QA Circle - Testers, quality engineers (D stage support)
4. Infrastructure Circle - DevOps, SRE (D stage support)

================================================================================

CHAPTER 12: PRACTICAL QUAD WORKFLOWS
================================================================================

> "Setup isn't just installing tools. It's building a system where you can
> code with AI, review effectively, and ship confidently."

Workflow 1: Brand New Laptop Setup

Step 1: Essential Tools (30 min)
  # Install Homebrew
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

  # Install Java 21 (LTS)
  brew install openjdk@21

  # Set JAVA_HOME
  echo 'export JAVA_HOME=$(/usr/libexec/java_home -v 21)' >> ~/.zshrc
  source ~/.zshrc

Step 2: IDE + AI
  brew install --cask intellij-idea

  AI Plugins to install:
  - GitHub Copilot - AI code completion
  - JetBrains AI Assistant - Built-in AI

  Claude Code CLI:
  npm install -g @anthropic-ai/claude-code

Workflow 2: First Day on a New Team

1. Get Access:
   □ GitHub/GitLab repository access
   □ Slack/Teams channel access
   □ Jira/Linear board access
   □ VPN/internal network access

2. Clone and Run:
   git clone git@github.com:company/main-app.git
   cd main-app
   ./mvnw install
   ./mvnw spring-boot:run

3. Understand QUAD Setup:
   - What's my Adoption Matrix level?
   - What's my role-stage participation?
   - Which Circle am I in?

Workflow 3: Your First Feature (End-to-End QUAD)

Q Stage (Question):
  - Clarify requirements with PM
  - Understand acceptance criteria
  - Identify dependencies

U Stage (Understand):
  - Design solution with AI
  - Review AI output using Chapter 10 checklist
  - Document architecture decisions

A Stage (Allocate):
  - Break into tasks
  - Estimate effort
  - Assign to developers

D Stage (Deliver):
  - Implement with AI assistance
  - Review generated code
  - Test and deploy

================================================================================

KEY TAKEAWAYS
================================================================================

After reading this book, you can:

1. ✅ Understand Java OOP deeply enough to catch AI mistakes
2. ✅ Know when AI should use streams vs loops
3. ✅ Spot wrong collection choices
4. ✅ Catch exception handling problems
5. ✅ Direct AI to extend existing classes
6. ✅ Review AI code for Java-specific issues
7. ✅ Understand your role in a QUAD-organized team
8. ✅ Know your AI Adoption Matrix level and what it means
9. ✅ Set up a complete Java AI development environment
10. ✅ Execute features end-to-end through Q-U-A-D stages

================================================================================

For the complete book with all 12 chapters, code examples, and detailed
workflows, visit: https://quadframe.work/book

QUAD Framework: https://quadframe.work
Source Code: https://github.com/sumanaddanki/books

================================================================================
                    © 2024-2025 A2Vibe Creators
                    Java for the AI Era - Version 3.0
================================================================================
`;

export async function POST(req: NextRequest) {
  try {
    // Check authentication
    const session = await getServerSession(authOptions);

    if (!session || !session.user) {
      return NextResponse.json(
        { error: 'Authentication required' },
        { status: 401 }
      );
    }

    // Log download (for analytics)
    console.log(`Book download by: ${session.user.email} at ${new Date().toISOString()}`);

    // Create text file response (for MVP - can be upgraded to PDF later)
    const encoder = new TextEncoder();
    const bookBuffer = encoder.encode(bookContent);

    // Return as downloadable text file
    return new NextResponse(bookBuffer, {
      status: 200,
      headers: {
        'Content-Type': 'text/plain; charset=utf-8',
        'Content-Disposition': 'attachment; filename="Java-for-the-AI-Era-QUAD.txt"',
        'Content-Length': bookBuffer.length.toString(),
      },
    });
  } catch (error) {
    console.error('Book download error:', error);
    return NextResponse.json(
      { error: 'Download failed' },
      { status: 500 }
    );
  }
}

// GET for info
export async function GET(req: NextRequest) {
  return NextResponse.json({
    title: 'Java for the AI Era',
    version: '3.0',
    chapters: 12,
    format: 'txt',
    requiresAuth: true,
    includes: [
      'Java fundamentals for AI era',
      'AI prompting techniques',
      'Code review checklists',
      'QUAD Framework',
      'Practical workflows',
    ],
  });
}
