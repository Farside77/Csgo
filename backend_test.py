import requests
import unittest
from datetime import datetime
import uuid

class CS2EsportsTrackerAPITest(unittest.TestCase):
    def setUp(self):
        self.base_url = "http://localhost:8001/api"
        self.test_match_id = None
        self.test_bet_id = None

    def test_01_api_root(self):
        """Test the API root endpoint"""
        print("\n🔍 Testing API root endpoint...")
        response = requests.get(f"{self.base_url}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "CS2 Esports Tracker API")
        print("✅ API root endpoint test passed")

    def test_02_get_matches(self):
        """Test getting matches"""
        print("\n🔍 Testing get matches endpoint...")
        response = requests.get(f"{self.base_url}/matches")
        self.assertEqual(response.status_code, 200)
        matches = response.json()
        self.assertIsInstance(matches, list)
        if matches:
            self.test_match_id = matches[0]["id"]
            print(f"Found {len(matches)} matches")
        print("✅ Get matches test passed")

    def test_03_refresh_matches(self):
        """Test refreshing matches"""
        print("\n🔍 Testing match refresh endpoint...")
        response = requests.post(f"{self.base_url}/refresh-matches")
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertIn("matches_updated", result)
        print(f"✅ Match refresh test passed. Updated {result['matches_updated']} matches")

    def test_04_create_bet(self):
        """Test creating a bet"""
        if not self.test_match_id:
            self.skipTest("No match ID available for betting test")

        print("\n🔍 Testing bet creation...")
        bet_data = {
            "match_id": self.test_match_id,
            "team_bet_on": "Natus Vincere",  # Using a known team from sample data
            "odds": 1.5,
            "stake": 100
        }
        response = requests.post(f"{self.base_url}/bets", json=bet_data)
        self.assertEqual(response.status_code, 200)
        bet = response.json()
        self.test_bet_id = bet["id"]
        self.assertEqual(bet["status"], "pending")
        print("✅ Bet creation test passed")

    def test_05_get_bets(self):
        """Test getting bets"""
        print("\n🔍 Testing get bets endpoint...")
        response = requests.get(f"{self.base_url}/bets")
        self.assertEqual(response.status_code, 200)
        bets = response.json()
        self.assertIsInstance(bets, list)
        print(f"Found {len(bets)} bets")
        print("✅ Get bets test passed")

    def test_06_update_bet(self):
        """Test updating a bet"""
        if not self.test_bet_id:
            self.skipTest("No bet ID available for update test")

        print("\n🔍 Testing bet update...")
        update_data = {
            "status": "settled",
            "result": "win",
            "actual_return": 150
        }
        response = requests.put(f"{self.base_url}/bets/{self.test_bet_id}", json=update_data)
        self.assertEqual(response.status_code, 200)
        updated_bet = response.json()
        self.assertEqual(updated_bet["status"], "settled")
        print("✅ Bet update test passed")

if __name__ == "__main__":
    unittest.main(verbosity=2)
