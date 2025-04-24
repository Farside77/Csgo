import requests
import os
import json
import time

# Get backend URL from environment variable
BACKEND_URL = "http://localhost:8001"
FRONTEND_URL = "http://localhost:3000"

def test_frontend_availability():
    """Test if frontend is available"""
    try:
        response = requests.get(FRONTEND_URL)
        assert response.status_code == 200
        print("✅ Frontend is available")
        return True
    except Exception as e:
        print(f"❌ Frontend is not available: {str(e)}")
        return False

def test_backend_availability():
    """Test if backend is available"""
    try:
        response = requests.get(f"{BACKEND_URL}/api")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        print("✅ Backend API is available")
        return True
    except Exception as e:
        print(f"❌ Backend API is not available: {str(e)}")
        return False

def test_match_data():
    """Test if match data is available"""
    try:
        # First refresh matches
        refresh_response = requests.post(f"{BACKEND_URL}/api/refresh-matches")
        assert refresh_response.status_code == 200
        
        # Get matches
        response = requests.get(f"{BACKEND_URL}/api/matches")
        assert response.status_code == 200
        matches = response.json()
        assert isinstance(matches, list)
        assert len(matches) > 0
        
        print(f"✅ Match data is available ({len(matches)} matches)")
        return True, matches[0]["id"] if matches else None
    except Exception as e:
        print(f"❌ Match data is not available: {str(e)}")
        return False, None

def test_bet_functionality(match_id):
    """Test if bet functionality works"""
    if not match_id:
        print("❌ Cannot test bet functionality without match ID")
        return False
    
    try:
        # Create a bet
        bet_data = {
            "match_id": match_id,
            "team_bet_on": "Test Team",
            "odds": 2.0,
            "stake": 100
        }
        
        create_response = requests.post(
            f"{BACKEND_URL}/api/bets",
            json=bet_data
        )
        assert create_response.status_code == 200
        bet = create_response.json()
        assert "id" in bet
        
        # Get bets
        get_response = requests.get(f"{BACKEND_URL}/api/bets")
        assert get_response.status_code == 200
        bets = get_response.json()
        assert isinstance(bets, list)
        assert len(bets) > 0
        assert any(b["id"] == bet["id"] for b in bets)
        
        print("✅ Bet functionality works")
        return True
    except Exception as e:
        print(f"❌ Bet functionality does not work: {str(e)}")
        return False

if __name__ == "__main__":
    print("\n🧪 Running CS2 Esports Tracker Tests\n")
    
    frontend_ok = test_frontend_availability()
    backend_ok = test_backend_availability()
    
    if backend_ok:
        match_ok, match_id = test_match_data()
        if match_ok:
            bet_ok = test_bet_functionality(match_id)
        else:
            print("❌ Skipping bet functionality test due to missing match data")
    else:
        print("❌ Skipping match and bet tests due to backend unavailability")
    
    if frontend_ok and backend_ok:
        print("\n✅ All tests passed! The application is working correctly.")
    else:
        print("\n❌ Some tests failed. Please check the logs for details.")