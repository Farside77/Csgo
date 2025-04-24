#!/bin/bash

# This script uses common terminal emulators to run the launcher
# with appropriate privileges

# Try different terminal emulators
if command -v gnome-terminal &> /dev/null; then
    gnome-terminal --wait -- sudo /app/launcher.sh
elif command -v xterm &> /dev/null; then
    xterm -e "sudo /app/launcher.sh"
elif command -v konsole &> /dev/null; then
    konsole -e "sudo /app/launcher.sh"
elif command -v xfce4-terminal &> /dev/null; then
    xfce4-terminal -e "sudo /app/launcher.sh"
elif command -v lxterminal &> /dev/null; then
    lxterminal -e "sudo /app/launcher.sh"
else
    # Fallback to direct execution
    sudo /app/launcher.sh
fi