#!/bin/bash

# The simplest possible script that stays open
echo "This is a test script that will stay open."
echo "If you can read this message, then terminal launching works!"
echo ""
echo "Press Ctrl+C to close this window."

trap 'echo "Exiting..."; exit' INT TERM

# Keep the terminal window open
while true; do
  sleep 1
done