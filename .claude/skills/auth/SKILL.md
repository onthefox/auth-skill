---
name: auth
description: "Authentication & authorization intelligence. OAuth2, JWT, session management, SAML, OpenID Connect, security best practices. Actions: implement, configure, review, fix, secure auth flows."
---
# Auth Skill - Authentication & Authorization Intelligence

Comprehensive authentication and authorization guidance. Contains OAuth2 flows, JWT claims, security headers, identity providers, and security best practices across multiple technology stacks.

## When to Apply

Reference these guidelines when:
- Implementing user authentication (login/logout)
- Configuring OAuth2/OpenID Connect providers
- Designing JWT token structures
- Securing APIs with authentication
- Reviewing code for auth vulnerabilities
- Implementing session management
- Setting up SSO/SAML integrations

## Rule Categories by Priority

| Priority | Category | Impact | Domain |
|----------|----------|--------|--------|
| 1 | Token Security | CRITICAL | `security`, `jwt` |
| 2 | Session Management | CRITICAL | `session`, `security` |
| 3 | OAuth2 Flows | CRITICAL | `oauth2`, `oidc` |
| 4 | Password Handling | CRITICAL | `security`, `auth` |
| 5 | Security Headers | HIGH | `headers`, `security` |
| 6 | CSRF Protection | HIGH | `security`, `web` |
| 7 | Rate Limiting | HIGH | `security`, `api` |
| 8 | MFA/2FA | MEDIUM | `auth`, `security` |

## Quick Reference

### 1. Token Security (CRITICAL)

- **JWT Storage**: Never store JWT in localStorage for sensitive apps; use httpOnly cookies
- **Token Expiration**: Access tokens should expire in 15-60 minutes
- **Refresh Tokens**: Use rotating refresh tokens with single-use policy
- **Token Signing**: Use RS256 (asymmetric) over HS256 for distributed systems
- **Secret Management**: Never commit secrets to version control

### 2. Session Management (CRITICAL)

- **Session ID**: Generate cryptographically secure random session IDs
- **Session Expiration**: Implement absolute and sliding expiration
- **Session Invalidation**: Invalidate sessions on password change, logout
- **Concurrent Sessions**: Limit concurrent sessions per user
- **Secure Cookies**: Always use Secure, HttpOnly, SameSite flags

### 3. OAuth2 Flows (CRITICAL)

| Flow | Use Case | Security |
|------|----------|----------|
| Authorization Code + PKCE | SPA, Mobile apps | High |
| Authorization Code | Server-side apps | High |
| Client Credentials | Machine-to-machine | Medium |
| Device Authorization | IoT, CLI apps | Medium |
| Implicit | **Deprecated** - Don't use | Low |

### 4. Password Handling (CRITICAL)

- **Hashing**: Use Argon2id, bcrypt, or scrypt (never MD5/SHA1)
- **Salt**: Always use unique per-user salt (auto-handled by modern algorithms)
- **Pepper**: Consider adding server-side pepper for extra security
- **Validation**: Enforce minimum 12 characters, check against breached passwords
- **Rate Limiting**: Implement progressive delays and account lockout

### 5. Security Headers (HIGH)

```
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Content-Security-Policy: default-src 'self'
X-XSS-Protection: 1; mode=block
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: geolocation=(), microphone=()
```

### 6. CSRF Protection (HIGH)

- Use SameSite=Strict cookies when possible
- Implement anti-CSRF tokens for state-changing operations
- Validate Origin and Referer headers
- Use double-submit cookie pattern for APIs

### 7. Rate Limiting (HIGH)

- Login attempts: 5 per minute per IP/user
- Password reset: 3 per hour per email
- API requests: Implement token bucket or sliding window
- Return 429 Too Many Requests with Retry-After header

---

## How to Use This Skill

When user requests auth work (implement, configure, review, secure, fix), follow this workflow:

### Step 1: Analyze Requirements

Extract key information:
- **Auth type**: OAuth2, JWT, session, SAML, OpenID Connect
- **Application type**: SPA, server-side, mobile, API
- **Provider**: Auth0, Okta, AWS Cognito, Keycloak, custom
- **Stack**: Node.js, Python, Go, Java, .NET

### Step 2: Search Auth Data

```bash
python3 skills/auth/scripts/search.py "<auth_topic>" --domain <domain>
```

### Step 3: Apply Security Rules

Always check security rules before implementing auth features.

---

## Search Reference

### Available Domains

| Domain | Use For | Example Keywords |
|--------|---------|------------------|
| `auth-methods` | Authentication method comparison | JWT, session, OAuth2, SAML, API key |
| `oauth2-flows` | OAuth2 grant type selection | authorization code, PKCE, client credentials |
| `jwt-claims` | JWT token structure | standard claims, custom claims, validation |
| `security-headers` | HTTP security headers | CSP, HSTS, X-Frame-Options |
| `oidc-providers` | Identity provider integration | Auth0, Okta, Cognito, Keycloak |
| `security-rules` | Security best practices | token storage, CSRF, rate limiting |

### Available Stacks

| Stack | Focus |
|-------|-------|
| `nodejs` | Express, Passport.js, next-auth, jose |
| `python` | Flask-Login, FastAPI security, Authlib |
| `go` | gorilla/sessions, golang-jwt, oauth2 |
| `java` | Spring Security, Shiro, Nimbus JOSE |
| `dotnet` | ASP.NET Core Identity, IdentityServer |

---

## Example Workflow

**User request:** "Implement OAuth2 login for a React SPA"

### Step 1: Analyze Requirements
- Auth type: OAuth2
- Application type: SPA (React)
- Flow needed: Authorization Code with PKCE
- Stack: nodejs (default for React)

### Step 2: Search Auth Data

```bash
# Get OAuth2 flow recommendation
python3 skills/auth/scripts/search.py "SPA React OAuth2 PKCE" --domain oauth2-flows

# Get security rules for token handling
python3 skills/auth/scripts/search.py "token storage SPA security" --domain security-rules

# Get provider integration guidance
python3 skills/auth/scripts/search.py "Auth0 React implementation" --domain oidc-providers
```

### Step 3: Implement with Security Rules

Apply security rules:
- Use PKCE for public clients
- Store tokens in memory (not localStorage)
- Implement token refresh rotation
- Add proper error handling

---

## Common Rules for Secure Auth

### Token Handling

| Rule | Do | Don't |
|------|-----|-------|
| **Token Storage** | Use httpOnly cookies or memory | Store JWT in localStorage for sensitive apps |
| **Token Transmission** | Always use HTTPS/TLS | Send tokens over HTTP |
| **Token Validation** | Validate signature, expiry, issuer | Trust tokens without validation |
| **Refresh Tokens** | Rotate on each use, single-use policy | Reuse refresh tokens indefinitely |

### Session Security

| Rule | Do | Don't |
|------|-----|-------|
| **Session ID** | Use crypto.randomBytes(32) | Use predictable session IDs |
| **Cookie Flags** | Secure, HttpOnly, SameSite=Strict | Omit Secure flag in production |
| **Session Fixation** | Regenerate session ID on login | Keep same session ID after auth |
| **Logout** | Invalidate session server-side | Just delete client cookie |

### Password Security

| Rule | Do | Don't |
|------|-----|-------|
| **Hashing** | Argon2id, bcrypt, scrypt | MD5, SHA1, SHA256 alone |
| **Validation** | Check against HaveIBeenPwned | Accept common passwords |
| **Reset Tokens** | Single-use, short expiry (15min) | Reusable tokens, long expiry |
| **Error Messages** | Generic "invalid credentials" | Reveal if email exists |

### OAuth2 Security

| Rule | Do | Don't |
|------|-----|-------|
| **PKCE** | Always use for SPAs/mobile | Use Implicit flow |
| **State Parameter** | Generate random, validate callback | Skip state parameter |
| **Redirect URIs** | Whitelist exact URIs | Allow wildcards or open redirect |
| **Scope Validation** | Validate scopes server-side | Trust client-requested scopes |

---

## Pre-Delivery Checklist

Before delivering auth implementation, verify:

### Token Security
- [ ] Tokens transmitted over HTTPS only
- [ ] JWT signed with RS256 or strong HS256 secret
- [ ] Token expiration set appropriately (< 60 min for access tokens)
- [ ] Refresh token rotation implemented
- [ ] Tokens validated on server (signature, expiry, issuer)

### Session Management
- [ ] Session IDs cryptographically random
- [ ] Cookies have Secure, HttpOnly, SameSite flags
- [ ] Session regeneration on login
- [ ] Session invalidation on logout/password change

### Password Handling
- [ ] Using Argon2id or bcrypt for hashing
- [ ] Rate limiting on login attempts
- [ ] Password reset tokens are single-use
- [ ] Generic error messages (no user enumeration)

### OAuth2/OIDC
- [ ] PKCE implemented for public clients
- [ ] State parameter used and validated
- [ ] Redirect URIs whitelisted
- [ ] Scope validation server-side

### Security Headers
- [ ] HSTS enabled
- [ ] CSP configured
- [ ] X-Frame-Options set
- [ ] X-Content-Type-Options: nosniff

### CSRF Protection
- [ ] Anti-CSRF tokens for state-changing ops
- [ ] SameSite cookie attribute set
- [ ] Origin/Referer validation

---

## Quick Commands

```bash
# Search for OAuth2 flow guidance
python3 skills/auth/scripts/search.py "OAuth2 SPA PKCE" --domain oauth2-flows

# Get JWT best practices
python3 skills/auth/scripts/search.py "JWT token security" --domain jwt-claims

# Find security headers config
python3 skills/auth/scripts/search.py "CSP HSTS headers" --domain security-headers

# Get provider integration help
python3 skills/auth/scripts/search.py "Auth0 Node.js Express" --domain oidc-providers

# Check security rules
python3 skills/auth/scripts/search.py "token storage session" --domain security-rules
```
