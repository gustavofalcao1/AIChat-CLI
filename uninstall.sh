#!/bin/bash

# Check if the script is being run as root
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root (sudo ./uninstall.sh)"
  exit
fi

# Remove the executable from /usr/local/bin
echo "Removing the executable from /usr/local/bin..."
sudo rm -f /usr/local/bin/aichat

# Remove the virtual environment
echo "Removing the virtual environment..."
rm -rf venv

# Remove the configuration and data files
echo "Removing configuration and data files..."
rm -rf ~/.aichat

# Finish
echo "Uninstallation complete."