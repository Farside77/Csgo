import unittest
import requests
import json
from datetime import datetime, timedelta

BACKEND_URL = "http://localhost:8001/api"

class CS2EsportsTrackerTest(unittest.TestCase):
    def setUp(self):
        self.base_url = BACKEND_URL
        self.test_match_id = None
        self.test_bet_id = None

    def test_01_api_root(self):
        """Test API root endpoint"""
        response = requests.get(f"{self.base_url}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["message"], "CS2 Esports Tracker API")

    def test_02_get_matches(self):
        """Test getting matches list"""
        response = requests.get(f"{self.base_url}/matches")
        self.assertEqual(response.status_code, 200)
        matches = response.json()
        self.assertIsInstance(matches, list)
        
        if matches:
            # Store a match ID for later tests
            self.test_match_id = matches[0]["id"]
            
            # Verify match structure
            match = matches[0]
            required_fields = ["id", "team1", "team2", "event", "date", "format"]
            for field in required_fields:
                self.assertIn(field, match)
            
            # Verify prediction data
            prediction_fields = ["predicted_winner", "win_probability", "predicted_score"]
            for field in prediction_fields:
                self.assertIn(field, match)
            
            # Verify LAN performance data in analysis
            if "analysis" in match:
                analysis = match["analysis"]
                lan_fields = ["team1_lan_win_rate", "team2_lan_win_rate", "is_lan"]
                for field in lan_fields:
                    self.assertIn(field, analysis)

    def test_03_refresh_matches(self):
        """Test match refresh endpoint"""
        response = requests.post(f"{self.base_url}/refresh-matches")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("matches_updated", data)
        self.assertIsInstance(data["matches_updated"], int)

    def test_04_create_bet(self):
        """Test bet creation"""
        if not self.test_match_id:
            self.skipTest("No test match ID available")

        # Get match details first
        response = requests.get(f"{self.base_url}/matches")
        matches = response.json()
        match = next((m for m in matches if m["id"] == self.test_match_id), None)
        
        if not match:
            self.skipTest("Test match not found")

        bet_data = {
            "match_id": self.test_match_id,
            "team_bet_on": match["team1"],
            "odds": 2.0,
            "stake": 100
        }

        response = requests.post(
            f"{self.base_url}/bets",
            json=bet_data
        )
        self.assertEqual(response.status_code, 200)
        bet = response.json()
        
        # Store bet ID for later tests
        self.test_bet_id = bet["id"]
        
        # Verify bet structure
        self.assertEqual(bet["match_id"], self.test_match_id)
        self.assertEqual(bet["team_bet_on"], match["team1"])
        self.assertEqual(bet["odds"], 2.0)
        self.assertEqual(bet["stake"], 100)
        self.assertEqual(bet["potential_return"], 200)
        self.assertEqual(bet["status"], "pending")

    def test_05_get_bets(self):
        """Test getting bets list"""
        response = requests.get(f"{self.base_url}/bets")
        self.assertEqual(response.status_code, 200)
        bets = response.json()
        self.assertIsInstance(bets, list)
        
        if bets:
            bet = bets[0]
            required_fields = ["id", "match_id", "team_bet_on", "odds", "stake", "potential_return", "status"]
            for field in required_fields:
                self.assertIn(field, bet)

    def test_06_update_bet(self):
        """Test updating bet result"""
        if not self.test_bet_id:
            self.skipTest("No test bet ID available")

        update_data = {
            "result": "win",
            "status": "settled",
            "actual_return": 200
        }

        response = requests.put(
            f"{self.base_url}/bets/{self.test_bet_id}",
            json=update_data
        )
        self.assertEqual(response.status_code, 200)
        bet = response.json()
        
        self.assertEqual(bet["result"], "win")
        self.assertEqual(bet["status"], "settled")
        self.assertEqual(bet["actual_return"], 200)

    def test_07_bet_validation(self):
        """Test bet validation rules"""
        invalid_bet = {
            "match_id": "invalid_id",
            "team_bet_on": "Invalid Team",
            "odds": 0.5,  # Invalid odds
            "stake": -100  # Invalid stake
        }

        response = requests.post(
            f"{self.base_url}/bets",
            json=invalid_bet
        )
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main(verbosity=2)
