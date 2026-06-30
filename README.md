<p align="center">
  <img src="https://sfapi.pythonanywhere.com/static/sixfinger-logo.jpg" width="100" />
</p>

<h1 align="center">Sixfinger API</h1>
<p align="center"><strong>Single API. 40+ models. Free Claude access included. OpenAI-compatible endpoints.</strong></p>

<p align="center">
  <a href="https://discord.gg/AtwqzqpwR8"><img src="https://img.shields.io/badge/Discord-Join%20Server-5865F2?logo=discord&logoColor=white" alt="Discord"></a>
  <a href="https://api.sixfinger.live"><img src="https://img.shields.io/badge/API-Live-brightgreen" alt="API Live"></a>
  <a href="https://api.sixfinger.live/docs"><img src="https://img.shields.io/badge/Docs-OpenAI%20Compatible-blue" alt="Docs"></a>
  <a href="https://pypi.org/project/sixfinger/"><img src="https://img.shields.io/badge/PyPI-sixfinger-orange" alt="PyPI"></a>
</p>

Sixfinger is a production-ready AI gateway with **OpenAI-compatible endpoints**. Route requests to 40+ models — including 13 Claude models (Sonnet, Haiku, Opus, Fable) and 7 G4F models (GPT-5, GLM-5, Kimi K2.7, DeepSeek V3.2/V4). Use the official OpenAI SDK with your Sixfinger key.

---

## Join Our Discord

**[https://discord.gg/AtwqzqpwR8](https://discord.gg/AtwqzqpwR8)**

- Test models with our **SixFinger API Test Bot**
- Request new models by opening issues
- Participate in giveaways
- Get support and share your projects

---

## OpenAI-Compatible API

Use the official OpenAI Python/Node.js SDK:

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://api.sixfinger.live/v1",
    api_key="sixfinger_xxx"
)

response = client.chat.completions.create(
    model="gpt-5",
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response.choices[0].message.content)
```

**Streaming:**

```python
for chunk in client.chat.completions.create(
    model="llama-8b-instant",
    messages=[{"role": "user", "content": "Tell me a story"}],
    stream=True
):
    content = chunk.choices[0].delta.content
    if content:
        print(content, end="", flush=True)
```

---

## Python SDK

```bash
pip install sixfinger
```

```python
from sixfinger import API

client = API(api_key="sixfinger_xxx")
response = client.chat("Hello!", model="gpt-5")
print(response.content)
```

---

## Free Claude API Access

Sixfinger includes **free Claude API access** — use Claude Sonnet 4.6, Sonnet 4.5, Haiku 4.5, and Sonnet 4 at no cost on the Free plan. Upgrade to Starter+ for Claude Opus, Fable, and 2.5x Fast variants.

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

## All Models

### Free Plan (20 models)

| Key | Model | Company |
|-----|-------|---------|
| `llama-8b-instant` | Llama 3.1 8B Instant | Meta |
| `allam-2-7b` | Allam 2 7B | SDAIA |
| `step-3.5-flash` | Step 3.5 Flash | StepFun |
| `nemotron-3-super-120b-a12b` | Nemotron 3 Super 120B | NVIDIA |
| `glm-46` | GLM-4.6 | Z.AI |
| `deepseek-v4-flash-free` | DeepSeek V4 Flash Free | DeepSeek |
| `mimo-v2.5-free` | Mimo V2.5 | Xiaomi |
| `north-mini-code-free` | North Mini Code | Cohere |
| `nemotron-3-ultra-free` | Nemotron 3 Ultra | NVIDIA |
| `claude-sonnet-4-6` | Claude Sonnet 4.6 | Anthropic |
| `claude-haiku-4-5` | Claude Haiku 4.5 | Anthropic |
| `claude-sonnet-4-5` | Claude Sonnet 4.5 | Anthropic |
| `claude-sonnet-4` | Claude Sonnet 4 | Anthropic |
| `gpt-5` | GPT-5 | OpenAI |
| `gpt-5.4` | GPT-5.4 | OpenAI |
| `gpt-5.5` | GPT-5.5 | OpenAI |
| `glm-5` | GLM-5 | Zhipu AI |
| `kimi-k2.7-code` | Kimi K2.7 Code | Moonshot AI |
| `deepseek-v3.2` | DeepSeek V3.2 | DeepSeek |
| `deepseek-v4-flash` | DeepSeek V4 Flash | DeepSeek |

### Starter+ Plan (additional models)

| Key | Model | Company |
|-----|-------|---------|
| `gpt4-nano` | GPT-4.1 Nano | OpenAI |
| `qwen3-32b` | Qwen3 32B | Alibaba |
| `llama-70b` | Llama 3.3 70B | Meta |
| `llama-scout-17b` | Llama Scout 17B | Meta |
| `llama-pg2-86m` | Llama Prompt Guard 2 86M | Meta |
| `gpt-oss-20b` | GPT-OSS 20B | OpenAI |
| `glm-4.5-air` | GLM 4.5 Air | Z.AI |
| `qwen3-coder` | Qwen3 Coder | Alibaba |
| `lfm-2.5-1.2b-thinking` | LFM 2.5 1.2B Thinking | Liquid |
| `claude-fable-5` | Claude Fable 5 | Anthropic |
| `claude-opus-4-8` | Claude Opus 4.8 | Anthropic |
| `claude-opus-4-7` | Claude Opus 4.7 | Anthropic |
| `claude-opus-4-5` | Claude Opus 4.5 | Anthropic |
| `claude-opus-4-1` | Claude Opus 4.1 | Anthropic |
| `claude-opus-4` | Claude Opus 4 | Anthropic |
| `claude-opus-4-8-fast` | Claude Opus 4.8 Fast | Anthropic |
| `claude-opus-4-7-fast` | Claude Opus 4.7 Fast | Anthropic |
| `claude-opus-4-6-fast` | Claude Opus 4.6 Fast | Anthropic |

### Pro+ Plan (additional models)

| Key | Model | Company |
|-----|-------|---------|
| `gpt-oss-120b` | GPT-OSS 120B | OpenAI |

---

## Plans

| Plan | Price | Requests/mo | Tokens/mo | RPM | RPH |
|------|------:|------------:|----------:|----:|----:|
| Free | 0 USD | 1,000 | 100,000 | 10 | 200 |
| Starter | 5 USD | 10,000 | 1,000,000 | 30 | 600 |
| Pro | 15 USD | 150,000 | 15,000,000 | 100 | 3,000 |
| Plus | 39 USD | 1,000,000 | 100,000,000 | 300 | 10,000 |

All plans include streaming, monthly quota tracking, and Claude model access. [Start free →](https://api.sixfinger.live)

---

## Developer Reward Program

Build an app with Sixfinger API and share it on our [Discord server](https://discord.gg/AtwqzqpwR8) to earn a **free Starter Plan** for 30 days!

**How to participate:**
1. Build something cool with Sixfinger API
2. Share your project in the `#showcase` channel on Discord
3. Include a link to your app/repo
4. Our team will review and approve your submission
5. Get upgraded to Starter Plan automatically!

**Starter Plan benefits:**
- 30 requests per minute
- 600 requests per hour  
- 10,000 requests per month
- 1,000,000 tokens per month
- Access to all models including Claude Opus

---

## Get Your API Key

1. Sign up at [api.sixfinger.live](https://api.sixfinger.live)
2. Verify your email
3. Grab your API key from the dashboard

---

## API Endpoints

### OpenAI-Compatible

```
POST /v1/chat/completions    — Chat completions (OpenAI format)
GET  /v1/models              — List available models
GET  /v1/models/:id          — Get single model
```

### Legacy

```
POST /api/v1/chat            — Chat (stream or sync)
GET  /api/v1/stats           — Usage stats
```

Full docs at [api.sixfinger.live/docs](https://api.sixfinger.live/docs)

---

## Community & Support

- **Discord:** [discord.gg/AtwqzqpwR8](https://discord.gg/AtwqzqpwR8) — Test bot, giveaways, support
- **Email:** sixfingerdev@gmail.com
- **GitHub:** [@sixfingerdev](https://github.com/sixfingerdev)

---

**If this saved you time, a star helps a lot!**
