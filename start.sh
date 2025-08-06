#!/bin/bash
# Startup script for Pionex Trading Bot
# Copyright © 2024 Telegram-Airdrop-Bot

echo "🚀 Starting Pionex Trading Bot..."

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    echo "❌ Error: main.py not found. Please run this from the project root."
    exit 1
fi

# Check Python version
python_version=$(python3 --version 2>&1)
echo "🐍 Python version: $python_version"

# Check if required files exist
echo "📁 Checking required files..."
required_files=("main.py" "gui_app.py" "requirements.txt")
for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file found"
    else
        echo "❌ $file not found"
        exit 1
    fi
done

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p logs
mkdir -p data
mkdir -p backup

# Set permissions
echo "🔐 Setting permissions..."
chmod 755 logs/
chmod 755 data/
chmod 755 backup/

# Check environment variables
echo "🔧 Checking environment variables..."
if [ -z "$PIONEX_API_KEY" ]; then
    echo "⚠️  Warning: PIONEX_API_KEY not set"
else
    echo "✅ PIONEX_API_KEY is set"
fi

if [ -z "$PIONEX_SECRET_KEY" ]; then
    echo "⚠️  Warning: PIONEX_SECRET_KEY not set"
else
    echo "✅ PIONEX_SECRET_KEY is set"
fi

# Check if SECRET_KEY is set
if [ -z "$SECRET_KEY" ]; then
    echo "⚠️  Warning: SECRET_KEY not set, using default"
    export SECRET_KEY="default-secret-key-for-production"
fi

# Get port from environment
PORT=${PORT:-5000}
echo "🌐 Using port: $PORT"

# Start the application
echo "🚀 Starting application..."
python3 main.py 