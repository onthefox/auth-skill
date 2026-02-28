# Auth Skill for Claude Code

Authentication and authorization intelligence for Claude Code. Provides searchable guidance on OAuth2, JWT, session management, security best practices, and identity providers.

## Features

- **6 Data Domains**: Auth methods, OAuth2 flows, JWT claims, security headers, OIDC providers, security rules
- **BM25 Search**: Fast, relevant search results from curated authentication data
- **Stack Support**: Node.js, Python, Go, Java, .NET implementation guidelines
- **Security First**: Critical security rules and best practices for auth implementations

## Installation

### Option 1: Clone to Claude Code Skills Directory

```bash
# Clone to your Claude Code skills directory
git clone https://github.com/onthefox/auth-skill.git
# Then copy/link to .claude/skills/auth
```

### Option 2: Manual Installation

1. Create the skill directory:
   ```bash
   mkdir -p .claude/skills/auth
   ```

2. Copy all files from this repo to `.claude/skills/auth/`

3. Verify installation:
   ```bash
   python3 .claude/skills/auth/scripts/search.py "OAuth2 PKCE" --domain oauth2-flows
   ```

## Usage

### Basic Search

```bash
# Search for OAuth2 flow guidance
python3 scripts/search.py "OAuth2 SPA PKCE" --domain oauth2-flows

# Search for JWT best practices
python3 scripts/search.py "JWT token security" --domain jwt-claims

# Search for security headers
python3 scripts/search.py "CSP HSTS headers" --domain security-headers

# Search for provider integration
python3 scripts/search.py "Auth0 Node.js Express" --domain oidc-providers

# Search for security rules
python3 scripts/search.py "token storage session" --domain security-rules
```

### Auto-Domain Detection

The skill automatically detects the most relevant domain from your query:

```bash
# Will auto-detect oauth2-flows domain
python3 scripts/search.py "authorization code flow for mobile app"

# Will auto-detect security-rules domain
python3 scripts/search.py "how to store JWT tokens securely"
```

### Stack-Specific Search

```bash
# Node.js auth implementation
python3 scripts/search.py "JWT authentication" --stack nodejs

# Python OAuth2 client
python3 scripts/search.py "OAuth2 client credentials" --stack python

# Go session management
python3 scripts/search.py "session middleware" --stack go
```

### JSON Output

```bash
python3 scripts/search.py "OAuth2" --domain oauth2-flows --json
```

## Available Domains

| Domain | Description | Example Query |
|--------|-------------|---------------|
| `auth-methods` | Authentication method comparison | "JWT vs session authentication" |
| `oauth2-flows` | OAuth2 grant types and flows | "PKCE authorization code flow" |
| `jwt-claims` | JWT token structure and claims | "standard JWT claims validation" |
| `security-headers` | HTTP security headers | "CSP HSTS configuration" |
| `oidc-providers` | Identity provider integration | "Auth0 vs Okta comparison" |
| `security-rules` | Security best practices | "token storage best practices" |

## Available Stacks

| Stack | Description |
|-------|-------------|
| `nodejs` | Express, Passport.js, next-auth, jose |
| `python` | Flask-Login, FastAPI security, Authlib |
| `go` | gorilla/sessions, golang-jwt, oauth2 |
| `java` | Spring Security, Shiro, Nimbus JOSE |
| `dotnet` | ASP.NET Core Identity, IdentityServer |

## Examples

### Example 1: Implementing OAuth2 for a React SPA

```bash
# Step 1: Get OAuth2 flow recommendation
python3 scripts/search.py "React SPA OAuth2 PKCE" --domain oauth2-flows

# Step 2: Get token security rules
python3 scripts/search.py "token storage SPA security" --domain security-rules

# Step 3: Get provider integration guidance
python3 scripts/search.py "Auth0 React implementation" --domain oidc-providers
```

### Example 2: Securing JWT Implementation

```bash
# Step 1: Get JWT claims guidance
python3 scripts/search.py "JWT claims validation" --domain jwt-claims

# Step 2: Get security rules for tokens
python3 scripts/search.py "JWT token storage expiration" --domain security-rules

# Step 3: Get security headers
python3 scripts/search.py "security headers API" --domain security-headers
```

### Example 3: Choosing an Identity Provider

```bash
# Search for provider comparison
python3 scripts/search.py "Auth0 Okta Cognito comparison" --domain oidc-providers

# Search for specific features
python3 scripts/search.py "SSO SAML enterprise" --domain oidc-providers
```

## Data Files

The skill includes the following curated data files:

- **auth-methods.csv**: 15 authentication methods with security levels and use cases
- **oauth2-flows.csv**: 10 OAuth2 grant types with security notes
- **jwt-claims.csv**: 25 JWT claims with validation rules
- **security-headers.csv**: 20 security headers with implementation guidance
- **oidc-providers.csv**: 20 identity providers with feature comparison
- **security-rules.csv**: 25 security rules with code examples

## Project Structure

```
onthefox/auth-skill/
├── .claude/skills/auth/
│   ├── SKILL.md              # Skill definition and documentation
│   ├── scripts/
│   │   ├── core.py           # BM25 search engine
│   │   └── search.py         # CLI entry point
│   └── data/
│       ├── auth-methods.csv
│       ├── oauth2-flows.csv
│       ├── jwt-claims.csv
│       ├── security-headers.csv
│       ├── oidc-providers.csv
│       └── security-rules.csv
├── README.md
└── .gitignore
```

## Development

### Adding New Data

1. Create a new CSV file in the `data/` directory
2. Add the domain configuration in `scripts/core.py`
3. Update the domain detection keywords

### BM25 Algorithm

The search uses the BM25 ranking algorithm with default parameters:
- `k1 = 1.5` (term frequency saturation)
- `b = 0.75` (length normalization)

## License

MIT License - See LICENSE file for details.

## Contributing

Contributions welcome! Please feel free to submit issues and pull requests.

## Support

For questions or issues, please open an issue on GitHub.
