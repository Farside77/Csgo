import requests
import pytest
import os
from datetime import datetime

# Get backend URL from environment variable
BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL', 'http://localhost:8001')

class TestCS2EsportsTracker:
    def test_api_root(self):
        """Test the API root endpoint"""
        response = requests.get(f"{BACKEND_URL}/api")
        assert response.status_code == 200
        assert response.json() == {"message": "CS2 Esports Tracker API"}

    def test_get_matches(self):
        """Test getting matches"""
        response = requests.get(f"{BACKEND_URL}/api/matches")
        assert response.status_code == 200
        matches = response.json()
        assert isinstance(matches, list)
        
        # If matches exist, verify their structure
        if matches:
            match = matches[0]
            required_fields = ['id', 'team1', 'team2', 'event', 'date', 'format', 'status']
            for field in required_fields:
                assert field in match

    def test_refresh_matches(self):
        """Test refreshing matches from HLTV"""
        response = requests.post(f"{BACKEND_URL}/api/refresh-matches")
        assert response.status_code == 200
        result = response.json()
        assert "status" in result
        assert "matches_updated" in result
        assert result["status"] == "success"

    def test_bet_workflow(self):
        """Test the complete betting workflow"""
        # First get matches to find one to bet on
        matches_response = requests.get(f"{BACKEND_URL}/api/matches")
        assert matches_response.status_code == 200
        matches = matches_response.json()
        
        if not matches:
            pytest.skip("No matches available for betting test")
        
        match = matches[0]
        
        # Create a bet
        bet_data = {
            "match_id": match["id"],
            "team_bet_on": match["team1"],
            "odds": 2.0,
            "stake": 100
        }
        
        create_bet_response = requests.post(
            f"{BACKEND_URL}/api/bets",
            json=bet_data
        )
        assert create_bet_response.status_code == 200
        bet = create_bet_response.json()
        assert bet["id"] is not None
        assert bet["potential_return"] == bet_data["odds"] * bet_data["stake"]
        
        # Get all bets
        get_bets_response = requests.get(f"{BACKEND_URL}/api/bets")
        assert get_bets_response.status_code == 200
        bets = get_bets_response.json()
        assert isinstance(bets, list)
        assert len(bets) > 0
        
        # Update bet result
        bet_update = {
            "result": "win",
            "status": "settled",
            "actual_return": bet["potential_return"]
        }
        update_response = requests.put(
            f"{BACKEND_URL}/api/bets/{bet['id']}",
            json=bet_update
        )
        assert update_response.status_code == 200
        updated_bet = update_response.json()
        assert updated_bet["status"] == "settled"
        assert updated_bet["result"] == "win"
        assert updated_bet["actual_return"] == bet["potential_return"]

if __name__ == "__main__":
    # Run the tests
    test = TestCS2EsportsTracker()
    
    print("\nTesting CS2 Esports Tracker API...")
    
    try:
        print("\n1. Testing API root...")
        test.test_api_root()
        print("✅ API root test passed")
        
        print("\n2. Testing get matches...")
        test.test_get_matches()
        print("✅ Get matches test passed")
        
        print("\n3. Testing refresh matches...")
        test.test_refresh_matches()
        print("✅ Refresh matches test passed")
        
        print("\n4. Testing bet workflow...")
        test.test_bet_workflow()
        print("✅ Bet workflow test passed")
        
        print("\n✅ All backend tests passed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        raise