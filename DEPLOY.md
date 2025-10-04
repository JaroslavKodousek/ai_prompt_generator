# Deployment Guide

This guide covers deploying the AI Prompt Generator to various platforms.

## 🐳 Docker Deployment

### Build and Run Locally

```bash
# Build the image
docker build -t ai-prompt-generator .

# Run with environment file
docker run -p 8000:8000 --env-file .env ai-prompt-generator

# Run with inline env vars
docker run -p 8000:8000 \
  -e GEMINI_API_KEY=your_key \
  ai-prompt-generator
```

### Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - MAX_CONCURRENT_REQUESTS=5
    volumes:
      - ./results:/app/results
    restart: unless-stopped
```

Run:
```bash
docker-compose up -d
```

## ☁️ Cloudflare Workers

### Prerequisites

```bash
npm install -g wrangler
wrangler login
```

### Deploy

```bash
# Set secrets
wrangler secret put GEMINI_API_KEY
wrangler secret put ANTHROPIC_API_KEY

# Deploy
wrangler deploy
```

### Custom Domain

In `wrangler.toml`:
```toml
routes = [
  { pattern = "api.yourdomain.com", custom_domain = true }
]
```

## 🚀 Heroku

```bash
# Login
heroku login

# Create app
heroku create ai-prompt-generator

# Set env vars
heroku config:set GEMINI_API_KEY=your_key

# Deploy
git push heroku main

# Scale
heroku ps:scale web=1
```

Create `Procfile`:
```
web: uvicorn api:app --host=0.0.0.0 --port=${PORT:-8000}
```

## 📦 AWS Lambda (with API Gateway)

### Using Zappa

Install:
```bash
pip install zappa
```

Initialize:
```bash
zappa init
```

Deploy:
```bash
zappa deploy production
```

### Using AWS SAM

Create `template.yaml`:
```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Resources:
  ApiFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: .
      Handler: api.app
      Runtime: python3.11
      Environment:
        Variables:
          GEMINI_API_KEY: !Ref GeminiApiKey
      Events:
        ApiEvent:
          Type: Api
          Properties:
            Path: /{proxy+}
            Method: ANY
```

## 🔵 Azure App Service

```bash
# Login
az login

# Create resource group
az group create --name ai-prompt-gen --location eastus

# Create app service plan
az appservice plan create \
  --name ai-prompt-plan \
  --resource-group ai-prompt-gen \
  --sku B1 \
  --is-linux

# Create web app
az webapp create \
  --resource-group ai-prompt-gen \
  --plan ai-prompt-plan \
  --name ai-prompt-generator \
  --runtime "PYTHON|3.11"

# Set env vars
az webapp config appsettings set \
  --resource-group ai-prompt-gen \
  --name ai-prompt-generator \
  --settings GEMINI_API_KEY=your_key

# Deploy
az webapp up --name ai-prompt-generator
```

## 🟢 Google Cloud Run

```bash
# Build container
gcloud builds submit --tag gcr.io/PROJECT_ID/ai-prompt-generator

# Deploy
gcloud run deploy ai-prompt-generator \
  --image gcr.io/PROJECT_ID/ai-prompt-generator \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY=your_key
```

## 🔴 Railway

```bash
# Install CLI
npm install -g railway

# Login
railway login

# Initialize
railway init

# Deploy
railway up

# Set env vars
railway variables set GEMINI_API_KEY=your_key
```

Or use the Railway button:

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template)

## 🟣 Render

Create `render.yaml`:

```yaml
services:
  - type: web
    name: ai-prompt-generator
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn api:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: GEMINI_API_KEY
        sync: false
      - key: PYTHON_VERSION
        value: 3.11.0
```

Deploy via Render dashboard or CLI.

## 🐙 GitHub Actions Auto-Deploy

The repo includes `.github/workflows/deploy-cloudflare.yml`.

### Setup Secrets

In GitHub repo settings → Secrets:

```
CLOUDFLARE_API_TOKEN=your_token
GEMINI_API_KEY=your_key
```

### Trigger Deployment

```bash
git push origin main
```

## 🔐 Environment Variables

All platforms need these:

```bash
# Required (choose one)
GEMINI_API_KEY=your_gemini_key
ANTHROPIC_API_KEY=your_anthropic_key

# Optional
MAX_CONCURRENT_REQUESTS=5
REQUEST_DELAY_SECONDS=0.5
MAX_TOKENS=4096
TEMPERATURE=0.0
LOG_LEVEL=INFO
```

## 📊 Monitoring

### Health Check Endpoint

```bash
curl https://your-api.com/health
```

### Logging

Most platforms automatically capture logs:

```bash
# Docker
docker logs <container_id>

# Heroku
heroku logs --tail

# Cloud Run
gcloud run services logs read ai-prompt-generator

# Cloudflare
wrangler tail
```

## 🔄 CI/CD Best Practices

1. **Test Before Deploy**
   - Run `pytest tests/` in CI
   - Check code quality with `flake8`

2. **Environment Separation**
   - Use different API keys for dev/staging/prod
   - Deploy to staging first

3. **Secrets Management**
   - Never commit `.env` to git
   - Use platform secret managers
   - Rotate keys regularly

4. **Monitoring**
   - Set up error tracking (Sentry)
   - Monitor API costs
   - Track response times

## 🚨 Troubleshooting

**Build Failures:**
```bash
# Check Python version
python --version  # Should be 3.11+

# Reinstall dependencies
pip install -r requirements.txt --no-cache-dir
```

**API Errors:**
```bash
# Verify env vars
echo $GEMINI_API_KEY

# Check logs
docker logs <container>
```

**Performance Issues:**
```bash
# Reduce concurrent requests
export MAX_CONCURRENT_REQUESTS=3

# Increase delay
export REQUEST_DELAY_SECONDS=1.0
```

## 📈 Scaling

### Horizontal Scaling

- Docker: Use orchestration (Kubernetes, Docker Swarm)
- Serverless: Auto-scales by default
- Cloud: Increase instance count

### Vertical Scaling

- Increase CPU/RAM allocation
- Use faster instance types
- Optimize `MAX_CONCURRENT_REQUESTS`

### Caching

Add Redis for result caching:

```python
# In api.py
import redis
cache = redis.Redis(host='localhost', port=6379)
```

## 💰 Cost Optimization

1. **Use Gemini Free Tier**
   - 1500 requests/day free
   - Much cheaper than Claude

2. **Cache Results**
   - Store extraction results
   - Avoid re-processing same docs

3. **Optimize Strategies**
   - Use fewer strategies for simple docs
   - Start with fast/cheap strategies

4. **Monitor Usage**
   - Track API costs daily
   - Set up billing alerts

---

For more help, see the [main README](README.md) or open an issue.
