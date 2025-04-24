#!/bin/bash

# This launcher will open a new terminal that stays open
# It tries different terminals in order

# Function to create a temporary script
create_temp_script() {
    TEMP_SCRIPT=$(mktemp)
    cat > "$TEMP_SCRIPT" << 'EOF'
#!/bin/bash
sudo /app/simple_launcher.sh
# In case the launcher exits early:
echo ""
echo "Press Enter to close this window..."
read dummy
EOF
    chmod +x "$TEMP_SCRIPT"
    echo "$TEMP_SCRIPT"
}

# Create the temporary script
TEMP_SCRIPT=$(create_temp_script)

# Try to open with a terminal that will stay open
if command -v xterm &> /dev/null; then
    xterm -hold -e "$TEMP_SCRIPT"
elif command -v gnome-terminal &> /dev/null; then
    gnome-terminal -- bash -c "$TEMP_SCRIPT; exec bash"
elif command -v konsole &> /dev/null; then
    konsole -e bash -c "$TEMP_SCRIPT; exec bash"
elif command -v xfce4-terminal &> /dev/null; then
    xfce4-terminal -e bash -c "$TEMP_SCRIPT; exec bash" --hold
elif command -v lxterminal &> /dev/null; then
    lxterminal -e bash -c "$TEMP_SCRIPT; exec bash"
else
    # Direct execution with a pause at the end
    sudo bash -c "/app/simple_launcher.sh; echo 'Press Enter to close...'; read dummy"
fi

# Clean up
rm -f "$TEMP_SCRIPT"