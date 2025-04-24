import requests
import pytest
from datetime import datetime, timedelta
import uuid

BACKEND_URL = "https://backend-cs2-esports-tracker.zanity.net/api"

class TestCS2EsportsTracker:
    def __init__(self):
        self.base_url = BACKEND_URL
        
    def test_api_root(self):
        """Test the API root endpoint"""
        response = requests.get(f"{self.base_url}")
        assert response.status_code == 200
        assert "message" in response.json()
        print("✅ API root endpoint test passed")

    def test_get_matches(self):
        """Test fetching matches"""
        response = requests.get(f"{self.base_url}/matches")
        assert response.status_code == 200
        matches = response.json()
        assert isinstance(matches, list)
        
        if len(matches) > 0:
            match = matches[0]
            required_fields = ['id', 'team1', 'team2', 'event', 'date', 'format', 
                             'team1_odds', 'team2_odds', 'predicted_winner', 
                             'win_probability', 'predicted_score']
            for field in required_fields:
                assert field in match
        print("✅ Get matches test passed")

    def test_refresh_matches(self):
        """Test match refresh endpoint"""
        response = requests.post(f"{self.base_url}/refresh-matches")
        assert response.status_code == 200
        data = response.json()
        assert "matches_updated" in data
        print("✅ Refresh matches test passed")

    def test_bet_workflow(self):
        """Test complete bet workflow"""
        # 1. Get matches to place a bet
        matches_response = requests.get(f"{self.base_url}/matches")
        assert matches_response.status_code == 200
        matches = matches_response.json()
        assert len(matches) > 0
        
        match = matches[0]
        
        # 2. Create a bet
        bet_data = {
            "match_id": match["id"],
            "team_bet_on": match["team1"],
            "odds": match["team1_odds"],
            "stake": 100
        }
        
        create_bet_response = requests.post(
            f"{self.base_url}/bets",
            json=bet_data
        )
        assert create_bet_response.status_code == 200
        bet = create_bet_response.json()
        assert "id" in bet
        bet_id = bet["id"]
        
        # 3. Get all bets
        get_bets_response = requests.get(f"{self.base_url}/bets")
        assert get_bets_response.status_code == 200
        bets = get_bets_response.json()
        assert len(bets) > 0
        
        # 4. Update bet result
        update_data = {
            "result": "win",
            "status": "settled",
            "actual_return": bet["potential_return"]
        }
        update_response = requests.put(
            f"{self.base_url}/bets/{bet_id}",
            json=update_data
        )
        assert update_response.status_code == 200
        updated_bet = update_response.json()
        assert updated_bet["status"] == "settled"
        assert updated_bet["result"] == "win"
        
        print("✅ Complete bet workflow test passed")

    def test_odds_sources(self):
        """Test odds from multiple sources"""
        response = requests.get(f"{self.base_url}/matches")
        assert response.status_code == 200
        matches = response.json()
        
        if len(matches) > 0:
            match = matches[0]
            # Check if odds sources are present
            assert "odds_sources" in match
            assert "hltv" in match["odds_sources"]
            assert "ggbet" in match["odds_sources"]
            print("✅ Odds sources test passed")
        else:
            print("⚠️ No matches found to test odds sources")

    def test_prediction_model(self):
        """Test enhanced prediction model"""
        response = requests.get(f"{self.base_url}/matches")
        assert response.status_code == 200
        matches = response.json()
        
        if len(matches) > 0:
            match = matches[0]
            # Verify prediction fields
            assert "predicted_winner" in match
            assert "win_probability" in match
            assert "predicted_score" in match
            assert "ev_value" in match
            
            # Validate probability range
            assert 0 <= match["win_probability"] <= 1
            print("✅ Prediction model test passed")
        else:
            print("⚠️ No matches found to test prediction model")

if __name__ == "__main__":
    # Create test instance
    tester = TestCS2EsportsTracker()
    
    # Run all tests
    print("\n🔍 Running CS2 Esports Tracker API Tests...")
    
    try:
        tester.test_api_root()
        tester.test_get_matches()
        tester.test_refresh_matches()
        tester.test_bet_workflow()
        tester.test_odds_sources()
        tester.test_prediction_model()
        print("\n✅ All tests completed successfully!")
    except Exception as e:
        print(f"\n❌ Tests failed: {str(e)}")
