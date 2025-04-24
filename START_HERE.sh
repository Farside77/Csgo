#!/bin/sh
# Most compatible script possible

# Display instructions
echo "==============================================="
echo "CS2 ESPORTS TRACKER - STARTER SCRIPT"
echo "==============================================="
echo ""
echo "This script will help you start the CS2 Esports Tracker."
echo ""
echo "OPTIONS:"
echo "1. Start the application"
echo "2. Check status"
echo "3. Restart all services"
echo "4. Run basic test"
echo "5. Exit"
echo ""
echo "Enter your choice (1-5): "
read choice

case "$choice" in
    1)
        echo "Starting CS2 Esports Tracker..."
        if [ "$(id -u)" -ne 0 ]; then
            sudo supervisorctl start mongodb backend frontend
        else
            supervisorctl start mongodb backend frontend
        fi
        echo "Application should now be running!"
        echo "Visit http://localhost:3000 in your browser."
        ;;
    2)
        echo "Checking status..."
        if [ "$(id -u)" -ne 0 ]; then
            sudo supervisorctl status
        else
            supervisorctl status
        fi
        ;;
    3)
        echo "Restarting all services..."
        if [ "$(id -u)" -ne 0 ]; then
            sudo supervisorctl restart all
        else
            supervisorctl restart all
        fi
        echo "All services restarted!"
        ;;
    4)
        echo "Running basic test..."
        /app/basic_test.sh
        ;;
    5)
        echo "Exiting..."
        exit 0
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac

echo ""
echo "Press Enter to close this window..."
read dummy_var