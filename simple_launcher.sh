#!/bin/bash

# This script launches the CS2 Tracker and ensures the terminal stays open

# Step 1: Make sure we run as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root or with sudo"
    exit 1
fi

# Step 2: Update supervisor configurations
supervisorctl reread
supervisorctl update

# Step 3: Start all services
supervisorctl restart mongodb backend frontend

# Step 4: Show status
echo ""
echo "==============================================="
echo "CS2 Esports Tracker is now running!"
echo "==============================================="
echo ""
echo "Frontend: http://localhost:3000"
echo "Backend: $(grep REACT_APP_BACKEND_URL /app/frontend/.env | cut -d'=' -f2)"
echo ""
echo "The application is now running in your browser."
echo "Press Ctrl+C to close this terminal (the application will continue running)."
echo ""

# Step 5: Show service status
supervisorctl status

# Step 6: Keep the terminal open
echo ""
echo "Terminal will stay open. Press Ctrl+C to close."
while true; do
    sleep 10
done