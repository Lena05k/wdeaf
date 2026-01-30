#!/bin/sh
set -e

# Check if package.json has changed and install dependencies
if [ -f package.json ]; then
  echo "Checking for new dependencies..."
  
  # Install dependencies if package.json or package-lock.json changed
  if [ ! -d "node_modules" ] || [ package.json -nt node_modules ] || [ package-lock.json -nt node_modules ]; then
    echo "Installing dependencies..."
    npm install
  else
    echo "Dependencies are up to date."
  fi
fi

# Execute the main command
exec "$@"
