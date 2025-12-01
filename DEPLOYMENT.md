# SharpSharks Deployment Guide

## 🚀 Architecture Overview

```
Frontend (React/Vite)          Backend (FastAPI)           Data Sources
├─ Vercel (sharpsharks.com)   ├─ Render (API)             ├─ TheOddsAPI
├─ Dark theme UI              ├─ Redis Cloud              ├─ Twitter/X API
├─ Mobile-first               ├─ SQLite DB                ├─ HOF Projections
└─ Real-time charts           └─ JWT Auth                 └─ SmartPicks ML
```

## Step 1: Environment Setup

### 1.1 Backend (.env)
Create `backend/.env`:
```env
ODDS_API_KEY=your-key-from-the-odds-api.com
X_BEARER_TOKEN=your-token-from-developer.twitter.com
REDIS_URL=rediss://default:password@host:port
JWT_SECRET=your-super-secret-key-change-this
DISCORD_WEBHOOK=https://discord.com/api/webhooks/...
PORT=5000
ENVIRONMENT=production
```

### 1.2 Frontend (.env.local)
Create `.env.local`:
```env
VITE_BACKEND_URL=https://sharpsharks-api.onrender.com
```

## Step 2: API Keys (5-10 min)

### TheOddsAPI (Props & Odds)
1. Visit https://the-odds-api.com
2. Sign up free (500 calls/month)
3. Copy API key → backend/.env `ODDS_API_KEY`

### Twitter/X API (Beat Writers)
1. Visit https://developer.twitter.com
2. Create App → Get Bearer Token
3. Copy → backend/.env `X_BEARER_TOKEN`

### Redis Cloud (Caching)
1. Visit https://redis.com/cloud
2. Create free instance
3. Copy connection string → backend/.env `REDIS_URL`
4. Format: `rediss://default:password@host:port`

### Discord Webhook (Alerts - Optional)
1. Create Discord server/channel
2. Right-click channel → Webhooks
3. Copy webhook URL → backend/.env `DISCORD_WEBHOOK`

## Step 3: Deploy Backend (Render)

### 3.1 Prepare Repository
```bash
git init
git add .
git commit -m "Initial SharpSharks backend"
git push origin main
```

### 3.2 Connect to Render
1. Visit https://render.com
2. New → Web Service
3. Connect GitHub repo
4. Configure:
   - **Name**: sharpsharks-api
   - **Root Directory**: backend/
   - **Build**: `pip install -r requirements.txt`
   - **Start**: `python main.py`
   - **Plan**: Starter (free tier)

### 3.3 Add Environment Variables in Render
Dashboard → Environment:
```
ODDS_API_KEY=your-key
X_BEARER_TOKEN=your-token
REDIS_URL=your-redis-url
JWT_SECRET=your-secret
DISCORD_WEBHOOK=your-webhook
ENVIRONMENT=production
```

### 3.4 Add Redis Database
1. Render → Create Resource → Redis
2. Select same region as API
3. Copy connection string
4. Add to Environment as `REDIS_URL`

**Result**: `https://sharpsharks-api.onrender.com` ✅

## Step 4: Deploy Frontend (Vercel)

### 4.1 Update Backend URL
Frontend `.env.local`:
```env
VITE_BACKEND_URL=https://sharpsharks-api.onrender.com
```

### 4.2 Connect to Vercel
1. Visit https://vercel.com
2. Import → GitHub repo
3. Configure:
   - **Project**: SharpSharks
   - **Framework**: Vite
   - **Build**: `npm run build`
   - **Output**: `dist`

### 4.3 Add Environment Variables
Settings → Environment Variables:
```
VITE_BACKEND_URL=https://sharpsharks-api.onrender.com
```

### 4.4 Custom Domain
1. Vercel → Domains
2. Add `sharpsharks.com`
3. Update DNS records per Vercel instructions

**Result**: `https://sharpsharks.com` ✅

## Step 5: Test Live API

### 5.1 Health Check
```bash
curl https://sharpsharks-api.onrender.com/health
```

### 5.2 Register User
```bash
curl -X POST https://sharpsharks-api.onrender.com/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@sharpsharks.com",
    "username": "sharpbettor",
    "password": "SecurePass123!"
  }'
```

### 5.3 Get Props
```bash
curl https://sharpsharks-api.onrender.com/api/props/NBA \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Step 6: Data Pipeline Setup

### 6.1 Enable Cron Jobs (Props Update)
Render → Cron Job:
```
Schedule: Every 1 minute
Endpoint: /api/props/refresh
Auth: Bearer token
```

### 6.2 Beat Writer Tracking
X API search every 5 minutes:
```
Query: (LeBron OR injury OR usage) from:@wojespn since:2025-12-01
Sentiment: NLP analysis → DB
Impact: ±5-15% to projections
```

### 6.3 Edge Alerts
User subscribes to: `league, player, min_edge_pct`
Trigger: When edge > threshold
Action: Discord webhook + Email

## Step 7: Production Checklist

- [ ] All API keys configured in Render
- [ ] Redis connection verified
- [ ] Backend health check passing
- [ ] Frontend builds successfully
- [ ] Auth login/register working
- [ ] Props API returning data
- [ ] Beats/Sentiment parsing working
- [ ] Discord webhooks sending
- [ ] HTTPS/SSL enabled
- [ ] Rate limiting active
- [ ] JWT token expiration set
- [ ] Database backups enabled

## Monitoring & Uptime

### Render Dashboard
- Monitor API response times
- View error logs
- Check Redis memory usage
- Auto-restart on failure

### Vercel Analytics
- Frontend performance metrics
- Core Web Vitals tracking
- Deployment history

### Alerts
Enable Render alerts for:
- API down > 1 min
- Error rate > 5%
- Memory > 80%
- Crashes/restarts

## Scaling (Post-MVP)

### Phase 2 (MLB/NHL/WNBA)
- Add sports to `/api/props/{league}`
- Expand beat writer list
- More ML models

### Phase 3 (Real-time WebSocket)
- Live odds streaming
- Push alerts to mobile app
- WebSocket props feed

### Phase 4 (Wallet & Payments)
- Stripe integration
- User transactions table
- Freemium tier ($9.99/mo)

## Troubleshooting

**API 401 Unauthorized**
- Check JWT token hasn't expired
- Verify Bearer token format
- Re-login to get fresh token

**Redis Connection Failed**
- Verify REDIS_URL format
- Check connection string in Render env
- Test Redis locally: `redis-cli`

**Props empty/stale**
- Check ODDS_API_KEY quota (500/month free)
- Verify cache TTL (5 min default)
- Check logs for API errors

**Twitter/X API rate limit**
- 450 requests/15min window
- Stagger requests with cache
- Upgrade API tier for higher limits

## Support & Resources

- Backend docs: `backend/README.md`
- API schema: http://localhost:5000/docs (Swagger)
- Render docs: https://render.com/docs
- Vercel docs: https://vercel.com/docs
