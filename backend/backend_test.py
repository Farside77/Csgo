import requests
import unittest
import os
from datetime import datetime

class CS2EsportsTrackerAPITest(unittest.TestCase):
    def setUp(self):
        # Get the backend URL from environment or use a default for testing
        self.base_url = os.getenv('REACT_APP_BACKEND_URL', 'http://localhost:8001')
        print(f"Testing against backend URL: {self.base_url}")

    def test_get_matches(self):
        """Test GET /api/matches endpoint"""
        print("\n🔍 Testing GET matches...")
        try:
            response = requests.get(f"{self.base_url}/api/matches")
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertIsInstance(data, list)
            if len(data) > 0:
                # Verify match structure
                match = data[0]
                required_fields = ['id', 'team1', 'team2', 'start_time', 'maps']
                for field in required_fields:
                    self.assertIn(field, match)
            print("✅ GET matches test passed")
        except Exception as e:
            print(f"❌ GET matches test failed: {str(e)}")
            raise

    def test_refresh_matches(self):
        """Test POST /api/refresh-matches endpoint"""
        print("\n🔍 Testing POST refresh-matches...")
        try:
            response = requests.post(f"{self.base_url}/api/refresh-matches")
            self.assertEqual(response.status_code, 200)
            print("✅ POST refresh-matches test passed")
        except Exception as e:
            print(f"❌ POST refresh-matches test failed: {str(e)}")
            raise

    def test_bets_crud(self):
        """Test betting endpoints (GET, POST, PUT)"""
        print("\n🔍 Testing betting endpoints...")
        try:
            # Test GET bets
            response = requests.get(f"{self.base_url}/api/bets")
            self.assertEqual(response.status_code, 200)
            initial_bets = response.json()
            self.assertIsInstance(initial_bets, list)
            print("✅ GET bets test passed")

            # Test POST bet
            test_bet = {
                "match_id": "test_match_123",
                "team": "Team1",
                "amount": 100,
                "odds": 1.5
            }
            response = requests.post(f"{self.base_url}/api/bets", json=test_bet)
            self.assertEqual(response.status_code, 200)
            new_bet = response.json()
            self.assertIn('id', new_bet)
            print("✅ POST bet test passed")

            # Test PUT bet
            bet_update = {
                "amount": 200,
                "status": "won"
            }
            response = requests.put(f"{self.base_url}/api/bets/{new_bet['id']}", json=bet_update)
            self.assertEqual(response.status_code, 200)
            updated_bet = response.json()
            self.assertEqual(updated_bet['amount'], 200)
            self.assertEqual(updated_bet['status'], 'won')
            print("✅ PUT bet test passed")

        except Exception as e:
            print(f"❌ Betting endpoints test failed: {str(e)}")
            raise

if __name__ == '__main__':
    unittest.main(verbosity=2)
