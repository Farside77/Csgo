import unittest
import requests
import json
from datetime import datetime

class CS2EsportsTrackerAPITest(unittest.TestCase):
    def setUp(self):
        self.base_url = "http://localhost:8001/api"
        self.test_match_id = None
        self.test_bet_id = None

    def test_1_get_matches(self):
        """Test fetching matches"""
        print("\nTesting GET /matches")
        response = requests.get(f"{self.base_url}/matches")
        self.assertEqual(response.status_code, 200)
        matches = response.json()
        self.assertIsInstance(matches, list)
        
        if len(matches) > 0:
            match = matches[0]
            self.test_match_id = match["id"]
            print(f"Found {len(matches)} matches")
            print("Sample match data:")
            print(json.dumps(match, indent=2))
            
            # Verify match structure
            required_fields = ["id", "team1", "team2", "event", "date", "format"]
            for field in required_fields:
                self.assertIn(field, match)
                
            # Verify prediction data
            prediction_fields = ["predicted_winner", "win_probability", "predicted_score"]
            for field in prediction_fields:
                self.assertIn(field, match)

    def test_2_refresh_matches(self):
        """Test refreshing match data"""
        print("\nTesting POST /refresh-matches")
        response = requests.post(f"{self.base_url}/refresh-matches")
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertIn("matches_updated", result)
        print(f"Refreshed {result['matches_updated']} matches")

    def test_3_create_bet(self):
        """Test creating a bet"""
        print("\nTesting POST /bets")
        if not self.test_match_id:
            print("Skipping bet creation test - no match ID available")
            return
            
        bet_data = {
            "match_id": self.test_match_id,
            "team_bet_on": "Natus Vincere",  # Using a sample team name
            "odds": 1.5,
            "stake": 100
        }
        
        response = requests.post(
            f"{self.base_url}/bets",
            json=bet_data
        )
        self.assertEqual(response.status_code, 200)
        bet = response.json()
        self.test_bet_id = bet["id"]
        print("Created bet:")
        print(json.dumps(bet, indent=2))
        
        # Verify bet structure
        required_fields = ["id", "match_id", "team_bet_on", "odds", "stake", "potential_return", "status"]
        for field in required_fields:
            self.assertIn(field, bet)

    def test_4_get_bets(self):
        """Test fetching bets"""
        print("\nTesting GET /bets")
        response = requests.get(f"{self.base_url}/bets")
        self.assertEqual(response.status_code, 200)
        bets = response.json()
        self.assertIsInstance(bets, list)
        print(f"Found {len(bets)} bets")
        if len(bets) > 0:
            print("Sample bet data:")
            print(json.dumps(bets[0], indent=2))

    def test_5_update_bet(self):
        """Test updating a bet result"""
        print("\nTesting PUT /bets/{id}")
        if not self.test_bet_id:
            print("Skipping bet update test - no bet ID available")
            return
            
        update_data = {
            "result": "win",
            "status": "settled",
            "actual_return": 150
        }
        
        response = requests.put(
            f"{self.base_url}/bets/{self.test_bet_id}",
            json=update_data
        )
        self.assertEqual(response.status_code, 200)
        updated_bet = response.json()
        print("Updated bet:")
        print(json.dumps(updated_bet, indent=2))
        
        # Verify update was applied
        self.assertEqual(updated_bet["result"], "win")
        self.assertEqual(updated_bet["status"], "settled")
        self.assertEqual(updated_bet["actual_return"], 150)

if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=2)
