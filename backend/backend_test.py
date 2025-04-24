import requests
import unittest
import os
import time
from datetime import datetime, timedelta
import uuid

class CS2EsportsTrackerAPITest(unittest.TestCase):
    def setUp(self):
        # Get the backend URL from environment or use a default for testing
        self.base_url = os.getenv('REACT_APP_BACKEND_URL', 'http://localhost:8001')
        print(f"Testing against backend URL: {self.base_url}")

    def test_api_root(self):
        """Test API root endpoint"""
        print("\n🔍 Testing API root...")
        try:
            response = requests.get(f"{self.base_url}/api")
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data["message"], "CS2 Esports Tracker API")
            print("✅ API root test passed")
        except Exception as e:
            print(f"❌ API root test failed: {str(e)}")
            raise

    def test_match_operations(self):
        """Test match-related operations"""
        print("\n🔍 Testing match operations...")
        try:
            # Test match refresh
            start_time = time.time()
            response = requests.post(f"{self.base_url}/api/refresh-matches")
            refresh_time = time.time() - start_time
            print(f"⏱️ Match refresh time: {refresh_time:.2f} seconds")
            
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertIn("matches_updated", data)
            self.assertGreater(data["matches_updated"], 0)
            print("✅ Match refresh test passed")

            # Test getting all matches
            start_time = time.time()
            response = requests.get(f"{self.base_url}/api/matches")
            fetch_time = time.time() - start_time
            print(f"⏱️ Match fetch time: {fetch_time:.2f} seconds")
            
            self.assertEqual(response.status_code, 200)
            matches = response.json()
            self.assertIsInstance(matches, list)
            self.assertGreater(len(matches), 0)

            # Verify match structure
            first_match = matches[0]
            required_fields = ["id", "team1", "team2", "event", "date", "format"]
            for field in required_fields:
                self.assertIn(field, first_match)

            # Test match prediction data
            prediction_fields = ["predicted_winner", "win_probability", "predicted_score"]
            for field in prediction_fields:
                self.assertIn(field, first_match)

            # Verify LAN performance weighting
            if "is_lan" in first_match:
                self.assertIn("analysis", first_match)
                analysis = first_match["analysis"]
                self.assertIn("team1_lan_win_rate", analysis)
                self.assertIn("team2_lan_win_rate", analysis)
            print("✅ Match structure and prediction test passed")

            # Test match filtering
            for status in ["upcoming", "live", "completed"]:
                response = requests.get(f"{self.base_url}/api/matches?status={status}")
                self.assertEqual(response.status_code, 200)
                filtered_matches = response.json()
                if filtered_matches:
                    self.assertEqual(filtered_matches[0]["status"], status)
            print("✅ Match filtering test passed")

        except Exception as e:
            print(f"❌ Match operations test failed: {str(e)}")
            raise

    def test_bet_operations(self):
        """Test betting operations"""
        print("\n🔍 Testing betting operations...")
        try:
            # Create test bet
            test_bet = {
                "match_id": str(uuid.uuid4()),
                "team_bet_on": "Test Team 1",
                "odds": 1.85,
                "stake": 100
            }

            # Test bet creation performance
            start_time = time.time()
            response = requests.post(f"{self.base_url}/api/bets", json=test_bet)
            create_time = time.time() - start_time
            print(f"⏱️ Bet creation time: {create_time:.2f} seconds")
            
            self.assertEqual(response.status_code, 200)
            created_bet = response.json()
            self.assertIn("id", created_bet)
            bet_id = created_bet["id"]
            print("✅ Bet creation test passed")

            # Test bet retrieval performance
            start_time = time.time()
            response = requests.get(f"{self.base_url}/api/bets")
            fetch_time = time.time() - start_time
            print(f"⏱️ Bet fetch time: {fetch_time:.2f} seconds")
            
            self.assertEqual(response.status_code, 200)
            bets = response.json()
            self.assertIsInstance(bets, list)
            self.assertGreater(len(bets), 0)
            print("✅ Bet retrieval test passed")

            # Test bet update
            update_data = {
                "status": "settled",
                "actual_return": 185.0,
                "result": "win"
            }
            start_time = time.time()
            response = requests.put(f"{self.base_url}/api/bets/{bet_id}", json=update_data)
            update_time = time.time() - start_time
            print(f"⏱️ Bet update time: {update_time:.2f} seconds")
            
            self.assertEqual(response.status_code, 200)
            updated_bet = response.json()
            self.assertEqual(updated_bet["status"], "settled")
            self.assertEqual(updated_bet["actual_return"], 185.0)
            print("✅ Bet update test passed")

        except Exception as e:
            print(f"❌ Betting operations test failed: {str(e)}")
            raise

    def test_edge_cases(self):
        """Test edge cases and error handling"""
        print("\n🔍 Testing edge cases...")
        try:
            # Test invalid bet creation
            invalid_bet = {
                "match_id": str(uuid.uuid4()),
                "team_bet_on": "Test Team 1",
                "odds": -1.85,  # Invalid odds
                "stake": -100  # Invalid stake
            }
            response = requests.post(f"{self.base_url}/api/bets", json=invalid_bet)
            self.assertNotEqual(response.status_code, 200)
            print("✅ Invalid bet handling test passed")

            # Test non-existent bet update
            fake_bet_id = str(uuid.uuid4())
            response = requests.put(
                f"{self.base_url}/api/bets/{fake_bet_id}",
                json={"status": "settled"}
            )
            self.assertEqual(response.status_code, 404)
            print("✅ Non-existent bet handling test passed")

            # Test invalid match status filter
            response = requests.get(f"{self.base_url}/api/matches?status=invalid")
            self.assertEqual(response.status_code, 200)  # Should return empty list
            matches = response.json()
            self.assertEqual(len(matches), 0)
            print("✅ Invalid match status handling test passed")

        except Exception as e:
            print(f"❌ Edge cases test failed: {str(e)}")
            raise

if __name__ == '__main__':
    unittest.main(verbosity=2)
