# Quick Start Guide

Get up and running in **5 minutes** with Google Gemini (FREE - 1500 requests/day!).

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Get Google Gemini API Key

1. Go to https://aistudio.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your key (starts with `AIza...`)

## Step 3: Configure .env

```bash
# Open .env file and add:
GEMINI_API_KEY=paste_your_key_here
```

## Step 4: Run Your First Extraction!

```bash
python main.py sample_documents/sample_invoice.txt
```

That's it! 🎉

## What Just Happened?

The app:
1. ✅ Loaded the sample invoice
2. ✅ Tested **20 different extraction strategies** using Gemini
3. ✅ Compared results and costs
4. ✅ Identified the best strategy
5. ✅ Saved detailed reports to `results/`
6. ✅ **All 20 strategies = FREE!** (Gemini free tier)

## Next Steps

### Try Different Providers

```bash
# Use OpenRouter (if you have a key)
python main.py sample_documents/sample_invoice.txt --provider openrouter

# Use Anthropic Claude (paid)
python main.py sample_documents/sample_invoice.txt --provider anthropic
```

### Test Your Own Documents

```bash
python main.py path/to/your/invoice.pdf
python main.py path/to/your/receipt.jpg
python main.py path/to/your/contract.txt
```

### With Validation

Create a ground truth file:

```json
// truth.json
{
  "invoice_number": "12345",
  "total": 500.00,
  "date": "2024-01-15"
}
```

Run with validation:

```bash
python main.py invoice.pdf --ground-truth truth.json
```

### Start the Web API

```bash
python api.py
```

Then visit http://localhost:8000/docs for interactive API docs!

## Provider Comparison

**Google Gemini (Default - RECOMMENDED):**
- ✅ **1500 free requests/day**
- ✅ Fast and reliable
- ✅ Good rate limits (60 req/min)
- ✅ Perfect for testing all 20 strategies
- Get key: https://aistudio.google.com/app/apikey

**OpenRouter (Alternative):**
- ✅ Access to 100+ models
- ✅ Some free models available
- ⚠️ Strict rate limits on free tier (only 1-2 strategies work)
- ✅ Best for trying different paid models
- Get key: https://openrouter.ai/keys

**Anthropic Claude (Enterprise):**
- ✅ Highest quality
- ❌ Paid only
- Get key: https://console.anthropic.com/settings/keys

## Understanding Results

After extraction, check `results/` folder:

```
results/
├── report_20250104_120000.json    # Full detailed report
├── summary_20250104_120000.csv    # CSV for spreadsheet analysis
└── extracted_data/                # Individual strategy results
    ├── strategy_01_extracted.json
    ├── strategy_02_extracted.json
    └── ...
```

## Cost Tracking

The app shows cost per strategy:

```
Running: Basic Direct Extraction
  ✓ Completed in 1.2s, cost: $0.0000  ← FREE!

Running: Chain-of-Thought Extraction
  ✓ Completed in 2.1s, cost: $0.0000  ← FREE!
```

**With free models, ALL extractions cost $0!**

## Troubleshooting

**"GEMINI_API_KEY not found"**
```bash
# Make sure .env file exists and has your key
cat .env | grep GEMINI_API_KEY

# Get your key from:
# https://aistudio.google.com/app/apikey
```

**"Rate limit exceeded"**
```bash
# Reduce concurrent requests
python main.py doc.pdf --max-concurrent 2 --delay 1.0
```

**Import errors**
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

## Need Help?

- 📖 Full guide: [README.md](README.md)
- 🔧 OpenRouter guide: [OPENROUTER.md](OPENROUTER.md)
- 🚀 Deployment guide: [DEPLOY.md](DEPLOY.md)
- 🐛 Report issues: https://github.com/yourusername/ai_prompt_generator/issues

---

**Happy extracting!** 🎉
