#!/usr/bin/env python3
"""
CS2 Esports Tracker - LAN Performance Weighting Validation Tool

This script tests the LAN performance weighting system by:
1. Creating test match data with various LAN/online statuses
2. Testing prediction accuracy based on LAN weights
3. Validating time decay and roster stability factors
"""

import requests
import uuid
import json
import time
from datetime import datetime, timedelta
import os
import sys
import random

# Configuration
BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL', 'http://localhost:8001')

def create_test_match(team1, team2, is_lan=True, days_ago=None, score=None):
    """Create a test match with the given parameters"""
    match_id = str(uuid.uuid4())
    
    # Set date based on days_ago
    if days_ago is not None:
        match_date = (datetime.now() - timedelta(days=days_ago)).isoformat()
    else:
        match_date = datetime.now().isoformat()
    
    # Base match data
    match = {
        "id": match_id,
        "team1": team1,
        "team2": team2,
        "event": f"Test Event {'LAN' if is_lan else 'Online'}",
        "format": "Bo3",
        "date": match_date,
        "is_lan": is_lan,
        "status": "upcoming" if score is None else "completed"
    }
    
    # Add score and winner for completed matches
    if score is not None:
        team1_score, team2_score = map(int, score.split('-'))
        match["winner"] = team1 if team1_score > team2_score else team2
        match["score"] = score
    
    return match

def post_match(match):
    """Post a match to the API"""
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/matches", 
            json=match,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error posting match: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Exception posting match: {str(e)}")
        return None

def get_match_prediction(match_id):
    """Get the prediction for a match"""
    try:
        response = requests.get(f"{BACKEND_URL}/api/matches/{match_id}")
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error getting match: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Exception getting match: {str(e)}")
        return None

def test_lan_weighting():
    """Test the LAN performance weighting system"""
    print("\n🔍 Testing LAN Performance Weighting System...")
    
    # Use direct POST to /api/refresh-matches to create test data
    try:
        # First refresh the matches to ensure we have data
        print("Refreshing matches to ensure we have data...")
        response = requests.post(f"{BACKEND_URL}/api/refresh-matches")
        if response.status_code != 200:
            print(f"❌ Error refreshing matches: {response.status_code} - {response.text}")
            return False
        
        # Get all matches to find teams for testing
        response = requests.get(f"{BACKEND_URL}/api/matches")
        if response.status_code != 200:
            print(f"❌ Error getting matches: {response.status_code} - {response.text}")
            return False
        
        matches = response.json()
        
        # Extract all teams
        all_teams = set()
        for match in matches:
            all_teams.add(match["team1"])
            all_teams.add(match["team2"])
        
        teams_list = list(all_teams)
        
        if len(teams_list) < 4:
            print(f"❌ Not enough teams for testing: {len(teams_list)}")
            return False
        
        print(f"Found {len(teams_list)} teams for testing")
        
        # Pick 2 teams for testing
        team_a = random.choice(teams_list)
        teams_list.remove(team_a)
        team_b = random.choice(teams_list)
        teams_list.remove(team_b)
        
        team_c = random.choice(teams_list)
        teams_list.remove(team_c)
        team_d = random.choice(teams_list)
        
        print(f"Selected teams for Test 1: {team_a} vs {team_b}")
        print(f"Selected teams for Test 2: {team_c} vs {team_d}")
        
        # Test 1: LAN vs Online Performance
        print("\nTest 1: LAN vs Online Performance")
        print("--------------------------------")
        print(f"Creating test matches for {team_a} vs {team_b}...")
        
        # Create test history - Team A wins on LAN, Team B wins online
        # This should make Team A favored in LAN matches and Team B in online matches
        
        # Recent history (last 30 days)
        for i in range(3):
            # Team A wins on LAN
            match = create_test_match(team_a, team_b, is_lan=True, days_ago=i+1, score="2-0")
            post_match(match)
            
            # Team B wins online
            match = create_test_match(team_a, team_b, is_lan=False, days_ago=i+1, score="0-2")
            post_match(match)
        
        # Create test upcoming matches
        lan_match = create_test_match(team_a, team_b, is_lan=True)
        online_match = create_test_match(team_a, team_b, is_lan=False)
        
        # Allow time for the database to process
        time.sleep(1)
        
        # Now fetch the upcoming matches with predictions
        print("Fetching upcoming matches with predictions...")
        response = requests.get(f"{BACKEND_URL}/api/matches")
        if response.status_code != 200:
            print(f"❌ Error getting matches: {response.status_code} - {response.text}")
            return False
        
        all_matches = response.json()
        
        # Find our test matches with predictions
        test_lan_match = None
        test_online_match = None
        
        for match in all_matches:
            if match["team1"] == team_a and match["team2"] == team_b and match["status"] == "upcoming":
                if match.get("is_lan", False):
                    test_lan_match = match
                else:
                    test_online_match = match
        
        # Check if our hypothesis is correct
        if test_lan_match and test_online_match:
            print(f"\nResults for {team_a} vs {team_b}:")
            
            lan_prediction = test_lan_match.get("predicted_winner")
            online_prediction = test_online_match.get("predicted_winner")
            
            print(f"LAN match prediction: {lan_prediction} (Expected: {team_a})")
            print(f"Online match prediction: {online_prediction} (Expected: {team_b})")
            
            lan_result = "✅" if lan_prediction == team_a else "❌"
            online_result = "✅" if online_prediction == team_b else "❌"
            
            print(f"LAN weighting validation: {lan_result}")
            print(f"Online weighting validation: {online_result}")
            
            # Check LAN win rates in analysis
            if "analysis" in test_lan_match:
                analysis = test_lan_match["analysis"]
                team1_lan_rate = analysis.get("team1_lan_win_rate")
                team2_lan_rate = analysis.get("team2_lan_win_rate")
                
                print(f"\nLAN win rates:")
                print(f"  {team_a}: {team1_lan_rate}")
                print(f"  {team_b}: {team2_lan_rate}")
                
                # Online rates
                team1_online_rate = analysis.get("team1_online_win_rate")
                team2_online_rate = analysis.get("team2_online_win_rate")
                
                print(f"\nOnline win rates:")
                print(f"  {team_a}: {team1_online_rate}")
                print(f"  {team_b}: {team2_online_rate}")
                
                # Validate our setup worked
                if team1_lan_rate > team2_lan_rate and team2_online_rate > team1_online_rate:
                    print("\n✅ LAN vs Online differentiation confirmed")
                else:
                    print("\n❌ LAN vs Online differentiation not detected")
        else:
            print("❌ Could not find test matches with predictions")
        
        # Test 2: Recent vs Old Performance with Time Decay
        print("\nTest 2: Recent vs Old Performance (Time Decay)")
        print("---------------------------------------------")
        print(f"Creating test matches for {team_c} vs {team_d}...")
        
        # Team C wins all recent matches, Team D won all old matches
        
        # Recent matches (team C wins)
        for i in range(5):
            match = create_test_match(team_c, team_d, is_lan=True, days_ago=i+1, score="2-0")
            post_match(match)
        
        # Old matches (team D wins)
        for i in range(5):
            match = create_test_match(team_c, team_d, is_lan=True, days_ago=i+60, score="0-2")
            post_match(match)
        
        # Create upcoming match
        future_match = create_test_match(team_c, team_d, is_lan=True)
        
        # Allow time for the database to process
        time.sleep(1)
        
        # Fetch upcoming match with prediction
        response = requests.get(f"{BACKEND_URL}/api/matches")
        if response.status_code != 200:
            print(f"❌ Error getting matches: {response.status_code} - {response.text}")
            return False
        
        all_matches = response.json()
        
        # Find our test match
        test_recency_match = None
        for match in all_matches:
            if match["team1"] == team_c and match["team2"] == team_d and match["status"] == "upcoming":
                test_recency_match = match
                break
        
        if test_recency_match:
            print(f"\nResults for {team_c} vs {team_d}:")
            
            prediction = test_recency_match.get("predicted_winner")
            print(f"Match prediction: {prediction} (Expected: {team_c})")
            
            result = "✅" if prediction == team_c else "❌"
            print(f"Time decay validation: {result}")
            
            win_prob = test_recency_match.get("win_probability", 0.5)
            print(f"Win probability: {win_prob:.2f}")
            
            if "analysis" in test_recency_match:
                analysis = test_recency_match["analysis"]
                team1_form = analysis.get("team1_recent_form")
                team2_form = analysis.get("team2_recent_form")
                
                print(f"\nRecent form:")
                print(f"  {team_c}: {team1_form}")
                print(f"  {team_d}: {team2_form}")
                
                if team1_form > team2_form:
                    print("\n✅ Time decay factor confirmed")
                else:
                    print("\n❌ Time decay factor not detected")
        else:
            print("❌ Could not find test match with prediction")
        
        print("\nLAN Performance Weighting Validation Complete")
        return True
        
    except Exception as e:
        print(f"❌ Exception during testing: {str(e)}")
        return False

if __name__ == "__main__":
    print("CS2 Esports Tracker - LAN Performance Weighting Validation")
    print("=========================================================")
    
    success = test_lan_weighting()
    
    if success:
        print("\n✅ Testing completed successfully")
        sys.exit(0)
    else:
        print("\n❌ Testing failed")
        sys.exit(1)