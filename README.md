# Sixfinger API

Private AI gateway with user management, plan enforcement, usage tracking, and multi-provider model routing.

> Repository is proprietary and not intended for open-source redistribution.

---


---

## Plans

| Plan    | Price  | Requests/mo | Tokens/mo  | Max tokens/req |
|---------|-------:|------------:|-----------:|---------------:|
| Free    | $0     | 200         | 20,000     | 100            |
| Starter | $79    | 3,000       | 300,000    | 500            |
| Pro     | $199   | 75,000      | 7,500,000  | 1,500          |
| Plus    | $499   | 500,000     | 50,000,000 | 3,000          |

All plans support streaming.

---

## Models

| Key               | Display Name        | Size  | Language       | Plans              |
|-------------------|---------------------|-------|----------------|--------------------|
| llama-8b-instant  | Llama 3.1 8B Instant| 8B    | Multilingual   | free+              |
| allam-2-7b        | Allam 2 7B          | 7B    | Turkish/Arabic | free+              |
| gpt4-nano         | GPT-4.1 Nano        | Nano  | Multilingual   | starter+           |
| qwen3-32b         | Qwen3 32B           | 32B   | Turkish/Chinese| starter+           |
| llama-70b         | Llama 3.3 70B       | 70B   | Multilingual   | starter+           |
| llama-maverick-17b| Llama Maverick 17B  | 17B   | Multilingual   | starter+           |
| llama-scout-17b   | Llama Scout 17B     | 17B   | Multilingual   | starter+           |
| gpt-oss-20b       | GPT-OSS 20B         | 20B   | Multilingual   | starter+           |
| gpt-oss-120b      | GPT-OSS 120B        | 120B  | Multilingual   | pro+               |
| kimi-k2           | Kimi K2             | -     | Chinese        | pro+               |

---

## Public API

### Chat

```
POST https://sfapi.pythonanywhere.com/api/v1/chat
X-API-Key: <key>
```

```json
{
  "message": "Hello",
  "model": "llama-8b-instant",
  "max_tokens": 100,
  "temperature": 0.7,
  "stream": false
}
```

Response:

```json
{
  "response": "...",
  "model_key": "llama-8b-instant",
  "usage": { "total_tokens": 42 }
}
```

### Usage Stats

```
GET /api/v1/stats
X-API-Key: <key>
```

### Health

```
GET /health
```

---

## Backend API (Internal)

Direct model dispatch — called by the Flask layer, not by end users.

| Method | Path              | Description                     |
|--------|-------------------|---------------------------------|
| GET    | /health           | Provider health check           |
| POST   | /api/chat         | Non-streaming chat              |
| POST   | /api/chat/stream  | SSE streaming chat              |
| GET    | /api/models       | Models available for a plan     |
| GET    | /api/providers    | Active provider list            |

Headers used by the Flask layer:

- `X-User-Plan` — user's current plan (free / starter / pro / plus)
- `X-Model` — preferred model key (optional)

---

## Features

### Identity & Access
- Register, email verify, login, forgot/reset password, resend verification
- Session-backed dashboard
- API key issuance and regeneration

### Plan & Usage Enforcement
- Per-plan model eligibility
- Rate limits: per-minute, per-hour, per-day, per-month
- Monthly token cap
- Bonus requests and tokens
- Plan upgrade requests with admin approval
- Automatic downgrade on expiry

### Growth
- Referral code generation
- Signup and paid-conversion rewards
- Bonus history

### Operations
- Rotating file logs
- DB + backend health checks
- Admin panel (user list, plan distribution, upgrade actions)
- HTTPS enforcement in production
- CORS allowlist, HSTS, security headers
- Brute-force protection on login
- API key gating on data endpoints
