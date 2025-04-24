import requests
import unittest
from datetime import datetime

class CS2EsportsTrackerAPITest(unittest.TestCase):
    def setUp(self):
        self.base_url = "http://localhost:8001/api"
        
    def test_root_endpoint(self):
        """Test the root API endpoint"""
        response = requests.get(f"{self.base_url}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "CS2 Esports Tracker API"})

    def test_get_matches(self):
        """Test fetching matches"""
        response = requests.get(f"{self.base_url}/matches")
        self.assertEqual(response.status_code, 200)
        matches = response.json()
        self.assertIsInstance(matches, list)
        
        if matches:
            match = matches[0]
            required_fields = ["id", "team1", "team2", "event", "date", "format"]
            for field in required_fields:
                self.assertIn(field, match)

    def test_refresh_matches(self):
        """Test refreshing matches"""
        response = requests.post(f"{self.base_url}/refresh-matches")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("status", data)
        self.assertEqual(data["status"], "success")
        self.assertIn("matches_updated", data)

    def test_create_and_get_bet(self):
        """Test creating and retrieving a bet"""
        # First get a match to bet on
        matches_response = requests.get(f"{self.base_url}/matches")
        self.assertEqual(matches_response.status_code, 200)
        matches = matches_response.json()
        
        if not matches:
            self.skipTest("No matches available for betting test")
            
        match = matches[0]
        
        # Create a bet
        bet_data = {
            "match_id": match["id"],
            "team_bet_on": match["team1"],
            "odds": 2.0,
            "stake": 100
        }
        
        create_response = requests.post(
            f"{self.base_url}/bets",
            json=bet_data
        )
        self.assertEqual(create_response.status_code, 200)
        created_bet = create_response.json()
        
        # Verify bet was created correctly
        self.assertEqual(created_bet["match_id"], bet_data["match_id"])
        self.assertEqual(created_bet["team_bet_on"], bet_data["team_bet_on"])
        self.assertEqual(created_bet["odds"], bet_data["odds"])
        self.assertEqual(created_bet["stake"], bet_data["stake"])
        self.assertEqual(created_bet["status"], "pending")
        
        # Get all bets and verify our bet is there
        bets_response = requests.get(f"{self.base_url}/bets")
        self.assertEqual(bets_response.status_code, 200)
        bets = bets_response.json()
        self.assertTrue(any(bet["id"] == created_bet["id"] for bet in bets))

    def test_update_bet(self):
        """Test updating a bet's result"""
        # First create a bet
        matches_response = requests.get(f"{self.base_url}/matches")
        matches = matches_response.json()
        
        if not matches:
            self.skipTest("No matches available for bet update test")
            
        match = matches[0]
        
        bet_data = {
            "match_id": match["id"],
            "team_bet_on": match["team1"],
            "odds": 2.0,
            "stake": 100
        }
        
        create_response = requests.post(
            f"{self.base_url}/bets",
            json=bet_data
        )
        created_bet = create_response.json()
        
        # Update bet result
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
