<p align="center">
  <img src="https://sfapi.pythonanywhere.com/static/sixfinger-logo.jpg" width="100" />
</p>

<h1 align="center">Sixfinger API</h1>
<p align="center"><strong>Single API. 41 models. Free Claude access included. 10-20x faster than typical direct endpoints.</strong></p>

Sixfinger is a production-ready AI gateway that routes requests to the best available model family — now with 13 Claude models (Sonnet, Haiku, Opus, Fable) alongside 28+ other LLMs. Streaming, plan-aware access control, and multilingual performance built in.

[![Free Plan](https://img.shields.io/badge/Free%20Plan-Available-brightgreen)](https://api.sixfinger.live)
[![Free Claude API](https://img.shields.io/badge/Free%20Claude%20API-Included-purple)](https://api.sixfinger.live)
[![Models](https://img.shields.io/badge/Models-41-blue)](https://api.sixfinger.live)
[![Streaming](https://img.shields.io/badge/Streaming-SSE-orange)](https://api.sixfinger.live)

---

## 🚀 Why Sixfinger?

| Provider | Speed |
|----------|-------|
| **Sixfinger API** | **~1,100 char/s** |
| Claude API | ~80–120 char/s |
| Typical GPT APIs | ~50–100 char/s |

One key. One endpoint. 13 Claude models included free. No provider switching.

---

## 🧠 Free Claude API Access

Sixfinger now includes **free Claude API access** — use Claude Sonnet 4.6, Sonnet 4.5, Haiku 4.5, and Sonnet 4 at no cost on the Free plan. Upgrade to Starter+ for Claude Opus, Fable, and 2.5x Fast variants.

| Key | Model | Speed | Plan |
|-----|-------|-------|------|
| `claude-sonnet-4-6` | Claude Sonnet 4.6 | Fast | **Free** |
| `claude-haiku-4-5` | Claude Haiku 4.5 | Very Fast | **Free** |
| `claude-sonnet-4-5` | Claude Sonnet 4.5 | Fast | **Free** |
| `claude-sonnet-4` | Claude Sonnet 4 | Fast | **Free** |
| `claude-fable-5` | Claude Fable 5 | Fast | Starter+ |
| `claude-opus-4-8` | Claude Opus 4.8 | Fast | Starter+ |
| `claude-opus-4-7` | Claude Opus 4.7 | Fast | Starter+ |
| `claude-opus-4-5` | Claude Opus 4.5 | Fast | Starter+ |
| `claude-opus-4-1` | Claude Opus 4.1 | Fast | Starter+ |
| `claude-opus-4` | Claude Opus 4 | Fast | Starter+ |
| `claude-opus-4-8-fast` | Opus 4.8 Fast 2.5x | Very Fast | Starter+ |
| `claude-opus-4-7-fast` | Opus 4.7 Fast 2.5x | Very Fast | Starter+ |
| `claude-opus-4-6-fast` | Opus 4.6 Fast 2.5x | Very Fast | Starter+ |

---

## Quick Start

```bash
curl -X POST https://api.sixfinger.live/v1/chat/completions \
  -H "X-API-Key: YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "claude-sonnet-4-6", "messages": [{"role": "user", "content": "Hello!"}]}'
```

```json
{
  "id": "chatcmpl-...",
  "object": "chat.completion",
  "model": "claude-sonnet-4-6",
  "choices": [{
    "index": 0,
    "message": {"role": "assistant", "content": "Hello! How can I help you?"},
    "finish_reason": "stop"
  }],
  "usage": {"prompt_tokens": 10, "completion_tokens": 8, "total_tokens": 18}
}
```

**Python SDK:**

```bash
pip install sixfinger
```

```python
from sixfinger import API

client = API(api_key="YOUR_KEY")
response = client.chat("Hello!", model="claude-sonnet-4-6")
print(response.content)
```

**OpenAI SDK:**

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://api.sixfinger.live/v1",
    api_key="YOUR_KEY"
)

response = client.chat.completions.create(
    model="claude-sonnet-4-6",
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response.choices[0].message.content)
```

**Streaming (SSE):**

```python
from openai import OpenAI

client = OpenAI(base_url="https://api.sixfinger.live/v1", api_key="YOUR_KEY")

for chunk in client.chat.completions.create(
    model="claude-haiku-4-5",
    messages=[{"role": "user", "content": "Tell me a story"}],
    stream=True
):
    content = chunk.choices[0].delta.content
    if content:
        print(content, end="", flush=True)
```

---

## All 41 Models

| Key | Model | Size | Language | Plan |
|-----|-------|------|----------|------|
| `llama-8b-instant` | Llama 3.1 8B Instant | 8B | Multilingual | Free+ |
| `allam-2-7b` | Allam 2 7B | 7B | Turkish / Arabic | Free+ |
| `step-3.5-flash` | Step 3.5 Flash | — | Multilingual | Free+ |
| `nemotron-3-super-120b-a12b` | Nemotron 3 Super 120B A12B | 120B | Multilingual | Free+ |
| `glm-46` | GLM-4.6 | — | Multilingual | Free+ |
| `deepseek-v4-flash-free` | DeepSeek V4 Flash Free | — | Multilingual | Free+ |
| `mimo-v2.5-free` | Mimo V2.5 | — | Multilingual | Free+ |
| `north-mini-code-free` | North Mini Code | — | Multilingual | Free+ |
| `nemotron-3-ultra-free` | Nemotron 3 Ultra | — | Multilingual | Free+ |
| `deepseek-v4-flash` | DeepSeek V4 Flash | — | Multilingual | Free+ |
| `deepseek-v4-pro` | DeepSeek V4 Pro | — | Multilingual | Free+ |
| `hy3-preview` | HY3 Preview | — | Multilingual | Free+ |
| `qwen3.7-plus` | Qwen 3.7 Plus | — | Multilingual | Free+ |
| `step-3.7-flash` | Step 3.7 Flash | — | Multilingual | Free+ |
| `gemini-3.1-flash-lite` | Gemini 3.1 Flash Lite | — | Multilingual | Free+ |
| `gemini-3-flash-preview` | Gemini 3 Flash Preview | — | Multilingual | Free+ |
| `gpt-5.4-mini` | GPT-5.4 Mini | — | Multilingual | Free+ |
| `minimax-m3` | MiniMax M3 | — | Multilingual | Free+ |
| `claude-sonnet-4-6` | Claude Sonnet 4.6 | — | Multilingual | Free+ |
| `claude-haiku-4-5` | Claude Haiku 4.5 | — | Multilingual | Free+ |
| `claude-sonnet-4-5` | Claude Sonnet 4.5 | — | Multilingual | Free+ |
| `claude-sonnet-4` | Claude Sonnet 4 | — | Multilingual | Free+ |
| `gpt4-nano` | GPT-4.1 Nano | Nano | Multilingual | Starter+ |
| `qwen3-32b` | Qwen3 32B | 32B | Turkish / Chinese | Starter+ |
| `llama-70b` | Llama 3.3 70B | 70B | Multilingual | Starter+ |
| `llama-scout-17b` | Llama Scout 17B | 17B | Multilingual | Starter+ |
| `llama-pg2-86m` | Llama Prompt Guard 2 86M | 86M | Multilingual | Starter+ |
| `gpt-oss-20b` | GPT-OSS 20B | 20B | Multilingual | Starter+ |
| `glm-4.5-air` | GLM 4.5 Air | — | Multilingual | Starter+ |
| `qwen3-coder` | Qwen3 Coder | — | Multilingual | Starter+ |
| `lfm-2.5-1.2b-thinking` | LFM 2.5 1.2B Thinking | 1.2B | Multilingual | Starter+ |
| `claude-fable-5` | Claude Fable 5 | — | Multilingual | Starter+ |
| `claude-opus-4-8` | Claude Opus 4.8 | — | Multilingual | Starter+ |
| `claude-opus-4-7` | Claude Opus 4.7 | — | Multilingual | Starter+ |
| `claude-opus-4-5` | Claude Opus 4.5 | — | Multilingual | Starter+ |
| `claude-opus-4-1` | Claude Opus 4.1 | — | Multilingual | Starter+ |
| `claude-opus-4` | Claude Opus 4 | — | Multilingual | Starter+ |
| `claude-opus-4-8-fast` | Claude Opus 4.8 Fast | — | Multilingual | Starter+ |
| `claude-opus-4-7-fast` | Claude Opus 4.7 Fast | — | Multilingual | Starter+ |
| `claude-opus-4-6-fast` | Claude Opus 4.6 Fast | — | Multilingual | Starter+ |
| `gpt-oss-120b` | GPT-OSS 120B | 120B | Multilingual | Pro+ |

---

## Plans

| Plan | Price | Requests/mo | Tokens/mo | RPM | RPH |
|------|------:|------------:|----------:|----:|----:|
| Free | 0 USD | 200 | 20,000 | 3 | 60 |
| Starter | 5 USD | 3,000 | 300,000 | 15 | 300 |
| Pro | 15 USD | 75,000 | 7,500,000 | 50 | 1,500 |
| Plus | 39 USD | 500,000 | 50,000,000 | 150 | 5,000 |

All plans include streaming, monthly quota tracking without daily caps, and Claude model access. [Start free →](https://api.sixfinger.live)

---

## Get Your API Key

1. Sign up at [https://api.sixfinger.live](https://api.sixfinger.live)
2. Verify your email
3. Grab your API key from the dashboard

---

## 🛠 What You Can Build

- **Coding assistants** — Claude Opus and Sonnet for complex code generation, Qwen3 Coder for specialized tasks
- **Support bots** — Claude Haiku for low-latency streaming, Llama 8B for general chat
- **Content pipelines** — Claude Fable and Opus for creative writing at scale
- **Multilingual apps** — Claude, Qwen3, and Allam models under one key
- **Internal automation** — summarization, tagging, and classification with Claude Sonnet
- **Reasoning workloads** — DeepSeek, Nemotron, and Claude Opus for chain-of-thought tasks

---

## Documentation

Full API docs at [api.sixfinger.live/docs](https://api.sixfinger.live/docs)

**Endpoints:**

```
POST /v1/chat/completions                      — OpenAI-compatible chat (stream or sync)
GET  /v1/models                                — List available models (OpenAI-compatible)
GET  /v1/models/:id                            — Get a single model
POST /api/v1/chat                              — Legacy chat (still supported)
GET  /api/v1/stats                             — Usage stats
GET  /health                                   — Health check
```

---

## Contact

**sixfingerdev@gmail.com** · Built by [@sixfingerdev](https://github.com/sixfingerdev)

---

 **If this saved you time, a star helps a lot!**
