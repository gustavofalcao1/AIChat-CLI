#!/bin/bash

# Check if the script is being run as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root (sudo ./install.sh)"
    exit 1
fi

# Function to handle errors
handle_error() {
    echo "Error: $1"
    exit 1
}

# Function to check if a command exists
check_command() {
    if ! command -v "$1" &> /dev/null; then
        handle_error "Command $1 not found. Please install it first."
    fi
}

# Update package list and install system dependencies
echo "Installing system dependencies..."
apt update || handle_error "Failed to update package list"

# Install dependences
apt install -y xclip 

# Install Python 3.10 (which is the default in Ubuntu 22.04)
apt install -y python3.10 python3.10-venv python3-pip binutils || handle_error "Failed to install Python and dependencies"

# Check if python3 is available
check_command python3

# Create and activate the virtual environment
echo "Creating virtual environment..."
python3 -m venv venv || handle_error "Failed to create virtual environment"

# Source the virtual environment
echo "Activating virtual environment..."
. venv/bin/activate || handle_error "Failed to activate virtual environment"

# Install project dependencies
echo "Installing project dependencies..."
pip install -r requirements.txt || handle_error "Failed to install project dependencies"

# Run the project setup
echo "Running project setup..."
python3 setup.py install || handle_error "Failed to run setup.py"

# Run the build script
echo "Running build script..."
python3 build.py || handle_error "Failed to run build.py"

# Move the executable to /usr/local/bin
echo "Moving the executable to /usr/local/bin..."
if [ -f "dist/aichat-cli" ]; then
    mv dist/aichat-cli /usr/local/bin/aichat || handle_error "Failed to move executable"
else
    handle_error "Executable not found in dist/aichat-cli"
fi

# Deactivate the virtual environment
deactivate

echo "Installation complete. You can run the program with the command 'aichat'."
