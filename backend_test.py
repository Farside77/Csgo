import requests
import unittest
import os
from datetime import datetime

class CS2EsportsTrackerAPITest(unittest.TestCase):
    def setUp(self):
        # Get the backend URL from frontend's .env file
        with open('/app/frontend/.env', 'r') as f:
            for line in f:
                if line.startswith('REACT_APP_BACKEND_URL='):
                    self.base_url = line.strip().split('=')[1].strip('"')
                    break
        
        if not hasattr(self, 'base_url'):
            raise Exception("Could not find REACT_APP_BACKEND_URL in frontend/.env")

    def test_root_endpoint(self):
        """Test the root API endpoint"""
        response = requests.get(f"{self.base_url}/api")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "CS2 Esports Tracker API"})

    def test_get_matches(self):
        """Test getting matches"""
        # Test getting all matches
        response = requests.get(f"{self.base_url}/api/matches")
        self.assertEqual(response.status_code, 200)
        matches = response.json()
        self.assertIsInstance(matches, list)
        
        if matches:  # If we have matches, verify their structure
            match = matches[0]
            required_fields = ['id', 'team1', 'team2', 'event', 'date', 'format']
            for field in required_fields:
                self.assertIn(field, match)

        # Test filtering by status
        response = requests.get(f"{self.base_url}/api/matches?status=upcoming")
        self.assertEqual(response.status_code, 200)
        upcoming_matches = response.json()
        if upcoming_matches:
            self.assertEqual(upcoming_matches[0]['status'], 'upcoming')

    def test_refresh_matches(self):
        """Test refreshing matches"""
        response = requests.post(f"{self.base_url}/api/refresh-matches")
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertIn('status', result)
        self.assertIn('matches_updated', result)
        self.assertEqual(result['status'], 'success')

    def test_bet_operations(self):
        """Test bet creation and retrieval"""
        # First get a match to bet on
        matches_response = requests.get(f"{self.base_url}/api/matches")
        self.assertEqual(matches_response.status_code, 200)
        matches = matches_response.json()
        
        if not matches:
            self.skipTest("No matches available for betting test")
            
        match = matches[0]
        
        # Create a bet
        bet_data = {
            "match_id": match['id'],
            "team_bet_on": match['team1'],
            "odds": 1.5,
            "stake": 100
        }
        
        create_response = requests.post(
            f"{self.base_url}/api/bets",
            json=bet_data
        )
        self.assertEqual(create_response.status_code, 200)
        created_bet = create_response.json()
        
        # Verify bet fields
        self.assertEqual(created_bet['match_id'], bet_data['match_id'])
        self.assertEqual(created_bet['team_bet_on'], bet_data['team_bet_on'])
        self.assertEqual(created_bet['odds'], bet_data['odds'])
        self.assertEqual(created_bet['stake'], bet_data['stake'])
        self.assertEqual(created_bet['status'], 'pending')
        
        # Get all bets
        get_response = requests.get(f"{self.base_url}/api/bets")
        self.assertEqual(get_response.status_code, 200)
        bets = get_response.json()
        self.assertIsInstance(bets, list)
        
        # Update bet
        bet_id = created_bet['id']
        update_data = {
            "status": "settled",
            "result": "win",
            "actual_return": 150
        }
        
        update_response = requests.put(
            f"{self.base_url}/api/bets/{bet_id}",
            json=update_data
        )
        self.assertEqual(update_response.status_code, 200)
        updated_bet = update_response.json()
        self.assertEqual(updated_bet['status'], 'settled')
        self.assertEqual(updated_bet['result'], 'win')
        self.assertEqual(updated_bet['actual_return'], 150)

    def test_error_handling(self):
        """Test error handling in various scenarios"""
        # Test invalid match ID in bet creation
        invalid_bet = {
            "match_id": "invalid_id",
            "team_bet_on": "Team A",
            "odds": 1.5,
            "stake": 100
        }
        response = requests.post(f"{self.base_url}/api/bets", json=invalid_bet)
        self.assertEqual(response.status_code, 404)

        # Test invalid bet update
        response = requests.put(
            f"{self.base_url}/api/bets/invalid_id",
            json={"status": "settled"}
        )
        self.assertEqual(response.status_code, 404)

        # Test invalid odds in bet creation
        invalid_odds_bet = {
            "match_id": "some_id",
            "team_bet_on": "Team A",
            "odds": 0.5,  # Invalid odds (must be > 1.0)
            "stake": 100
        }
        response = requests.post(f"{self.base_url}/api/bets", json=invalid_odds_bet)
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=2)
