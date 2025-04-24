#!/bin/bash

# The most basic script possible
echo "If you can see this, the script is working!"
echo "This is the basic_test.sh script."
echo "Your shell is: $SHELL"
echo "Current PATH: $PATH"

if command -v bash &> /dev/null; then
    echo "bash is available at: $(which bash)"
else
    echo "bash was not found in PATH"
fi

echo ""
echo "Press Enter to continue..."
read dummy