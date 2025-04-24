from fastapi import FastAPI, HTTPException, Query, Body
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import uvicorn
import os
import logging
from pathlib import Path
import httpx
import asyncio
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import uuid
from pydantic import BaseModel
from typing import List, Dict, Optional, Any

# /backend
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
client = AsyncIOMotorClient(mongo_url)
db = client.get_database(os.environ.get('DB_NAME', 'cs2_esports_tracker'))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Models
class Match(BaseModel):
    id: str
    team1: str
    team2: str
    event: str
    date: str
    format: str
    maps: Optional[List[str]] = None
    team1_odds: Optional[float] = None
    team2_odds: Optional[float] = None
    predicted_winner: Optional[str] = None
    win_probability: Optional[float] = None
    predicted_score: Optional[str] = None
    ev_value: Optional[float] = None
    status: str = "upcoming"  # upcoming, live, completed

class BetRecord(BaseModel):
    id: str
    match_id: str
    team_bet_on: str
    odds: float
    stake: float
    potential_return: float
    actual_return: Optional[float] = None
    result: Optional[str] = None  # win, loss, pending
    created_at: str
    status: str = "pending"  # pending, settled

# Helper Functions
async def fetch_hltv_matches():
    """
    Fetches upcoming matches from HLTV
    """
    try:
        # Use headers to mimic a browser request to avoid being blocked
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://www.google.com/',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
        }
        
        # If we can't fetch real data, generate sample data for demo purposes
        use_sample_data = True
        
        if not use_sample_data:
            async with httpx.AsyncClient() as client:
                logger.info("Attempting to fetch HLTV matches...")
                response = await client.get("https://www.hltv.org/matches", headers=headers, timeout=10.0)
                
                if response.status_code != 200:
                    logger.error(f"Failed to fetch HLTV matches: {response.status_code}")
                    return generate_sample_matches()
                
                logger.info("Successfully fetched HLTV matches")
                
                # Parse HTML with BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract upcoming matches
                matches = []
                match_elements = soup.select('.upcomingMatch')
                
                logger.info(f"Found {len(match_elements)} potential match elements")
                
                for match_element in match_elements:
                    try:
                        # Extract match details
                        match_id = match_element.get('href', '').split('/')[-1]
                        teams = match_element.select('.matchTeamName')
                        team1 = teams[0].text.strip() if len(teams) > 0 else "TBD"
                        team2 = teams[1].text.strip() if len(teams) > 1 else "TBD"
                        
                        # Extract event name
                        event_element = match_element.select_one('.matchEventName')
                        event = event_element.text.strip() if event_element else "Unknown Event"
                        
                        # Extract date
                        date_element = match_element.select_one('.matchTime')
                        date_str = date_element.get('data-unix') if date_element else None
                        
                        if date_str:
                            # Convert Unix timestamp to datetime
                            date = datetime.fromtimestamp(int(date_str) / 1000).isoformat()
                        else:
                            date = datetime.now().isoformat()
                        
                        # Extract format
                        format_element = match_element.select_one('.matchMeta')
                        match_format = format_element.text.strip() if format_element else "Unknown Format"
                        
                        # For real implementation, we would fetch odds from multiple bookmakers
                        # and store them for comparison
                        hltv_odds = await fetch_hltv_odds(match_id)
                        ggbet_odds = await fetch_ggbet_odds(team1, team2)
                        
                        # Use the best odds available
                        team1_odds = max(hltv_odds.get("team1", 0), ggbet_odds.get("team1", 0))
                        team2_odds = max(hltv_odds.get("team2", 0), ggbet_odds.get("team2", 0))
                        
                        # If we couldn't get real odds, generate some reasonable ones
                        if team1_odds == 0 or team2_odds == 0:
                            team1_odds = round(1.5 + (0.5 * (hash(team1) % 10) / 10), 2)
                            team2_odds = round(1.5 + (0.5 * (hash(team2) % 10) / 10), 2)
                        
                        # Create match object
                        match = {
                            "id": match_id or str(uuid.uuid4()),
                            "team1": team1,
                            "team2": team2,
                            "event": event,
                            "date": date,
                            "format": match_format,
                            "team1_odds": team1_odds,
                            "team2_odds": team2_odds,
                            "odds_sources": {
                                "hltv": hltv_odds,
                                "ggbet": ggbet_odds
                            },
                            "status": "upcoming"
                        }
                        
                        matches.append(match)
                    except Exception as e:
                        logger.error(f"Error processing match element: {e}")
                
                if not matches:
                    logger.warning("No matches found in HLTV response, using sample data")
                    return generate_sample_matches()
                    
                return matches
        else:
            logger.info("Using sample match data")
            return generate_sample_matches()
    except Exception as e:
        logger.error(f"Error fetching HLTV matches: {e}")
        logger.info("Falling back to sample data")
        return generate_sample_matches()


async def fetch_hltv_odds(match_id):
    """
    Fetch odds from HLTV for a specific match
    In a real implementation, this would scrape the odds from the match page
    """
    try:
        # This is a placeholder for actual scraping
        # In a real implementation, we would fetch the match page and extract the odds
        return {
            "team1": 0,
            "team2": 0
        }
    except Exception as e:
        logger.error(f"Error fetching HLTV odds: {e}")
        return {
            "team1": 0,
            "team2": 0
        }


async def fetch_ggbet_odds(team1, team2):
    """
    Fetch odds from GG.Bet for a specific match
    In a real implementation, this would use their API or scrape their site
    """
    try:
        # This is a placeholder for actual API calls or scraping
        # In a real implementation, we would:
        # 1. Search for the match on GG.Bet
        # 2. Extract the odds for each team
        
        # For now, we'll return some simulated odds
        # In real life, these would be the actual odds from GG.Bet
        return {
            "team1": round(1.6 + (0.6 * (hash(team1) % 10) / 10), 2),
            "team2": round(1.6 + (0.6 * (hash(team2) % 10) / 10), 2)
        }
    except Exception as e:
        logger.error(f"Error fetching GG.Bet odds: {e}")
        return {
            "team1": 0,
            "team2": 0
        }


def generate_sample_matches():
    """
    Generate sample matches for demo purposes when HLTV data can't be fetched
    """
    teams = [
        "Natus Vincere", "Astralis", "Vitality", "G2 Esports", "FaZe Clan",
        "Gambit", "Heroic", "Virtus.pro", "NIP", "Fnatic", "BIG", "Complexity",
        "OG", "Evil Geniuses", "Team Liquid", "ENCE", "FURIA", "mousesports",
        "Complexity", "Cloud9", "TYLOO", "Renegades", "Team Spirit"
    ]
    
    events = [
        "ESL Pro League S17", "BLAST Premier Spring", "IEM Katowice 2025",
        "PGL Major Stockholm", "DreamHack Masters", "BLAST Premier Fall",
        "ESL One Cologne", "IEM Winter", "BLAST Premier Global Final"
    ]
    
    formats = ["Bo1", "Bo3", "Bo5"]
    
    matches = []
    
    # Generate 15 sample matches
    for i in range(15):
        # Avoid duplicate teams in same match
        team_idx1 = (hash(str(i)) % len(teams))
        team_idx2 = (hash(str(i + 100)) % len(teams))
        while team_idx1 == team_idx2:
            team_idx2 = (team_idx2 + 1) % len(teams)
            
        team1 = teams[team_idx1]
        team2 = teams[team_idx2]
        
        event = events[i % len(events)]
        match_format = formats[i % len(formats)]
        
        # Generate random but realistic odds
        team1_odds = round(1.5 + (0.5 * (hash(team1) % 10) / 10), 2)
        team2_odds = round(1.5 + (0.5 * (hash(team2) % 10) / 10), 2)
        
        # Create future dates
        days_ahead = i % 7
        hours_ahead = (i * 3) % 24
        match_time = datetime.now() + timedelta(days=days_ahead, hours=hours_ahead)
        
        match = {
            "id": str(uuid.uuid4()),
            "team1": team1,
            "team2": team2,
            "event": event,
            "date": match_time.isoformat(),
            "format": match_format,
            "team1_odds": team1_odds,
            "team2_odds": team2_odds,
            "status": "upcoming"
        }
        
        matches.append(match)
    
    return matches

async def calculate_match_predictions(match):
    """
    A simple statistical model to predict match outcomes
    This is a placeholder for a more sophisticated model
    """
    # Get team historical data from database
    team1_stats = await db.team_stats.find_one({"team_name": match["team1"]})
    team2_stats = await db.team_stats.find_one({"team_name": match["team2"]})
    
    # If we don't have stats, use defaults
    if not team1_stats:
        team1_stats = {"win_rate": 0.5, "form": 0.5}
    if not team2_stats:
        team2_stats = {"win_rate": 0.5, "form": 0.5}
    
    # Simple win probability calculation
    team1_prob = (team1_stats.get("win_rate", 0.5) + team1_stats.get("form", 0.5)) / 2
    team2_prob = (team2_stats.get("win_rate", 0.5) + team2_stats.get("form", 0.5)) / 2
    
    # Normalize probabilities
    total = team1_prob + team2_prob
    team1_prob = team1_prob / total
    team2_prob = team2_prob / total
    
    # Determine predicted winner
    if team1_prob > team2_prob:
        predicted_winner = match["team1"]
        win_probability = team1_prob
    else:
        predicted_winner = match["team2"]
        win_probability = team2_prob
    
    # Calculate EV if odds are available
    ev_value = None
    if match.get("team1_odds") and match.get("team2_odds"):
        if predicted_winner == match["team1"]:
            implied_prob = 1 / match["team1_odds"]
            ev_value = (win_probability * match["team1_odds"]) - 1
        else:
            implied_prob = 1 / match["team2_odds"]
            ev_value = (win_probability * match["team2_odds"]) - 1
    
    # Predict score (placeholder logic)
    map_count = 1
    if "bo3" in match.get("format", "").lower():
        map_count = 3
    elif "bo5" in match.get("format", "").lower():
        map_count = 5
    
    if team1_prob > team2_prob:
        if map_count == 1:
            predicted_score = "1-0"
        elif map_count == 3:
            predicted_score = "2-1" if team1_prob < 0.7 else "2-0"
        else:  # bo5
            predicted_score = "3-2" if team1_prob < 0.7 else "3-1"
    else:
        if map_count == 1:
            predicted_score = "0-1"
        elif map_count == 3:
            predicted_score = "1-2" if team2_prob < 0.7 else "0-2"
        else:  # bo5
            predicted_score = "2-3" if team2_prob < 0.7 else "1-3"
    
    return {
        "predicted_winner": predicted_winner,
        "win_probability": round(win_probability, 2),
        "predicted_score": predicted_score,
        "ev_value": round(ev_value, 2) if ev_value is not None else None
    }

# API Routes
@app.get("/api")
async def root():
    return {"message": "CS2 Esports Tracker API"}

@app.get("/api/matches")
async def get_matches(status: str = "all"):
    """Get matches with optional filtering by status"""
    try:
        filter_query = {}
        if status != "all":
            filter_query["status"] = status
        
        # Get matches from DB
        cursor = db.matches.find(filter_query).sort("date", 1)
        matches = await cursor.to_list(length=100)
        
        # Convert ObjectId to string for JSON serialization
        for match in matches:
            match["_id"] = str(match["_id"])
        
        return matches
    except Exception as e:
        logger.error(f"Error getting matches: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/refresh-matches")
async def refresh_matches():
    """Manually trigger refresh of match data from HLTV"""
    try:
        matches = await fetch_hltv_matches()
        
        # Add predictions to matches
        for match in matches:
            predictions = await calculate_match_predictions(match)
            match.update(predictions)
            
            # Check if match already exists
            existing_match = await db.matches.find_one({"id": match["id"]})
            if existing_match:
                # Update existing match
                await db.matches.update_one(
                    {"id": match["id"]},
                    {"$set": match}
                )
            else:
                # Insert new match
                await db.matches.insert_one(match)
        
        return {"status": "success", "matches_updated": len(matches)}
    except Exception as e:
        logger.error(f"Error refreshing matches: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/bets")
async def create_bet(bet: dict = Body(...)):
    """Create a new bet record"""
    try:
        bet_id = str(uuid.uuid4())
        bet_record = {
            "id": bet_id,
            "match_id": bet["match_id"],
            "team_bet_on": bet["team_bet_on"],
            "odds": bet["odds"],
            "stake": bet["stake"],
            "potential_return": bet["odds"] * bet["stake"],
            "status": "pending",
            "created_at": datetime.now().isoformat()
        }
        
        result = await db.bets.insert_one(bet_record)
        bet_record["_id"] = str(result.inserted_id)
        
        return bet_record
    except Exception as e:
        logger.error(f"Error creating bet: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/bets")
async def get_bets(status: str = "all"):
    """Get bet records with optional filtering by status"""
    try:
        filter_query = {}
        if status != "all":
            filter_query["status"] = status
        
        cursor = db.bets.find(filter_query).sort("created_at", -1)
        bets = await cursor.to_list(length=100)
        
        # Convert ObjectId to string for JSON serialization
        for bet in bets:
            bet["_id"] = str(bet["_id"])
        
        return bets
    except Exception as e:
        logger.error(f"Error getting bets: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/bets/{bet_id}")
async def update_bet(bet_id: str, bet_update: dict = Body(...)):
    """Update an existing bet record"""
    try:
        result = await db.bets.update_one(
            {"id": bet_id},
            {"$set": bet_update}
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Bet not found")
        
        updated_bet = await db.bets.find_one({"id": bet_id})
        updated_bet["_id"] = str(updated_bet["_id"])
        
        return updated_bet
    except Exception as e:
        logger.error(f"Error updating bet: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Scheduled tasks
async def scheduled_match_refresh():
    """Refresh matches data periodically"""
    while True:
        try:
            await refresh_matches()
            logger.info("Scheduled match refresh completed")
        except Exception as e:
            logger.error(f"Error in scheduled match refresh: {e}")
        
        # Wait for 30 minutes before refreshing again
        await asyncio.sleep(30 * 60)

@app.on_event("startup")
async def startup_event():
    # Create database indexes
    await db.matches.create_index("id", unique=True)
    await db.bets.create_index("id", unique=True)
    
    # Start the scheduled match refresh task
    asyncio.create_task(scheduled_match_refresh())

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
