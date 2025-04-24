# CS2 Esports Tracker

This application allows you to track CS2 esports matches, view predictions, calculate expected value (EV) for betting opportunities, and track your betting performance.

## Features

- View upcoming CS2 matches
- See predictions for match outcomes and scores
- Calculate EV (Expected Value) for betting opportunities
- Track bets and analyze performance

## Installation

### Automatic Installation

Run the installation script as root or with sudo:

```bash
sudo /app/install.sh
```

This script will:
1. Install all required system dependencies
2. Set up MongoDB
3. Install backend Python dependencies
4. Install frontend Node.js dependencies
5. Configure supervisor for all services
6. Create a desktop shortcut for easy access

### Manual Installation

If you prefer to install manually, you'll need:

1. MongoDB installed and running
2. Python 3 with pip
3. Node.js and Yarn
4. Supervisor for process management

Then install dependencies:

```bash
# Backend dependencies
cd /app/backend
pip install -r requirements.txt

# Frontend dependencies
cd /app/frontend
yarn install
```

## Running the Application

### One-Click Launcher

Simply run the launcher script to start the application:

```bash
/app/launcher.sh
```

This will:
1. Check if the application is installed, and run the installer if needed
2. Start MongoDB if it's not running
3. Start the backend server
4. Start the frontend application
5. Display the URLs where you can access the application

### Manual Start

If you prefer to start the services manually, you can use the following commands:

```bash
# Start MongoDB
sudo supervisorctl start mongodb

# Start the backend
sudo supervisorctl start backend

# Start the frontend
sudo supervisorctl start frontend
```

### Accessing the Application

- Frontend: http://localhost:3000
- Backend API: See the REACT_APP_BACKEND_URL in /app/frontend/.env

## Managing Services

You can manage the application services using the following supervisor commands:

```bash
# View service status
sudo supervisorctl status

# Restart all services
sudo supervisorctl restart all

# Restart individual services
sudo supervisorctl restart mongodb
sudo supervisorctl restart backend
sudo supervisorctl restart frontend

# Stop services
sudo supervisorctl stop all

# Start services
sudo supervisorctl start all
```

## Troubleshooting

If you encounter any issues:

1. Check the service logs:
   ```bash
   cat /var/log/supervisor/mongodb.err.log
   cat /var/log/supervisor/backend.err.log
   cat /var/log/supervisor/frontend.err.log
   ```

2. Restart the services:
   ```bash
   sudo supervisorctl restart all
   ```

3. Ensure MongoDB is running:
   ```bash
   sudo supervisorctl status mongodb
   ```

4. Re-run the installation script:
   ```bash
   sudo /app/install.sh
   ```
