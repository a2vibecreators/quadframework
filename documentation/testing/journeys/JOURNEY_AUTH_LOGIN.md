# QUAD Framework - Authentication & Login Journey

**Author:** Suman Addanki
**Version:** 1.0
**Last Updated:** January 6, 2026

---

## Overview

This document contains end-to-end test scenarios for **Authentication & Login Journey** covering all authentication methods and account linking flows.

**Features Covered:**
- OAuth SSO Authentication (Google, GitHub, Azure AD, Okta, Auth0)
- Email OTP (Passwordless) Authentication
- Account Linking (Same email across different auth methods)
- Session Management
- JWT Token Generation

**Industry Standard:** Email-based account linking - Same email = Same account regardless of authentication method.

**QUAD Authentication Philosophy:**
- ✅ **Startup/Business:** Passwordless (Email OTP) - No password required
- ✅ **Enterprise:** OAuth SSO only (Okta, Azure AD, Google Workspace)
- ✅ **Account Linking:** User can sign in with OAuth, then use email OTP next time (same account)

---

## Prerequisites

Before testing, ensure:

- [ ] DEV backend is running: `docker ps | grep quad-services-dev`
- [ ] DEV web is running: `docker ps | grep quad-web-dev`
- [ ] DEV database is running: `docker ps | grep postgres-quad-dev`
- [ ] Backend health check: `curl http://localhost:14101/v1/auth/health`
- [ ] Web app accessible: `https://dev.quadframe.work`

---

## Test Environment URLs

| Environment | Web App | Backend API | Database |
|-------------|---------|-------------|----------|
| DEV | https://dev.quadframe.work | http://localhost:14101 | localhost:14201 |
| QA | https://qa.quadframe.work | http://localhost:15101 | localhost:15201 |
| PROD | https://quadframe.work | https://quad-services-prod-*.run.app | Cloud SQL |

---

## SECTION A: OAUTH SSO AUTHENTICATION

---

## Scenario 1A: OAuth Sign-In (New User - Google)

**User Type:** New User (First time sign-in)
**Features Tested:** OAuth SSO, Auto Account Creation, Account Linking Detection

### User Flow (UI):

| Step | Screen | UI Element | Action | Expected Result | Pass/Fail |
|------|--------|------------|--------|-----------------|-----------|
| 1A.1 | Login Page | URL Bar | Navigate to `https://dev.quadframe.work/auth/login` | Login page loads | [ ] |
| 1A.2 | Login Page | "Sign in with Google" button | Click button | Redirect to Google OAuth consent | [ ] |
| 1A.3 | Google OAuth | Account Selector | Select Google account | Google auth popup | [ ] |
| 1A.4 | Google OAuth | "Allow" button | Grant permissions | Redirect back to QUAD | [ ] |
| 1A.5 | Signup Page | URL Bar | Check URL | Redirected to `/auth/signup?oauth=true&provider=google&email=user@example.com&name=John Doe` | [ ] |
| 1A.6 | Signup Page | Email Field | Verify pre-filled | Email is pre-filled and disabled | [ ] |
| 1A.7 | Signup Page | Full Name Field | Verify pre-filled | Name is pre-filled | [ ] |
| 1A.8 | Signup Page | Organization Type Radio | Select "Startup" | "Startup" selected | [ ] |
| 1A.9 | Signup Page | "Create Account" button | Click button | Loading indicator | [ ] |
| 1A.10 | Dashboard | URL Bar | Check URL | Redirected to `/dashboard` | [ ] |
| 1A.11 | Dashboard | User Avatar/Name | Verify display | Shows "John Doe" in header | [ ] |

### Technical Flow (Backend):

| Step | Component | API Call | Description |
|------|-----------|----------|-------------|
| 1 | Frontend | `GET /api/auth/signin?provider=google` | Initiates OAuth flow |
| 2 | NextAuth | Google OAuth Redirect | User authenticates with Google |
| 3 | NextAuth | `signIn` callback | Checks if user exists via `getUserByEmail()` |
| 4 | Java Backend | `GET /v1/users/email/{email}` | Returns 404 (new user) |
| 5 | NextAuth | `redirect` callback | Redirects to `/auth/signup?oauth=true` |
| 6 | Frontend | `/auth/signup` page | Displays signup form with pre-filled data |
| 7 | Frontend | `POST /api/auth/complete-oauth-signup` | Submits org type selection |
| 8 | Next.js API | `POST /v1/auth/signup` | Proxies to Java backend |
| 9 | Java Backend | `AuthService.signup()` | Creates organization + user |
| 10 | Java Backend | `JwtUtil.generateToken()` | Generates JWT token |
| 11 | NextAuth | `jwt` callback | Fetches user data, stores in token |
| 12 | NextAuth | `session` callback | Creates session with user data |
| 13 | Frontend | Navigate to `/dashboard` | User logged in |

### Database Tables Involved:

| Table | Operation | Description |
|-------|-----------|-------------|
| `quad_organizations` | INSERT | Creates new organization |
| `quad_users` | INSERT | Creates user with `email_verified=true` |
| `quad_users` | SELECT | Fetches user by email for session |

### SQL Queries for Testing:

```sql
-- Verify organization created
SELECT id, name, slug, created_at
FROM quad_organizations
WHERE name LIKE '%John Doe%'
ORDER BY created_at DESC
LIMIT 1;

-- Verify user created with OAuth provider
SELECT
    id,
    email,
    full_name,
    role,
    org_id,
    email_verified,  -- Should be TRUE for OAuth
    password_hash,   -- Should be random hash (not used for OAuth)
    created_at
FROM quad_users
WHERE email = 'user@example.com';

-- Verify user linked to organization
SELECT
    u.email,
    u.full_name,
    o.name AS org_name,
    u.org_id = o.id AS is_linked
FROM quad_users u
JOIN quad_organizations o ON u.org_id = o.id
WHERE u.email = 'user@example.com';
```

### API Endpoints Tested:
- `GET /api/auth/signin?provider=google` (NextAuth)
- `GET /v1/users/email/{email}` (Java - Returns 404 for new users)
- `POST /api/auth/complete-oauth-signup` (Next.js proxy)
- `POST /v1/auth/signup` (Java backend)

---

## Scenario 1B: OAuth Sign-In (Existing User - Account Linking)

**User Type:** Existing User (Previously signed up with OAuth or Email OTP)
**Features Tested:** Account Linking, Automatic Login

### User Flow (UI):

| Step | Screen | UI Element | Action | Expected Result | Pass/Fail |
|------|--------|------------|--------|-----------------|-----------|
| 1B.1 | Login Page | URL Bar | Navigate to `/auth/login` | Login page loads | [ ] |
| 1B.2 | Login Page | "Sign in with Google" button | Click button | Redirect to Google OAuth | [ ] |
| 1B.3 | Google OAuth | Account Selector | Select same account as before | Google auth popup | [ ] |
| 1B.4 | Google OAuth | "Allow" button | Grant permissions | Redirect back to QUAD | [ ] |
| 1B.5 | Dashboard | URL Bar | Check URL | **Directly** redirected to `/dashboard` (NO signup page) | [ ] |
| 1B.6 | Dashboard | User Avatar/Name | Verify display | Shows existing user name | [ ] |
| 1B.7 | Dashboard | Session Data | Check user data | Shows correct org, role, etc. | [ ] |

### Technical Flow (Backend):

| Step | Component | API Call | Description |
|------|-----------|----------|-------------|
| 1 | Frontend | `GET /api/auth/signin?provider=google` | Initiates OAuth flow |
| 2 | NextAuth | Google OAuth Redirect | User authenticates with Google |
| 3 | NextAuth | `signIn` callback | Checks if user exists via `getUserByEmail()` |
| 4 | Java Backend | `GET /v1/users/email/{email}` | Returns 200 (existing user found) |
| 5 | NextAuth | `signIn` callback | Returns `true` (allow sign-in, account linking) |
| 6 | NextAuth | `redirect` callback | Detects existing user, redirects to `/dashboard` |
| 7 | NextAuth | `jwt` callback | Fetches user data, stores in token |
| 8 | NextAuth | `session` callback | Creates session with existing user data |
| 9 | Frontend | Navigate to `/dashboard` | User logged in to existing account |

### Database Tables Involved:

| Table | Operation | Description |
|-------|-----------|-------------|
| `quad_users` | SELECT | Fetches existing user by email |
| `quad_organizations` | SELECT | Fetches organization details |

### SQL Queries for Testing:

```sql
-- Verify user exists (created previously)
SELECT
    id,
    email,
    full_name,
    role,
    org_id,
    email_verified,
    created_at,
    last_login_at  -- Should update on each login
FROM quad_users
WHERE email = 'user@example.com';

-- Verify last login timestamp updated
SELECT
    email,
    last_login_at,
    NOW() - last_login_at AS time_since_login
FROM quad_users
WHERE email = 'user@example.com';
-- time_since_login should be < 1 minute
```

### API Endpoints Tested:
- `GET /api/auth/signin?provider=google` (NextAuth)
- `GET /v1/users/email/{email}` (Java - Returns 200 with user data)

---

## SECTION B: EMAIL OTP (PASSWORDLESS) AUTHENTICATION

---

## Scenario 2A: Email OTP Signup (New User)

**User Type:** New User
**Features Tested:** Passwordless Signup, OTP Generation, Email Verification

### User Flow (UI):

| Step | Screen | UI Element | Action | Expected Result | Pass/Fail |
|------|--------|------------|--------|-----------------|-----------|
| 2A.1 | Login Page | "Sign Up" link | Click link | Redirect to `/auth/signup` | [ ] |
| 2A.2 | Signup Page | Email Field | Enter `newuser@test.com` | Email field accepts input | [ ] |
| 2A.3 | Signup Page | Full Name Field | Enter `Jane Smith` | Name field accepts input | [ ] |
| 2A.4 | Signup Page | Organization Type | Select "Startup" | "Startup" radio selected | [ ] |
| 2A.5 | Signup Page | "Create Account" button | Click button | Loading indicator | [ ] |
| 2A.6 | Verify Page | URL Bar | Check URL | Redirected to `/auth/verify?email=newuser@test.com` | [ ] |
| 2A.7 | Verify Page | OTP Input Fields | See 6 digit input | 6 separate input boxes displayed | [ ] |
| 2A.8 | Verify Page | Email Display | Check email shown | Shows "Enter code sent to newuser@test.com" | [ ] |
| 2A.9 | Email Client | Check inbox | Open email | Email received with 6-digit code | [ ] |
| 2A.10 | Verify Page | OTP Fields | Enter code (e.g., 123456) | Auto-advances between fields | [ ] |
| 2A.11 | Verify Page | "Verify" button | Click button | Loading indicator | [ ] |
| 2A.12 | Dashboard | URL Bar | Check URL | Redirected to `/dashboard` | [ ] |
| 2A.13 | Dashboard | User Avatar | Verify display | Shows "Jane Smith" | [ ] |

### Technical Flow (Backend):

| Step | Component | API Call | Description |
|------|-----------|----------|-------------|
| 1 | Frontend | `POST /api/auth/signup` | Submits email, name, org type |
| 2 | Next.js API | `POST /v1/auth/signup` | Proxies to Java backend |
| 3 | Java Backend | `AuthService.signup()` | Checks if user exists (new user: proceed) |
| 4 | Java Backend | `organizationRepository.save()` | Creates organization |
| 5 | Java Backend | `userRepository.save()` | Creates user with `email_verified=false` |
| 6 | Java Backend | Generate OTP | Creates 6-digit random code |
| 7 | Java Backend | Store OTP | Saves to `quad_login_codes` table |
| 8 | Java Backend | Send Email | Sends OTP via email service |
| 9 | Java Backend | Return response | `requiresVerification: true` |
| 10 | Frontend | Navigate to `/auth/verify` | Shows OTP input |
| 11 | Frontend | `POST /api/auth/verify-otp` | Submits OTP code |
| 12 | Java Backend | Validate OTP | Checks code, expiry (5 min) |
| 13 | Java Backend | Update user | Sets `email_verified=true` |
| 14 | Java Backend | Generate JWT | Creates access token |
| 15 | NextAuth | Create session | Establishes user session |
| 16 | Frontend | Navigate to `/dashboard` | User logged in |

### Database Tables Involved:

| Table | Operation | Description |
|-------|-----------|-------------|
| `quad_organizations` | INSERT | Creates new organization |
| `quad_users` | INSERT | Creates user with `email_verified=false` |
| `quad_login_codes` | INSERT | Stores OTP code with expiry |
| `quad_login_codes` | SELECT | Validates OTP code |
| `quad_users` | UPDATE | Sets `email_verified=true` after OTP verification |

### SQL Queries for Testing:

```sql
-- Verify organization created
SELECT id, name, slug, created_at
FROM quad_organizations
WHERE name LIKE '%Jane Smith%'
ORDER BY created_at DESC
LIMIT 1;

-- Verify user created (email NOT verified initially)
SELECT
    id,
    email,
    full_name,
    role,
    org_id,
    email_verified,  -- Should be FALSE initially
    created_at
FROM quad_users
WHERE email = 'newuser@test.com';

-- Verify OTP code generated and stored
SELECT
    user_id,
    code,
    expires_at,
    used_at,
    NOW() < expires_at AS is_valid,
    EXTRACT(EPOCH FROM (expires_at - NOW())) AS seconds_until_expiry
FROM quad_login_codes
WHERE user_id = (SELECT id FROM quad_users WHERE email = 'newuser@test.com')
ORDER BY created_at DESC
LIMIT 1;

-- After OTP verification, check email_verified updated
SELECT
    email,
    email_verified,  -- Should be TRUE after verification
    last_login_at
FROM quad_users
WHERE email = 'newuser@test.com';
```

### API Endpoints Tested:
- `POST /api/auth/signup` (Next.js proxy)
- `POST /v1/auth/signup` (Java backend - returns `requiresVerification: true`)
- `POST /api/auth/verify-otp` (Next.js proxy)
- `POST /v1/auth/verify-otp` (Java backend - validates OTP)

---

## Scenario 2B: Email OTP Login (Existing User - Account Linking)

**User Type:** Existing User (Previously signed up with OAuth)
**Features Tested:** Account Linking, Passwordless Login for OAuth Users

### User Flow (UI):

| Step | Screen | UI Element | Action | Expected Result | Pass/Fail |
|------|--------|------------|--------|-----------------|-----------|
| 2B.1 | Login Page | "Sign Up" link | Click link | Redirect to `/auth/signup` | [ ] |
| 2B.2 | Signup Page | Email Field | Enter `user@example.com` (OAuth user) | Email field accepts input | [ ] |
| 2B.3 | Signup Page | Full Name Field | Enter any name | Name field accepts input | [ ] |
| 2B.4 | Signup Page | Organization Type | Select "Startup" | "Startup" radio selected | [ ] |
| 2B.5 | Signup Page | "Create Account" button | Click button | Loading indicator | [ ] |
| 2B.6 | Verify Page | URL Bar | Check URL | Redirected to `/auth/verify?email=user@example.com` | [ ] |
| 2B.7 | Verify Page | Message | Check message | "Verification code sent to user@example.com" | [ ] |
| 2B.8 | Email Client | Check inbox | Open email | Email received with 6-digit code | [ ] |
| 2B.9 | Verify Page | OTP Fields | Enter code | Auto-advances between fields | [ ] |
| 2B.10 | Verify Page | "Verify" button | Click button | Loading indicator | [ ] |
| 2B.11 | Dashboard | URL Bar | Check URL | Redirected to `/dashboard` | [ ] |
| 2B.12 | Dashboard | User Data | Verify existing data | Shows **existing** user's organization and data | [ ] |

### Technical Flow (Backend):

| Step | Component | API Call | Description |
|------|-----------|----------|-------------|
| 1 | Frontend | `POST /api/auth/signup` | Submits email, name, org type |
| 2 | Next.js API | `POST /v1/auth/signup` | Proxies to Java backend |
| 3 | Java Backend | `AuthService.signup()` | **Finds existing user by email** |
| 4 | Java Backend | Account Linking Check | Detects `isPasswordless=true` (Startup org type) |
| 5 | Java Backend | Generate OTP | Creates 6-digit random code |
| 6 | Java Backend | Store OTP | Saves to `quad_login_codes` table |
| 7 | Java Backend | Send Email | Sends OTP to existing user's email |
| 8 | Java Backend | Return response | `requiresVerification: true, userId: <existing_user_id>` |
| 9 | Frontend | Navigate to `/auth/verify` | Shows OTP input |
| 10 | Frontend | `POST /api/auth/verify-otp` | Submits OTP code |
| 11 | Java Backend | Validate OTP | Checks code, expiry |
| 12 | Java Backend | Fetch existing user | Retrieves user from database |
| 13 | Java Backend | Generate JWT | Creates token with **existing** user's org_id, role |
| 14 | NextAuth | Create session | Session contains **existing** user data |
| 15 | Frontend | Navigate to `/dashboard` | User logged into **existing** account |

### Database Tables Involved:

| Table | Operation | Description |
|-------|-----------|-------------|
| `quad_users` | SELECT | Finds existing user by email |
| `quad_login_codes` | INSERT | Stores OTP code |
| `quad_login_codes` | SELECT | Validates OTP code |
| `quad_organizations` | SELECT | Fetches existing organization |

### SQL Queries for Testing:

```sql
-- Verify user ALREADY exists (created via OAuth previously)
SELECT
    id,
    email,
    full_name,
    role,
    org_id,
    email_verified,
    created_at
FROM quad_users
WHERE email = 'user@example.com';
-- Should show creation date from previous OAuth signup

-- Verify OTP code generated for existing user
SELECT
    user_id,
    code,
    expires_at,
    used_at,
    NOW() < expires_at AS is_valid
FROM quad_login_codes
WHERE user_id = (SELECT id FROM quad_users WHERE email = 'user@example.com')
ORDER BY created_at DESC
LIMIT 1;

-- Verify NO new organization created (uses existing)
SELECT
    COUNT(*) AS org_count,
    MAX(created_at) AS latest_org_created
FROM quad_organizations
WHERE id = (SELECT org_id FROM quad_users WHERE email = 'user@example.com');
-- Should show org_count = 1 (not 2)

-- Verify account linking: Same user, multiple auth methods
SELECT
    email,
    COUNT(*) AS account_count
FROM quad_users
WHERE email = 'user@example.com'
GROUP BY email;
-- Should show account_count = 1 (same account)
```

### API Endpoints Tested:
- `POST /api/auth/signup` (Next.js proxy)
- `POST /v1/auth/signup` (Java backend - detects existing user, sends OTP)
- `POST /api/auth/verify-otp` (Next.js proxy)
- `POST /v1/auth/verify-otp` (Java backend)

---

## SECTION C: ACCOUNT LINKING VERIFICATION

---

## Scenario 3A: Account Linking - OAuth → Email OTP

**Test Objective:** Verify same email = same account across auth methods

### Steps:

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 3A.1 | Sign up with Google OAuth (`test@example.com`) | Account created | [ ] |
| 3A.2 | Note organization ID and user ID | Record IDs | [ ] |
| 3A.3 | Sign out | Return to login page | [ ] |
| 3A.4 | Sign up with Email OTP (same email) | OTP sent | [ ] |
| 3A.5 | Enter OTP code | Logged in | [ ] |
| 3A.6 | Check organization ID | **Same** org ID as step 2 | [ ] |
| 3A.7 | Check user ID | **Same** user ID as step 2 | [ ] |

### SQL Verification:

```sql
-- Should find ONLY 1 user with this email
SELECT COUNT(*) AS user_count
FROM quad_users
WHERE email = 'test@example.com';
-- Expected: user_count = 1

-- Should find ONLY 1 organization for this user
SELECT COUNT(DISTINCT org_id) AS org_count
FROM quad_users
WHERE email = 'test@example.com';
-- Expected: org_count = 1

-- Verify login history (both OAuth and OTP)
SELECT
    u.email,
    u.created_at AS account_created,
    u.last_login_at AS last_login,
    COUNT(lc.id) AS otp_codes_sent
FROM quad_users u
LEFT JOIN quad_login_codes lc ON lc.user_id = u.id
WHERE u.email = 'test@example.com'
GROUP BY u.id, u.email, u.created_at, u.last_login_at;
```

---

## Scenario 3B: Account Linking - Email OTP → OAuth

**Test Objective:** Verify OAuth sign-in works for Email OTP users

### Steps:

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 3B.1 | Sign up with Email OTP (`test2@example.com`) | Account created, OTP verified | [ ] |
| 3B.2 | Note organization ID and user ID | Record IDs | [ ] |
| 3B.3 | Sign out | Return to login page | [ ] |
| 3B.4 | Click "Sign in with Google" (same email) | Google OAuth flow starts | [ ] |
| 3B.5 | Complete Google auth | Logged in **directly** to dashboard | [ ] |
| 3B.6 | Check organization ID | **Same** org ID as step 2 | [ ] |
| 3B.7 | Check user ID | **Same** user ID as step 2 | [ ] |

### SQL Verification:

```sql
-- Should find ONLY 1 user
SELECT COUNT(*) AS user_count
FROM quad_users
WHERE email = 'test2@example.com';
-- Expected: user_count = 1

-- Verify user can authenticate via multiple methods
SELECT
    email,
    email_verified,  -- Should be TRUE
    password_hash IS NOT NULL AS has_password,
    created_at,
    last_login_at
FROM quad_users
WHERE email = 'test2@example.com';
```

---

## SECTION D: SESSION MANAGEMENT

---

## Scenario 4A: Session Creation

**Features Tested:** JWT Token, Session Storage

### Technical Flow:

| Step | Component | Action | Result |
|------|-----------|--------|--------|
| 1 | Java Backend | `JwtUtil.generateToken()` | Creates JWT with user data |
| 2 | NextAuth | `jwt` callback | Stores token in session |
| 3 | NextAuth | `session` callback | Creates session object |
| 4 | Frontend | `getSession()` | Retrieves session from cookies |

### Session Data Structure:

```typescript
{
  user: {
    id: "uuid",
    email: "user@example.com",
    fullName: "John Doe",
    role: "OWNER",
    companyId: "uuid",
    orgId: "uuid",
    domainId?: "uuid",
    domainRole?: "string",
    allocationPercentage?: number
  },
  accessToken: "jwt-token-string",
  expires: "2026-01-07T12:00:00.000Z"
}
```

### SQL Queries for Testing:

```sql
-- Verify session matches user data
SELECT
    id AS user_id,
    email,
    full_name,
    role,
    org_id,
    company_id
FROM quad_users
WHERE email = 'user@example.com';
-- Compare with session.user object

-- Verify JWT token validity (decode token and compare)
-- Use https://jwt.io to decode accessToken
-- Check: userId, email, role, companyId match database
```

---

## Scenario 4B: Session Expiry

**Features Tested:** Token Expiration, Auto Logout

### Steps:

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 4B.1 | Login successfully | Session created | [ ] |
| 4B.2 | Check session expiry | Shows 24 hours from now | [ ] |
| 4B.3 | Wait 24 hours (or mock time) | Session expires | [ ] |
| 4B.4 | Try to access protected page | Redirect to `/auth/login` | [ ] |
| 4B.5 | Check error message | "Session expired. Please login again." | [ ] |

---

## SECTION E: ERROR HANDLING & NEGATIVE TESTS

---

## Scenario 5A: Invalid OTP Code

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 5A.1 | Request OTP code | Code sent to email | [ ] |
| 5A.2 | Enter wrong code (e.g., 000000) | Error: "Invalid verification code" | [ ] |
| 5A.3 | Try 3 times | Still shows error | [ ] |
| 5A.4 | Click "Resend Code" | New code sent | [ ] |
| 5A.5 | Enter new code correctly | Logged in successfully | [ ] |

### SQL Verification:

```sql
-- Check OTP attempts
SELECT
    code,
    used_at,
    created_at,
    expires_at
FROM quad_login_codes
WHERE user_id = (SELECT id FROM quad_users WHERE email = 'user@example.com')
ORDER BY created_at DESC;
-- Should show multiple codes if resent
```

---

## Scenario 5B: Expired OTP Code

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 5B.1 | Request OTP code | Code sent (expires in 5 min) | [ ] |
| 5B.2 | Wait 6 minutes | Code expires | [ ] |
| 5B.3 | Enter expired code | Error: "Verification code expired" | [ ] |
| 5B.4 | Click "Resend Code" | New code sent | [ ] |
| 5B.5 | Enter new code within 5 min | Logged in successfully | [ ] |

### SQL Verification:

```sql
-- Check OTP expiry
SELECT
    code,
    expires_at,
    NOW() > expires_at AS is_expired,
    EXTRACT(EPOCH FROM (NOW() - expires_at)) AS seconds_expired
FROM quad_login_codes
WHERE user_id = (SELECT id FROM quad_users WHERE email = 'user@example.com')
ORDER BY created_at DESC
LIMIT 1;
```

---

## Scenario 5C: Duplicate Email Signup (Edge Case)

**Test Objective:** Verify account linking prevents duplicate accounts

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 5C.1 | Sign up with Google (`dup@example.com`) | Account created | [ ] |
| 5C.2 | Sign out | Logged out | [ ] |
| 5C.3 | Sign up with Email OTP (same email) | OTP sent (NO error) | [ ] |
| 5C.4 | Enter OTP | Logged into **existing** account | [ ] |

### SQL Verification:

```sql
-- Should have ONLY 1 account
SELECT COUNT(*) AS account_count
FROM quad_users
WHERE email = 'dup@example.com';
-- Expected: account_count = 1 (NOT 2)
```

---

## API Endpoint Coverage Matrix

### NextAuth.js Endpoints

| Endpoint | Method | Scenario(s) | Description |
|----------|--------|-------------|-------------|
| `/api/auth/signin?provider=google` | GET | 1A, 1B | Initiates Google OAuth flow |
| `/api/auth/signin?provider=github` | GET | - | Initiates GitHub OAuth flow |
| `/api/auth/callback/google` | GET | 1A, 1B | Google OAuth callback |
| `/api/auth/session` | GET | All | Retrieves current session |
| `/api/auth/signout` | POST | All | Logs out user |

### Next.js API Routes (Proxy)

| Endpoint | Method | Scenario(s) | Description |
|----------|--------|-------------|-------------|
| `/api/auth/signup` | POST | 2A, 2B | Proxies to Java signup |
| `/api/auth/complete-oauth-signup` | POST | 1A | Completes OAuth signup |
| `/api/auth/verify-otp` | POST | 2A, 2B, 5A, 5B | Verifies OTP code |

### Java Backend Endpoints

| Endpoint | Method | Scenario(s) | Description |
|----------|--------|-------------|-------------|
| `/v1/auth/signup` | POST | 1A, 2A, 2B | Creates user + org OR links account |
| `/v1/auth/login` | POST | - | Password login (future) |
| `/v1/auth/verify-otp` | POST | 2A, 2B | Validates OTP code |
| `/v1/auth/resend-otp` | POST | 5A, 5B | Resends OTP code |
| `/v1/users/email/{email}` | GET | 1A, 1B | Checks if user exists (account linking) |
| `/v1/auth/health` | GET | - | Health check |

---

## Database Schema

### quad_organizations

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| name | VARCHAR(255) | Organization name |
| slug | VARCHAR(100) | URL-safe identifier |
| contact_email | VARCHAR(255) | Contact email |
| ai_tier | VARCHAR(50) | AI pricing tier |
| is_active | BOOLEAN | Active status |
| created_at | TIMESTAMP | Creation time |
| updated_at | TIMESTAMP | Last update time |

### quad_users

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| email | VARCHAR(255) | Unique email |
| password_hash | VARCHAR(255) | Hashed password (random for OAuth) |
| full_name | VARCHAR(255) | User's full name |
| name | VARCHAR(255) | Display name |
| role | VARCHAR(50) | User role (OWNER, ADMIN, etc.) |
| org_id | UUID | Organization FK |
| company_id | UUID | Company FK (backward compat) |
| email_verified | BOOLEAN | Email verification status |
| is_active | BOOLEAN | Active status |
| is_admin | BOOLEAN | Admin flag |
| last_login_at | TIMESTAMP | Last login time |
| created_at | TIMESTAMP | Creation time |
| updated_at | TIMESTAMP | Last update time |

### quad_login_codes

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| user_id | UUID | User FK |
| code | VARCHAR(6) | 6-digit OTP code |
| expires_at | TIMESTAMP | Expiry time (5 min) |
| used_at | TIMESTAMP | When code was used |
| created_at | TIMESTAMP | When code was created |

---

## Test Results Summary

| Scenario | Description | Status | Notes |
|----------|-------------|--------|-------|
| 1A | OAuth Sign-In (New User) | [ ] Pending | |
| 1B | OAuth Sign-In (Existing User) | [ ] Pending | Account linking test |
| 2A | Email OTP Signup (New User) | [ ] Pending | |
| 2B | Email OTP Login (Existing OAuth User) | [ ] Pending | Account linking test |
| 3A | Account Linking: OAuth → Email OTP | [ ] Pending | |
| 3B | Account Linking: Email OTP → OAuth | [ ] Pending | |
| 4A | Session Creation | [ ] Pending | |
| 4B | Session Expiry | [ ] Pending | |
| 5A | Invalid OTP Code | [ ] Pending | |
| 5B | Expired OTP Code | [ ] Pending | |
| 5C | Duplicate Email Signup | [ ] Pending | |

**Total Scenarios:** 11
**Passed:** ___ / 11
**Failed:** ___ / 11
**Blocked:** ___ / 11

---

## Testing Checklist (For QA Team)

### Before Testing

- [ ] DEV environment running (web, backend, database)
- [ ] Google OAuth credentials configured in `.env.local`
- [ ] Email service configured for OTP delivery
- [ ] Database schema up to date
- [ ] Test email accounts available

### Test Data Preparation

- [ ] Create test Google account: `qatest@example.com`
- [ ] Create test email: `qatest2@example.com`
- [ ] Clear previous test data from database
- [ ] Verify database tables exist: `quad_users`, `quad_organizations`, `quad_login_codes`

### Test Execution

- [ ] Execute all scenarios in order
- [ ] Mark Pass/Fail in each scenario table
- [ ] Document any errors in Notes column
- [ ] Take screenshots of failures
- [ ] Save SQL query results for verification

### Post-Testing

- [ ] Clean up test data
- [ ] Document bugs in Jira
- [ ] Update test status in summary table
- [ ] Share results with dev team

---

## Known Issues & Edge Cases

### Issue 1: OAuth Email Mismatch
**Description:** User signs in with Google using work email, but wants to use personal email for notifications.
**Current Behavior:** Account tied to OAuth email only.
**Proposed Fix:** Allow secondary email addition in profile settings.

### Issue 2: OTP Code Rate Limiting
**Description:** No rate limit on OTP generation - users can spam "Resend Code".
**Current Behavior:** Unlimited OTP requests.
**Proposed Fix:** Limit to 5 OTP requests per email per hour.

### Issue 3: Session Persistence Across Devices
**Description:** User logs in on desktop, then mobile - sees different session.
**Current Behavior:** Each device has separate session.
**Expected:** Same account, different sessions per device (intended behavior).

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Jan 6, 2026 | Initial version - 11 scenarios covering OAuth, Email OTP, Account Linking |

---

## Related Documentation

- [OAuth Implementation Guide](../auth/OAUTH_IMPLEMENTATION.md)
- [Authentication Flow](../auth/AUTHENTICATION_FLOW.md)
- [Database Schema](../database/DATABASE_SCHEMA.md)
- [Journey 1: Onboarding](JOURNEY_01_ONBOARDING.md)

---

**End of Document**
