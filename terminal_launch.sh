#!/bin/bash

# This script attempts to open the simple_launcher.sh in a terminal
# that will definitely stay open

# Try using the most reliable combination first
if command -v xterm &> /dev/null; then
    echo "Launching with xterm (should stay open)"
    xterm -hold -e "sudo /app/simple_launcher.sh" &
    exit 0
fi

if command -v gnome-terminal &> /dev/null; then
    echo "Launching with gnome-terminal (should stay open)"
    gnome-terminal -- bash -c "sudo /app/simple_launcher.sh; exec bash" &
    exit 0
fi

if command -v konsole &> /dev/null; then
    echo "Launching with konsole (should stay open)"
    konsole -e "bash -c 'sudo /app/simple_launcher.sh; exec bash'" &
    exit 0
fi

if command -v xfce4-terminal &> /dev/null; then
    echo "Launching with xfce4-terminal (should stay open)"
    xfce4-terminal -e "bash -c 'sudo /app/simple_launcher.sh; exec bash'" --hold &
    exit 0
fi

if command -v lxterminal &> /dev/null; then
    echo "Launching with lxterminal (should stay open)"
    lxterminal -e "bash -c 'sudo /app/simple_launcher.sh; exec bash'" &
    exit 0
fi

# If all else fails, try to run the launcher directly
echo "No suitable terminal emulator found. Trying direct execution."
echo "If this closes too quickly, please open a terminal and run: sudo /app/simple_launcher.sh"
sudo /app/simple_launcher.sh