#!/bin/bash

# Try to launch with xterm first (most likely to work)
if command -v xterm &> /dev/null; then
    xterm -hold -e "/app/simple_test.sh"
    exit
fi

# Try other terminals with exec bash to keep them open
if command -v gnome-terminal &> /dev/null; then
    gnome-terminal -- bash -c "/app/simple_test.sh; exec bash"
    exit
fi

if command -v konsole &> /dev/null; then
    konsole -e bash -c "/app/simple_test.sh; exec bash"
    exit
fi

if command -v xfce4-terminal &> /dev/null; then
    xfce4-terminal -e bash -c "/app/simple_test.sh; exec bash" --hold
    exit
fi

if command -v lxterminal &> /dev/null; then
    lxterminal -e bash -c "/app/simple_test.sh; exec bash"
    exit
fi

# If none of the above worked, try direct bash
bash -c "/app/simple_test.sh"