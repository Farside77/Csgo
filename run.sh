#!/bin/sh
# Plain sh script (not bash) for maximum compatibility

echo "Starting CS2 Esports Tracker..."

# Try to run as root if needed
if [ "$(id -u)" -ne 0 ]; then
    echo "Trying to run with sudo..."
    sudo sh "$0"
    exit $?
fi

# Start all necessary services
echo "Starting services..."
supervisorctl start mongodb
supervisorctl start backend
supervisorctl start frontend

echo ""
echo "CS2 Esports Tracker should now be running!"
echo "Access the application at: http://localhost:3000"
echo ""
echo "Press Enter to close this window..."
read dummy_var