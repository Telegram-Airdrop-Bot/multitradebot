from pionex_api import PionexAPI
from bybit_api import BybitAPI
import logging
import yaml
import os
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class TradingBot:
    def __init__(self, config_path: str = 'config.yaml'):
        self.config = self.load_config(config_path)
        self.pionex_api = None
        self.bybit_api = None
        self.initialize_apis()
        
    def load_config(self, config_path: str) -> Dict:
        """Load configuration from YAML file"""
        try:
            with open(config_path, 'r') as file:
                return yaml.safe_load(file)
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            return {}
    
    def initialize_apis(self):
        """Initialize both Pionex (spot) and Bybit (futures) APIs"""
        try:
            # Initialize Pionex API for spot trading
            if self.config.get('api', {}).get('key') and self.config.get('api', {}).get('secret'):
                self.pionex_api = PionexAPI(
                    api_key=self.config['api']['key'],
                    api_secret=self.config['api']['secret']
                )
                logger.info("Pionex API initialized for spot trading")
            
            # Initialize Bybit API for futures trading
            if (self.config.get('bybit', {}).get('enabled') and 
                self.config.get('bybit', {}).get('api_key') and 
                self.config.get('bybit', {}).get('api_secret')):
                
                self.bybit_api = BybitAPI(
                    api_key=self.config['bybit']['api_key'],
                    api_secret=self.config['bybit']['api_secret'],
                    testnet=self.config['bybit'].get('testnet', False)
                )
                logger.info("Bybit API initialized for futures trading")
                
        except Exception as e:
            logger.error(f"Error initializing APIs: {e}")
    
    def get_account_balance(self) -> Dict:
        """Get combined balance from both exchanges"""
        result = {
            'success': True,
            'data': {
                'spot': {},
                'futures': {},
                'total': {}
            }
        }
        
        # Get Pionex spot balance
        if self.pionex_api:
            try:
                spot_balance = self.pionex_api.get_balance()
                if spot_balance.get('success'):
                    result['data']['spot'] = spot_balance.get('data', {})
                else:
                    result['data']['spot'] = {'error': spot_balance.get('error', 'Failed to load')}
            except Exception as e:
                logger.error(f"Error getting spot balance: {e}")
                result['data']['spot'] = {'error': str(e)}
        
        # Get Bybit futures balance
        if self.bybit_api:
            try:
                futures_balance = self.bybit_api.get_futures_balance()
                if futures_balance.get('success'):
                    result['data']['futures'] = futures_balance.get('data', {})
                else:
                    result['data']['futures'] = {'error': futures_balance.get('error', 'Failed to load')}
            except Exception as e:
                logger.error(f"Error getting futures balance: {e}")
                result['data']['futures'] = {'error': str(e)}
        
        # Calculate total balance
        try:
            total_balance = 0
            total_available = 0
            
            # Add spot balance
            if result['data']['spot'] and 'total' in result['data']['spot']:
                total_balance += float(result['data']['spot']['total'] or 0)
                total_available += float(result['data']['spot'].get('available', 0) or 0)
            
            # Add futures balance
            if result['data']['futures'] and 'list' in result['data']['futures']:
                for account in result['data']['futures']['list']:
                    if account.get('coin') == 'USDT':
                        total_balance += float(account.get('walletBalance', 0) or 0)
                        total_available += float(account.get('availableToWithdraw', 0) or 0)
            
            result['data']['total'] = {
                'total': total_balance,
                'available': total_available
            }
            
        except Exception as e:
            logger.error(f"Error calculating total balance: {e}")
            result['data']['total'] = {'error': str(e)}
        
        return result
    
    def get_positions(self) -> Dict:
        """Get combined positions from both exchanges"""
        result = {
            'success': True,
            'data': {
                'spot': [],
                'futures': [],
                'combined': []
            }
        }
        
        # Get Pionex spot positions (balances)
        if self.pionex_api:
            try:
                spot_positions = self.pionex_api.get_positions()
                if spot_positions.get('success'):
                    # Convert spot balances to position format
                    spot_data = spot_positions.get('data', {})
                    if 'list' in spot_data:
                        for balance in spot_data['list']:
                            if float(balance.get('free', 0)) > 0:
                                result['data']['spot'].append({
                                    'symbol': balance.get('asset', ''),
                                    'size': float(balance.get('free', 0)),
                                    'type': 'SPOT',
                                    'exchange': 'PIONEX'
                                })
                else:
                    result['data']['spot'] = []
            except Exception as e:
                logger.error(f"Error getting spot positions: {e}")
                result['data']['spot'] = []
        
        # Get Bybit futures positions
        if self.bybit_api:
            try:
                futures_positions = self.bybit_api.get_futures_positions()
                if futures_positions.get('success'):
                    futures_data = futures_positions.get('data', {})
                    if 'list' in futures_data:
                        for position in futures_data['list']:
                            if float(position.get('size', 0)) > 0:
                                result['data']['futures'].append({
                                    'symbol': position.get('symbol', ''),
                                    'size': float(position.get('size', 0)),
                                    'side': position.get('side', ''),
                                    'entryPrice': float(position.get('avgPrice', 0)),
                                    'markPrice': float(position.get('markPrice', 0)),
                                    'unrealizedPnl': float(position.get('unrealisedPnl', 0)),
                                    'leverage': int(position.get('leverage', 1)),
                                    'type': 'FUTURES',
                                    'exchange': 'BYBIT'
                                })
                else:
                    result['data']['futures'] = []
            except Exception as e:
                logger.error(f"Error getting futures positions: {e}")
                result['data']['futures'] = []
        
        # Combine all positions
        result['data']['combined'] = result['data']['spot'] + result['data']['futures']
        
        return result
    
    def execute_spot_trade(self, symbol: str, side: str, qty: float, order_type: str = 'MARKET', price: float = None) -> Dict:
        """Execute spot trade on Pionex"""
        if not self.pionex_api:
            return {'success': False, 'error': 'Pionex API not initialized'}
        
        try:
            result = self.pionex_api.place_order(
                symbol=symbol,
                side=side,
                order_type=order_type,
                quantity=qty,
                price=str(price) if price else None
            )
            return result
        except Exception as e:
            logger.error(f"Error executing spot trade: {e}")
            return {'success': False, 'error': str(e)}
    
    def execute_futures_trade(self, symbol: str, side: str, qty: float, 
                             order_type: str = 'MARKET', price: float = None,
                             leverage: int = None, stop_loss: float = None,
                             take_profit: float = None) -> Dict:
        """Execute futures trade on Bybit"""
        if not self.bybit_api:
            return {'success': False, 'error': 'Bybit API not initialized'}
        
        try:
            # Set leverage if specified
            if leverage:
                leverage_result = self.bybit_api.set_leverage(symbol, leverage)
                if not leverage_result.get('success'):
                    logger.warning(f"Failed to set leverage: {leverage_result.get('error')}")
            
            # Use default leverage from config if not specified
            if not leverage:
                leverage = self.config.get('futures', {}).get('default_leverage', 10)
            
            result = self.bybit_api.place_futures_order(
                symbol=symbol,
                side=side,
                order_type=order_type,
                qty=qty,
                price=price,
                leverage=leverage,
                stop_loss=stop_loss,
                take_profit=take_profit
            )
            return result
        except Exception as e:
            logger.error(f"Error executing futures trade: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_trading_status(self) -> Dict:
        """Get trading status for both exchanges"""
        return {
            'success': True,
            'data': {
                'spot_enabled': self.pionex_api is not None,
                'futures_enabled': self.bybit_api is not None,
                'trading_mode': self.config.get('trading_mode', 'SPOT_ONLY'),
                'current_pair': self.config.get('trading_pair', 'BTC_USDT')
            }
        }
    
    def update_trading_pair(self, new_pair: str) -> Dict:
        """Update trading pair for both exchanges"""
        try:
            self.config['trading_pair'] = new_pair
            # Save config
            with open('config.yaml', 'w') as file:
                yaml.dump(self.config, file, default_flow_style=False)
            
            return {'success': True, 'data': {'trading_pair': new_pair}}
        except Exception as e:
            logger.error(f"Error updating trading pair: {e}")
            return {'success': False, 'error': str(e)} 