#!/bin/sh
set -e

# Check if requirements.txt has changed and install dependencies
if [ -f requirements.txt ]; then
  echo "Checking for new Python dependencies..."
  
  # Install dependencies if requirements.txt changed
  if [ ! -d ".venv" ] && [ requirements.txt -nt /tmp/requirements.installed ]; then
    echo "Installing Python dependencies..."
    pip install --no-cache-dir -r requirements.txt
    touch /tmp/requirements.installed
  else
    echo "Python dependencies are up to date."
  fi
fi

# Execute the main command
exec "$@"
