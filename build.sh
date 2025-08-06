#!/bin/bash
# Build script for Pionex Trading Bot
# Copyright © 2024 Telegram-Airdrop-Bot

echo "Starting build process..."

# Update package list
echo "Updating package list..."
apt-get update

# Install system dependencies
echo "Installing system dependencies..."
apt-get install -y \
    libsqlite3-dev \
    python3-dev \
    build-essential \
    pkg-config

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
echo "Creating directories..."
mkdir -p logs
mkdir -p data
mkdir -p backup

# Set permissions
echo "Setting permissions..."
chmod 755 logs/
chmod 755 data/
chmod 755 backup/

echo "Build completed successfully!" 