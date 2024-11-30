#!/bin/bash

# Check if the script is being run as root
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root (sudo ./install.sh)"
  exit
fi

# Update package list and install system dependencies
echo "Installing system dependencies..."
sudo apt update
sudo apt install -y python3.12-venv binutils

# Create and activate the virtual environment
echo "Creating and activating the virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install project dependencies
echo "Installing project dependencies..."
pip install -r requirements.txt

# Run the project setup
echo "Running project setup..."
python setup.py install

# Run the build script
echo "Running build script..."
python build.py

# Move the executable to /usr/local/bin
echo "Moving the executable to /usr/local/bin..."
sudo mv dist/aichat-cli /usr/local/bin/aichat

# Finish
echo "Installation complete. You can run the program with the command 'aichat'."

# Deactivate the virtual environment
deactivate