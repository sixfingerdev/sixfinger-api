

# ⚡ Sixfinger - Ultra-Fast AI Platform

**10-20x Faster AI Chat API + On-Device Language Models**

Sixfinger delivers responses 10-20x faster than popular AI services like OpenAI GPT-4 or Claude, giving you access to 13 powerful AI models—including Meta Llama 3.3 70B, Qwen3 32B, GPT-4.1-NANO, LLAMA Maverick, DeepSeek-R1 and GPT-OSS 120B—with real-time streaming and Turkish-optimized models.

**Now includes on-device language models** optimized for CPU inference, perfect for mobile and edge deployments!

---
![PyPI](https://img.shields.io/pypi/v/sixfinger)
![Downloads](https://img.shields.io/pypi/dm/sixfinger)
![License](https://img.shields.io/pypi/l/sixfinger)
![Python Version](https://img.shields.io/pypi/pyversions/sixfinger)

## 🚀 Features

### ☁️ Cloud API
- ⚡ Ultra-fast: ~1,100 characters/sec
- 🤖 13 powerful AI models:
  - Meta Llama 3.3 70B
  - Llama 4 Series
  - Qwen3 32B (Turkish-optimized)
  - GPT-OSS 120B
  - Allam 2 7B (TR/AR)
  - Kimi K2 (Chinese)
- 🔄 Real-time streaming (Server-Sent Events)
- 🔐 Secure: API key & email verification, rate limiting
- 📊 Detailed usage stats
- 🎁 Referral program: bonus tokens for you and your friends

### 📱 On-Device Transformers (NEW!)
- 🚀 CPU-optimized language models
- 💻 No internet required after model download
- 🔒 Complete privacy - your data stays local
- 📦 Lightweight and portable
- 🎯 Perfect for mobile, edge, and offline applications

---

## ⚡ Speed Comparison
| Service         | Characters/sec |
|-----------------|----------------|
| Sixfinger API   | ~1,100         |
| Anthropic Claude| 80-120         |
| OpenAI GPT-4    | 50-100         |
| Other APIs      | 30-60          |

---

## 💎 Plans & Pricing
| Plan    | Price      | Requests/month | Tokens/month |
|---------|------------|----------------|-------------|
| Free    | $0         | 200            | 20,000      |
| Starter | $8.99      | 3,000          | 300,000     |
| Pro     | $22.99     | 75,000         | 7,500,000   |
| Plus    | $57.99     | 500,000        | 50,000,000  |

---

## 📦 Installation

### Basic Installation (Cloud API only)
```bash
pip install sixfinger
```

### With Async Support
```bash
pip install sixfinger[async]
```

### With On-Device Transformers
```bash
pip install sixfinger[transformers]
```

### Complete Installation (All Features)
```bash
pip install sixfinger[all]
```

---

## 🚀 Quick Start

### ☁️ Cloud API Usage

#### Basic Chat
```python
from sixfinger import API

client = API(api_key="sixfinger_xxx")
response = client.chat("Merhaba!")
print(response.content)
```

#### Conversation with Context
```python
from sixfinger import API

client = API(api_key="sixfinger_xxx")
conv = client.conversation()

conv.send("Merhaba!")
conv.send("Python nedir?")
conv.send("Neden popüler?")  # Remembers context!
```

#### Streaming
```python
from sixfinger import API

client = API(api_key="sixfinger_xxx")

for chunk in client.chat("Tell me a story", stream=True):
    print(chunk, end='', flush=True)
```

#### Async Support
```python
import asyncio
from sixfinger import AsyncAPI

async def main():
    async with AsyncAPI(api_key="sixfinger_xxx") as client:
        response = await client.chat("Merhaba!")
        print(response.content)

asyncio.run(main())
```

#### Model Selection
```python
# Auto model (recommended)
response = client.chat("Merhaba!")

# Turkish-optimized
response = client.chat("Osmanlı tarihi", model="qwen3-32b")

# Complex tasks
response = client.chat("Explain quantum physics", model="llama-70b")

# Fast responses
response = client.chat("Quick answer", model="llama-8b-instant")
```

### 📱 On-Device Transformers Usage

```python
from sixfinger.transformers import SpeedLM

# Initialize model
model = SpeedLM()

# Train on your data
model.train_file('data.txt')

# Generate text
output = model.generate(b'Hello', length=100)
print(output.decode())
```

---

## 🤖 Available Cloud Models

| Model | Key | Size | Language | Plan |
|-------|-----|------|----------|------|
| Llama 3.1 8B Instant | `llama-8b-instant` | 8B | Multilingual | FREE+ |
| Allam 2 7B | `allam-2-7b` | 7B | Turkish/Arabic | FREE+ |
| Qwen3 32B ⭐ | `qwen3-32b` | 32B | Turkish | STARTER+ |
| Llama 3.3 70B | `llama-70b` | 70B | Multilingual | STARTER+ |
| GPT-OSS 120B | `gpt-oss-120b` | 120B | Multilingual | PRO+ |

---

## 📚 Documentation & Resources
- 🎯 [Start for Free](https://sfapi.pythonanywhere.com)
- 📖 [API Documentation](https://sfapi.pythonanywhere.com/docs)
- 💬 [Email Support](mailto:sixfingerdev@gmail.com)

---

## 🔑 Getting Your API Key

1. Sign up at [sfapi.pythonanywhere.com](https://sfapi.pythonanywhere.com)
2. Verify your email
3. Get your API key from the Dashboard

---

## 📂 Repository Structure

```
sixfinger/
├── api.py              # Cloud API client (sync + async)
├── models.py           # Data models
├── errors.py           # Custom exceptions
└── transformers/       # On-device language models
    ├── cli/           # Command-line tools
    ├── generation/    # Text generation utilities
    ├── models/        # SpeedLM model implementation
    └── utils/         # Helper utilities
```

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## ⚡ Why Sixfinger?

Sixfinger is one of the fastest AI platforms in the world, offering:
- **Cloud API**: 10-20x faster than competitors with automatic model selection
- **On-Device Models**: Run AI anywhere without internet
- **Multi-language Support**: Optimized for Turkish, Arabic, Chinese and more
- **Real-time Streaming**: Get responses as they're generated
- **Privacy Options**: Choose between cloud speed or local privacy

Perfect for production applications, mobile apps, and edge deployments!
