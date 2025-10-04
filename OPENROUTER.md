# Using OpenRouter

OpenRouter gives you access to **100+ AI models** through a single API!

## Why OpenRouter?

- **Many FREE models**: Gemini 2.0 Flash, Llama 3.2, and more
- **Access to ANY model**: GPT-4, Claude, Gemini, Llama, Mistral, etc.
- **One API key for all**: No need for separate keys
- **Real-time pricing**: See costs for each model
- **No rate limits on free tier**

## Setup

### 1. Get API Key

Get your free API key: https://openrouter.ai/keys

### 2. Add to .env

```bash
OPENROUTER_API_KEY=sk-or-v1-your_key_here
```

### 3. Choose Model (Optional)

Browse models: https://openrouter.ai/models

In `.env`:
```bash
# Free models (recommended!)
OPENROUTER_MODEL=google/gemini-2.0-flash-exp:free
# or
OPENROUTER_MODEL=meta-llama/llama-3.2-3b-instruct:free

# Paid models
OPENROUTER_MODEL=anthropic/claude-3.5-sonnet
OPENROUTER_MODEL=openai/gpt-4o
OPENROUTER_MODEL=google/gemini-pro-1.5
```

## Usage

### CLI

```bash
# Default (uses OPENROUTER_MODEL from .env)
python main.py sample_documents/sample_invoice.txt

# Specify model
python main.py document.pdf --model "anthropic/claude-3.5-sonnet"

# Different provider
python main.py document.pdf --provider openrouter --model "openai/gpt-4o"
```

### API

```bash
# With curl
curl -X POST http://localhost:8000/extract \
  -F "file=@invoice.pdf" \
  -F "provider=openrouter" \
  -F "model=google/gemini-2.0-flash-exp:free"

# Different model
curl -X POST http://localhost:8000/extract \
  -F "file=@invoice.pdf" \
  -F "provider=openrouter" \
  -F "model=anthropic/claude-3.5-sonnet"
```

### Python

```python
import requests

files = {"file": open("invoice.pdf", "rb")}
data = {
    "provider": "openrouter",
    "model": "google/gemini-2.0-flash-exp:free"
}

response = requests.post(
    "http://localhost:8000/extract",
    files=files,
    data=data
)
```

## Popular Models

### Free Models

| Model | Best For |
|-------|----------|
| `google/gemini-2.0-flash-exp:free` | General purpose, fast |
| `meta-llama/llama-3.2-3b-instruct:free` | Small, efficient |
| `meta-llama/llama-3.2-1b-instruct:free` | Ultra fast |

### Paid Models (Cheap)

| Model | Cost/1M tokens | Best For |
|-------|----------------|----------|
| `google/gemini-flash-1.5` | $0.075 | Fast, affordable |
| `anthropic/claude-3-haiku` | $0.25 | Balanced |
| `openai/gpt-3.5-turbo` | $0.50 | Legacy support |

### Premium Models

| Model | Cost/1M tokens | Best For |
|-------|----------------|----------|
| `anthropic/claude-3.5-sonnet` | $3.00 | Best quality |
| `openai/gpt-4o` | $2.50 | Strong reasoning |
| `google/gemini-pro-1.5` | $1.25 | Long context |

## Model Specification

### In Code

You can specify model in **3 ways**:

1. **Environment Variable** (.env):
   ```bash
   OPENROUTER_MODEL=google/gemini-2.0-flash-exp:free
   ```

2. **Command Line**:
   ```bash
   python main.py doc.pdf --model "anthropic/claude-3.5-sonnet"
   ```

3. **API Request**:
   ```bash
   curl -F "model=openai/gpt-4o" ...
   ```

Priority: **CLI/API > Environment Variable > Default**

### Default Model

If not specified, defaults to: `google/gemini-2.0-flash-exp:free`

## Cost Tracking

The app automatically tracks costs for each strategy:

```bash
# Free models show $0.0000
✓ Strategy 01: $0.0000 (free model)

# Paid models show actual cost
✓ Strategy 01: $0.0023 (paid model)
```

## Switching Models Mid-Session

You can test different models easily:

```bash
# Test with free model
python main.py doc.pdf --model "google/gemini-2.0-flash-exp:free"

# Test with premium model
python main.py doc.pdf --model "anthropic/claude-3.5-sonnet"

# Compare results and costs!
```

## Tips

1. **Start with free models** - They're surprisingly good!
2. **Compare costs** - Check pricing before running 20 strategies
3. **Use specialized models** - Some models excel at specific tasks
4. **Monitor usage** - Check dashboard at https://openrouter.ai/activity
5. **Set limits** - Configure spending limits in OpenRouter dashboard

## Troubleshooting

**Invalid model error:**
```bash
# Check available models
https://openrouter.ai/models

# Make sure model name is exact
OPENROUTER_MODEL=google/gemini-2.0-flash-exp:free
```

**API key errors:**
```bash
# Verify key in .env
cat .env | grep OPENROUTER

# Key should start with: sk-or-v1-
```

**Rate limits:**
```bash
# Reduce concurrent requests
python main.py doc.pdf --max-concurrent 2 --delay 1.0
```

## More Info

- **Models**: https://openrouter.ai/models
- **Pricing**: https://openrouter.ai/docs/pricing
- **API Docs**: https://openrouter.ai/docs
- **Dashboard**: https://openrouter.ai/activity

---

OpenRouter makes it easy to experiment with different models and find the best one for your use case!
