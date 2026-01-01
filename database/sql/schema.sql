-- ============================================================================
-- QUAD Framework Database Schema Loader
-- Date: January 1, 2026
-- Purpose: Load all QUAD_ prefixed tables for shared database with NutriNine
-- ============================================================================

-- This is a loader file that includes all individual SQL files
-- Run this file to create the complete schema

\echo '============================================='
\echo 'QUAD Framework Schema Installation'
\echo '============================================='

-- ============================================================================
-- FUNCTIONS (must be created first for triggers)
-- ============================================================================
\echo 'Loading functions...'
\i functions/QUAD_update_updated_at_column.fnc.sql

-- ============================================================================
-- CORE TABLES (in dependency order)
-- ============================================================================
\echo 'Loading core tables...'

-- Companies first (no dependencies)
\i tables/core/QUAD_companies.tbl.sql

-- Roles (depends on companies)
\i tables/core/QUAD_roles.tbl.sql

-- Users (depends on companies, optional role_id)
\i tables/core/QUAD_users.tbl.sql

-- User sessions (depends on users)
\i tables/core/QUAD_user_sessions.tbl.sql

-- Domains (depends on companies)
\i tables/core/QUAD_domains.tbl.sql

-- Domain members (depends on users, domains)
\i tables/core/QUAD_domain_members.tbl.sql

-- Domain resources (depends on domains, users)
\i tables/core/QUAD_domain_resources.tbl.sql

-- Resource attributes (depends on domain_resources)
\i tables/core/QUAD_resource_attributes.tbl.sql

-- ============================================================================
-- FEATURE TABLES
-- ============================================================================
\echo 'Loading feature tables...'

-- Adoption matrix (depends on users)
\i tables/features/QUAD_adoption_matrix.tbl.sql

-- Workload metrics (depends on users, domains)
\i tables/features/QUAD_workload_metrics.tbl.sql

-- Circles (depends on domains, users)
\i tables/features/QUAD_circles.tbl.sql

-- Circle members (depends on circles, users)
\i tables/features/QUAD_circle_members.tbl.sql

-- Flows (depends on domains, users)
\i tables/features/QUAD_flows.tbl.sql

-- Flow stage history (depends on flows, users)
\i tables/features/QUAD_flow_stage_history.tbl.sql

-- Work sessions (depends on users)
\i tables/features/QUAD_work_sessions.tbl.sql

-- ============================================================================
-- AUTO-INIT FUNCTIONS (must be after tables exist)
-- ============================================================================
\echo 'Loading auto-init functions...'
\i functions/QUAD_init_company_roles.fnc.sql
\i functions/QUAD_init_user_adoption_matrix.fnc.sql
\i functions/QUAD_init_domain_circles.fnc.sql

-- ============================================================================
-- COMPLETE
-- ============================================================================
\echo '============================================='
\echo 'QUAD Framework Schema Installation Complete!'
\echo '============================================='
\echo ''
\echo 'Tables created:'
\echo '  - QUAD_companies'
\echo '  - QUAD_roles'
\echo '  - QUAD_users'
\echo '  - QUAD_user_sessions'
\echo '  - QUAD_domains'
\echo '  - QUAD_domain_members'
\echo '  - QUAD_domain_resources'
\echo '  - QUAD_resource_attributes'
\echo '  - QUAD_adoption_matrix'
\echo '  - QUAD_workload_metrics'
\echo '  - QUAD_circles'
\echo '  - QUAD_circle_members'
\echo '  - QUAD_flows'
\echo '  - QUAD_flow_stage_history'
\echo '  - QUAD_work_sessions'
\echo ''
\echo 'Auto-init triggers created for:'
\echo '  - Company → Creates default roles'
\echo '  - User → Creates adoption matrix entry'
\echo '  - Domain → Creates 4 circles'
\echo ''
