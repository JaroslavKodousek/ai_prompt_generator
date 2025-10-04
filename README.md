# AI Prompt Generator - Document Data Extraction

A powerful tool that tests **20 different AI extraction strategies** to find the best approach for extracting data from documents.

## ✨ Features

- 🎯 **20 Different Strategies** - Tests multiple extraction approaches
- 🔄 **Multi-Provider Support** - Works with **OpenRouter** (100+ models), **Google Gemini**, AND **Anthropic Claude**
- 🆓 **FREE Models Available** - Use Gemini 2.0 Flash, Llama 3.2, and more for FREE via OpenRouter
- 📊 **Comprehensive Validation** - Compares results against ground truth
- 💰 **Cost Analysis** - Tracks API costs and token usage for each strategy
- ⚡ **Parallel Execution** - Runs strategies concurrently with rate limiting
- 📈 **Detailed Reports** - Generates JSON, CSV, and console reports
- 🌐 **Web API** - FastAPI endpoint for integration
- ☁️ **Cloud Ready** - Deploy to Cloudflare, Docker, or any cloud platform

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/ai_prompt_generator.git
cd ai_prompt_generator

# Install dependencies
pip install -r requirements.txt

# Set up your API key
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY or ANTHROPIC_API_KEY
```

### 2. Configure API Key

Edit `.env` and add your API key:

```bash
# For Google Gemini (RECOMMENDED - FREE tier: 1500 req/day!)
GEMINI_API_KEY=your_gemini_api_key_here

# OR for OpenRouter (100+ models, some free but strict rate limits)
OPENROUTER_API_KEY=sk-or-v1-your_key_here
OPENROUTER_MODEL=google/gemini-2.0-flash-exp:free

# OR for Anthropic Claude
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

Get your API keys:
- **Gemini**: https://aistudio.google.com/app/apikey (RECOMMENDED - 1500 free requests/day!)
- **OpenRouter**: https://openrouter.ai/keys (100+ models, some free with rate limits)
- **Anthropic**: https://console.anthropic.com/settings/keys

### 3. Run Extraction

```bash
# Using Google Gemini (default, RECOMMENDED - 1500 free req/day!)
python main.py sample_documents/sample_invoice.txt

# Using OpenRouter with specific model
python main.py sample_documents/sample_invoice.txt --provider openrouter --model "anthropic/claude-3.5-sonnet"

# Using Anthropic Claude directly
python main.py sample_documents/sample_invoice.txt --provider anthropic

# With ground truth validation
python main.py sample_documents/sample_invoice.txt --ground-truth sample_documents/ground_truth.json

# List all strategies
python main.py --list-strategies

# Customize settings
python main.py document.pdf --max-concurrent 3 --delay 1.0
```

**📖 See [OPENROUTER.md](OPENROUTER.md) for complete OpenRouter guide with model selection!**

## 📡 Web API Usage

Start the API server:

```bash
# Start server
python api.py

# Or with uvicorn
uvicorn api:app --host 0.0.0.0 --port 8000
```

API Endpoints:

```bash
# List strategies
curl http://localhost:8000/strategies

# Extract from document (using OpenRouter - FREE!)
curl -X POST http://localhost:8000/extract \
  -F "file=@invoice.pdf" \
  -F "provider=openrouter" \
  -F "model=google/gemini-2.0-flash-exp:free"

# Use different model
curl -X POST http://localhost:8000/extract \
  -F "file=@invoice.pdf" \
  -F "provider=openrouter" \
  -F "model=anthropic/claude-3.5-sonnet"

# Extract with Gemini
curl -X POST http://localhost:8000/extract \
  -F "file=@invoice.pdf" \
  -F "provider=gemini"
```

## ☁️ Deployment

### Docker Deployment

```bash
# Build image
docker build -t ai-prompt-generator .

# Run container
docker run -p 8000:8000 --env-file .env ai-prompt-generator

# Or with docker-compose
docker-compose up
```

### Cloudflare Workers

```bash
# Install Wrangler
npm install -g wrangler

# Login to Cloudflare
wrangler login

# Deploy
wrangler deploy
```

### GitHub Actions

The repo includes CI/CD workflows:
- `.github/workflows/ci.yml` - Runs tests on push
- `.github/workflows/deploy-cloudflare.yml` - Auto-deploys to Cloudflare

Set secrets in GitHub:
- `CLOUDFLARE_API_TOKEN`

## 🎯 20 Extraction Strategies

| ID | Strategy | Category | Use Case |
|----|----------|----------|----------|
| 01 | Basic Direct | basic | Simple documents |
| 02 | Structured Schema | structured | Predefined schemas |
| 03 | Chain-of-Thought | reasoning | Complex documents |
| 04 | Expert Role | role-based | Domain-specific docs |
| 05 | Few-Shot Learning | few-shot | Pattern-based extraction |
| 06 | Step-by-Step | instructional | Multi-field documents |
| 07 | Table-Focused | specialized | Tables and invoices |
| 08 | Entity-Focused | specialized | Named entity extraction |
| 09 | Minimal | efficiency | Cost optimization |
| 10 | Verbose Detailed | detailed | Maximum accuracy |
| 11 | Context-Aware | contextual | Variable formats |
| 12 | XML Format | format-variation | Hierarchical data |
| 13 | Confidence Scoring | quality-aware | Quality assessment |
| 14 | Multi-Pass | iterative | Complex documents |
| 15 | Template Matching | pattern-based | Standard forms |
| 16 | Key-Value Pairs | specialized | Label-value documents |
| 17 | Semantic | semantic | Unstructured text |
| 18 | Prioritized | priority-based | Large documents |
| 19 | Comparative | multi-interpretation | Ambiguous documents |
| 20 | Hybrid | hybrid | Maximum accuracy |

## 📁 Project Structure

```
ai_prompt_generator/
├── main.py                   # CLI application
├── api.py                    # FastAPI web service
├── Dockerfile               # Docker container
├── wrangler.toml           # Cloudflare Workers config
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create this)
├── .github/workflows/      # GitHub Actions CI/CD
├── src/
│   ├── core/              # Core engine and models
│   │   ├── llm_provider.py     # Multi-provider support
│   │   ├── base_strategy.py
│   │   ├── extraction_engine.py
│   │   ├── models.py
│   │   └── validator.py
│   ├── strategies/        # 20 extraction strategies
│   │   ├── strategy_01_basic.py
│   │   └── ...
│   └── utils/            # Utilities
│       ├── document_loader.py
│       └── reporter.py
├── tests/                # Tests
├── sample_documents/     # Sample files
└── results/             # Output directory
```

## 💡 Usage Examples

### CLI Examples

```bash
# Basic extraction with OpenRouter (default - FREE!)
python main.py invoice.pdf

# Use specific model
python main.py invoice.pdf --model "anthropic/claude-3.5-sonnet"

# Use Gemini directly
python main.py invoice.pdf --provider gemini

# With validation
python main.py invoice.pdf --ground-truth truth.json

# Custom settings
python main.py document.pdf --max-concurrent 10 --delay 0.2
```

### API Examples

```python
import requests

# Upload and extract with OpenRouter (FREE model!)
files = {"file": open("invoice.pdf", "rb")}
data = {
    "provider": "openrouter",
    "model": "google/gemini-2.0-flash-exp:free"
}
response = requests.post("http://localhost:8000/extract", files=files, data=data)
results = response.json()

print(f"Best strategy: {results['best_strategy']}")
print(f"Total cost: ${results['total_cost']}")  # $0.00 for free models!
```

## 🔧 Configuration

Environment variables in `.env`:

```bash
# API Keys (choose one or more)
OPENROUTER_API_KEY=sk-or-v1-your_key  # RECOMMENDED
GEMINI_API_KEY=your_gemini_key
ANTHROPIC_API_KEY=your_anthropic_key

# OpenRouter Model Selection (100+ models available!)
OPENROUTER_MODEL=google/gemini-2.0-flash-exp:free  # FREE
# or: meta-llama/llama-3.2-3b-instruct:free (also FREE)
# or: anthropic/claude-3.5-sonnet (paid, high quality)
# See all: https://openrouter.ai/models

# Configuration
MAX_CONCURRENT_REQUESTS=5
REQUEST_DELAY_SECONDS=0.5
MAX_TOKENS=4096
TEMPERATURE=0.0
```

## 📊 Output Files

After extraction:

- `results/report_TIMESTAMP.json` - Full detailed report
- `results/summary_TIMESTAMP.csv` - CSV summary for analysis
- `results/extracted_data/` - Individual extraction results per strategy

## 🧪 Validation Metrics

Calculated metrics:
- **Accuracy**: Match rate against ground truth
- **Completeness**: Percentage of fields extracted
- **Consistency**: Exact match rate
- **Cost**: Total API cost in USD
- **Speed**: Execution time per strategy

## 📄 Supported Document Types

- PDF files (.pdf)
- Images (.png, .jpg, .jpeg, .tiff, .bmp) - with OCR
- Text files (.txt, .md)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `pytest tests/`
5. Submit a pull request

## 📝 License

MIT License - see LICENSE file

## 🆘 Troubleshooting

**API Key Errors:**
```bash
# Check your .env file
cat .env

# Make sure the key is correct
# For Gemini: starts with "AI..."
# For Anthropic: starts with "sk-ant-..."
```

**Module Import Errors:**
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

**Rate Limiting:**
```bash
# Reduce concurrent requests
python main.py document.pdf --max-concurrent 2 --delay 1.0
```

## 🌟 Why Use This Tool?

- **Save Time**: Test 20 strategies in parallel instead of manually
- **Save Money**: Find the most cost-effective approach (FREE models available!)
- **Improve Accuracy**: Compare strategies to find the best performer
- **100+ Models**: Access to Gemini, Claude, GPT-4, Llama, Mistral, and more via OpenRouter
- **Flexible**: Switch between providers and models easily
- **Production Ready**: API, Docker, Cloudflare deployment included

## 💰 Cost Comparison

| Provider | Free Tier | Rate Limits | Best For |
|----------|-----------|-------------|----------|
| **Gemini** | ✅ 1500 req/day | Good (60 req/min) | **RECOMMENDED** - Testing all 20 strategies |
| **OpenRouter** | ✅ Some free models | Very strict | Access to 100+ models, but slow for free tier |
| **Anthropic** | ❌ Paid only | High | Enterprise use, best quality |

**Recommendation**: Use **Gemini** for testing (1500 free requests/day), switch to OpenRouter paid models for production!

## 📞 Support

- Issues: https://github.com/yourusername/ai_prompt_generator/issues
- Discussions: https://github.com/yourusername/ai_prompt_generator/discussions

---

Made with ❤️ for the AI community
