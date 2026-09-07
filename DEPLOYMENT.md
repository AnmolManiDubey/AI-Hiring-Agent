# 🚀 Deployment Guide

This guide will help you deploy your LinkedIn Sourcing Agent to production.

## 📋 Prerequisites

- GitHub account
- Vercel account (free tier available)
- Railway account (free tier available) or alternative backend hosting
- API keys configured

## 🎯 Deployment Strategy

We'll deploy the **frontend to Vercel** and the **backend to Railway** (or alternative).

### Frontend (Vercel) + Backend (Railway) Architecture

```
┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │
│   (Vercel)      │◄──►│   (Railway)     │
│   - HTML/CSS/JS │    │   - FastAPI     │
│   - Static      │    │   - Python      │
└─────────────────┘    └─────────────────┘
```

## 🎨 Frontend Deployment (Vercel)

### Step 1: Prepare Frontend

1. **Update API Configuration**
   - The frontend is already configured to use `/api` proxy in production
   - Local development uses `http://localhost:8000`

2. **Create Vercel Configuration**
   - `frontend/vercel.json` is already created
   - Update the backend URL in `vercel.json` after backend deployment

### Step 2: Deploy to Vercel

1. **Install Vercel CLI** (optional):
   ```bash
   npm i -g vercel
   ```

2. **Deploy via GitHub** (Recommended):
   - Push your code to GitHub
   - Go to [vercel.com](https://vercel.com)
   - Import your GitHub repository
   - Set root directory to `frontend`
   - Deploy

3. **Deploy via CLI**:
   ```bash
   cd frontend
   vercel
   ```

### Step 3: Configure Environment Variables

In Vercel dashboard:
- Go to your project settings
- Add environment variables:
  ```
  BACKEND_URL=https://your-backend-url.railway.app
  ```

## ⚙️ Backend Deployment (Railway)

### Step 1: Prepare Backend

1. **Environment Variables**
   Create a `.env` file for local testing:
   ```env
   GOOGLE_API_KEY=your_google_api_key
   GOOGLE_SEARCH_ENGINE_ID=your_search_engine_id
   GROQ_API_KEY=your_groq_api_key
   PORT=8000
   ```

2. **Railway Configuration**
   - `railway.json` is already created
   - `Procfile` is created for Heroku alternative

### Step 2: Deploy to Railway

1. **Install Railway CLI**:
   ```bash
   npm install -g @railway/cli
   ```

2. **Login to Railway**:
   ```bash
   railway login
   ```

3. **Deploy**:
   ```bash
   railway init
   railway up
   ```

4. **Set Environment Variables**:
   ```bash
   railway variables set GOOGLE_API_KEY=your_key
   railway variables set GOOGLE_SEARCH_ENGINE_ID=your_id
   railway variables set GROQ_API_KEY=your_key
   ```

### Step 3: Get Backend URL

After deployment, Railway will provide a URL like:
```
https://your-app-name.railway.app
```

## 🔗 Connect Frontend to Backend

### Update Vercel Configuration

1. **Update `frontend/vercel.json`**:
   ```json
   {
     "routes": [
       {
         "src": "/api/(.*)",
         "dest": "https://your-app-name.railway.app/$1"
       }
     ]
   }
   ```

2. **Redeploy frontend**:
   - Push changes to GitHub
   - Vercel will auto-deploy

## 🚀 Alternative Backend Hosting

### Option 1: Render

1. **Create account** at [render.com](https://render.com)
2. **Connect GitHub repository**
3. **Create Web Service**:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `cd backend && uvicorn enhanced_main:app --host 0.0.0.0 --port $PORT`
4. **Set environment variables**

### Option 2: Heroku

1. **Create account** at [heroku.com](https://heroku.com)
2. **Install Heroku CLI**:
   ```bash
   curl https://cli-assets.heroku.com/install.sh | sh
   ```
3. **Deploy**:
   ```bash
   heroku create your-app-name
   git push heroku main
   ```
4. **Set environment variables**:
   ```bash
   heroku config:set GOOGLE_API_KEY=your_key
   heroku config:set GOOGLE_SEARCH_ENGINE_ID=your_id
   heroku config:set GROQ_API_KEY=your_key
   ```

### Option 3: DigitalOcean App Platform

1. **Create account** at [digitalocean.com](https://digitalocean.com)
2. **Create App** from GitHub repository
3. **Configure**:
   - Source: GitHub repository
   - Build Command: `pip install -r requirements.txt`
   - Run Command: `cd backend && uvicorn enhanced_main:app --host 0.0.0.0 --port $PORT`

## 🔧 Environment Variables

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `GOOGLE_API_KEY` | Google Programmable Search Engine API key | `AIzaSyC...` |
| `GOOGLE_SEARCH_ENGINE_ID` | Google PSE Search Engine ID | `012345678901234567890:abcdefghijk` |
| `GROQ_API_KEY` | Groq API key (optional) | `gsk_...` |

### How to Get API Keys

1. **Google API Key**:
   - Go to [Google Cloud Console](https://console.cloud.google.com)
   - Enable Custom Search API
   - Create credentials

2. **Google Search Engine ID**:
   - Go to [Programmable Search Engine](https://programmablesearchengine.google.com/)
   - Create new search engine
   - Configure for LinkedIn profiles

3. **Groq API Key**:
   - Sign up at [Groq Console](https://console.groq.com)
   - Generate API key

## 🧪 Testing Deployment

### Frontend Testing

1. **Visit your Vercel URL**
2. **Test the interface**
3. **Check browser console** for errors

### Backend Testing

1. **Health Check**:
   ```bash
   curl https://your-backend-url.railway.app/health
   ```

2. **API Test**:
   ```bash
   curl -X POST https://your-backend-url.railway.app/search \
     -H "Content-Type: application/json" \
     -d '{"description": "Software Engineer", "profile_count": 5}'
   ```

## 🐛 Troubleshooting

### Common Issues

1. **CORS Errors**:
   - Check `vercel.json` proxy configuration
   - Verify backend URL is correct

2. **API Key Errors**:
   - Verify environment variables are set
   - Check API key permissions

3. **Build Failures**:
   - Check `requirements.txt` is up to date
   - Verify Python version compatibility

4. **Runtime Errors**:
   - Check Railway/Heroku logs
   - Verify start command is correct

### Debug Commands

```bash
# Check Railway logs
railway logs

# Check Heroku logs
heroku logs --tail

# Test local backend
cd backend && python enhanced_main.py

# Test local frontend
cd frontend && python -m http.server 3000
```

## 📊 Monitoring

### Vercel Analytics
- Built-in analytics in Vercel dashboard
- Performance monitoring
- Error tracking

### Railway Monitoring
- Logs in Railway dashboard
- Resource usage
- Performance metrics

## 🔄 Continuous Deployment

### GitHub Actions (Optional)

Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy
on:
  push:
    branches: [main]

jobs:
  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v20
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.ORG_ID }}
          vercel-project-id: ${{ secrets.PROJECT_ID }}
```

## 🎉 Success!

After deployment, you'll have:
- ✅ Frontend: `https://your-app.vercel.app`
- ✅ Backend: `https://your-app.railway.app`
- ✅ Full-stack LinkedIn Sourcing Agent in production!

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section
2. Review platform-specific documentation
3. Check logs for error messages
4. Verify environment variables are set correctly 