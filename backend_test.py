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
            print("Sample match data:", json.dumps(matches[0], indent=2))
        print("✅ Get matches test passed")

    def test_3_refresh_matches(self):
        """Test refreshing matches"""
        print("\nTesting refresh matches endpoint...")
        response = requests.post(f"{self.base_url}/api/refresh-matches")
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertIn("matches_updated", result)
        print(f"Refreshed {result['matches_updated']} matches")
        print("✅ Refresh matches test passed")

    def test_4_create_bet(self):
        """Test creating a bet"""
        print("\nTesting create bet endpoint...")
        if not self.test_match_id:
            print("⚠️ Skipping bet creation test - no match ID available")
            return

        # Get match details first
        response = requests.get(f"{self.base_url}/api/matches")
        matches = response.json()
        test_match = next((m for m in matches if m["id"] == self.test_match_id), None)
        
        if not test_match:
            print("⚠️ Test match not found")
            return

        bet_data = {
            "match_id": self.test_match_id,
            "team_bet_on": test_match["team1"],
            "odds": test_match["team1_odds"],
            "stake": 10.0
        }

        response = requests.post(
            f"{self.base_url}/api/bets",
            json=bet_data
        )
        self.assertEqual(response.status_code, 200)
        bet = response.json()
        self.test_bet_id = bet["id"]
        print("Created bet:", json.dumps(bet, indent=2))
        print("✅ Create bet test passed")

    def test_5_get_bets(self):
        """Test getting bets"""
        print("\nTesting get bets endpoint...")
        response = requests.get(f"{self.base_url}/api/bets")
        self.assertEqual(response.status_code, 200)
        bets = response.json()
        self.assertIsInstance(bets, list)
        if bets:
            print(f"Found {len(bets)} bets")
            print("Sample bet data:", json.dumps(bets[0], indent=2))
        print("✅ Get bets test passed")

    def test_6_update_bet(self):
        """Test updating a bet"""
        print("\nTesting update bet endpoint...")
        if not self.test_bet_id:
            print("⚠️ Skipping bet update test - no bet ID available")
            return

        update_data = {
            "result": "win",
            "status": "settled"
        }

        response = requests.put(
            f"{self.base_url}/api/bets/{self.test_bet_id}",
            json=update_data
        )
        self.assertEqual(response.status_code, 200)
        updated_bet = response.json()
        print("Updated bet:", json.dumps(updated_bet, indent=2))
        print("✅ Update bet test passed")

if __name__ == "__main__":
    unittest.main(verbosity=2)
