import requests
import pytest
import os
from datetime import datetime

class TestCS2EsportsTracker:
    def __init__(self):
        # Get backend URL from frontend .env
        with open('/app/frontend/.env', 'r') as f:
            for line in f:
                if 'REACT_APP_BACKEND_URL' in line:
                    self.base_url = line.split('=')[1].strip()
                    break
        
        if not self.base_url:
            raise Exception("Backend URL not found in frontend/.env")
        
        self.tests_run = 0
        self.tests_passed = 0

    def run_test(self, name, method, endpoint, expected_status, data=None):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}
        
        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=headers)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                return True, response.json() if response.text else {}
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                return False, {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def test_api_root(self):
        """Test API root endpoint"""
        return self.run_test(
            "API Root",
            "GET",
            "api",
            200
        )

    def test_get_matches(self):
        """Test getting matches"""
        return self.run_test(
            "Get Matches",
            "GET",
            "api/matches",
            200
        )

    def test_refresh_matches(self):
        """Test refreshing matches"""
        return self.run_test(
            "Refresh Matches",
            "POST",
            "api/refresh-matches",
            200
        )

    def test_create_bet(self):
        """Test creating a bet"""
        # First get a match to bet on
        success, matches = self.test_get_matches()
        if not success or not matches:
            print("❌ Failed to get matches for betting test")
            return False, {}

        match = matches[0]
        bet_data = {
            "match_id": match["id"],
            "team_bet_on": match["team1"],
            "odds": match["team1_odds"],
            "stake": 100
        }

        return self.run_test(
            "Create Bet",
            "POST",
            "api/bets",
            200,
            data=bet_data
        )

    def test_get_bets(self):
        """Test getting bets"""
        return self.run_test(
            "Get Bets",
            "GET",
            "api/bets",
            200
        )

def main():
    tester = TestCS2EsportsTracker()
    
    # Run API tests
    tester.test_api_root()
    tester.test_get_matches()
    tester.test_refresh_matches()
    tester.test_create_bet()
    tester.test_get_bets()

    # Print results
    print(f"\n📊 Tests passed: {tester.tests_passed}/{tester.tests_run}")
    return 0 if tester.tests_passed == tester.tests_run else 1

if __name__ == "__main__":
    exit(main())
