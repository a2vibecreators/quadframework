"""
QUAD API - POC
==============

Local API for QUAD context retrieval.
NO AI calls - just database lookup.

Endpoints:
- GET /health - Health check
- POST /context - Get project context for a question

Copyright (c) 2026 Gopi Suman Addanke. All Rights Reserved.
"""

import os
import re
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 14201)),
    "dbname": os.getenv("DB_NAME", "quad_dev_db"),
    "user": os.getenv("DB_USER", "quad_user"),
    "password": os.getenv("DB_PASSWORD", "quad_dev_pass"),
}

VALID_API_KEY = os.getenv("QUAD_API_KEY", "quad_dev_key_abc123")

# FastAPI app
app = FastAPI(
    title="QUAD API",
    description="Context API for QUAD commands - NO AI, just database",
    version="0.1.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─────────────────────────────────────────────────────────────
# Models
# ─────────────────────────────────────────────────────────────

class ContextRequest(BaseModel):
    question: str
    org_code: Optional[str] = None
    domain_slug: Optional[str] = None


class TeamMember(BaseModel):
    name: str
    email: str
    role: str
    allocation_pct: int
    available_hrs: int


class ContextResponse(BaseModel):
    success: bool
    context_type: str
    domain: Optional[str] = None
    summary: str
    data: Optional[List[Dict[str, Any]]] = None
    prompt_addition: str


# ─────────────────────────────────────────────────────────────
# Database
# ─────────────────────────────────────────────────────────────

def get_db_connection():
    """Get database connection"""
    try:
        conn = psycopg.connect(
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            dbname=DB_CONFIG["dbname"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            row_factory=dict_row
        )
        return conn
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {e}")


# ─────────────────────────────────────────────────────────────
# Auth
# ─────────────────────────────────────────────────────────────

def verify_api_key(authorization: str = Header(None)):
    """Verify API key from Authorization header"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    # Expected format: "Bearer quad_xxx"
    parts = authorization.split(" ")
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid Authorization format")

    token = parts[1]
    if token != VALID_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    return token


# ─────────────────────────────────────────────────────────────
# Question Analysis (Rule-based, NO AI)
# ─────────────────────────────────────────────────────────────

def analyze_question(question: str) -> str:
    """
    Determine what type of context is needed based on keywords.
    NO AI - just pattern matching.
    """
    q = question.lower()

    # Availability patterns
    if any(word in q for word in ["available", "availability", "free", "capacity", "hours", "bandwidth"]):
        return "availability"

    # Team patterns
    if any(word in q for word in ["team", "who", "members", "people", "developer", "qa", "manager"]):
        return "team"

    # Project patterns
    if any(word in q for word in ["project", "domain", "working on", "assigned"]):
        return "project"

    # Allocation patterns
    if any(word in q for word in ["allocation", "allocated", "percentage", "time"]):
        return "allocation"

    # Status patterns
    if any(word in q for word in ["status", "progress", "update"]):
        return "status"

    # Default: return full context
    return "full"


# ─────────────────────────────────────────────────────────────
# Context Queries
# ─────────────────────────────────────────────────────────────

def get_availability_context(conn, domain_slug: str = None) -> Dict:
    """Get team availability"""
    with conn.cursor() as cur:
        sql = """
            SELECT
                u.name,
                u.email,
                dm.role,
                dm.allocation_percentage as allocation_pct,
                (40 * (100 - dm.allocation_percentage) / 100) as available_hrs
            FROM quad_domain_members dm
            JOIN quad_users u ON dm.user_id = u.id
            JOIN quad_domains d ON dm.domain_id = d.id
            WHERE 1=1
        """
        params = []

        if domain_slug:
            sql += " AND d.slug = %s"
            params.append(domain_slug)

        sql += " ORDER BY available_hrs DESC"

        cur.execute(sql, params)
        rows = cur.fetchall()

    # Build summary
    available = [r for r in rows if r['available_hrs'] > 0]
    summary_lines = [f"Team Availability ({len(available)} members with capacity):"]
    for r in rows:
        summary_lines.append(f"- {r['name']} ({r['role']}): {r['available_hrs']} hrs available ({r['allocation_pct']}% allocated)")

    return {
        "context_type": "availability",
        "data": [dict(r) for r in rows],
        "summary": "\n".join(summary_lines)
    }


def get_team_context(conn, domain_slug: str = None) -> Dict:
    """Get team members"""
    with conn.cursor() as cur:
        sql = """
            SELECT
                u.name,
                u.email,
                u.job_title,
                dm.role,
                dm.allocation_percentage as allocation_pct,
                d.name as domain_name
            FROM quad_domain_members dm
            JOIN quad_users u ON dm.user_id = u.id
            JOIN quad_domains d ON dm.domain_id = d.id
            WHERE 1=1
        """
        params = []

        if domain_slug:
            sql += " AND d.slug = %s"
            params.append(domain_slug)

        sql += " ORDER BY dm.role, u.name"

        cur.execute(sql, params)
        rows = cur.fetchall()

    summary_lines = [f"Team Members ({len(rows)} total):"]
    for r in rows:
        summary_lines.append(f"- {r['name']} - {r['role']} on {r['domain_name']}")

    return {
        "context_type": "team",
        "data": [dict(r) for r in rows],
        "summary": "\n".join(summary_lines)
    }


def get_project_context(conn, domain_slug: str = None) -> Dict:
    """Get project/domain info"""
    with conn.cursor() as cur:
        sql = """
            SELECT
                d.name,
                d.slug,
                d.description,
                d.methodology,
                o.name as org_name,
                COUNT(dm.id) as team_size
            FROM quad_domains d
            JOIN quad_organizations o ON d.company_id = o.id
            LEFT JOIN quad_domain_members dm ON dm.domain_id = d.id
            WHERE d.is_active = true
        """
        params = []

        if domain_slug:
            sql += " AND d.slug = %s"
            params.append(domain_slug)

        sql += " GROUP BY d.id, o.id ORDER BY d.name"

        cur.execute(sql, params)
        rows = cur.fetchall()

    summary_lines = [f"Projects ({len(rows)} active):"]
    for r in rows:
        summary_lines.append(f"- {r['name']} ({r['slug']}): {r['description'] or 'No description'} | Team: {r['team_size']} members")

    return {
        "context_type": "project",
        "data": [dict(r) for r in rows],
        "summary": "\n".join(summary_lines)
    }


def get_full_context(conn, domain_slug: str = None) -> Dict:
    """Get full context (project + team + availability)"""
    project = get_project_context(conn, domain_slug)
    team = get_team_context(conn, domain_slug)
    availability = get_availability_context(conn, domain_slug)

    summary = f"""Organization Context:

{project['summary']}

{team['summary']}

{availability['summary']}"""

    return {
        "context_type": "full",
        "data": {
            "projects": project['data'],
            "team": team['data'],
            "availability": availability['data']
        },
        "summary": summary
    }


# ─────────────────────────────────────────────────────────────
# Endpoints
# ─────────────────────────────────────────────────────────────

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "quad-api-poc"}


@app.post("/context", response_model=ContextResponse)
def get_context(
    request: ContextRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Get context for a question.

    NO AI calls - just database lookup based on question keywords.
    """
    # Analyze question to determine context type
    context_type = analyze_question(request.question)

    # Get database connection
    conn = get_db_connection()

    try:
        # Fetch context based on type
        if context_type == "availability":
            result = get_availability_context(conn, request.domain_slug)
        elif context_type == "team":
            result = get_team_context(conn, request.domain_slug)
        elif context_type == "project":
            result = get_project_context(conn, request.domain_slug)
        else:
            result = get_full_context(conn, request.domain_slug)

        # Build prompt addition for Claude CLI
        prompt_addition = f"""<quad-context>
{result['summary']}
</quad-context>

Based on the above context, please answer: {request.question}"""

        return ContextResponse(
            success=True,
            context_type=result['context_type'],
            domain=request.domain_slug,
            summary=result['summary'],
            data=result['data'] if isinstance(result['data'], list) else None,
            prompt_addition=prompt_addition
        )

    finally:
        conn.close()


@app.get("/domains")
def list_domains(api_key: str = Depends(verify_api_key)):
    """List all active domains/projects"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT d.slug, d.name, d.description, COUNT(dm.id) as team_size
                FROM quad_domains d
                LEFT JOIN quad_domain_members dm ON dm.domain_id = d.id
                WHERE d.is_active = true
                GROUP BY d.id
                ORDER BY d.name
            """)
            rows = cur.fetchall()
        return {"domains": [dict(r) for r in rows]}
    finally:
        conn.close()


# ─────────────────────────────────────────────────────────────
# Run
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 3000))
    print(f"Starting QUAD API POC on {host}:{port}")
    uvicorn.run(app, host=host, port=port)
