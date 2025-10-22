#!/bin/bash

# Activate virtual environment (if you have one)
# source venv/bin/activate

# Run Flask app in background
echo "Starting Flask app..."
python3 app.py &

# Run bot
echo "Starting Bot..."
python3 main.py
