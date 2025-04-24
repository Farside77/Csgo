#!/bin/bash

# CS2 Esports Tracker Installation Script
echo "========================================="
echo "CS2 Esports Tracker Installation Script"
echo "========================================="

# Exit on error
set -e

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

# Update package lists
status "Updating package lists"
apt-get update

# Install system dependencies
status "Installing system dependencies"
apt-get install -y supervisor python3 python3-pip nodejs npm git curl

# Install MongoDB (with alternative fallback options)
status "Installing MongoDB"
if ! mongod --version &> /dev/null; then
    # Try the official MongoDB repo first
    if apt-get install -y gnupg; then
        curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | apt-key add - || true
        echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/7.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-7.0.list
        apt-get update || true
        apt-get install -y mongodb-org || {
            # If that fails, try mongodb-server package from default repos
            apt-get install -y mongodb-server || {
                # If that also fails, try mongodb package
                apt-get install -y mongodb || {
                    echo "Warning: Could not install MongoDB from repositories."
                    echo "Will try to use an existing MongoDB or run without it."
                }
            }
        }
    else
        echo "Warning: Could not install gnupg, skipping MongoDB installation from official repo."
        apt-get install -y mongodb-server || apt-get install -y mongodb || true
    fi
else
    status "MongoDB is already installed"
fi

# Create MongoDB data directory
status "Setting up MongoDB data directory"
mkdir -p /data/db
chown -R $(whoami):$(whoami) /data/db

# Create supervisor configuration for MongoDB
status "Setting up MongoDB supervisor configuration"
cat > /etc/supervisor/conf.d/mongodb.conf << EOF
[program:mongodb]
command=mongod --dbpath /data/db
directory=/data
autostart=true
autorestart=true
stderr_logfile=/var/log/supervisor/mongodb.err.log
stdout_logfile=/var/log/supervisor/mongodb.out.log
EOF

# Start MongoDB
status "Starting MongoDB service"
supervisorctl reread
supervisorctl update
supervisorctl start mongodb

# Clone the repository if it doesn't exist
if [ ! -d "/app/Csgo" ]; then
    status "Cloning repository"
    cd /app
    git clone https://github.com/Farside77/Csgo.git -b test
else
    status "Repository already exists, updating"
    cd /app/Csgo
    git pull
fi

# Install Python dependencies
status "Installing backend dependencies"
cd /app/Csgo/backend
pip install -r requirements.txt

# Additional Python dependencies that might be needed
status "Installing additional Python dependencies"
pip install httpx pymongo[srv]

# Install Node.js dependencies
status "Installing frontend dependencies"
cd /app/Csgo/frontend
npm install -g yarn
yarn install

# Copy files to the appropriate directories
status "Setting up application directories"
mkdir -p /app/backend /app/frontend
cp -r /app/Csgo/backend/* /app/backend/
cp -r /app/Csgo/frontend/* /app/frontend/

# Create supervisor configuration for backend
status "Setting up backend supervisor configuration"
cat > /etc/supervisor/conf.d/backend.conf << EOF
[program:backend]
command=python /app/backend/server.py
directory=/app/backend
autostart=true
autorestart=true
stderr_logfile=/var/log/supervisor/backend.err.log
stdout_logfile=/var/log/supervisor/backend.out.log
environment=PYTHONUNBUFFERED=1
EOF

# Create supervisor configuration for frontend
status "Setting up frontend supervisor configuration"
cat > /etc/supervisor/conf.d/frontend.conf << EOF
[program:frontend]
command=yarn --cwd /app/frontend start
directory=/app/frontend
autostart=true
autorestart=true
stderr_logfile=/var/log/supervisor/frontend.err.log
stdout_logfile=/var/log/supervisor/frontend.out.log
environment=NODE_ENV=development
EOF

# Create desktop shortcuts
status "Creating desktop shortcuts"

# Determine the best terminal emulator available
TERMINAL_CMD=""
if command -v gnome-terminal &> /dev/null; then
    TERMINAL_CMD="gnome-terminal --wait --"
elif command -v xterm &> /dev/null; then
    TERMINAL_CMD="xterm -e"
elif command -v konsole &> /dev/null; then
    TERMINAL_CMD="konsole -e"
elif command -v xfce4-terminal &> /dev/null; then
    TERMINAL_CMD="xfce4-terminal -e"
elif command -v lxterminal &> /dev/null; then
    TERMINAL_CMD="lxterminal -e"
else
    TERMINAL_CMD=""
    echo "Warning: No suitable terminal emulator found. Using direct execution."
fi

# Create launcher desktop entry
mkdir -p /usr/share/applications
if [ -n "$TERMINAL_CMD" ]; then
    cat > /usr/share/applications/cs2-tracker.desktop << EOF
[Desktop Entry]
Type=Application
Name=CS2 Esports Tracker
Comment=Track CS2 Esports matches and betting opportunities
Exec=${TERMINAL_CMD} /app/launcher.sh
Icon=/app/frontend/public/favicon.ico
Terminal=false
Categories=Game;Utility;
EOF
else
    cat > /usr/share/applications/cs2-tracker.desktop << EOF
[Desktop Entry]
Type=Application
Name=CS2 Esports Tracker
Comment=Track CS2 Esports matches and betting opportunities
Exec=/app/launcher.sh
Icon=/app/frontend/public/favicon.ico
Terminal=true
Categories=Game;Utility;
EOF
fi

# Create install desktop entry
if [ -n "$TERMINAL_CMD" ]; then
    cat > /usr/share/applications/cs2-tracker-install.desktop << EOF
[Desktop Entry]
Type=Application
Name=Install CS2 Esports Tracker
Comment=Install the CS2 Esports Tracker application
Exec=pkexec ${TERMINAL_CMD} /app/install.sh
Icon=/app/frontend/public/favicon.ico
Terminal=false
Categories=Game;Utility;
EOF
fi

# Create uninstall desktop entry
if [ -n "$TERMINAL_CMD" ]; then
    cat > /usr/share/applications/cs2-tracker-uninstall.desktop << EOF
[Desktop Entry]
Type=Application
Name=Uninstall CS2 Esports Tracker
Comment=Uninstall the CS2 Esports Tracker application
Exec=pkexec ${TERMINAL_CMD} /app/uninstall.sh
Icon=/app/frontend/public/favicon.ico
Terminal=false
Categories=Game;Utility;
EOF
fi

# Copy the alternative desktop entries (which try multiple terminal emulators)
mkdir -p /app/desktop-entries
cp -f /app/desktop-entries/*.desktop /usr/local/share/applications/ 2>/dev/null || true

# Reload supervisor configurations
status "Reloading supervisor configurations"
supervisorctl reread
supervisorctl update

# Start the services
status "Starting services"
if mongod --version &> /dev/null || [ -f "/etc/supervisor/conf.d/mongodb.conf" ]; then
    supervisorctl restart mongodb || true
fi
supervisorctl restart backend frontend

status "Installation complete!"
echo ""
echo "The CS2 Esports Tracker is now installed and running!"
echo "Frontend: http://localhost:3000"
echo "Backend: $(grep REACT_APP_BACKEND_URL /app/frontend/.env | cut -d'=' -f2)"
echo ""
echo "You can launch the application with: /app/launcher.sh"
echo ""
echo "Thank you for installing CS2 Esports Tracker!"
echo "========================================="

# Keep the terminal window open until the user presses a key
echo ""
echo "Press any key to close this window..."
read -n 1 -s