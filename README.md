# CS2 Esports Tracker

This application allows you to track CS2 esports matches, view predictions, calculate expected value (EV) for betting opportunities, and track your betting performance.

## Features

- View upcoming CS2 matches
- See predictions for match outcomes and scores
- Calculate EV (Expected Value) for betting opportunities
- Track bets and analyze performance

## Getting Started

### One-Click Launcher

Simply run the launcher script to start the application:

```bash
/app/launcher.sh
```

This will:
1. Start the backend server
2. Start the frontend application
3. Display the URLs where you can access the application

### Manual Start

If you prefer to start the services manually, you can use the following commands:

```bash
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

# Restart services
sudo supervisorctl restart backend
sudo supervisorctl restart frontend

# Stop services
sudo supervisorctl stop backend
sudo supervisorctl stop frontend

# Start services
sudo supervisorctl start backend
sudo supervisorctl start frontend
```

## Troubleshooting

If you encounter any issues:

1. Check the service logs:
   ```bash
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
