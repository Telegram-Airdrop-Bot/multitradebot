#!/usr/bin/env python3
"""
Pionex Trading Bot - Main Entry Point for Production
Copyright © 2024 Telegram-Airdrop-Bot
https://github.com/Telegram-Airdrop-Bot/autotradebot

Production entry point for the Pionex Trading Bot with proper
deployment settings for cloud platforms like Render.
"""

import os
import sys
import logging
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

# Configure logging for production
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('logs/app.log') if os.path.exists('logs') else logging.NullHandler()
    ]
)

logger = logging.getLogger(__name__)

def create_app():
    """Create and configure the Flask application for production"""
    try:
        from gui_app import app, socketio
        
        # Configure for production
        app.config['ENV'] = 'production'
        app.config['DEBUG'] = False
        app.config['TESTING'] = False
        
        # Ensure logs directory exists
        os.makedirs('logs', exist_ok=True)
        
        logger.info("✅ Flask application created successfully")
        return app, socketio
        
    except Exception as e:
        logger.error(f"❌ Error creating Flask application: {e}")
        raise

def main():
    """Main entry point for production deployment"""
    try:
        logger.info("🚀 Starting Pionex Trading Bot for Production...")
        
        # Check environment variables
        api_key = os.getenv('PIONEX_API_KEY')
        api_secret = os.getenv('PIONEX_SECRET_KEY')
        
        if not api_key or not api_secret:
            logger.error("❌ Missing required environment variables: PIONEX_API_KEY, PIONEX_SECRET_KEY")
            logger.info("Please set these variables in your deployment environment")
            return
        
        logger.info("✅ Environment variables check passed")
        
        # Create Flask app
        app, socketio = create_app()
        
        # Get port from environment (for Render and other cloud platforms)
        port = int(os.environ.get('PORT', 5000))
        host = '0.0.0.0'  # Bind to all interfaces for production
        
        logger.info(f"🌐 Starting server on {host}:{port}")
        
        # Start the application with production settings
        socketio.run(
            app,
            host=host,
            port=port,
            debug=False,
            allow_unsafe_werkzeug=True,
            log_output=True
        )
        
    except KeyboardInterrupt:
        logger.info("🛑 Application stopped by user")
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 