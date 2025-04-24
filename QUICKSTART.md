# CS2 Esports Tracker Quick Start Guide

## Option 1: GUI Method (Recommended)

1. Open a terminal window
2. Enter the following command:
   ```
   xterm -hold -e "/app/simple_launcher.sh" &
   ```
   If xterm is not available, try one of these alternatives:
   ```
   gnome-terminal -- bash -c "/app/simple_launcher.sh; exec bash" &
   ```
   ```
   konsole -e "bash -c '/app/simple_launcher.sh; exec bash'" &
   ```

## Option 2: Command Line Method

1. Open a terminal window
2. Enter the following command:
   ```
   sudo /app/simple_launcher.sh
   ```
   This will start the application. The terminal will stay open with status information.

## Option 3: Test Terminal Method

If you're having issues with terminals closing too quickly, try:
```
/app/launch_test.sh
```

This will open a simple test script in a terminal that will definitely stay open.

## Desktop Icons

If desktop icons aren't appearing, try:
1. Copy the icon to your desktop manually:
   ```
   cp /app/cs2-tracker.desktop ~/Desktop/
   ```
2. Then make it executable:
   ```
   chmod +x ~/Desktop/cs2-tracker.desktop
   ```

## After Starting

Once launched, you can access the application at:
- Frontend: http://localhost:3000
- Backend: Check the output in the terminal

## Troubleshooting

If the application doesn't start:
1. Check MongoDB:
   ```
   sudo supervisorctl status mongodb
   ```
2. Check backend:
   ```
   sudo supervisorctl status backend
   ```
3. Check frontend:
   ```
   sudo supervisorctl status frontend
   ```
4. Restart everything:
   ```
   sudo supervisorctl restart all
   ```

## Dependencies

This application requires:
- MongoDB
- Python 3 with pip
- Node.js and Yarn
- Supervisor

If any of these are missing, run:
```
sudo /app/install.sh
```