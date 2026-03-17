<p align="center">
  <img src="https://sfapi.pythonanywhere.com/static/sixfinger-logo.jpg" width="100" />
</p>

<h1 align="center">Sixfinger API</h1>
<p align="center"><strong>Single API. 10 models. 10-20x faster than OpenAI & Claude.</strong></p>

Sixfinger is a production-ready AI gateway that routes your requests to the best available models — with streaming, plan-based access control, and Turkish-optimized options built in.

[![Free Plan](https://img.shields.io/badge/Free%20Plan-Available-brightgreen)](https://sfapi.pythonanywhere.com)
[![Models](https://img.shields.io/badge/Models-10-blue)](https://sfapi.pythonanywhere.com/docs)
[![Streaming](https://img.shields.io/badge/Streaming-SSE-orange)](https://sfapi.pythonanywhere.com/docs)
[![Turkish](https://img.shields.io/badge/Turkish-Optimized-red)](https://sfapi.pythonanywhere.com)

---

## 🚀 Why Sixfinger?

| Provider | Speed |
|----------|-------|
| **Sixfinger API** | **~1,100 char/s** |
| Claude-class APIs | ~80–120 char/s |
| Typical GPT APIs | ~50–100 char/s |

One key. One endpoint. No provider switching.

---

## ⚡ Quick Start

```bash
curl -X POST https://sfapi.pythonanywhere.com/api/v1/chat \
  -H "X-API-Key: YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!", "model": "llama-8b-instant", "stream": false}'
```

```json
{
  "response": "Hello! How can I help you?",
  "model_key": "llama-8b-instant",
  "usage": { "total_tokens": 12 }
}
```

**Streaming (SSE):**

```python
import requests

url = "https://sfapi.pythonanywhere.com/api/v1/chat"
headers = {"X-API-Key": "YOUR_KEY", "Content-Type": "application/json"}
body = {"message": "Tell me a story", "model": "llama-70b", "stream": True}

with requests.post(url, headers=headers, json=body, stream=True) as r:
    for chunk in r.iter_content(chunk_size=None):
        print(chunk.decode(), end="", flush=True)
```

---

## 🤖 Available Models

| Key | Model | Size | Language | Plan |
|-----|-------|------|----------|------|
| `llama-8b-instant` | Llama 3.1 8B Instant | 8B | Multilingual | Free+ |
| `allam-2-7b` | Allam 2 7B | 7B | Turkish / Arabic | Free+ |
| `gpt4-nano` | GPT-4.1 Nano | Nano | Multilingual | Starter+ |
| `qwen3-32b` | Qwen3 32B ⭐ | 32B | Turkish / Chinese | Starter+ |
| `llama-70b` | Llama 3.3 70B | 70B | Multilingual | Starter+ |
| `llama-maverick-17b` | Llama Maverick 17B | 17B | Multilingual | Starter+ |
| `llama-scout-17b` | Llama Scout 17B | 17B | Multilingual | Starter+ |
| `gpt-oss-20b` | GPT-OSS 20B | 20B | Multilingual | Starter+ |
| `gpt-oss-120b` | GPT-OSS 120B | 120B | Multilingual | Pro+ |
| `kimi-k2` | Kimi K2 | — | Chinese | Pro+ |

---

## 💎 Plans

| Plan | Price | Requests/mo | Tokens/mo | RPM |
|------|------:|------------:|----------:|----:|
| Free | 0 TRY | 200 | 20,000 | 3 |
| Starter | 79 TRY | 3,000 | 300,000 | 15 |
| Pro | 199 TRY | 75,000 | 7,500,000 | 50 |
| Plus | 499 TRY | 500,000 | 50,000,000 | 150 |

All plans include streaming. [Start free →](https://sfapi.pythonanywhere.com)

---

## 🔑 Get Your API Key

1. Sign up at [sfapi.pythonanywhere.com](https://sfapi.pythonanywhere.com)
2. Verify your email
3. Grab your API key from the dashboard

---

## 🛠 What You Can Build

- **Support bots** — low-latency streaming responses with plan-safe limits
- **Coding assistants** — route heavy tasks to GPT-OSS or larger model tiers
- **Multilingual apps** — Turkish-focused and multilingual models under one key
- **Content pipelines** — scale generation with usage analytics and upgrade paths
- **Internal automation** — summarization, tagging, classification bots

---

## 📖 Documentation

Full API docs at [sfapi.pythonanywhere.com/docs](https://sfapi.pythonanywhere.com/docs)

**Endpoints:**

```
POST /api/v1/chat     — Chat (stream or sync)
GET  /api/v1/stats    — Usage stats
GET  /health          — Health check
```

---

## 📬 Contact

**sixfingerdev@gmail.com** · Built by [@sixfingerdev](https://github.com/sixfingerdev)

---

⭐ **If this saved you time, a star helps a lot!**
