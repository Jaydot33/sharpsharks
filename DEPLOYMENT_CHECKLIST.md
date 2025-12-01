# 🦈 SharpSharks Deployment Checklist

## Pre-Deployment (Have These Ready)

- [ ] GitHub account
- [ ] Render account (render.com)
- [ ] Vercel account (vercel.com)
- [ ] Redis Cloud account (redis.com/cloud)
- [ ] API Keys:
  - [ ] TheOddsAPI: `b4442eb07c0cdc3007a1b5120144cfd3`
  - [ ] Twitter/X Bearer Token: `AAAAAAAAAAAAAAAAAKa%2F5gEAAAAA2O2ya%2BwsvFZ1J2bl%2BTOldXA0RWs%3DWhghPKidflvDm3raeL1LHvcEIgKolnmbce95dz5kCaWr0WUuOF`
  - [ ] Redis Password: `JaysProppulse2025`

---

## Backend Deployment (Render)

### GitHub Setup
- [ ] Create GitHub repo: `sharpsharks`
- [ ] Push all code to main branch
- [ ] Verify structure includes `backend/` folder

### Redis Cloud
- [ ] Sign up at https://redis.com/cloud
- [ ] Create database named `sharpsharks-cache`
- [ ] Set password to `JaysProppulse2025`
- [ ] Copy Redis URL (starts with `rediss://`)
- [ ] Save URL for Render step

### Render Deployment
- [ ] Go to https://render.com
- [ ] Sign in with GitHub
- [ ] Click "New Web Service"
- [ ] Select `sharpsharks` repo
- [ ] Set Build Command: `pip install -r backend/requirements.txt`
- [ ] Set Start Command: `cd backend && gunicorn main:app --workers 4`
- [ ] Add Environment Variables:
  - `ODDS_API_KEY=b4442eb07c0cdc3007a1b5120144cfd3`
  - `X_BEARER_TOKEN=AAAAAAAAAAAAAAAAAKa%2F5gEAAAAA2O2ya%2BwsvFZ1J2bl%2BTOldXA0RWs%3DWhghPKidflvDm3raeL1LHvcEIgKolnmbce95dz5kCaWr0WUuOF`
  - `REDIS_URL=rediss://default:JaysProppulse2025@your-redis-host:port`
  - `ENVIRONMENT=production`
- [ ] Click "Create Web Service"
- [ ] Wait 3-5 minutes for build
- [ ] Copy backend URL (e.g., `sharpsharks-api.onrender.com`)
- [ ] Test: Visit `/health` endpoint - should return `{"status": "healthy"}`

---

## Frontend Deployment (Vercel)

### Environment Setup
- [ ] Create `.env.production` file:
  ```
  VITE_BACKEND_URL=https://sharpsharks-api.onrender.com
  ```
- [ ] Verify `src/lib/client.ts` exports BACKEND_URL

### Vercel Deployment
- [ ] Go to https://vercel.com
- [ ] Click "New Project"
- [ ] Import `sharpsharks` repository
- [ ] Framework: Vite
- [ ] Build Command: `npm run build`
- [ ] Output Directory: `dist`
- [ ] Add Environment Variable:
  - Name: `VITE_BACKEND_URL`
  - Value: `https://sharpsharks-api.onrender.com`
- [ ] Click "Deploy"
- [ ] Wait 1-2 minutes
- [ ] Copy frontend URL (e.g., `sharpsharks-xxx.vercel.app`)
- [ ] Visit URL - verify Scanner shows NBA/NFL props

---

## Domain Configuration

### Option A: Buy from Vercel
- [ ] Vercel Dashboard → Settings → Domains
- [ ] Click "Add"
- [ ] Enter `sharpsharks.com`
- [ ] Click "Buy" ($12/year)
- [ ] Auto-configured

### Option B: Existing Domain
- [ ] Go to domain registrar (GoDaddy, Namecheap, etc.)
- [ ] Add DNS Records:
  - [ ] CNAME: `www` → `sharpsharks-xxx.vercel.app`
  - [ ] A: `@` → `76.76.19.163`
  - [ ] CNAME: `@` → `sharpsharks-xxx.vercel.app`
- [ ] Vercel Dashboard → Settings → Domains → Add Custom Domain
- [ ] Enter `sharpsharks.com`
- [ ] Wait 5-30 minutes for DNS propagation
- [ ] Visit `https://sharpsharks.com` - should load

---

## Post-Deployment Testing

### Backend Verification
- [ ] `/health` returns `{"status": "healthy"}`
- [ ] `/api/props/nba` returns today's NBA props
- [ ] `/api/props/nfl` returns today's NFL props
- [ ] `/api/props/ncaab` returns NCAAB team props
- [ ] `/api/props/cfb` returns CFB team props
- [ ] Redis connection successful (check Render logs)

### Frontend Verification
- [ ] Scanner loads without errors
- [ ] NBA tab shows player props
- [ ] NFL tab shows player props
- [ ] NCAAB tab shows team props
- [ ] CFB tab shows team props
- [ ] Edge % calculations displaying
- [ ] Sorting/filtering works
- [ ] Mobile responsive (test on phone/tablet)

### Feature Testing
- [ ] Beat Buzz loads Twitter sentiment
- [ ] Smart Picks shows ML recommendations
- [ ] Analytics dashboard renders charts
- [ ] All tabs accessible
- [ ] No console errors (F12)

---

## Monitoring & Maintenance

### Daily Checks
- [ ] Render logs for backend errors
- [ ] Vercel Analytics for frontend performance
- [ ] Redis connection status
- [ ] API call counts vs quota

### Weekly Checks
- [ ] Backend response times (<500ms)
- [ ] Frontend load times (<2s)
- [ ] Data accuracy (compare to sportsbooks)
- [ ] No security warnings

### Monthly Tasks
- [ ] Review API usage
- [ ] Check cost breakdown
- [ ] Update API keys if needed
- [ ] Analyze user engagement

---

## Emergency Troubleshooting

### Backend Won't Deploy
```
1. Check Render logs for Python errors
2. Verify requirements.txt has all packages
3. Verify env vars are set correctly
4. Restart deployment
```

### Frontend Shows Blank Page
```
1. Open browser console (F12)
2. Check Network tab for failed requests
3. Verify VITE_BACKEND_URL is correct
4. Clear browser cache and reload
```

### Props Not Loading
```
1. Test TheOddsAPI directly: 
   https://api.the-odds-api.com/v4/sports/basketball_nba/events?apiKey=b4442eb07c0cdc3007a1b5120144cfd3
2. Check Redis connection in Render logs
3. Verify ODDS_API_KEY is correct
4. Restart backend service
```

### CORS Errors
```
1. Verify BACKEND_URL in frontend
2. Check backend CORS configuration
3. Ensure headers are set correctly in FastAPI
```

---

## 🎯 Success Indicators

After complete deployment, you should have:

✅ Backend running at `sharpsharks-api.onrender.com`  
✅ Frontend deployed at `sharpsharks.com`  
✅ Today's NBA/NFL/NCAAB/CFB props loading in Scanner  
✅ Edge calculations showing in green for >5%  
✅ Beat Buzz showing Twitter sentiment  
✅ Smart Picks carousel working  
✅ Analytics dashboard rendering  
✅ All mobile responsive  
✅ <2s frontend load time  
✅ <500ms backend response time  

---

## 📞 Support

If issues arise during deployment:

1. **Check DEPLOYMENT_WALKTHROUGH.md** for detailed steps
2. **Review Render logs** for backend errors
3. **Check browser console** (F12) for frontend errors
4. **Verify all API keys** are correct
5. **Test endpoints** directly with curl or Postman

Your SharpSharks sports betting analytics platform is production-ready! 🦈🚀
