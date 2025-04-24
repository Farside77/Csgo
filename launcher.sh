#!/bin/bash

# CS2 Esports Tracker Launcher
echo "Starting CS2 Esports Tracker..."

# Update supervisor config
sudo supervisorctl reread
sudo supervisorctl update

# Restart services
sudo supervisorctl restart mongodb
sudo supervisorctl restart backend
sudo supervisorctl restart frontend

echo "CS2 Esports Tracker is now running!"
echo "Backend is running at $(grep REACT_APP_BACKEND_URL /app/frontend/.env | cut -d'=' -f2)"
echo "Frontend should be accessible at http://localhost:3000"
echo ""
echo "You can use the following commands to manage the services:"
echo "  - sudo supervisorctl status                 # View service status"
echo "  - sudo supervisorctl restart all            # Restart all services"
echo "  - sudo supervisorctl restart mongodb        # Restart MongoDB database"
echo "  - sudo supervisorctl restart backend        # Restart backend"
echo "  - sudo supervisorctl restart frontend       # Restart frontend"
echo "  - sudo supervisorctl stop all               # Stop all services"
echo "  - sudo supervisorctl start all              # Start all services"