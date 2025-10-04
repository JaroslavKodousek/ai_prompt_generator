# 🚀 Deploy to Cloud - Step by Step

**Important:** Cloudflare Workers doesn't fully support Python FastAPI yet. Use Railway, Render, or Fly.io instead.

---

## Option 1: Railway (Recommended ⭐)

**Best for:** Easiest deployment, automatic HTTPS, free tier available

### Steps:

1. **Sign up at [Railway.app](https://railway.app)**
   - Use GitHub login

2. **Push your code to GitHub:**
   ```bash
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/ai_prompt_generator.git
   git push -u origin main
   ```

3. **Create new project in Railway:**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Railway auto-detects Python and deploys!

4. **Add environment variables:**
   - Go to your project → Variables tab
   - Add these secrets:
     ```
     GEMINI_API_KEY=your_key_here
     OPENROUTER_API_KEY=your_key_here
     ANTHROPIC_API_KEY=your_key_here
     ```

5. **Get your URL:**
   - Railway provides a URL like: `https://your-app.railway.app`
   - Your app is live! 🎉

**Cost:** Free tier includes $5/month credit (plenty for testing)

---

## Option 2: Render

**Best for:** True free tier (no credit card required)

### Steps:

1. **Sign up at [Render.com](https://render.com)**

2. **Push code to GitHub** (same as Railway step 2)

3. **Create Web Service:**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Render auto-detects `render.yaml`!

4. **Configure (if auto-detect doesn't work):**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn api:app --host 0.0.0.0 --port $PORT`
   - Python Version: 3.11

5. **Add environment variables:**
   - In the dashboard → Environment tab
   - Add your API keys

6. **Deploy:**
   - Click "Create Web Service"
   - Wait 2-3 minutes
   - Get URL: `https://your-app.onrender.com`

**Cost:** Completely free tier (spins down after inactivity, takes 30s to wake up)

---

## Option 3: Fly.io

**Best for:** Global deployment, multiple regions

### Steps:

1. **Install Fly CLI:**
   ```bash
   # Windows (PowerShell)
   powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"

   # Mac/Linux
   curl -L https://fly.io/install.sh | sh
   ```

2. **Sign up and login:**
   ```bash
   fly auth signup
   # or
   fly auth login
   ```

3. **Launch app:**
   ```bash
   fly launch
   ```
   - Choose app name
   - Select region
   - Don't deploy yet (we need to add secrets)

4. **Set secrets:**
   ```bash
   fly secrets set GEMINI_API_KEY=your_key_here
   fly secrets set OPENROUTER_API_KEY=your_key_here
   fly secrets set ANTHROPIC_API_KEY=your_key_here
   ```

5. **Deploy:**
   ```bash
   fly deploy
   ```

6. **Open app:**
   ```bash
   fly open
   ```

**Cost:** Free tier includes 3 small VMs

---

## Option 4: Cloudflare Pages (Static Frontend Only)

Since Cloudflare doesn't support FastAPI, you can deploy just the frontend to Cloudflare Pages and host the backend elsewhere.

### Steps:

1. **Deploy backend to Railway/Render** (see above)

2. **Update `static/app.js` line 2:**
   ```javascript
   const API_BASE = 'https://your-railway-app.railway.app';
   ```

3. **Deploy static files to Cloudflare Pages:**
   ```bash
   # Install Wrangler
   npm install -g wrangler

   # Login
   wrangler login

   # Deploy static folder
   wrangler pages deploy static --project-name=ai-prompt-tester
   ```

4. **Your frontend is on Cloudflare, backend on Railway!**

---

## Quick Comparison

| Platform | Free Tier | Setup Time | Best For |
|----------|-----------|------------|----------|
| **Railway** | $5/month credit | 2 min | Easiest, best DX |
| **Render** | ✅ True free | 3 min | No credit card needed |
| **Fly.io** | 3 small VMs | 5 min | Global deployment |
| **Cloudflare** | ❌ No Python support | - | Not compatible |

---

## After Deployment

### Update API Keys
All platforms let you update environment variables without redeploying:
- Railway: Project → Variables
- Render: Dashboard → Environment
- Fly.io: `fly secrets set KEY=value`

### Monitor Usage
- Check your API provider dashboards for usage
- Most LLM providers have free tiers with limits
- Consider adding rate limiting for production

### Custom Domain (Optional)
All platforms support custom domains:
1. Add CNAME record: `your-domain.com → app-url.platform.com`
2. Add domain in platform dashboard
3. Platform handles SSL automatically

---

## Recommended Approach

**For Testing:**
→ Use **Render** (completely free, no card needed)

**For Production:**
→ Use **Railway** (best performance, easy monitoring)

**For Global Scale:**
→ Use **Fly.io** (multi-region support)

---

## Need Help?

Each platform has excellent docs:
- Railway: https://docs.railway.app
- Render: https://render.com/docs
- Fly.io: https://fly.io/docs

All support FastAPI out of the box! 🚀
