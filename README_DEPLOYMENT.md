# Web Frontend Deployment Guide

## Quick Start - Run Locally

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up your API keys in `.env`:**
   ```
   GEMINI_API_KEY=your_key_here
   OPENROUTER_API_KEY=your_key_here
   ANTHROPIC_API_KEY=your_key_here
   ```

3. **Run the web server:**
   ```bash
   python api.py
   ```

4. **Open your browser:**
   Navigate to `http://localhost:8000`

## Deployment to Cloudflare

### Option 1: Cloudflare Pages (Recommended for Static + Serverless)

Cloudflare Pages now supports Python with Cloudflare Workers:

1. **Install Wrangler CLI:**
   ```bash
   npm install -g wrangler
   ```

2. **Login to Cloudflare:**
   ```bash
   wrangler login
   ```

3. **Update `wrangler.toml` with your account details**

4. **Deploy:**
   ```bash
   wrangler deploy
   ```

5. **Set environment variables in Cloudflare dashboard:**
   - Go to Workers & Pages > Your Worker > Settings > Variables
   - Add your API keys as secrets:
     - `GEMINI_API_KEY`
     - `OPENROUTER_API_KEY`
     - `ANTHROPIC_API_KEY`

### Option 2: Deploy to Railway/Render/Fly.io

These platforms have better Python support:

#### Railway
1. Connect your GitHub repo
2. Set environment variables
3. Railway auto-detects FastAPI and deploys

#### Render
1. Create new Web Service
2. Connect GitHub repo
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn api:app --host 0.0.0.0 --port $PORT`
5. Add environment variables

#### Fly.io
```bash
fly launch
fly secrets set GEMINI_API_KEY=xxx OPENROUTER_API_KEY=xxx
fly deploy
```

### Option 3: Traditional VPS (DigitalOcean, AWS, etc.)

1. **SSH into your server**

2. **Clone the repository:**
   ```bash
   git clone <your-repo>
   cd ai_prompt_generator
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

5. **Run with production server:**
   ```bash
   # Using gunicorn
   pip install gunicorn
   gunicorn api:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

   # Or using uvicorn directly
   uvicorn api:app --host 0.0.0.0 --port 8000 --workers 4
   ```

6. **Set up nginx as reverse proxy (optional but recommended)**

7. **Set up systemd service for auto-restart**

## Important Notes

### API Keys Security
- Never commit API keys to Git
- Use environment variables or secrets management
- For Cloudflare, use encrypted environment variables in the dashboard

### Rate Limiting
- Add rate limiting to prevent abuse
- Consider implementing user authentication for production
- Monitor API costs closely

### File Upload Limits
- Default FastAPI limit is 1MB
- Increase if needed in `api.py`:
  ```python
  app.add_middleware(
      Middleware,
      max_upload_size=10_000_000  # 10MB
  )
  ```

### CORS Configuration
- Current setup allows all origins (`allow_origins=["*"]`)
- For production, restrict to your domain:
  ```python
  allow_origins=["https://yourdomain.com"]
  ```

## Architecture

```
┌─────────────┐
│   Browser   │
│  (Frontend) │
└──────┬──────┘
       │
       │ HTTP/Upload
       │
┌──────▼──────┐
│  FastAPI    │
│  (Backend)  │
└──────┬──────┘
       │
       │ API Calls
       │
┌──────▼──────────┐
│   LLM Provider  │
│ (Gemini/Claude) │
└─────────────────┘
```

## Features

✅ **Upload documents** (PDF, images, text)
✅ **Test 20 extraction strategies** simultaneously
✅ **Interactive results dashboard** with charts
✅ **Educational content** explaining each strategy
✅ **Responsive design** for mobile/desktop
✅ **Dark theme** UI
✅ **Cost tracking** per strategy
✅ **Performance metrics** (speed, tokens, accuracy)

## Development

- Frontend: Vanilla JavaScript (no framework needed)
- Backend: FastAPI (Python)
- Styling: Custom CSS with CSS Grid/Flexbox
- API: RESTful with async support

## Support

For issues or questions, check the main README.md or open an issue on GitHub.
