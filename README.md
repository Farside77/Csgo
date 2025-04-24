# CS2 Esports Tracker

A tool for tracking Counter-Strike 2 esports matches, analyzing betting opportunities, and tracking your bet performance.

## Features

- View upcoming CS2 matches from HLTV
- Get predictions for match outcomes and scores
- Calculate EV (Expected Value) for betting opportunities
- Track your bets and analyze performance
- Simple, intuitive interface

## Installation Guide

### Prerequisites

- Docker installed on your machine
- Internet connection

### Step-by-Step Installation

#### Option 1: Using Docker Compose (Easiest)

1. Download the application files to your computer
```
git clone https://github.com/yourusername/cs2-esports-tracker.git
cd cs2-esports-tracker
```

2. Start the application using Docker Compose
```
docker-compose up -d
```

3. Access the application in your browser
```
http://localhost:3000
```

#### Option 2: Manual Setup

1. Make sure MongoDB is installed and running on your machine

2. Install backend dependencies
```
cd backend
pip install -r requirements.txt
```

3. Start the backend server
```
cd backend
uvicorn server:app --host 0.0.0.0 --port 8001
```

4. Install frontend dependencies
```
cd frontend
npm install
```

5. Start the frontend server
```
cd frontend
npm start
```

6. Access the application in your browser
```
http://localhost:3000
```

## Usage Guide

### Viewing Matches

1. When you first open the application, you'll see the "Matches" tab with upcoming CS2 matches
2. Click "Refresh Matches" to get the latest match data from HLTV
3. Each match card shows:
   - Teams playing
   - Event name
   - Match date and time
   - Match format (BO1, BO3, etc.)
   - Predicted winner and score
   - EV value (if available)

### Placing Bets

1. Click the "Place Bet" button on any match
2. Select the team you want to bet on
3. Enter the odds you're getting from your betting platform
4. Enter your stake amount
5. The potential return will be calculated automatically
6. Click "Place Bet" to save the bet

### Tracking Bets

1. Go to the "My Bets" tab to see all your recorded bets
2. For pending bets, click "Win" or "Loss" to record the outcome
3. View your betting performance metrics at the top:
   - Total bets placed
   - Win rate
   - Total profit/loss
   - ROI (Return on Investment)

## Troubleshooting

- If the application doesn't load, check that both backend and frontend servers are running
- If match data isn't loading, check your internet connection and try refreshing
- For any other issues, check the console logs in your browser

## Maintenance

- The application automatically refreshes match data every 30 minutes
- You can manually refresh the data using the "Refresh Matches" button
