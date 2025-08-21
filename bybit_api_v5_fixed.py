#!/usr/bin/env python3
"""
Bybit V5 API - Fixed Implementation
Copyright © 2024 Telegram-Airdrop-Bot

Fixed implementation following official Bybit V5 API documentation.
"""

import hashlib
import hmac
import time
import requests
import json
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class BybitAPIV5:
    def __init__(self, api_key: str, api_secret: str, testnet: bool = False):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = 'https://api-testnet.bybit.com' if testnet else 'https://api.bybit.com'
        self.session = requests.Session()
        
    def _generate_signature(self, timestamp: str, recv_window: str, params: str) -> str:
        """Generate HMAC SHA256 signature for Bybit V5 API"""
        # V5 API signature format: timestamp + api_key + recv_window + params
        param_str = str(timestamp) + self.api_key + recv_window + params
        logger.debug(f"Signature input: timestamp={timestamp}, api_key={self.api_key}, recv_window={recv_window}, params={params}")
        logger.debug(f"Full param string for signature: {param_str}")
        
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            param_str.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        logger.debug(f"Generated signature: {signature}")
        return signature
    
    def _make_request(self, method: str, endpoint: str, params: Dict = None, signed: bool = False) -> Dict:
        """Make HTTP request to Bybit V5 API"""
        url = f"{self.base_url}{endpoint}"
        headers = {'Content-Type': 'application/json'}
        
        if signed:
            timestamp = str(int(time.time() * 1000))
            recv_window = "5000"
            
            if params:
                if method.upper() == 'GET':
                    # GET requests: parameters in URL query string
                    sorted_params = sorted(params.items())
                    param_str = "&".join([f"{k}={v}" for k, v in sorted_params])
                    logger.debug(f"GET request param string: {param_str}")
                else:
                    # POST requests: parameters in JSON body
                    param_str = json.dumps(params, separators=(',', ':'))
                    logger.debug(f"POST request param string: {param_str}")
            else:
                param_str = ""
                logger.debug("No params provided")
            
            # Generate signature with timestamp + api_key + recv_window + params
            signature = self._generate_signature(timestamp, recv_window, param_str)
            
            # Add signature headers - V5 API format
            headers.update({
                'X-BAPI-API-KEY': self.api_key,
                'X-BAPI-SIGNATURE': signature,
                'X-BAPI-SIGNATURE-TYPE': '2',
                'X-BAPI-TIMESTAMP': timestamp,
                'X-BAPI-RECV-WINDOW': recv_window
            })
            
            logger.debug(f"Request headers: {headers}")
        
        try:
            if method.upper() == 'GET':
                # GET: params go in URL query string
                logger.debug(f"Making GET request to {url} with params: {params}")
                response = self.session.get(url, params=params, headers=headers)
            elif method.upper() == 'POST':
                # POST: params go in JSON body
                logger.debug(f"Making POST request to {url} with JSON body: {params}")
                response = self.session.post(url, json=params, headers=headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            data = response.json()
            
            logger.debug(f"Response data: {data}")
            
            # Check for V5 API response format
            if data.get('retCode') == 0:
                return {'success': True, 'data': data.get('result', data)}
            else:
                return {
                    'success': False, 
                    'error': data.get('retMsg', 'Unknown error'), 
                    'code': data.get('retCode')
                }
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Bybit API request error: {e}")
            return {'success': False, 'error': str(e)}
        except Exception as e:
            logger.error(f"Bybit API error: {e}")
            return {'success': False, 'error': str(e)}
    
    # ===== ACCOUNT ENDPOINTS =====
    
    def get_account_info(self) -> Dict:
        """Get account information"""
        params = {'accountType': 'UNIFIED'}
        return self._make_request('GET', '/v5/account/wallet-balance', params, signed=True)
    
    def get_futures_balance(self) -> Dict:
        """Get futures wallet balance"""
        params = {'accountType': 'UNIFIED'}
        return self._make_request('GET', '/v5/account/wallet-balance', params, signed=True)
    
    # ===== POSITION ENDPOINTS =====
    
    def get_futures_positions(self, symbol: str = None) -> Dict:
        """Get open futures positions"""
        params = {'category': 'linear'}
        if symbol:
            params['symbol'] = symbol
        return self._make_request('GET', '/v5/position/list', params, signed=True)
    
    def set_futures_leverage(self, symbol: str, leverage: int) -> Dict:
        """Set leverage for futures trading"""
        params = {
            'category': 'linear',
            'symbol': symbol,
            'buyLeverage': str(leverage),
            'sellLeverage': str(leverage)
        }
        return self._make_request('POST', '/v5/position/set-leverage', params, signed=True)
    
    # ===== ORDER ENDPOINTS =====
    
    def place_futures_order(self, symbol: str, side: str, order_type: str, 
                           qty: float, price: float = None, 
                           time_in_force: str = "GTC", reduce_only: bool = False,
                           close_on_trigger: bool = False) -> Dict:
        """Place futures order with V5 API parameters"""
        params = {
            'category': 'linear',
            'symbol': symbol,
            'side': side.title(),  # V5 uses title case: "Buy" or "Sell"
            'orderType': order_type.title(),  # "Limit" or "Market"
            'qty': str(qty),
            'timeInForce': time_in_force,
            'reduceOnly': reduce_only,
            'closeOnTrigger': close_on_trigger
        }
        
        # Add price for limit orders
        if price and order_type.upper() == 'LIMIT':
            params['price'] = str(price)
        
        return self._make_request('POST', '/v5/order/create', params, signed=True)
    
    def get_futures_open_orders(self, symbol: str = None) -> Dict:
        """Get open futures orders"""
        params = {'category': 'linear'}
        if symbol:
            params['symbol'] = symbol
        return self._make_request('GET', '/v5/order/realtime', params, signed=True)
    
    def cancel_futures_order(self, symbol: str, order_id: str) -> Dict:
        """Cancel futures order"""
        params = {
            'category': 'linear',
            'symbol': symbol,
            'orderId': order_id
        }
        return self._make_request('POST', '/v5/order/cancel', params, signed=True)
    
    # ===== MARKET DATA ENDPOINTS =====
    
    def get_futures_market_status(self) -> Dict:
        """Get overall futures market status"""
        return self._make_request('GET', '/v5/market/time')
    
    def get_futures_ticker(self, symbol: str) -> Dict:
        """Get specific futures ticker data"""
        params = {
            'category': 'linear',
            'symbol': symbol
        }
        return self._make_request('GET', '/v5/market/tickers', params)
    
    def get_futures_klines(self, symbol: str, interval: str = '5', 
                           limit: int = 200, start_time: int = None, 
                           end_time: int = None) -> Dict:
        """Get futures kline/candlestick data with V5 API parameters"""
        params = {
            'category': 'linear',
            'symbol': symbol,
            'interval': interval,
            'limit': limit
        }
        
        if start_time:
            params['start'] = start_time
        
        if end_time:
            params['end'] = end_time
        
        return self._make_request('GET', '/v5/market/kline', params)
    
    def get_futures_funding_rate(self, symbol: str) -> Dict:
        """Get funding rate for specific futures symbol"""
        params = {
            'category': 'linear',
            'symbol': symbol,
            'limit': 1
        }
        return self._make_request('GET', '/v5/market/funding/history', params)
    
    def get_futures_market_summary(self) -> Dict:
        """Get market summary for top futures pairs"""
        try:
            # Get data for major pairs
            major_pairs = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT']
            market_summary = {}
            
            for pair in major_pairs:
                ticker_data = self.get_futures_ticker(pair)
                if ticker_data.get('success') and ticker_data['data'].get('list'):
                    ticker = ticker_data['data']['list'][0]
                    
                    market_summary[pair] = {
                        'price': float(ticker.get('lastPrice', 0)),
                        'change_24h': float(ticker.get('price24hPcnt', 0)) * 100,
                        'volume_24h': float(ticker.get('volume24h', 0)),
                        'high_24h': float(ticker.get('highPrice24h', 0)),
                        'low_24h': float(ticker.get('lowPrice24h', 0)),
                        'funding_rate': 0.0,  # Will be fetched separately if needed
                        'timestamp': ticker.get('timestamp', '')
                    }
            
            return {'success': True, 'data': market_summary}
            
        except Exception as e:
            logger.error(f"Error fetching market summary: {e}")
            return {'success': False, 'error': str(e)}
    
    # ===== UTILITY METHODS =====
    
    def close_futures_position(self, symbol: str, side: str, qty: float, 
                              order_type: str = "Market") -> Dict:
        """Close futures position with V5 API parameters"""
        params = {
            'category': 'linear',
            'symbol': symbol,
            'side': 'Sell' if side.upper() == 'BUY' else 'Buy',  # V5 title case
            'orderType': order_type.title(),
            'qty': str(qty),
            'reduceOnly': True,  # V5 specific parameter for closing positions
            'timeInForce': 'GTC'
        }
        
        return self._make_request('POST', '/v5/order/create', params, signed=True)

# For backward compatibility
BybitAPI = BybitAPIV5 