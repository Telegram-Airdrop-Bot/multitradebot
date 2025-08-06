#!/usr/bin/env python3
"""
Pionex Trading Bot - Web GUI Application
Copyright © 2024 Telegram-Airdrop-Bot
https://github.com/Telegram-Airdrop-Bot/autotradebot

A comprehensive web-based GUI for the Pionex Trading Bot with real-time
market data, automated trading, and advanced analytics.

This software is provided "as is" without warranty. Trading involves
significant financial risk. Use at your own risk.
"""

import os
import sys
import logging
import threading
import time
import json
from datetime import datetime
from pathlib import Path
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_socketio import SocketIO, emit
import webbrowser
from dotenv import load_dotenv
import traceback

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config_loader import get_config, reload_config
from pionex_api import PionexAPI
from trading_strategies import TradingStrategies

# Try to import database - fallback to simple database if SQLite is not available
try:
    from database import Database
    logger.info("Using SQLite database")
except ImportError as e:
    logger.warning(f"SQLite database not available: {e}")
    logger.info("Using simple JSON-based database")
    from simple_database import SimpleDatabase as Database

from auto_trader import get_auto_trader, start_auto_trading, stop_auto_trading, restart_auto_trading, get_auto_trading_status
from futures_trading import (
    get_futures_trader, create_futures_grid, create_hedging_grid,
    get_dynamic_limits, check_liquidation_risk, get_strategy_status,
    get_performance_metrics
)
from backtesting import (
    run_backtest, enable_paper_trading, disable_paper_trading, get_paper_trading_ledger
)
from pionex_ws import PionexWebSocket

# Load environment variables
load_dotenv()

# Configure Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
app.config['ENV'] = 'production'
app.config['DEBUG'] = False
app.config['TESTING'] = False

# Configure SocketIO
socketio = SocketIO(app, cors_allowed_origins="*", logger=True, engineio_logger=True)

# Error handling middleware
@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    return jsonify({
        'error': 'Internal server error',
        'message': 'Something went wrong on our end',
        'timestamp': datetime.now().isoformat()
    }), 500

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({
        'error': 'Not found',
        'message': 'The requested resource was not found',
        'timestamp': datetime.now().isoformat()
    }), 404

@app.errorhandler(Exception)
def handle_exception(e):
    logger.error(f"Unhandled exception: {e}")
    logger.error(f"Traceback: {traceback.format_exc()}")
    return jsonify({
        'error': 'Server error',
        'message': 'An unexpected error occurred',
        'timestamp': datetime.now().isoformat()
    }), 500

# Configure logging
config = get_config()
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=getattr(logging, config.get('logging', {}).get('level', 'INFO'))
)
logger = logging.getLogger(__name__)

class TradingBotGUI:
    def __init__(self):
        self.api = PionexAPI()
        self.strategies = TradingStrategies(self.api)
        self.db = Database()
        self.config = get_config()
        
        # Initialize WebSocket for real-time data
        self.ws = None
        self.ws_connected = False
        self.real_time_data = {}
        self.ws_thread = None
        
        # Start WebSocket connection
        self._start_websocket()
        
        # Auto trading status
        self.auto_trading_enabled = False
        self.current_user = None
    
    def check_auth(self, user_id: str) -> bool:
        """Check if user is authorized"""
        allowed_users = self.config.get('allowed_users', [])
        return str(user_id) in allowed_users or not allowed_users
    
    def get_account_balance(self):
        """Get account balance"""
        try:
            balance = self.api.get_account_balance()
            return {'success': True, 'data': balance}
        except Exception as e:
            logger.error(f"Error getting balance: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_positions(self):
        """Get current positions"""
        try:
            positions_response = self.api.get_positions()
            
            if 'error' in positions_response:
                return {'success': False, 'error': positions_response['error']}
            
            # Convert the response to a list format expected by the GUI
            positions = []
            balances = positions_response.get('data', {}).get('balances', [])
            
            for balance in balances:
                if float(balance.get('total', 0)) > 0:
                    positions.append({
                        'symbol': balance.get('currency', ''),
                        'size': float(balance.get('total', 0)),
                        'entryPrice': 0,  # Not available in balance response
                        'markPrice': 0,   # Not available in balance response
                        'unrealizedPnl': 0,  # Not available in balance response
                        'roe': 0,  # Not available in balance response
                        'notional': float(balance.get('total', 0))
                    })
            
            return {'success': True, 'data': positions}
        except Exception as e:
            logger.error(f"Error getting positions: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_portfolio(self):
        """Get portfolio information"""
        try:
            balance = self.api.get_account_balance()
            positions_response = self.api.get_positions()
            
            if 'error' in balance:
                return {'success': False, 'error': balance['error']}
            
            if 'error' in positions_response:
                return {'success': False, 'error': positions_response['error']}
            
            # Calculate portfolio metrics
            total_value = 0
            total_pnl = 0
            
            # Process positions from balance data
            balances = positions_response.get('data', {}).get('balances', [])
            positions = []
            
            for balance_item in balances:
                if float(balance_item.get('total', 0)) > 0:
                    notional = float(balance_item.get('total', 0))
                    total_value += notional
                    
                    position = {
                        'symbol': balance_item.get('currency', ''),
                        'size': float(balance_item.get('total', 0)),
                        'notional': notional,
                        'unrealizedPnl': 0  # Not available in balance response
                    }
                    positions.append(position)
            
            portfolio = {
                'balance': balance,
                'positions': positions,
                'total_value': total_value,
                'total_pnl': total_pnl,
                'timestamp': datetime.now().isoformat()
            }
            
            return {'success': True, 'data': portfolio}
        except Exception as e:
            logger.error(f"Error getting portfolio: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_trading_history(self):
        """Get trading history"""
        try:
            # Get recent trades from database
            trades = self.db.get_recent_trades(limit=50)
            return {'success': True, 'data': trades}
        except Exception as e:
            logger.error(f"Error getting trading history: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_settings(self):
        """Get current settings"""
        try:
            settings = {
                'trading_pair': self.config.get('trading_pair'),
                'position_size': self.config.get('position_size'),
                'leverage': self.config.get('leverage'),
                'trading_amount': self.config.get('trading_amount', 100),
                'max_daily_loss': self.config.get('max_daily_loss', 500),
                'rsi': self.config.get('rsi', {}),
                'volume_filter': self.config.get('volume_filter', {}),
                'macd': self.config.get('macd', {}),
                'stop_loss_percentage': self.config.get('stop_loss_percentage'),
                'take_profit_percentage': self.config.get('take_profit_percentage'),
                'trailing_stop_percentage': self.config.get('trailing_stop_percentage'),
                'trading_hours': self.config.get('trading_hours', {}),
                'notifications': self.config.get('notifications', {}),
                'auto_trading_enabled': self.auto_trading_enabled
            }
            return {'success': True, 'data': settings}
        except Exception as e:
            logger.error(f"Error getting settings: {e}")
            return {'success': False, 'error': str(e)}
    
    def update_settings(self, new_settings):
        """Update settings"""
        try:
            # Handle strategy update separately
            if 'default_strategy' in new_settings:
                strategy_name = new_settings['default_strategy']
                # Update user settings in database
                if self.current_user:
                    self.db.update_user_setting(self.current_user, 'default_strategy', strategy_name)
                # Update config
                self.config['default_strategy'] = strategy_name
            
            # Handle trading hours settings
            if 'trading_hours' in new_settings:
                trading_hours = new_settings['trading_hours']
                self.config['trading_hours'] = {
                    'enabled': trading_hours.get('enabled', True),
                    'start': trading_hours.get('start', '19:30'),
                    'end': trading_hours.get('end', '01:30'),
                    'timezone': trading_hours.get('timezone', 'UTC-5'),
                    'exclude_weekends': trading_hours.get('exclude_weekends', False),
                    'exclude_holidays': trading_hours.get('exclude_holidays', False)
                }
            
            # Handle notification settings
            if 'notifications' in new_settings:
                notifications = new_settings['notifications']
                self.config['notifications'] = {
                    'telegram': {
                        'enabled': notifications.get('telegram_enabled', False),
                        'bot_token': notifications.get('telegram_token', ''),
                        'user_id': notifications.get('telegram_user_id', '')
                    },
                    'email': {
                        'enabled': notifications.get('email_enabled', False),
                        'recipient_email': notifications.get('notification_email', ''),
                        'sender_email': notifications.get('sender_email', ''),
                        'sender_password': notifications.get('sender_password', ''),
                        'smtp_server': notifications.get('smtp_server', 'smtp.gmail.com'),
                        'smtp_port': 587
                    },
                    'types': {
                        'trade_notifications': notifications.get('notify_trades', True),
                        'error_notifications': notifications.get('notify_errors', True),
                        'balance_notifications': notifications.get('notify_balance', True),
                        'status_notifications': notifications.get('notify_status', True)
                    }
                }
            
            # Handle RSI parameters
            if 'rsi_settings' in new_settings:
                rsi_settings = new_settings['rsi_settings']
                if 'rsi' not in self.config:
                    self.config['rsi'] = {}
                self.config['rsi'].update({
                    'period': int(rsi_settings.get('period', 7)),
                    'overbought': int(rsi_settings.get('overbought', 70)),
                    'oversold': int(rsi_settings.get('oversold', 30))
                })
            
            # Update other config settings
            for key, value in new_settings.items():
                if key not in ['default_strategy', 'trading_hours', 'notifications', 'rsi_settings'] and key in self.config:
                    if isinstance(self.config[key], dict) and isinstance(value, dict):
                        self.config[key].update(value)
                    else:
                        self.config[key] = value
            
            # Add new settings that might not exist in config
            new_config_keys = ['trading_amount', 'max_daily_loss', 'trailing_stop_percentage']
            for key in new_config_keys:
                if key in new_settings:
                    self.config[key] = new_settings[key]
            
            # Save to config file
            import yaml
            with open('config.yaml', 'w') as f:
                yaml.dump(self.config, f, default_flow_style=False)
            
            # Reload config
            reload_config()
            
            logger.info(f"Settings updated successfully: {list(new_settings.keys())}")
            return {'success': True, 'message': 'Settings updated successfully'}
        except Exception as e:
            logger.error(f"Error updating settings: {e}")
            return {'success': False, 'error': str(e)}
    
    def enable_auto_trading(self):
        """Enable auto trading"""
        try:
            # Check balance before enabling auto trading
            balance_response = self.get_account_balance()
            if not balance_response['success']:
                return {'success': False, 'error': 'Failed to check account balance'}
            
            balance_data = balance_response['data']
            available_balance = float(balance_data.get('available', 0))
            
            if available_balance <= 0:
                return {
                    'success': False, 
                    'error': 'Cannot enable auto trading with zero balance. Please add funds to your account.'
                }
            
            # Check if balance is too low for meaningful trading
            if available_balance < 10:  # Minimum $10 for auto trading
                return {
                    'success': False, 
                    'error': f'Balance too low for auto trading. Available: ${available_balance:.2f}, Minimum required: $10.00'
                }
            
            self.auto_trading_enabled = True
            start_auto_trading(self.current_user or 1)
            return {'success': True, 'message': 'Auto trading enabled'}
        except Exception as e:
            logger.error(f"Error enabling auto trading: {e}")
            return {'success': False, 'error': str(e)}
    
    def disable_auto_trading(self):
        """Disable auto trading"""
        try:
            self.auto_trading_enabled = False
            stop_auto_trading(self.current_user or 1)
            return {'success': True, 'message': 'Auto trading disabled'}
        except Exception as e:
            logger.error(f"Error disabling auto trading: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_auto_trading_status(self):
        """Get auto trading status"""
        try:
            status = get_auto_trading_status(self.current_user or 1)
            return {'success': True, 'data': status}
        except Exception as e:
            logger.error(f"Error getting auto trading status: {e}")
            return {'success': False, 'error': str(e)}
    
    def execute_manual_trade(self, symbol, side, quantity, order_type='MARKET', price=None):
        """Execute manual trade"""
        try:
            # First check account balance
            balance_response = self.get_account_balance()
            if not balance_response['success']:
                return {'success': False, 'error': 'Failed to check account balance'}
            
            balance_data = balance_response['data']
            available_balance = float(balance_data.get('available', 0))
            
            # Calculate required amount for the trade
            if side == 'BUY':
                # For buying, we need USDT balance
                if 'USDT' not in symbol:
                    return {'success': False, 'error': 'Only USDT pairs are supported for buying'}
                
                # Get current price to calculate required USDT
                ticker_response = self.api.get_ticker_price(symbol)
                if 'error' in ticker_response:
                    return {'success': False, 'error': f'Failed to get price for {symbol}'}
                
                current_price = float(ticker_response['data']['price'])
                required_usdt = quantity * current_price
                
                if available_balance < required_usdt:
                    return {
                        'success': False, 
                        'error': f'Insufficient USDT balance. Required: ${required_usdt:.2f}, Available: ${available_balance:.2f}'
                    }
            
            elif side == 'SELL':
                # For selling, check if we have enough of the asset
                asset_symbol = symbol.replace('USDT', '')  # e.g., BTC from BTCUSDT
                positions_response = self.get_positions()
                
                if positions_response['success']:
                    positions = positions_response['data']
                    asset_balance = 0
                    
                    for position in positions:
                        if position['symbol'] == asset_symbol:
                            asset_balance = float(position['size'])
                            break
                    
                    if asset_balance < quantity:
                        return {
                            'success': False, 
                            'error': f'Insufficient {asset_symbol} balance. Required: {quantity}, Available: {asset_balance}'
                        }
                else:
                    return {'success': False, 'error': 'Failed to check asset balance'}
            
            # If balance check passes, proceed with the trade
            if order_type == 'MARKET':
                order = self.api.place_market_order(symbol, side, quantity)
            elif order_type == 'LIMIT':
                order = self.api.place_limit_order(symbol, side, quantity, price)
            else:
                return {'success': False, 'error': 'Invalid order type'}
            
            return {'success': True, 'data': order}
        except Exception as e:
            logger.error(f"Error executing trade: {e}")
            return {'success': False, 'error': str(e)}
    
    def validate_trade_requirements(self, symbol, side, quantity, order_type='MARKET', price=None):
        """Validate trade requirements before execution"""
        try:
            # Check account balance
            balance_response = self.get_account_balance()
            if not balance_response['success']:
                return {'valid': False, 'error': 'Failed to check account balance'}
            
            balance_data = balance_response['data']
            available_balance = float(balance_data.get('available', 0))
            
            validation_result = {
                'valid': True,
                'warnings': [],
                'estimated_cost': 0,
                'available_balance': available_balance
            }
            
            if side == 'BUY':
                # Get current price for cost estimation
                ticker_response = self.api.get_ticker_price(symbol)
                if 'error' in ticker_response:
                    return {'valid': False, 'error': f'Failed to get price for {symbol}'}
                
                current_price = float(ticker_response['data']['price'])
                estimated_cost = quantity * current_price
                validation_result['estimated_cost'] = estimated_cost
                
                if available_balance < estimated_cost:
                    validation_result['valid'] = False
                    validation_result['error'] = f'Insufficient USDT balance. Required: ${estimated_cost:.2f}, Available: ${available_balance:.2f}'
                    return validation_result
                
                # Add warnings for large trades
                if estimated_cost > available_balance * 0.8:
                    validation_result['warnings'].append(f'This trade will use {((estimated_cost/available_balance)*100):.1f}% of your available balance')
                
            elif side == 'SELL':
                # Check asset balance for selling
                asset_symbol = symbol.replace('USDT', '')
                positions_response = self.get_positions()
                
                if positions_response['success']:
                    positions = positions_response['data']
                    asset_balance = 0
                    
                    for position in positions:
                        if position['symbol'] == asset_symbol:
                            asset_balance = float(position['size'])
                            break
                    
                    if asset_balance < quantity:
                        validation_result['valid'] = False
                        validation_result['error'] = f'Insufficient {asset_symbol} balance. Required: {quantity}, Available: {asset_balance}'
                        return validation_result
                else:
                    validation_result['valid'] = False
                    validation_result['error'] = 'Failed to check asset balance'
                    return validation_result
            
            return validation_result
            
        except Exception as e:
            logger.error(f"Error validating trade requirements: {e}")
            return {'valid': False, 'error': str(e)}
    
    def get_technical_analysis(self, symbol):
        """Get technical analysis for symbol"""
        try:
            # Convert symbol format for Pionex API (e.g., BTCUSDT -> BTC_USDT)
            # Handle both BTCUSDT and BTC_USDT formats
            if 'USDT' in symbol and '_' not in symbol:
                formatted_symbol = symbol.replace('USDT', '_USDT')
            else:
                formatted_symbol = symbol
            
            # Try to get market data from klines first
            market_data = self.strategies.get_market_data(formatted_symbol)
            
            if market_data.empty:
                # Fallback to basic ticker data if klines fail
                ticker_response = self.api.get_ticker_price(formatted_symbol)
                if 'data' in ticker_response and 'price' in ticker_response['data']:
                    current_price = float(ticker_response['data']['price'])
                    analysis = {
                        'symbol': symbol,
                        'current_price': current_price,
                        'rsi': 50.0,  # Neutral RSI when no historical data
                        'macd': {
                            'line': 0,
                            'signal': 0,
                            'histogram': 0
                        },
                        'bollinger_bands': {
                            'upper': current_price * 1.02,  # 2% above
                            'middle': current_price,
                            'lower': current_price * 0.98   # 2% below
                        },
                        'timestamp': datetime.now().isoformat(),
                        'note': 'Basic analysis using ticker data only'
                    }
                    return {'success': True, 'data': analysis}
                else:
                    return {'success': False, 'error': f"Could not get price data for {symbol}"}
            
            # Calculate indicators from klines data
            prices = market_data['close'].tolist()
            rsi = self.strategies.calculate_rsi(prices)
            macd_line, macd_signal, macd_histogram = self.strategies.calculate_macd(prices)
            bb_upper, bb_middle, bb_lower = self.strategies.calculate_bollinger_bands(prices)
            
            analysis = {
                'symbol': symbol,
                'current_price': prices[-1] if prices else 0,
                'rsi': rsi[-1] if rsi else 50,
                'macd': {
                    'line': macd_line[-1] if macd_line else 0,
                    'signal': macd_signal[-1] if macd_signal else 0,
                    'histogram': macd_histogram[-1] if macd_histogram else 0
                },
                'bollinger_bands': {
                    'upper': bb_upper[-1] if bb_upper else 0,
                    'middle': bb_middle[-1] if bb_middle else 0,
                    'lower': bb_lower[-1] if bb_lower else 0
                },
                'timestamp': datetime.now().isoformat()
            }
            
            return {'success': True, 'data': analysis}
        except Exception as e:
            logger.error(f"Error getting technical analysis: {e}")
            return {'success': False, 'error': str(e)}
    
    def _start_websocket(self):
        """Start WebSocket connection for real-time data"""
        try:
            self.ws = PionexWebSocket()
            self.ws_connected = True
            logger.info("WebSocket connection started")
        except Exception as e:
            logger.error(f"Error starting WebSocket: {e}")
            self.ws_connected = False

    def get_real_time_price(self, symbol: str) -> float:
        """Get real-time price for a symbol"""
        try:
            return self.api.get_real_time_price(symbol)
        except Exception as e:
            logger.error(f"Error getting real-time price for {symbol}: {e}")
            return 0.0

    def get_current_strategy(self):
        """Get current active strategy"""
        try:
            # Get strategy from user settings or config
            user_settings = self.db.get_user_settings(self.current_user) if self.current_user else {}
            current_strategy = user_settings.get('default_strategy', 'ADVANCED_STRATEGY')
            
            # Get strategy descriptions
            strategy_descriptions = {
                'RSI_STRATEGY': 'Uses RSI indicator for entry/exit signals. Good for trending markets.',
                'VOLUME_FILTER_STRATEGY': 'Combines volume analysis with price action. Filters out low-volume periods.',
                'ADVANCED_STRATEGY': 'Multi-indicator approach with RSI, MACD, Volume, Candlestick patterns, OBV, and Support/Resistance analysis. Includes dynamic SL/TP.',
                'GRID_TRADING_STRATEGY': 'Places buy/sell orders at regular intervals. Good for range-bound markets.',
                'DCA_STRATEGY': 'Dollar Cost Averaging approach. Buys more when price drops.'
            }
            
            return {
                'success': True,
                'data': {
                    'current_strategy': current_strategy,
                    'available_strategies': list(strategy_descriptions.keys()),
                    'descriptions': strategy_descriptions,
                    'status': 'active' if self.auto_trading_enabled else 'inactive'
                }
            }
        except Exception as e:
            logger.error(f"Error getting current strategy: {e}")
            return {'success': False, 'error': str(e)}
    
    def update_strategy(self, strategy_name: str):
        """Update the active trading strategy"""
        try:
            # Validate strategy name
            valid_strategies = [
                'RSI_STRATEGY',
                'VOLUME_FILTER_STRATEGY', 
                'ADVANCED_STRATEGY',
                'GRID_TRADING_STRATEGY',
                'DCA_STRATEGY'
            ]
            
            if strategy_name not in valid_strategies:
                return {'success': False, 'error': f'Invalid strategy: {strategy_name}'}
            
            # Update user settings
            if self.current_user:
                self.db.update_user_setting(self.current_user, 'default_strategy', strategy_name)
            
            # Update config
            self.config['default_strategy'] = strategy_name
            
            # Save config
            import yaml
            with open('config.yaml', 'w') as f:
                yaml.dump(self.config, f, default_flow_style=False)
            
            logger.info(f"Strategy updated to: {strategy_name}")
            return {'success': True, 'message': f'Strategy updated to {strategy_name}'}
            
        except Exception as e:
            logger.error(f"Error updating strategy: {e}")
            return {'success': False, 'error': str(e)}
    
    def test_strategy(self, strategy_name: str, symbol: str = None):
        """Test a trading strategy with current market data"""
        try:
            if not symbol:
                symbol = self.config.get('trading_pair', 'BTC_USDT')
            
            # Convert symbol format for Pionex API (BTCUSDT -> BTC_USDT)
            formatted_symbol = symbol
            if 'USDT' in symbol and '_' not in symbol:
                formatted_symbol = symbol.replace('USDT', '_USDT')
            elif 'USDC' in symbol and '_' not in symbol:
                formatted_symbol = symbol.replace('USDC', '_USDC')
            elif 'BUSD' in symbol and '_' not in symbol:
                formatted_symbol = symbol.replace('BUSD', '_BUSD')
            
            # Get current balance for strategy testing
            balance_response = self.get_account_balance()
            if not balance_response['success']:
                return {'success': False, 'error': 'Failed to get account balance for strategy testing'}
            
            balance = float(balance_response['data'].get('available', 0))
            
            # Get market data with correct symbol format
            df = self.strategies.get_market_data(formatted_symbol, '5M', 100)
            if df.empty:
                return {'success': False, 'error': 'No market data available for testing'}
            
            # Test the strategy with balance parameter
            if strategy_name == 'RSI_STRATEGY':
                signal = self.strategies.rsi_strategy(formatted_symbol, balance)
            elif strategy_name == 'VOLUME_FILTER_STRATEGY':
                signal = self.strategies.volume_filter_strategy(formatted_symbol, balance)
            elif strategy_name == 'ADVANCED_STRATEGY':
                signal = self.strategies.advanced_strategy(formatted_symbol, balance)
            elif strategy_name == 'GRID_TRADING_STRATEGY':
                signal = self.strategies.grid_trading_strategy(formatted_symbol, balance)
            elif strategy_name == 'DCA_STRATEGY':
                signal = self.strategies.dca_strategy(formatted_symbol, balance)
            else:
                return {'success': False, 'error': f'Unknown strategy: {strategy_name}'}
            
            # Format test results
            test_result = {
                'strategy': strategy_name,
                'symbol': symbol,
                'formatted_symbol': formatted_symbol,
                'signal': signal,
                'market_data_points': len(df),
                'current_price': float(df['close'].iloc[-1]) if not df.empty else 0,
                'balance': balance,
                'timestamp': datetime.now().isoformat()
            }
            
            return {'success': True, 'data': test_result}
            
        except Exception as e:
            logger.error(f"Error testing strategy {strategy_name}: {e}")
            return {'success': False, 'error': str(e)}

# Initialize trading bot
trading_bot = TradingBotGUI()

# Routes
@app.route('/')
def index():
    """Main dashboard"""
    return render_template('index.html')

@app.route('/health')
def health_check():
    """Health check endpoint for deployment platforms"""
    try:
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0'
        })
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/health')
def api_health():
    """API health check"""
    try:
        # Test basic functionality
        api_key = os.getenv('PIONEX_API_KEY')
        api_secret = os.getenv('PIONEX_SECRET_KEY')
        
        health_status = {
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'environment': {
                'api_key_set': bool(api_key),
                'api_secret_set': bool(api_secret),
                'flask_env': app.config.get('ENV', 'unknown'),
                'debug_mode': app.config.get('DEBUG', False)
            }
        }
        
        return jsonify(health_status)
    except Exception as e:
        logger.error(f"API health check error: {e}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/balance')
def api_balance():
    """API endpoint for balance"""
    result = trading_bot.get_account_balance()
    return jsonify(result)

@app.route('/api/positions')
def api_positions():
    """API endpoint for positions"""
    result = trading_bot.get_positions()
    return jsonify(result)

@app.route('/api/portfolio')
def api_portfolio():
    """API endpoint for portfolio"""
    result = trading_bot.get_portfolio()
    return jsonify(result)

@app.route('/api/history')
def api_history():
    """API endpoint for trading history"""
    result = trading_bot.get_trading_history()
    return jsonify(result)

@app.route('/api/settings')
def api_settings():
    """API endpoint for settings"""
    result = trading_bot.get_settings()
    return jsonify(result)

@app.route('/api/settings', methods=['POST'])
def api_update_settings():
    """API endpoint for updating settings"""
    data = request.get_json()
    result = trading_bot.update_settings(data)
    return jsonify(result)

@app.route('/api/auto-trading/enable', methods=['POST'])
def api_enable_auto_trading():
    """API endpoint for enabling auto trading"""
    result = trading_bot.enable_auto_trading()
    return jsonify(result)

@app.route('/api/auto-trading/disable', methods=['POST'])
def api_disable_auto_trading():
    """API endpoint for disabling auto trading"""
    result = trading_bot.disable_auto_trading()
    return jsonify(result)

@app.route('/api/auto-trading/status')
def api_auto_trading_status():
    """API endpoint for auto trading status"""
    result = trading_bot.get_auto_trading_status()
    return jsonify(result)

@app.route('/api/trade', methods=['POST'])
def api_trade():
    """API endpoint for manual trading"""
    data = request.get_json()
    symbol = data.get('symbol')
    side = data.get('side')
    quantity = data.get('quantity')
    order_type = data.get('order_type', 'MARKET')
    price = data.get('price')
    
    result = trading_bot.execute_manual_trade(symbol, side, quantity, order_type, price)
    return jsonify(result)

@app.route('/api/trade/validate', methods=['POST'])
def api_validate_trade():
    """API endpoint for trade validation"""
    data = request.get_json()
    symbol = data.get('symbol')
    side = data.get('side')
    quantity = data.get('quantity')
    order_type = data.get('order_type', 'MARKET')
    price = data.get('price')
    
    result = trading_bot.validate_trade_requirements(symbol, side, quantity, order_type, price)
    return jsonify(result)

@app.route('/api/analysis/<symbol>')
def api_analysis(symbol):
    """API endpoint for technical analysis"""
    result = trading_bot.get_technical_analysis(symbol)
    return jsonify(result)

@app.route('/api/chart-data/<symbol>')
def api_chart_data(symbol):
    """Get chart data for a symbol"""
    try:
        # Get timeframe from query parameter
        timeframe = request.args.get('timeframe', '5M')
        
        # Convert symbol format for Pionex API (BTCUSDT -> BTC_USDT)
        formatted_symbol = symbol
        if 'USDT' in symbol and '_' not in symbol:
            formatted_symbol = symbol.replace('USDT', '_USDT')
        elif 'USDC' in symbol and '_' not in symbol:
            formatted_symbol = symbol.replace('USDC', '_USDC')
        elif 'BUSD' in symbol and '_' not in symbol:
            formatted_symbol = symbol.replace('BUSD', '_BUSD')
        
        logger.info(f"Fetching chart data for symbol: {symbol} -> {formatted_symbol} with timeframe: {timeframe}")
        
        # Try multiple intervals to get the best data, starting with requested timeframe
        intervals_to_try = [timeframe, '5M', '1M', '15M', '1H']
        klines_data = []
        successful_interval = None
        
        for interval in intervals_to_try:
            try:
                logger.info(f"Trying interval {interval} for {formatted_symbol}")
                klines_response = trading_bot.api.get_klines(
                    symbol=formatted_symbol,
                    interval=interval,
                    limit=100
                )
                
                logger.info(f"Klines response for {formatted_symbol} with interval {interval}: {klines_response}")
                
                # Check for API errors
                if 'error' in klines_response:
                    logger.warning(f"API error for {formatted_symbol} with interval {interval}: {klines_response['error']}")
                    continue
                
                # Check for code 0 (success) or other success indicators
                if 'code' in klines_response and klines_response['code'] == 0:
                    logger.info(f"API returned code 0 for {formatted_symbol} with interval {interval}")
                    # This is a successful response, but we need to extract data
                    if 'data' in klines_response:
                        if isinstance(klines_response['data'], dict) and 'klines' in klines_response['data']:
                            klines_data = klines_response['data']['klines']
                        elif isinstance(klines_response['data'], list):
                            klines_data = klines_response['data']
                        successful_interval = interval
                        break
                
                # Handle different response formats
                if 'data' in klines_response:
                    if isinstance(klines_response['data'], dict) and 'klines' in klines_response['data']:
                        klines_data = klines_response['data']['klines']
                    elif isinstance(klines_response['data'], list):
                        klines_data = klines_response['data']
                
                if klines_data:
                    logger.info(f"Successfully got {len(klines_data)} data points with interval {interval}")
                    successful_interval = interval
                    break
                        
            except Exception as e:
                logger.warning(f"Failed to get klines with interval {interval}: {e}")
                continue
        
        if not klines_data:
            logger.warning(f"No klines data received for {formatted_symbol} with any interval")
            # Try to get basic ticker data as fallback
            try:
                ticker_response = trading_bot.api.get_ticker_price(formatted_symbol)
                logger.info(f"Ticker response as fallback: {ticker_response}")
                if 'data' in ticker_response and 'price' in ticker_response['data']:
                    current_price = float(ticker_response['data']['price'])
                    # Create sample chart data
                    import time
                    current_time = int(time.time() * 1000)
                    sample_data = {
                        'labels': ['Current'],
                        'prices': [current_price],
                        'volumes': [0],
                        'timestamps': [current_time],
                        'high': [current_price],
                        'low': [current_price],
                        'open': [current_price],
                        'timeframe': '1M'
                    }
                    return jsonify({
                        'success': True,
                        'data': sample_data,
                        'symbol': symbol,
                        'formatted_symbol': formatted_symbol,
                        'note': 'Using ticker data as fallback'
                    })
            except Exception as e:
                logger.error(f"Failed to get ticker data as fallback: {e}")
            
            return jsonify({'success': False, 'error': 'No data available for this symbol'})
        
        # Process klines data for chart
        chart_data = {
            'labels': [],
            'prices': [],
            'volumes': [],
            'timestamps': [],
            'high': [],
            'low': [],
            'open': [],
            'timeframe': successful_interval  # Use the successful interval
        }
        
        for kline in klines_data:
            try:
                # Handle different kline formats
                if len(kline) >= 6:
                    timestamp = int(kline[0])  # Open time
                    open_price = float(kline[1])
                    high_price = float(kline[2])
                    low_price = float(kline[3])
                    close_price = float(kline[4])
                    volume = float(kline[5])
                    
                    # Use close price for the main chart
                    chart_data['prices'].append(close_price)
                    chart_data['volumes'].append(volume)
                    chart_data['timestamps'].append(timestamp)
                    chart_data['high'].append(high_price)
                    chart_data['low'].append(low_price)
                    chart_data['open'].append(open_price)
                    
                    # Format time for labels
                    from datetime import datetime
                    time_obj = datetime.fromtimestamp(timestamp / 1000)
                    chart_data['labels'].append(time_obj.strftime('%H:%M'))
                    
            except (IndexError, ValueError, TypeError) as e:
                logger.warning(f"Error processing kline data: {e}")
                continue
        
        if not chart_data['prices']:
            logger.error(f"No valid chart data processed for {symbol}")
            return jsonify({'success': False, 'error': 'Failed to process chart data'})
        
        logger.info(f"Successfully processed {len(chart_data['prices'])} data points for {symbol}")
        
        return jsonify({
            'success': True, 
            'data': chart_data,
            'symbol': symbol,
            'formatted_symbol': formatted_symbol,
            'timeframe': chart_data['timeframe']
        })
        
    except Exception as e:
        logger.error(f"Error getting chart data for {symbol}: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/market-data/<symbol>')
def api_market_data(symbol):
    """Get real-time market data for a symbol"""
    try:
        market_data = trading_bot.api.get_real_time_market_data(symbol)
        
        if 'error' in market_data:
            return jsonify({'success': False, 'error': market_data['error']})
        
        return jsonify({
            'success': True,
            'data': market_data
        })
        
    except Exception as e:
        logger.error(f"Error getting market data for {symbol}: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/live-trades/<symbol>')
def api_live_trades(symbol):
    """Get live trades for a symbol"""
    try:
        limit = request.args.get('limit', 50, type=int)
        trades_data = trading_bot.api.get_live_trades(symbol, limit)
        
        if 'error' in trades_data:
            return jsonify({'success': False, 'error': trades_data['error']})
        
        return jsonify({
            'success': True,
            'data': trades_data
        })
        
    except Exception as e:
        logger.error(f"Error getting live trades for {symbol}: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/market-depth/<symbol>')
def api_market_depth(symbol):
    """Get market depth (order book) for a symbol"""
    try:
        limit = request.args.get('limit', 20, type=int)
        depth_data = trading_bot.api.get_market_depth(symbol, limit)
        
        if 'error' in depth_data:
            return jsonify({'success': False, 'error': depth_data['error']})
        
        return jsonify({
            'success': True,
            'data': depth_data
        })
        
    except Exception as e:
        logger.error(f"Error getting market depth for {symbol}: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/real-time-price/<symbol>')
def api_real_time_price(symbol):
    """Get real-time price for a symbol"""
    try:
        price = trading_bot.api.get_real_time_price(symbol)
        
        return jsonify({
            'success': True,
            'data': {
                'symbol': symbol,
                'price': price,
                'timestamp': int(time.time() * 1000)
            }
        })
        
    except Exception as e:
        logger.error(f"Error getting real-time price for {symbol}: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/24hr-ticker/<symbol>')
def api_24hr_ticker(symbol):
    """Get 24-hour ticker statistics"""
    try:
        ticker_data = trading_bot.api.get_24hr_ticker(symbol)
        
        if 'error' in ticker_data:
            return jsonify({'success': False, 'error': ticker_data['error']})
        
        return jsonify({
            'success': True,
            'data': ticker_data
        })
        
    except Exception as e:
        logger.error(f"Error getting 24hr ticker for {symbol}: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/strategy', methods=['GET'])
def api_get_strategy():
    """API endpoint for getting current strategy"""
    result = trading_bot.get_current_strategy()
    return jsonify(result)

@app.route('/api/strategy', methods=['POST'])
def api_update_strategy():
    """API endpoint for updating strategy"""
    data = request.get_json()
    strategy_name = data.get('strategy')
    
    if not strategy_name:
        return jsonify({'success': False, 'error': 'Strategy name is required'})
    
    result = trading_bot.update_strategy(strategy_name)
    return jsonify(result)

@app.route('/api/strategy/test', methods=['POST'])
def api_test_strategy():
    """API endpoint for testing strategy"""
    data = request.get_json()
    strategy_name = data.get('strategy')
    symbol = data.get('symbol')
    
    if not strategy_name:
        return jsonify({'success': False, 'error': 'Strategy name is required'})
    
    result = trading_bot.test_strategy(strategy_name, symbol)
    return jsonify(result)

@app.route('/api/test-email', methods=['POST'])
def api_test_email():
    """API endpoint for testing email notification"""
    try:
        data = request.get_json()
        email_config = data.get('email_config', {})
        
        # Test email configuration
        smtp_server = email_config.get('smtp_server', 'smtp.gmail.com')
        smtp_port = email_config.get('smtp_port', 587)
        sender_email = email_config.get('sender_email', '')
        sender_password = email_config.get('sender_password', '')
        recipient_email = email_config.get('recipient_email', '')
        
        if not sender_email or not sender_password or not recipient_email:
            return jsonify({
                'success': False, 
                'error': 'Missing email configuration. Please provide sender_email, sender_password, and recipient_email.'
            })
        
        # Create test message
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        import smtplib
        
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = "🤖 Pionex Trading Bot - Email Test"
        
        body = f"""
        🎉 Email Notification Test Successful!
        
        This is a test email from your Pionex Trading Bot.
        
        📧 Email Configuration:
        - SMTP Server: {smtp_server}
        - SMTP Port: {smtp_port}
        - Sender: {sender_email}
        - Recipient: {recipient_email}
        
        ⏰ Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        
        ✅ If you received this email, your email notification is working correctly!
        
        ---
        This is an automated test message from your trading bot.
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send test email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        
        logger.info(f"Test email sent successfully to {recipient_email}")
        
        return jsonify({
            'success': True, 
            'message': f'Test email sent successfully to {recipient_email}'
        })
        
    except smtplib.SMTPAuthenticationError:
        return jsonify({
            'success': False, 
            'error': 'Authentication failed. Please check your email and password. For Gmail, you may need to use an App Password.'
        })
    except smtplib.SMTPException as e:
        return jsonify({
            'success': False, 
            'error': f'SMTP error: {str(e)}'
        })
    except Exception as e:
        logger.error(f"Error sending test email: {e}")
        return jsonify({
            'success': False, 
            'error': f'Failed to send test email: {str(e)}'
        })

@app.route('/api/test-symbol-format/<symbol>')
def api_test_symbol_format(symbol):
    """Test symbol format conversion"""
    try:
        result = trading_bot.api.test_symbol_format(symbol)
        return jsonify({
            'success': True,
            'data': result
        })
    except Exception as e:
        logger.error(f"Error testing symbol format for {symbol}: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/test-api-response/<symbol>')
def api_test_api_response(symbol):
    """Test API response for debugging"""
    try:
        # Convert symbol format
        formatted_symbol = symbol
        if 'USDT' in symbol and '_' not in symbol:
            formatted_symbol = symbol.replace('USDT', '_USDT')
        
        logger.info(f"Testing API response for symbol: {symbol} -> {formatted_symbol}")
        
        # Test different API endpoints
        results = {}
        
        # Test klines
        try:
            klines_response = trading_bot.api.get_klines(formatted_symbol, '5M', 10)
            results['klines'] = {
                'response': klines_response,
                'has_error': 'error' in klines_response,
                'has_data': 'data' in klines_response,
                'has_code': 'code' in klines_response,
                'code_value': klines_response.get('code', 'N/A')
            }
        except Exception as e:
            results['klines'] = {'error': str(e)}
        
        # Test ticker
        try:
            ticker_response = trading_bot.api.get_ticker_price(formatted_symbol)
            results['ticker'] = {
                'response': ticker_response,
                'has_error': 'error' in ticker_response,
                'has_data': 'data' in ticker_response
            }
        except Exception as e:
            results['ticker'] = {'error': str(e)}
        
        # Test market data
        try:
            market_data = trading_bot.api.get_real_time_market_data(symbol)
            results['market_data'] = {
                'response': market_data,
                'has_error': 'error' in market_data
            }
        except Exception as e:
            results['market_data'] = {'error': str(e)}
        
        return jsonify({
            'success': True,
            'data': {
                'symbol': symbol,
                'formatted_symbol': formatted_symbol,
                'results': results
            }
        })
        
    except Exception as e:
        logger.error(f"Error testing API response for {symbol}: {e}")
        return jsonify({'success': False, 'error': str(e)})

# WebSocket events
@socketio.on('connect')
def handle_connect():
    """Handle WebSocket connection"""
    emit('connected', {'data': 'Connected to trading bot'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle WebSocket disconnection"""
    print('Client disconnected')

@socketio.on('subscribe_price')
def handle_subscribe_price(data):
    """Handle price subscription"""
    symbol = data.get('symbol')
    if symbol:
        # Subscribe to real-time price updates
        emit('price_update', {'symbol': symbol, 'price': trading_bot.get_real_time_price(symbol)})

def main():
    """Main entry point"""
    print("🚀 Starting Pionex Trading Bot GUI...")
    
    # Check environment
    api_key = os.getenv('PIONEX_API_KEY')
    api_secret = os.getenv('PIONEX_SECRET_KEY')
    
    if not api_key or not api_secret:
        print("❌ Missing required environment variables: PIONEX_API_KEY, PIONEX_SECRET_KEY")
        print("Please set these variables in your .env file")
        return
    
    print("✅ Environment variables check passed")
    
    # Start Flask app with production settings
    socketio.run(app, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False, allow_unsafe_werkzeug=True)

if __name__ == '__main__':
    main() 