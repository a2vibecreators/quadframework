# OAuth Implementation Guide

## Overview

QUAD supports OAuth 2.0 sign-in via Google, GitHub, Azure AD, Okta, and Auth0.

## OAuth Flow

```
1. User clicks "Sign in with Google" on /auth/login
   ↓
2. Redirects to Google OAuth consent screen
   ↓
3. User approves → Google redirects back to NextAuth callback
   ↓
4. NextAuth callback checks GET /users/email/{email}
   ├─ User exists (200) → Create session, redirect to /dashboard
   └─ User not found (404) → Redirect to /auth/complete-signup
   ↓
5. User selects account type (Startup/Business/Enterprise)
   ↓
6. POST /api/auth/complete-oauth-signup
   ├─ Calls Java backend POST /auth/signup with OAuth flag
   ├─ Creates organization + user account
   └─ Returns success
   ↓
7. Redirect to /dashboard with new session
```

## Backend Endpoints

### Java Backend (quad-services)

| Endpoint | Method | Purpose | Auth Required |
|----------|--------|---------|---------------|
| `/users/email/{email}` | GET | Check if user exists | No |
| `/users/email/{email}/exists` | GET | Boolean existence check | No |
| `/auth/signup` | POST | Create organization + user | No |
| `/auth/login` | POST | Authenticate user | No |

### Next.js API Routes (quad-web)

| Endpoint | Purpose |
|----------|---------|
| `/api/auth/[...nextauth]` | NextAuth OAuth handlers |
| `/api/auth/complete-oauth-signup` | Complete OAuth signup after account type selection |

## File Structure

```
quad-services/src/main/java/com/quad/services/
├── controller/
│   ├── AuthController.java        # /auth/signup, /auth/login
│   └── UserController.java        # /users/email/{email}
├── service/
│   ├── AuthService.java
│   └── UserService.java           # findByEmail(), existsByEmail()
├── repository/
│   └── UserRepository.java        # JPA repository
└── config/
    └── SecurityConfig.java        # Permit /users/**, /auth/**

quad-web/src/
├── app/api/auth/
│   ├── [....nextauth]/route.ts   # NextAuth config
│   ├── complete-oauth-signup/route.ts
│   ├── signup/route.ts
│   └── login/route.ts
├── lib/
│   ├── authOptions.ts            # NextAuth callbacks + OAuth config
│   └── java-backend.ts           # getUserByEmail() function
└── app/auth/
    ├── login/page.tsx            # Sign-in page with OAuth buttons
    └── complete-signup/page.tsx  # Account type selection
```

## Configuration

### Environment Variables

**quad-web (.env.local):**
```bash
# OAuth Providers
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret

# NextAuth
NEXTAUTH_SECRET=your-secret-key
NEXTAUTH_URL=http://localhost:3000

# Java Backend
QUAD_API_URL=http://quad-services-dev:8080  # Docker network name
```

**quad-services (Docker environment):**
```bash
SPRING_DATASOURCE_URL=jdbc:postgresql://postgres-quad-dev:5432/quad_dev_db
SPRING_DATASOURCE_USERNAME=quad_user
SPRING_DATASOURCE_PASSWORD=quad_dev_pass
JWT_SECRET=your-jwt-secret
JWT_EXPIRATION_MS=86400000
```

### Docker Networking

**CRITICAL:** All containers must be on the same Docker network:

```bash
# Connect containers to dev-network
docker network connect dev-network postgres-quad-dev
docker network connect dev-network quad-services-dev
docker network connect dev-network quad-web-dev
```

**Why:** quad-web needs to call quad-services using hostname `quad-services-dev:8080`

## Security Configuration

`SecurityConfig.java` permits unauthenticated access to:
- `/auth/**` - Signup, login, password reset
- `/users/**` - User lookup for OAuth account linking
- `/health` - Health check endpoint

All other endpoints require JWT authentication.

## OAuth Providers

### Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create OAuth 2.0 credentials
3. Authorized redirect URIs: `http://localhost:3000/api/auth/callback/google`
4. Switch from Testing → Production mode to allow all users

### GitHub OAuth Setup

1. Go to GitHub Settings → Developer Settings → OAuth Apps
2. Create new OAuth app
3. Authorization callback URL: `http://localhost:3000/api/auth/callback/github`

## Account Linking

If a user signs in with Google but already has an account with email/password:
- OAuth callback finds existing user via `/users/email/{email}`
- Automatically links OAuth provider to existing account
- User can now sign in with either method

## Troubleshooting

**Error: "Failed to get user by email"**
- Check Docker networking: `docker network inspect dev-network`
- Verify quad-services is running: `curl http://localhost:14101/auth/health`
- Check logs: `docker logs quad-services-dev --tail 50`

**Error: "ENOTFOUND quad-services-dev"**
- quad-web container not on dev-network
- Fix: `docker network connect dev-network quad-web-dev && docker restart quad-web-dev`

**OAuth redirects back to login page**
- Check if endpoint returns 404 (expected for new users)
- Verify SecurityConfig allows `/users/**`
- Ensure complete-signup page exists

## Build Requirements

**Java Backend:**
- Java 17 (for compilation): `brew install openjdk@17`
- Lombok 1.18.36 (for Java 21 compatibility)
- Spring Boot 3.2.1
- PostgreSQL 15

**Build Command:**
```bash
export JAVA_HOME=/opt/homebrew/opt/openjdk@17
cd quad-services
mvn clean package -DskipTests
```

## Testing

**1. Test user lookup endpoint:**
```bash
curl http://localhost:14101/users/email/test@example.com
# Expected: {"error":"User not found"}
```

**2. Test OAuth flow:**
- Go to http://localhost:3000/auth/login
- Click "Sign in with Google"
- Approve consent screen
- Should redirect to /auth/complete-signup
- Select account type → redirects to /dashboard

**3. Test account linking:**
- Create account with email/password
- Sign out
- Sign in with Google (same email)
- Should link automatically and go to dashboard
