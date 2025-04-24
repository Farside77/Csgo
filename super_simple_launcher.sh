#!/bin/bash

# Super simple launcher
echo "Starting CS2 Esports Tracker..."

# Start services (only with basic commands)
echo "Starting MongoDB..."
supervisorctl start mongodb

echo "Starting backend..."
supervisorctl start backend

echo "Starting frontend..."
supervisorctl start frontend

echo "All services started!"
echo "You can access the application at: http://localhost:3000"
echo ""
echo "Press Enter to close this window..."
read dummy