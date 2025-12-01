# 🦈 SharpSharks Deployment Walkthrough

## Part 1: Backend Deployment (Render) - 10 minutes

### Step 1: Prepare GitHub Repository

1. **Create a GitHub repo** (or use existing):
   ```bash
   git init
   git remote add origin https://github.com/yourusername/sharpsharks.git
   git add .
   git commit -m "Initial SharpSharks commit"
   git branch -M main
   git push -u origin main
   ```

2. **Verify structure** - Your repo should have:
   ```
   sharpsharks/
   ├── backend/
   │   ├── main.py
   │   ├── requirements.txt
   │   ├── services/
   │   ├── models/
   │   └── routes/
   ├── src/
   │   ├── App.tsx
   │   ├── components/
   │   └── ...
   ├── vite.config.ts
   └── package.json
   ```

### Step 2: Set Up Redis Cloud (2 minutes)

1. **Go to** https://redis.com/cloud
2. **Sign up** (free tier)
3. **Create database:**
   - Name: `sharpsharks-cache`
   - Region: Closest to you
   - Password: `JaysProppulse2025` (or create new)
4. **Copy connection string** (should look like):
   ```
   rediss://default:JaysProppulse2025@redis-xxxxx.c1.us-west-2-2.ec2.cloud.redislabs.com:16461
   ```
5. **Save this URL** - you'll need it in 30 seconds

### Step 3: Deploy Backend to Render (5 minutes)

1. **Go to** https://render.com
2. **Sign in** with GitHub
3. **Create New → Web Service**
4. **Connect repository:**
   - Select your `sharpsharks` repo
   - Click "Connect"
5. **Configure service:**
   - **Name:** `sharpsharks-api`
   - **Environment:** Python 3
   - **Build command:** `pip install -r backend/requirements.txt`
   - **Start command:** `cd backend && gunicorn main:app --workers 4`
   - **Plan:** Free (or $7/mo for always-on)

6. **Add Environment Variables** (click "Add Environment Variable"):
   ```
   ODDS_API_KEY = b4442eb07c0cdc3007a1b5120144cfd3
   X_BEARER_TOKEN = AAAAAAAAAAAAAAAAAKa%2F5gEAAAAA2O2ya%2BwsvFZ1J2bl%2BTOldXA0RWs%3DWhghPKidflvDm3raeL1LHvcEIgKolnmbce95dz5kCaWr0WUuOF
   REDIS_URL = rediss://default:JaysProppulse2025@redis-xxxxx.c1.us-west-2-2.ec2.cloud.redislabs.com:16461
   ENVIRONMENT = production
   ```

7. **Click "Create Web Service"** - Render starts building
8. **Wait 3-5 minutes** for deployment to complete
9. **Copy your backend URL** - will look like:
   ```
   https://sharpsharks-api.onrender.com
   ```
   ✅ **Save this URL** - needed for frontend

### Step 4: Verify Backend is Running (2 minutes)

1. **Visit:** `https://sharpsharks-api.onrender.com/health`
2. **Should see:**
   ```json
   {"status": "healthy", "redis": "connected"}
   ```
3. **Test props endpoint:** `https://sharpsharks-api.onrender.com/api/props/nba`
4. **Should return** array of today's NBA props with edges

✅ **Backend is LIVE!**

---

## Part 2: Frontend Deployment (Vercel) - 8 minutes

### Step 5: Update Frontend Environment

1. **Create `.env.production`** in project root:
   ```
   VITE_BACKEND_URL=https://sharpsharks-api.onrender.com
   ```

2. **Update `vite.config.ts`** (if not already set):
   ```typescript
   import { defineConfig } from 'vite'
   import react from '@vitejs/plugin-react'
   
   export default defineConfig({
     plugins: [react()],
     build: {
       outDir: 'dist',
     }
   })
   ```

3. **Verify `src/lib/client.ts`** has:
   ```typescript
   export const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:5000'
   ```

### Step 6: Deploy Frontend to Vercel (5 minutes)

1. **Go to** https://vercel.com
2. **Sign in** with GitHub
3. **Click "New Project"**
4. **Import repository:**
   - Select `sharpsharks` repo
   - Click "Import"

5. **Configure project:**
   - **Framework Preset:** Vite
   - **Root Directory:** `./` (default)
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`

6. **Add Environment Variable:**
   - Click "Environment Variables"
   - Name: `VITE_BACKEND_URL`
   - Value: `https://sharpsharks-api.onrender.com`
   - Click "Add"

7. **Click "Deploy"** - Vercel builds and deploys
8. **Wait 1-2 minutes** for deployment
9. **Get your frontend URL:**
   ```
   https://sharpsharks-xxx.vercel.app
   ```

### Step 7: Test Frontend Works (2 minutes)

1. **Visit** your Vercel URL
2. **Check Scanner tab** - should show today's NBA/NFL props
3. **Click different leagues** (NBA | NFL | NCAAB | CFB)
4. **Verify data loads:**
   - Player names
   - Lines and odds
   - Edge percentages (green if >5%)
   - No console errors (F12)

✅ **Frontend is LIVE!**

---

## Part 3: Custom Domain Setup - 5 minutes

### Step 8: Connect sharpsharks.com Domain

1. **You have two options:**

#### Option A: Buy from Vercel
```
Vercel Dashboard → Settings → Domains → Add
Domain: sharpsharks.com
Click "Buy" ($12/year)
Auto-configured DNS
```

#### Option B: Existing Domain (GoDaddy, Namecheap, etc.)
```
1. Go to your domain registrar
2. Find DNS settings
3. Add CNAME record:
   Name: www
   Value: sharpsharks-xxx.vercel.app
   
4. Add A record:
   Name: @
   Value: 76.76.19.163 (Vercel's IP)
   
5. Add CNAME record:
   Name: @
   Value: sharpsharks-xxx.vercel.app

6. Back in Vercel → Settings → Domains → Add Custom Domain
7. Enter sharpsharks.com
8. DNS verified automatically (takes 5-30 min)
```

### Step 9: Enable HTTPS (Automatic)

- Vercel auto-enables SSL certificate
- All traffic redirected to HTTPS
- No configuration needed
- Deployed in seconds

✅ **Domain is LIVE at sharpsharks.com!**

---

## Part 4: Monitor & Optimize

### Step 10: Monitor Backend Performance

**Render Dashboard:**
```
Dashboard → sharpsharks-api → Metrics
- CPU usage
- Memory usage
- Response times
- Request count
```

**Check logs:**
```
Click "Logs" tab
Look for errors or warnings
Should see healthy Redis connections
```

### Step 11: Monitor Frontend Performance

**Vercel Dashboard:**
```
Dashboard → sharpsharks → Analytics
- Page load times
- Core Web Vitals
- Traffic patterns
```

### Step 12: Test All Features

**Scanner:**
- [ ] NBA props loading
- [ ] NFL props loading
- [ ] NCAAB team props loading
- [ ] CFB team props loading
- [ ] Edge % sorting works
- [ ] Filter by team/player works

**Beat Buzz:**
- [ ] Twitter sentiment loading
- [ ] Reporter names showing
- [ ] Sentiment bars visible

**Smart Picks:**
- [ ] Carousel showing recommendations
- [ ] Confidence scores visible
- [ ] ML reasoning displayed

**Analytics:**
- [ ] Charts loading
- [ ] Filters working (date, player, league)
- [ ] Responsive on mobile

---

## Part 5: Troubleshooting

### Backend Not Starting?

**Check Render logs:**
```
Dashboard → sharpsharks-api → Logs
Look for Python errors
```

**Common issues:**
```
❌ "ModuleNotFoundError: No module named 'redis'"
✅ Fix: requirements.txt missing package

❌ "ConnectionError: Redis connection failed"
✅ Fix: REDIS_URL env var incorrect

❌ "401 Unauthorized"
✅ Fix: ODDS_API_KEY or X_BEARER_TOKEN wrong
```

### Frontend Not Connecting to Backend?

**Check browser console (F12):**
```
Network tab → look for API calls
Should show requests to sharpsharks-api.onrender.com
```

**Common issues:**
```
❌ "CORS error"
✅ Fix: Backend needs CORS headers (already included)

❌ "Failed to fetch"
✅ Fix: VITE_BACKEND_URL wrong in .env

❌ "404 Not Found"
✅ Fix: Backend endpoint path incorrect
```

### Data Not Loading?

**Check TheOddsAPI:**
```
curl "https://api.the-odds-api.com/v4/sports/basketball_nba/events?apiKey=b4442eb07c0cdc3007a1b5120144cfd3"
Should return today's games
```

**Check Redis:**
```
Verify connection string in Render env vars
Test: redis-cli (if installed locally)
```

---

## 🎯 Your SharpSharks URLs

After deployment:

| Service | URL |
|---------|-----|
| **Frontend** | https://sharpsharks.com |
| **Backend API** | https://sharpsharks-api.onrender.com |
| **Health Check** | https://sharpsharks-api.onrender.com/health |
| **NBA Props** | https://sharpsharks-api.onrender.com/api/props/nba |
| **NFL Props** | https://sharpsharks-api.onrender.com/api/props/nfl |
| **NCAAB Props** | https://sharpsharks-api.onrender.com/api/props/ncaab |
| **CFB Props** | https://sharpsharks-api.onrender.com/api/props/cfb |

---

## 📊 Performance Targets

After deployment:

- **Backend response time:** <500ms (cached)
- **Frontend load time:** <2s
- **Odds update frequency:** Every 5 minutes (Redis TTL)
- **Beat writer check:** Every 10 minutes
- **Uptime:** 99.9% on both Render & Vercel

---

## 🚀 You're Done!

Your sports betting analytics platform is **live and production-ready**. 

**Next steps:**
1. Share with beta users
2. Monitor performance metrics
3. Implement refinements (Parlay UI, WebSocket stream, etc.)
4. Add payment processing for Pro tier
5. Expand to MLB/NHL/WNBA/EPL/MLS/PGA

**Let's dominate the sports betting market! 🦈**
