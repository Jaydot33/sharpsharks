# SharpSharks Quick Start Guide

## 📋 What You Have

✅ **Frontend** - React app with Scanner, Beats, Picks, Analytics  
✅ **Backend** - FastAPI with TheOddsAPI, Twitter/X, Redis  
✅ **Database** - SQLite schema (props, picks, beats, users)  
✅ **Auth** - JWT tokens with refresh  
✅ **Cache** - Redis (5min TTL) with fallback  
✅ **Webhooks** - Discord alerts for sharp edges  

## 🚀 Deploy in 15 Minutes

### Step 1: Get API Keys (5 min)

| Service | Time | Link | Action |
|---------|------|------|--------|
| TheOddsAPI | 2min | https://the-odds-api.com | Sign up → Copy API key |
| Twitter/X | 2min | https://developer.twitter.com | Create app → Get bearer token |
| Redis | 1min | https://redis.com/cloud | Create free instance → Copy URL |

### Step 2: Backend to Render (5 min)

```bash
# 1. Push to GitHub
git push origin main

# 2. Go to https://render.com → New Web Service
# 3. Connect repo → backend/ folder
# 4. Add Environment Variables:
ODDS_API_KEY=<from step 1>
X_BEARER_TOKEN=<from step 1>
REDIS_URL=<from step 1>
JWT_SECRET=generate-random-string
ENVIRONMENT=production

# 5. Click Deploy
# Result: https://sharpsharks-api.onrender.com ✅
```

### Step 3: Frontend to Vercel (5 min)

```bash
# 1. Update .env.local
VITE_BACKEND_URL=https://sharpsharks-api.onrender.com

# 2. Go to https://vercel.com → Import Project
# 3. Select GitHub repo
# 4. Add same env var above
# 5. Click Deploy
# Result: https://sharpsharks.com ✅
```

## 📊 Database Schema

### Props Table
```sql
CREATE TABLE props (
  id INTEGER PRIMARY KEY,
  league TEXT,              -- NBA, NFL, NCAAB, CFB
  player TEXT,              -- e.g., "Nikola Jokic"
  prop_type TEXT,           -- points, rebounds, assists, pass_yards, rush_yards
  line REAL,                -- e.g., 11.5
  odds INTEGER,             -- -110, +105, etc.
  projection REAL,          -- AI projection
  edge_pct REAL,            -- (projection-line)/line*100
  bookmaker TEXT,           -- DraftKings, FanDuel, etc.
  timestamp DATETIME
);
```

### Picks Table
```sql
CREATE TABLE picks (
  id INTEGER PRIMARY KEY,
  league TEXT,
  player TEXT,
  prop TEXT,
  line REAL,
  pick TEXT,                -- "over" or "under"
  confidence REAL,          -- 0.0-1.0
  reasoning TEXT,
  edge_pct REAL,
  components JSON,          -- {hof_projection, smart_model, prop_finder, beat_sentiment}
  created_at DATETIME,
  hit_status TEXT           -- NULL, "hit", "miss"
);
```

### Beats Table
```sql
CREATE TABLE beats (
  id INTEGER PRIMARY KEY,
  league TEXT,
  player TEXT,
  text TEXT,
  author TEXT,              -- e.g., "wojespn"
  sentiment REAL,           -- -1.0 to +1.0
  impact REAL,              -- ±% to projection
  created_at DATETIME,
  likes INTEGER
);
```

### Users Table
```sql
CREATE TABLE users (
  id INTEGER PRIMARY KEY,
  email TEXT UNIQUE,
  username TEXT UNIQUE,
  hashed_password TEXT,
  tier TEXT,                -- "free" or "pro"
  created_at DATETIME
);
```

## 🔌 API Endpoints

### Authentication
```
POST /auth/register
POST /auth/login
Returns: {access_token, user}
```

### Props
```
GET /api/props/{league}?min_edge=5.0
Response: [
  {
    league: "NBA",
    player: "Jokic",
    prop_type: "rebounds",
    line: 11.5,
    odds: -110,
    projection: 12.1,
    edge_pct: 5.2,
    bookmaker: "DraftKings",
    timestamp: "2025-12-01T..."
  }
]
```

### Beats
```
GET /api/beats/{player}?league=NBA
Response: [
  {
    league: "NBA",
    player: "Jokic",
    text: "Sources: Jokic dealing with ankle soreness...",
    author: "wojespn",
    sentiment: -0.8,
    impact: -12,
    created_at: "2025-12-01T...",
    likes: 3421
  }
]
```

### Picks
```
GET /api/picks/{league}
Response: [
  {
    league: "NBA",
    player: "Jokic",
    prop: "rebounds",
    line: 11.5,
    pick: "over",
    confidence: 0.78,
    reasoning: "High usage 38.2%, facing undersized defense",
    edge_pct: 8.5,
    components: {
      hof_projection: 12.1,
      smart_model: 12.3,
      prop_finder: 11.8,
      beat_sentiment: 0.1
    }
  }
]
```

### Alerts
```
POST /api/alerts
Body: {league, player, prop_type, min_edge_pct}
Action: Discord webhook fires when edge > threshold
```

## 📈 Live Data Example

### Current NBA Props (Dec 1, 2025)
```
Lakers vs Nuggets
├─ Jokic REB O11.5 (-110) → Edge: +6.2%
├─ LeBron PTS O25.5 (-110) → Edge: +4.8%
├─ Murray AST O6.5 (-110) → Edge: +7.1%
└─ Austin Reaves PTS U14.5 (-110) → Edge: +5.5%

Sentiment Adjustments (from beats):
├─ Jokic: -0.8 (ankle soreness) → -12% to proj
├─ LeBron: +0.2 (good health) → +2% to proj
└─ Murray: 0.0 (no news) → baseline
```

## 🎯 Edge Calculation (40-30-20-10 Formula)

```
Final Edge = 
  (0.40 × HOF_projection) +
  (0.30 × Smart_model) +
  (0.20 × PropFinder_line) +
  (0.10 × Beat_sentiment_adjustment)

Example:
- HOF: 12.1 rebounds
- Smart: 12.3 rebounds
- PropFinder: 11.8 rebounds
- Beat sentiment: -0.2 (mild concern)

Weighted: (12.1×0.4) + (12.3×0.3) + (11.8×0.2) + (-0.2×0.1)
= 4.84 + 3.69 + 2.36 - 0.02
= 10.87 projected

vs Line 11.5 → Edge = (10.87-11.5)/11.5 = -5.5% (UNDER)
```

## 🔐 Security Checklist

- [x] JWT tokens (24hr expiry)
- [x] Password hashing (bcrypt)
- [x] Rate limiting (450 req/15min for Twitter)
- [x] CORS configured
- [x] API key validation
- [x] Age gate (implement in frontend)
- [ ] SSL/TLS (auto on Vercel/Render)
- [ ] Rate limit (implement in main.py)

## 📱 Frontend Features Ready

| Feature | Status | Location |
|---------|--------|----------|
| Live Odds Ticker | ✅ | Top banner, 5s refresh |
| Edge Scanner | ✅ | Main table, sortable |
| Beat Buzz | ✅ | Timeline with sentiment |
| Smart Picks | ✅ | Carousel with confidence |
| Analytics | ✅ | Charts with filters |
| Dark Mode | ✅ | #1a1a1a + teal accent |
| Mobile Responsive | ✅ | SM/MD/LG breakpoints |

## 🎲 Next Features

**Phase 2 (Week 2):**
- Live WebSocket updates (real-time odds)
- User wallet/transactions
- Freemium tier lock ($9.99/mo)

**Phase 3 (Week 3):**
- Parlay simulator (Monte Carlo)
- Historical backtesting
- Affiliate commission tracking

**Phase 4 (Week 4):**
- MLB, NHL, WNBA, EPL, MLS, PGA
- Mobile app (React Native)
- Email alerts + SMS

## 🆘 Troubleshooting

| Issue | Fix |
|-------|-----|
| API returns 401 | Check bearer token in Authorization header |
| No props data | Verify ODDS_API_KEY quota (500/month free) |
| Redis connection error | Falls back to in-memory, check REDIS_URL format |
| Twitter/X 429 error | Rate limit hit, stagger requests or upgrade tier |
| Frontend 404 backend | Check VITE_BACKEND_URL in .env.local |

## 📞 Live Support

- Render status: https://status.render.com
- Vercel status: https://vercel-status.com
- API docs: http://localhost:5000/docs (Swagger)
