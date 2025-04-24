# CS2 Esports Tracker - Installation Guide

This guide provides easy step-by-step instructions for setting up the CS2 Esports Tracker on your local machine.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed on your machine
- [Docker Compose](https://docs.docker.com/compose/install/) installed on your machine

## Installation Steps

### 1. Download the Application

Download the CS2 Esports Tracker files to your computer.

```bash
git clone https://github.com/yourusername/cs2-esports-tracker.git
cd cs2-esports-tracker
```

### 2. Start the Application

Run the following command to start all components of the application:

```bash
docker-compose up -d
```

This command will:
- Start MongoDB database
- Start the backend API server
- Start the frontend web interface

### 3. Access the Application

Once all containers are running, you can access the application in your web browser:

```
http://localhost:3000
```

## Stopping the Application

To stop the application, run:

```bash
docker-compose down
```

To completely remove all data (including the database), run:

```bash
docker-compose down -v
```

## Usage Guide

### Viewing Matches

1. When you first open the application, you'll see the "Matches" tab with upcoming CS2 matches
2. Click "Refresh Matches" to get the latest match data
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

- If the application doesn't load, ensure all Docker containers are running:
  ```bash
  docker-compose ps
  ```
- If match data isn't loading, check that the backend container is running and accessible
- For any other issues, check the container logs:
  ```bash
  docker-compose logs
  ```