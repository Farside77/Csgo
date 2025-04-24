#!/bin/bash

# CS2 Esports Tracker Uninstallation Script
echo "========================================="
echo "CS2 Esports Tracker Uninstallation Script"
echo "========================================="

# Function to display status messages
status() {
    echo ""
    echo ">>> $1"
    echo ""
}

# Check if script is run as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run this script as root or with sudo."
    exit 1
fi

# Ask for confirmation
read -p "Are you sure you want to uninstall CS2 Esports Tracker? This will stop all services and remove all application files. (y/n): " -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Uninstallation cancelled."
    exit 0
fi

# Stop all services
status "Stopping all services"
supervisorctl stop all || true

# Remove supervisor configurations
status "Removing supervisor configurations"
rm -f /etc/supervisor/conf.d/mongodb.conf
rm -f /etc/supervisor/conf.d/backend.conf
rm -f /etc/supervisor/conf.d/frontend.conf
supervisorctl reread
supervisorctl update

# Remove application files
status "Removing application files"
rm -rf /app/backend
rm -rf /app/frontend
rm -f /app/launcher.sh
rm -f /app/install.sh

# Remove desktop shortcut
status "Removing desktop shortcut"
rm -f /usr/share/applications/cs2-tracker.desktop

# Ask if MongoDB data should be removed
read -p "Do you want to remove MongoDB data? (y/n): " -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    status "Removing MongoDB data directory"
    rm -rf /data/db
else
    echo "MongoDB data directory preserved."
fi

# Ask if cloned repository should be removed
read -p "Do you want to remove the cloned repository? (y/n): " -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    status "Removing cloned repository"
    rm -rf /app/Csgo
else
    echo "Cloned repository preserved."
fi

status "Uninstallation complete!"
echo "CS2 Esports Tracker has been uninstalled."
echo "========================================="

# Keep uninstall script
echo "This uninstall script can be deleted manually if no longer needed:"
echo "rm -f /app/uninstall.sh"