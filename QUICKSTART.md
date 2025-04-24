# CS2 Esports Tracker Quick Start Guide

## When You See "Command Not Found" Error

If you're getting "command not found" when running the scripts, try these alternatives:

## Option 1: Use the START_HERE.sh Script (Recommended)

1. Open a terminal window
2. Run this command:
   ```
   sh /app/START_HERE.sh
   ```
   This uses `sh` which should be available on all systems.

## Option 2: Minimal Start (Most Compatible)

1. Open a terminal window
2. Run this command:
   ```
   sh /app/minimal_start.sh
   ```

## Option 3: Start Directly with Supervisor

1. Open a terminal window
2. Run these commands:
   ```
   sudo supervisorctl start mongodb
   sudo supervisorctl start backend
   sudo supervisorctl start frontend
   ```

## Option 4: HTML Instructions

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