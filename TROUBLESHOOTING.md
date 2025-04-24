# CS2 Esports Tracker - Troubleshooting Guide

## Frontend Connection Issues

If you're experiencing issues with the frontend connecting to the backend, follow these steps:

### Step 1: Verify Services Are Running

```bash
sudo supervisorctl status
```

Both `frontend` and `backend` should show as `RUNNING`.

### Step 2: Check Backend API Directly

```bash
curl http://localhost:8001/api
```

You should see a response like: `{"message":"CS2 Esports Tracker API"}`

### Step 3: Test API Connectivity Using Debug Tools

1. Open http://localhost:3000/debug.html in your browser
2. Click "Test API Connection" to verify backend connectivity
3. Click "Fetch & Render Matches" to test match data retrieval
4. Click "Refresh Match Data" to test the refresh functionality
5. Click "Test Bet Creation" to verify betting works

### Step 4: Check Environment Variables

The frontend's `.env` file should contain:

```
REACT_APP_BACKEND_URL=http://localhost:8001/api
```

And the backend should have:

```
MONGO_URL=mongodb://localhost:27017
DB_NAME=cs2_esports_tracker
```

### Step 5: Check for CORS Issues

If you see CORS errors in the browser console, verify the CORS middleware in the backend:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://10.64.137.72:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["Content-Type"],
)
```

### Step 6: Check Backend Logs

```bash
tail -n 100 /var/log/supervisor/backend.err.log
```

Look for any error messages or exceptions.

### Step 7: Check Frontend Logs

```bash
tail -n 100 /var/log/supervisor/frontend.err.log
```

Look for any error messages related to API requests.

## Common Issues and Solutions

### 1. Browser Cache Issues

Try opening the application in an incognito/private window or clear your browser cache.

### 2. API Path Issue

Ensure you're not double-adding the `/api` prefix. If BACKEND_URL already includes `/api`, don't add it again in fetch calls.

### 3. MongoDB Connection Issues

If the backend can't connect to MongoDB, check:

```bash
sudo supervisorctl status mongodb
```

### 4. Render Issue with Match Data

If match data is retrieved but not displayed:
- Check the data structure matches what the frontend expects
- Ensure React state is being properly updated
- Look for React rendering errors in the browser console

### 5. State Management Problems

If the UI doesn't update correctly:
- Check React component rendering logic
- Verify useState hooks are working correctly
- Make sure data is properly flowing between components

## Advanced Debugging

### Running Tests

```bash
python3 /app/backend_test.py
python3 /app/frontend_performance_test.py
python3 /app/lan_performance_test.py
```

### Manually Testing API Endpoints

```bash
# Get all matches
curl http://localhost:8001/api/matches

# Refresh match data
curl -X POST http://localhost:8001/api/refresh-matches

# Create a bet
curl -X POST -H "Content-Type: application/json" \
  -d '{"match_id":"match_id_here","team_bet_on":"Team Name","odds":1.5,"stake":100}' \
  http://localhost:8001/api/bets
```

### Diagnosing Network Issues

If you're deploying remotely, check:
- Firewall rules allowing connections between services
- Network routing between containers/services
- DNS resolution if using hostnames

## Resetting the Application

If you need a clean slate:

```bash
# Restart all services
sudo supervisorctl restart all

# Clear MongoDB data
mongo cs2_esports_tracker --eval "db.dropDatabase()"

# Refresh match data
curl -X POST http://localhost:8001/api/refresh-matches
```

## Contact Support

If you're still experiencing issues after trying these steps, please provide:
1. Screenshots of any error messages
2. Output of the debug tools
3. The backend and frontend logs
4. Steps to reproduce the issue

This information will help troubleshoot your specific issue more effectively.