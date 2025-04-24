import requests
import unittest
from datetime import datetime
import uuid

class CS2EsportsTrackerAPITest(unittest.TestCase):
    def setUp(self):
        self.base_url = "http://localhost:8001/api"
        self.test_match_id = str(uuid.uuid4())
        self.test_bet_id = str(uuid.uuid4())

    def test_01_api_root(self):
        """Test API root endpoint"""
        response = requests.get(f"{self.base_url}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "CS2 Esports Tracker API"})

    def test_02_get_matches(self):
        """Test getting matches"""
        response = requests.get(f"{self.base_url}/matches")
        self.assertEqual(response.status_code, 200)
        matches = response.json()
        self.assertIsInstance(matches, list)
        if matches:
            self.assertIn("id", matches[0])
            self.assertIn("team1", matches[0])
            self.assertIn("team2", matches[0])
            self.assertIn("event", matches[0])
            self.assertIn("date", matches[0])
            self.assertIn("format", matches[0])

    def test_03_refresh_matches(self):
        """Test refreshing matches"""
        response = requests.post(f"{self.base_url}/refresh-matches")
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertIn("status", result)
        self.assertIn("matches_updated", result)
        self.assertEqual(result["status"], "success")

    def test_04_create_and_get_bet(self):
        """Test creating and retrieving a bet"""
        # First get a match to bet on
        matches_response = requests.get(f"{self.base_url}/matches")
        matches = matches_response.json()
        self.assertTrue(len(matches) > 0, "No matches available for testing")
        
        test_match = matches[0]
        
        # Create bet data
        bet_data = {
            "match_id": test_match["id"],
            "team_bet_on": test_match["team1"],
            "odds": 2.0,
            "stake": 100
        }
        
        # Create bet
        create_response = requests.post(f"{self.base_url}/bets", json=bet_data)
        self.assertEqual(create_response.status_code, 200)
        created_bet = create_response.json()
        self.assertIn("id", created_bet)
        self.assertEqual(created_bet["match_id"], bet_data["match_id"])
        self.assertEqual(created_bet["team_bet_on"], bet_data["team_bet_on"])
        
        # Get all bets
        get_response = requests.get(f"{self.base_url}/bets")
        self.assertEqual(get_response.status_code, 200)
        bets = get_response.json()
        self.assertIsInstance(bets, list)
        self.assertTrue(any(bet["id"] == created_bet["id"] for bet in bets))

    def test_05_update_bet(self):
        """Test updating a bet"""
        # First create a bet
        matches_response = requests.get(f"{self.base_url}/matches")
        matches = matches_response.json()
        test_match = matches[0]
        
        bet_data = {
            "match_id": test_match["id"],
            "team_bet_on": test_match["team1"],
            "odds": 2.0,
            "stake": 100
        }
        
        create_response = requests.post(f"{self.base_url}/bets", json=bet_data)
        created_bet = create_response.json()
        
        # Update bet
        update_data = {
            "result": "win",
            "status": "settled",
            "actual_return": 200
        }
        
        update_response = requests.put(
            f"{self.base_url}/bets/{created_bet['id']}", 
            json=update_data
        )
        self.assertEqual(update_response.status_code, 200)
        updated_bet = update_response.json()
        self.assertEqual(updated_bet["result"], "win")
        self.assertEqual(updated_bet["status"], "settled")
        self.assertEqual(updated_bet["actual_return"], 200)

if __name__ == "__main__":
    unittest.main(verbosity=2)
