# 🚀 Quick Start - Web Interface

## Run the Web Application

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up API keys in `.env`:**
   ```bash
   # At minimum, set one of these:
   GEMINI_API_KEY=your_gemini_key_here
   # OR
   OPENROUTER_API_KEY=your_openrouter_key_here
   # OR
   ANTHROPIC_API_KEY=your_anthropic_key_here
   ```

3. **Start the server:**
   ```bash
   python api.py
   ```

4. **Open your browser:**
   ```
   http://localhost:8000
   ```

## Features

### 1. **Test Strategies Tab**
- Upload any document (PDF, image, or text)
- Choose your AI provider (Gemini, OpenRouter, or Anthropic)
- Click "Analyze with All 20 Strategies"
- Wait for results (this may take 1-2 minutes)

### 2. **Learn About Strategies Tab**
- Browse all 20 extraction strategies
- See descriptions, categories, and cost estimates
- Understand what each strategy does differently

### 3. **Results Dashboard Tab**
- View comparative results from all strategies
- See which strategy performed best
- Check execution time, cost, and accuracy metrics
- Inspect extracted data from each strategy

## What You'll See

The dashboard shows:
- ✅ **Success Rate** - How many strategies succeeded
- ⏱️ **Execution Time** - How fast each strategy ran
- 💰 **Cost** - Estimated API cost per strategy
- 📊 **Extracted Data** - The actual data extracted by each strategy
- 🏆 **Best Strategy** - Recommended strategy for your document type

## Example Use Cases

### Invoice Processing
1. Upload an invoice PDF
2. See which strategy best extracts:
   - Invoice number
   - Line items
   - Totals
   - Dates
   - Vendor info

### Resume Parsing
1. Upload a resume
2. Compare strategies for extracting:
   - Contact info
   - Work experience
   - Skills
   - Education

### Form Data Extraction
1. Upload a scanned form
2. Find the best strategy for:
   - Key-value pairs
   - Tables
   - Checkboxes
   - Signatures

## Tips

- **Start with Gemini** - It's free and fast
- **Use OpenRouter** - For testing multiple model types
- **Compare costs** - See which strategies are most economical
- **Check accuracy** - Some strategies are better for specific document types

## Troubleshooting

### Server won't start
```bash
# Make sure FastAPI is installed
pip install fastapi uvicorn python-multipart

# Try running directly
uvicorn api:app --reload
```

### Can't access localhost:8000
- Check if port 8000 is already in use
- Try a different port: `uvicorn api:app --port 8080`

### API key errors
- Make sure `.env` file exists in the project root
- Verify the API key is valid
- Check you have credits/quota remaining

## Next Steps

Once you've tested locally:
1. See `README_DEPLOYMENT.md` for deployment options
2. Deploy to Railway, Render, or Fly.io for free
3. Share with users to test strategies on their documents
4. Analyze which strategies work best for your use case

## Development

To customize the frontend:
- Edit `static/index.html` for structure
- Edit `static/styles.css` for styling
- Edit `static/app.js` for functionality

The API automatically serves the updated files.

## API Endpoints

If you want to integrate with other tools:

- `GET /` - Web interface
- `GET /strategies` - List all strategies
- `POST /extract` - Extract with all strategies
- `POST /extract-single` - Extract with one strategy
- `GET /health` - Health check

Example API call:
```bash
curl -X POST "http://localhost:8000/extract" \
  -F "file=@invoice.pdf" \
  -F "provider=gemini" \
  -F "max_concurrent=5"
```

Enjoy testing your prompting strategies! 🎉
