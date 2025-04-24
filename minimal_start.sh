#!/bin/sh
# Absolutely minimal starter script
sudo supervisorctl start mongodb backend frontend
echo "Application running at http://localhost:3000"
echo "Press Enter to close..."
read x