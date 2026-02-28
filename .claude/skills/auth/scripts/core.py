#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auth Skill Core - BM25 search engine for authentication/authorization data
"""

import csv
import re
from pathlib import Path
from math import log
from collections import defaultdict

# ============ CONFIGURATION ============
DATA_DIR = Path(__file__).parent.parent / "data"
MAX_RESULTS = 3

CSV_CONFIG = {
    "auth-methods": {
        "file": "auth-methods.csv",
        "search_cols": ["Method", "Type", "Use Case", "Pros", "Cons"],
        "output_cols": ["Method", "Type", "Security Level", "Use Case", "Pros", "Cons", "Implementation Complexity", "Token Format", "Session Storage"]
    },
    "oauth2-flows": {
        "file": "oauth2-flows.csv",
        "search_cols": ["Flow Name", "Grant Type", "Use Case", "Client Type"],
        "output_cols": ["Flow Name", "Grant Type", "Use Case", "Security Level", "PKCE Required", "Client Type", "Redirect URI", "Token Response", "Refresh Token Support", "Security Notes"]
    },
    "jwt-claims": {
        "file": "jwt-claims.csv",
        "search_cols": ["Claim Name", "Claim Key", "Description", "Validation Rules"],
        "output_cols": ["Claim Name", "Claim Key", "Type", "Required", "Description", "Example Value", "Validation Rules", "Security Notes"]
    },
    "security-headers": {
        "file": "security-headers.csv",
        "search_cols": ["Header Name", "Description", "Security Benefit"],
        "output_cols": ["Header Name", "Header Value", "Priority", "Description", "Security Benefit", "Implementation Notes", "Browser Support", "Common Mistakes"]
    },
    "oidc-providers": {
        "file": "oidc-providers.csv",
        "search_cols": ["Provider", "Type", "Key Features", "Best For"],
        "output_cols": ["Provider", "Type", "Free Tier", "Pricing Model", "Key Features", "Best For", "OAuth2 Support", "OIDC Support", "SAML Support", "SDKs Available", "Custom Domains", "Multi-Factor Auth", "User Store", "Compliance"]
    },
    "security-rules": {
        "file": "security-rules.csv",
        "search_cols": ["Category", "Rule", "Description", "Implementation"],
        "output_cols": ["Rule ID", "Category", "Rule", "Severity", "Description", "Implementation", "Code Example", "Mistake to Avoid", "Testing Method"]
    }
}

STACK_CONFIG = {
    "nodejs": {"file": "stacks/nodejs.csv"},
    "python": {"file": "stacks/python.csv"},
    "go": {"file": "stacks/go.csv"},
    "java": {"file": "stacks/java.csv"},
    "dotnet": {"file": "stacks/dotnet.csv"}
}

# Common columns for all stacks
_STACK_COLS = {
    "search_cols": ["Category", "Guideline", "Description", "Do", "Don't"],
    "output_cols": ["Category", "Guideline", "Description", "Do", "Don't", "Code Example", "Library", "Severity"]
}

AVAILABLE_STACKS = list(STACK_CONFIG.keys())


# ============ BM25 IMPLEMENTATION ============
class BM25:
    """BM25 ranking algorithm for text search"""

    def __init__(self, k1=1.5, b=0.75):
        self.k1 = k1
        self.b = b
        self.corpus = []
        self.doc_lengths = []
        self.avgdl = 0
        self.idf = {}
        self.doc_freqs = defaultdict(int)
        self.N = 0

    def tokenize(self, text):
        """Lowercase, split, remove punctuation, filter short words"""
        text = re.sub(r'[^\w\s]', ' ', str(text).lower())
        return [w for w in text.split() if len(w) > 2]

    def fit(self, documents):
        """Build BM25 index from documents"""
        self.corpus = [self.tokenize(doc) for doc in documents]
        self.N = len(self.corpus)
        if self.N == 0:
            return
        self.doc_lengths = [len(doc) for doc in self.corpus]
        self.avgdl = sum(self.doc_lengths) / self.N

        for doc in self.corpus:
            seen = set()
            for word in doc:
                if word not in seen:
                    self.doc_freqs[word] += 1
                    seen.add(word)

        for word, freq in self.doc_freqs.items():
            self.idf[word] = log((self.N - freq + 0.5) / (freq + 0.5) + 1)

    def score(self, query):
        """Score all documents against query"""
        query_tokens = self.tokenize(query)
        scores = []

        for idx, doc in enumerate(self.corpus):
            score = 0
            doc_len = self.doc_lengths[idx]
            term_freqs = defaultdict(int)
            for word in doc:
                term_freqs[word] += 1

            for token in query_tokens:
                if token in self.idf:
                    tf = term_freqs[token]
                    idf = self.idf[token]
                    numerator = tf * (self.k1 + 1)
                    denominator = tf + self.k1 * (1 - self.b + self.b * doc_len / self.avgdl)
                    score += idf * numerator / denominator

            scores.append((idx, score))

        return sorted(scores, key=lambda x: x[1], reverse=True)


# ============ SEARCH FUNCTIONS ============
def _load_csv(filepath):
    """Load CSV and return list of dicts"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def _search_csv(filepath, search_cols, output_cols, query, max_results):
    """Core search function using BM25"""
    if not filepath.exists():
        return []

    data = _load_csv(filepath)

    # Build documents from search columns
    documents = [" ".join(str(row.get(col, "")) for col in search_cols) for row in data]

    # BM25 search
    bm25 = BM25()
    bm25.fit(documents)
    ranked = bm25.score(query)

    # Get top results with score > 0
    results = []
    for idx, score in ranked[:max_results]:
        if score > 0:
            row = data[idx]
            results.append({col: row.get(col, "") for col in output_cols if col in row})

    return results


def detect_domain(query):
    """Auto-detect the most relevant domain from query"""
    query_lower = query.lower()

    domain_keywords = {
        "auth-methods": ["jwt", "session", "oauth", "saml", "api key", "bearer", "basic auth", "mtls", "passwordless", "webauthn", "magic link", "cognito", "auth0", "okta", "keycloak"],
        "oauth2-flows": ["oauth2", "authorization code", "pkce", "implicit", "client credentials", "device", "refresh token", "grant type", "flow"],
        "jwt-claims": ["jwt", "token", "claims", "iss", "sub", "aud", "exp", "iat", "scope", "roles", "permissions"],
        "security-headers": ["headers", "csp", "hsts", "x-frame", "security header", "http header", "cors"],
        "oidc-providers": ["provider", "auth0", "okta", "cognito", "azure ad", "firebase", "keycloak", "identity", "sso", "idp"],
        "security-rules": ["security", "token storage", "password", "rate limit", "csrf", "session", "mfa", "2fa", "validation", "https", "tls"]
    }

    scores = {domain: sum(1 for kw in keywords if kw in query_lower) for domain, keywords in domain_keywords.items()}
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "security-rules"


def search(query, domain=None, max_results=MAX_RESULTS):
    """Main search function with auto-domain detection"""
    if domain is None:
        domain = detect_domain(query)

    config = CSV_CONFIG.get(domain, CSV_CONFIG["security-rules"])
    filepath = DATA_DIR / config["file"]

    if not filepath.exists():
        return {"error": f"File not found: {filepath}", "domain": domain}

    results = _search_csv(filepath, config["search_cols"], config["output_cols"], query, max_results)

    return {
        "domain": domain,
        "query": query,
        "file": config["file"],
        "count": len(results),
        "results": results
    }


def search_stack(query, stack, max_results=MAX_RESULTS):
    """Search stack-specific guidelines"""
    if stack not in STACK_CONFIG:
        return {"error": f"Unknown stack: {stack}. Available: {', '.join(AVAILABLE_STACKS)}"}

    filepath = DATA_DIR / STACK_CONFIG[stack]["file"]

    if not filepath.exists():
        return {"error": f"Stack file not found: {filepath}", "stack": stack}

    results = _search_csv(filepath, _STACK_COLS["search_cols"], _STACK_COLS["output_cols"], query, max_results)

    return {
        "domain": "stack",
        "stack": stack,
        "query": query,
        "file": STACK_CONFIG[stack]["file"],
        "count": len(results),
        "results": results
    }
