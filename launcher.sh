#!/bin/bash

# CS2 Esports Tracker Launcher
echo "========================================="
echo "CS2 Esports Tracker Launcher"
echo "========================================="

# Function to display status messages
status() {
    echo ""
    echo ">>> $1"
    echo ""
}

# Check if we need to run the installation script
if [ ! -d "/app/backend" ] || [ ! -d "/app/frontend" ]; then
    status "Application not fully installed. Running installation script..."
    if [ -x "/app/install.sh" ]; then
        sudo /app/install.sh
        exit $?
    else
        echo "Error: Installation script not found or not executable."
        echo "Please run: sudo chmod +x /app/install.sh && sudo /app/install.sh"
        exit 1
    fi
fi

# Check if supervisor is installed
if ! command -v supervisorctl &> /dev/null; then
    status "Supervisor not installed. Installing..."
    sudo apt-get update && sudo apt-get install -y supervisor
fi

status "Starting CS2 Esports Tracker..."

# Update supervisor config
sudo supervisorctl reread
sudo supervisorctl update

# Check if MongoDB is available and configured
if command -v mongod &> /dev/null && [ -f "/etc/supervisor/conf.d/mongodb.conf" ]; then
    # Check if MongoDB is running, if not, try to start it
    if ! sudo supervisorctl status mongodb | grep -q "RUNNING"; then
        status "MongoDB not running. Starting MongoDB..."
        sudo supervisorctl start mongodb
        sleep 2
    fi
    
    # Restart MongoDB
    status "Restarting MongoDB..."
    sudo supervisorctl restart mongodb
else
    status "MongoDB not installed or configured. Skipping MongoDB restart."
fi

# Restart backend and frontend services
status "Restarting application services..."
sudo supervisorctl restart backend frontend

# Check services status
status "Checking service status..."
sudo supervisorctl status

status "CS2 Esports Tracker is now running!"
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
echo "========================================="