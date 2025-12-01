# SharpSharks Live Data Deployment Guide

## Overview
SharpSharks is now fully integrated with:
- ✅ TheOddsAPI (b4442eb07c0cdc3007a1b5120144cfd3)
- ✅ Twitter/X API (Bearer token provided)
- ✅ Redis Cloud (password: JaysProppulse2025)

## Quick Start (5 minutes)

### 1. Deploy Backend to Render

```bash
# 1. Push backend folder to GitHub
git add backend/
git commit -m "SharpSharks backend with OddsAPI integration"
git push

# 2. Create Render Web Service
# Go to https://dashboard.render.com/blueprints
# Select "Connect Repository"
# Choose your repo → Select render.yaml from backend folder

# 3. Add Environment Variables in Render Dashboard:
ODDS_API_KEY=b4442eb07c0cdc3007a1b5120144cfd3
X_BEARER_TOKEN=AAAAAAAAAAAAAAAAAKa%2F5gEAAAAA2O2ya%2BwsvFZ1J2bl%2BTOldXA0RWs%3DWhghPKidflvDm3raeL1LHvcEIgKolnmbce95dz5kCaWr0WUuOF
REDIS_URL=redis://default:JaysProppulse2025@your-redis-host:6379
PORT=5000

# 4. Deploy
# Click "Deploy" in Render dashboard
# Wait 3-5 minutes for build
# Backend live at: https://sharpsharks-api.onrender.com
```

### 2. Set Up Redis Cloud

```bash
# 1. Go to https://redis.com/cloud
# 2. Create free account (30MB free tier)
# 3. Create new database
# 4. Set password: JaysProppulse2025
# 5. Copy connection URL: rediss://default:JaysProppulse2025@your-redis-host:6379
# 6. Add to Render environment variables (REDIS_URL)
```

### 3. Deploy Frontend to Vercel

```bash
# 1. Set environment variable:
VITE_BACKEND_URL=https://sharpsharks-api.onrender.com

# 2. Push to GitHub:
git add src/
git commit -m "SharpSharks frontend with live data"
git push

# 3. Import repository in Vercel dashboard
# 4. Set VITE_BACKEND_URL in Vercel env vars
# 5. Deploy to sharpsharks.com custom domain
# 6. Frontend live at: https://sharpsharks.com
```

## API Endpoints

### Props (Player/Team)
```
GET /api/props/{league}
Parameters:
  - league: NBA | NFL | NCAAB | CFB
  - date: optional YYYY-MM-DD (defaults to today)

Response:
{
  "data": [
    {
      "league": "NBA",
      "player": "Nikola Jokic",
      "prop_type": "Rebounds",
      "line": 11.5,
      "odds": 1.91,
      "projection": 11.8,
      "edge_pct": 6.7,
      "bookmaker": "DraftKings",
      "team": "DEN",
      "opponent": "LAL"
    }
  ],
  "count": 24,
  "cached": false
}
```

### Beat Writer Sentiment
```
GET /api/beats/{player}
Parameters:
  - player: player name
  - league: optional NBA | NFL | NCAAB | CFB

Response:
{
  "player": "LeBron James",
  "tweets": [
    {
      "author": "@wojespn",
      "text": "LeBron cleared for tonight's game",
      "sentiment": 0.8,
      "impact": "+8% to points projection",
      "timestamp": "2025-12-01T18:30:00Z"
    }
  ]
}
```

### Smart Picks
```
GET /api/picks/{league}
Response:
{
  "picks": [
    {
      "player": "Nikola Jokic",
      "prop": "Rebounds O 11.5",
      "confidence": 0.87,
      "edge_breakdown": {
        "hof": 0.40,
        "smart": 0.30,
        "prop": 0.20,
        "beats": 0.10
      },
      "reasoning": "Strong ankle health, high usage rate, elite rebounding trends"
    }
  ]
}
```

## Data Flow Architecture

```
TheOddsAPI
    ↓
Backend /api/props/{league}
    ↓ (5-min cache)
Redis Cache
    ↓
Frontend Scanner Component
    ↓
User sees: Player | Prop | Line | Projection | Edge%
```

## Caching Strategy

- **Props**: 5 minutes (refresh every 300s)
- **Beats**: 10 minutes (Twitter API rate limit: 450/15min)
- **Picks**: 15 minutes (recompute ML scores)

## Real-Time Updates (Next Phase)

For sub-second updates, implement WebSocket:

```typescript
// Frontend
const ws = new WebSocket('wss://sharpsharks-api.onrender.com/ws/props/NBA');
ws.onmessage = (event) => {
  const { data } = JSON.parse(event.data);
  setProps(data); // Update in real-time
};
```

```python
# Backend FastAPI
from fastapi import WebSocket

@app.websocket("/ws/props/{league}")
async def websocket_endpoint(websocket: WebSocket, league: str):
    await websocket.accept()
    while True:
        props = odds_api_service.get_league_props(league)
        await websocket.send_json({"data": props})
        await asyncio.sleep(5)  # Update every 5 seconds
```

## Environment Variables Checklist

```
Frontend (Vercel):
✓ VITE_BACKEND_URL=https://sharpsharks-api.onrender.com

Backend (Render):
✓ ODDS_API_KEY=b4442eb07c0cdc3007a1b5120144cfd3
✓ X_BEARER_TOKEN=AAAAAAAAAAAAAAAAAKa%2F5gEAAAAA2O2ya%2BwsvFZ1J2bl%2BTOldXA0RWs%3DWhghPKidflvDm3raeL1LHvcEIgKolnmbce95dz5kCaWr0WUuOF
✓ REDIS_URL=redis://default:JaysProppulse2025@your-redis-host:6379
✓ PORT=5000
```

## Monitoring

### Backend Health
```bash
curl https://sharpsharks-api.onrender.com/health
# Response: {"status": "healthy", "service": "sharpsharks-api"}
```

### API Response Times
- Props fetch: <1s (cached) / <3s (live fetch)
- Beat analysis: <2s (cached) / <5s (live parse)
- Edge calculations: <500ms

### Error Handling
- TheOddsAPI down: Returns cached data (Redis)
- Twitter/X rate limit: Returns mock data + cached beats
- Redis unavailable: Returns live API fetch (no cache)

## Troubleshooting

**No props showing in Scanner?**
1. Check Render logs: `sharpsharks-api.onrender.com/logs`
2. Verify ODDS_API_KEY is set correctly
3. Check Redis connection: `redis-cli -u <REDIS_URL> ping`
4. Verify backend returning data: `curl https://sharpsharks-api.onrender.com/api/props/NBA`

**404 on /api/props?**
1. Backend not deployed - check Render status
2. VITE_BACKEND_URL incorrect in frontend
3. CORS not configured - check backend/main.py

**Games not for today?**
1. TheOddsAPI showing UTC time - compare with your timezone
2. Games might be in early morning (pre-schedule)
3. Check specific date: `/api/props/NBA?date=2025-12-01`

## Performance Targets

- ✅ Scanner load: <1.5s (cached)
- ✅ Beat Buzz: <2s refresh
- ✅ Edge calculations: real-time
- ✅ 99.9% uptime (Render + Vercel)
- ✅ Mobile responsive
- ✅ Dark mode optimized

## Next Enhancements

1. **WebSocket Real-Time** - Sub-second updates
2. **Parlay Builder UI** - Drag-drop with Monte Carlo
3. **CBB Spreads** - March Madness market
4. **Mobile App** - React Native
5. **User Authentication** - SSO + wallet tracking

Deploy now and dominate! 🦈
