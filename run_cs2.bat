@echo off
echo Starting CS2 Esports Tracker...
bash -c "sudo supervisorctl start mongodb backend frontend"
echo.
echo Application should now be running!
echo Visit http://localhost:3000 in your browser.
echo.
pause