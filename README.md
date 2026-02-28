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

---

<div align="center">

**onthefox** • Bridge Builder • Cross-Chain Architect

```
  /\_/\  
 ( 😎‿😎) 
 (  💻  ) 
 /|     |\ 
/_|     |_\
```

**KOTEBALTVOYROT**

![Stars](https://img.shields.io/github/stars/onthefox/auth-skill?style=flat&logo=github&color=orange)
![License](https://img.shields.io/github/license/onthefox/auth-skill?style=flat&color=blue)
![Topics](https://img.shields.io/github/topics/onthefox/auth-skill?style=flat)

*Built with* 🔥 *by onthefox*

</div>
