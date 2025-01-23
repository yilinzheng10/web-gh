#!/bin/bash

# Check if the virtual environment folder exists
if [ -d "./env" ]; then
    # Activate the virtual environment
    source ./env/bin/activate
    echo "App already installed"
else
    echo "Installing app, this may take a few minutes..."
    # Create the virtual environment
    python3 -m venv env
    # Activate the virtual environment
    source ./env/bin/activate
    # Install the required packages
    pip install -r requirements.txt
    echo "App successfully installed"
fi

# Check if the local_variables.sh file exists
if [ -f "./local_variables.sh" ]; then
    # Source the local variables
    source ./local_variables.sh
fi

# Set environment variables
export FLASK_APP=server.py
export FLASK_DEBUG=1
export APP_CONFIG_FILE=settings.py

# Run the Flask application
flask run