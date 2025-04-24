import unittest
import requests
import json
from datetime import datetime

class CS2EsportsTrackerAPITest(unittest.TestCase):
    def setUp(self):
        self.base_url = "http://localhost:8001"
        self.test_match_id = None
        self.test_bet_id = None

    def test_1_api_root(self):
        """Test API root endpoint"""
        print("\nTesting API root endpoint...")
        response = requests.get(f"{self.base_url}/api")
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json())
        print("✅ API root endpoint test passed")

    def test_2_get_matches(self):
        """Test getting matches"""
        print("\nTesting get matches endpoint...")
        response = requests.get(f"{self.base_url}/api/matches")
        self.assertEqual(response.status_code, 200)
        matches = response.json()
        self.assertIsInstance(matches, list)
        if matches:
            self.test_match_id = matches[0]["id"]
            print(f"Found {len(matches)} matches")
        print("✅ Get matches test passed")

    def test_3_refresh_matches(self):
        """Test refreshing matches"""
        print("\nTesting refresh matches endpoint...")
        response = requests.post(f"{self.base_url}/api/refresh-matches")
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertIn("matches_updated", result)
        print(f"✅ Refreshed {result['matches_updated']} matches")

    def test_4_create_bet(self):
        """Test creating a bet"""
        print("\nTesting create bet endpoint...")
        if not self.test_match_id:
            print("⚠️ Skipping bet creation test - no match ID available")
            return

        bet_data = {
            "match_id": self.test_match_id,
            "team_bet_on": "Team1",
            "odds": 1.5,
            "stake": 10.0
        }

        response = requests.post(
            f"{self.base_url}/api/bets",
            json=bet_data
        )
        self.assertEqual(response.status_code, 200)
        bet = response.json()
        self.test_bet_id = bet["id"]
        print("✅ Created bet successfully")

    def test_5_get_bets(self):
        """Test getting bets"""
        print("\nTesting get bets endpoint...")
        response = requests.get(f"{self.base_url}/api/bets")
        self.assertEqual(response.status_code, 200)
        bets = response.json()
        self.assertIsInstance(bets, list)
        print(f"✅ Found {len(bets)} bets")

if __name__ == "__main__":
    unittest.main(verbosity=2)
