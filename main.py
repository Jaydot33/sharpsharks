from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="SharpSharks API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ODDS_API_KEY = os.getenv("ODDS_API_KEY", "b4442eb07c0cdc3007a1b5120144cfd3")
X_BEARER_TOKEN = os.getenv("X_BEARER_TOKEN", "AAAAAAAAAAAAAAAAAKa/5gEAAAAA2O2ya+wsvFZ1J2bl+TOldXA0RWs=WhghPKidflvDm3raeL1LHvcEIgKolnmbce95dz5kCaWr0WUuOF")

@app.get("/")
async def root():
    return {
        "service": "SharpSharks API",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "health": "/health",
            "props": "/api/props/{league}",
            "beat_buzz": "/api/beat-buzz/{league}",
            "smart_picks": "/api/smart-picks"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "SharpSharks API"}

@app.get("/api/props/{league}")
async def get_props(league: str):
    league_map = {
        "nba": "basketball_nba",
        "nfl": "americanfootball_nfl",
        "ncaab": "basketball_ncaab",
        "cfb": "americanfootball_ncaaf"
    }
    
    if league not in league_map:
        raise HTTPException(status_code=400, detail=f"Invalid league. Use: {', '.join(league_map.keys())}")
    
    odds_league = league_map[league]
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://api.the-odds-api.com/v4/sports/{odds_league}/events",
                params={
                    "apiKey": ODDS_API_KEY,
                    "limit": 50
                }
            )
            response.raise_for_status()
            return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/beat-buzz/{league}")
async def get_beat_buzz(league: str):
    try:
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {X_BEARER_TOKEN}"}
            response = await client.get(
                "https://api.twitter.com/2/tweets/search/recent",
                params={
                    "query": f"#{league} props beat writer",
                    "max_results": 10,
                    "tweet.fields": "created_at,public_metrics"
                },
                headers=headers
            )
            response.raise_for_status()
            return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/smart-picks")
async def get_smart_picks():
    return {
        "picks": [
            {
                "id": 1,
                "player": "LeBron James",
                "prop": "Points Over 25.5",
                "league": "NBA",
                "confidence": 0.87,
                "odds": -110,
                "analysis": "Strong home game matchup, recent form 28.3 PPG"
            },
            {
                "id": 2,
                "player": "Patrick Mahomes",
                "prop": "Passing Yards Over 285.5",
                "league": "NFL",
                "confidence": 0.82,
                "odds": -110,
                "analysis": "Favorable weather conditions, opponent weak pass defense"
            }
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)

