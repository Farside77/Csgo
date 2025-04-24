import requests
import pytest
import os
from datetime import datetime
import time

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
        # First refresh matches
        refresh_response = requests.post(f"{BACKEND_URL}/api/refresh-matches")
        assert refresh_response.status_code == 200
        
        # Wait a bit for matches to be processed
        time.sleep(2)
        
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
            print(f"Found {len(matches)} matches")
            return matches
        else:
            print("No matches found")
            return []

    def test_refresh_matches(self):
        """Test refreshing matches from HLTV"""
        response = requests.post(f"{BACKEND_URL}/api/refresh-matches")
        assert response.status_code == 200
        result = response.json()
        assert "status" in result
        assert "matches_updated" in result
        assert result["status"] == "success"
        print(f"Updated {result['matches_updated']} matches")

    def test_bet_workflow(self, matches=None):
        """Test the complete betting workflow"""
        if not matches:
            # Get matches if not provided
            matches_response = requests.get(f"{BACKEND_URL}/api/matches")
            assert matches_response.status_code == 200
            matches = matches_response.json()
        
        if not matches:
            print("No matches available for betting test")
            return
        
        match = matches[0]
        print(f"\nTesting bet on match: {match['team1']} vs {match['team2']}")
        
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
        print(f"Created bet on {bet['team_bet_on']} with stake ${bet['stake']}")
        
        # Get all bets
        get_bets_response = requests.get(f"{BACKEND_URL}/api/bets")
        assert get_bets_response.status_code == 200
        bets = get_bets_response.json()
        assert isinstance(bets, list)
        assert len(bets) > 0
        print(f"Found {len(bets)} total bets")
        
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
        print(f"Successfully settled bet as a win with return ${updated_bet['actual_return']}")

if __name__ == "__main__":
    # Run the tests
    test = TestCS2EsportsTracker()
    
    print("\nTesting CS2 Esports Tracker API...")
    
    try:
        print("\n1. Testing API root...")
        test.test_api_root()
        print("✅ API root test passed")
        
        print("\n2. Testing get matches...")
        matches = test.test_get_matches()
        print("✅ Get matches test passed")
        
        print("\n3. Testing refresh matches...")
        test.test_refresh_matches()
        print("✅ Refresh matches test passed")
        
        print("\n4. Testing bet workflow...")
        test.test_bet_workflow(matches)
        print("✅ Bet workflow test passed")
        
        print("\n✅ All backend tests passed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        raise