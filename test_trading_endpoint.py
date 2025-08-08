#!/usr/bin/env python3
"""
Trading Endpoint Test
Test the exact trading endpoint and parameters
"""

import os
import requests
import time
import json
import hmac
import hashlib
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_trading_endpoint():
    """Test the trading endpoint with different parameters"""
    
    base_url = "https://api.pionex.com"
    api_key = os.getenv('PIONEX_API_KEY')
    secret_key = os.getenv('PIONEX_SECRET_KEY')
    
    print("🔍 Trading Endpoint Test")
    print("=" * 50)
    
    if not api_key or not secret_key:
        print("❌ Missing API credentials!")
        return
    
    # Get server timestamp
    try:
        response = requests.get(f"{base_url}/api/v1/market/tickers", timeout=5)
        if response.status_code == 200:
            data = response.json()
            server_timestamp = data.get('timestamp', int(time.time() * 1000))
        else:
            server_timestamp = int(time.time() * 1000)
    except:
        server_timestamp = int(time.time() * 1000)
    
    print(f"Server timestamp: {server_timestamp}")
    print()
    
    # Test different trading endpoints
    endpoints = [
        "/api/v1/trade/order",
        "/api/v1/order",
        "/api/v1/trade",
        "/api/v1/spot/order"
    ]
    
    for endpoint in endpoints:
        print(f"Testing endpoint: {endpoint}")
        
        # Test parameters
        params = {
            'symbol': 'BTC_USDT',
            'side': 'BUY',
            'type': 'MARKET',
            'quantity': '0.0001',
            'timestamp': str(server_timestamp)
        }
        
        # Generate signature
        sorted_items = sorted(params.items())
        query_string = '&'.join(f'{k}={v}' for k, v in sorted_items)
        path_url = f"{endpoint}?{query_string}"
        sign_str = f"POST{path_url}"
        body = json.dumps(params, separators=(',', ':'))
        sign_str += body
        signature = hmac.new(secret_key.encode(), sign_str.encode(), hashlib.sha256).hexdigest()
        
        headers = {
            'Content-Type': 'application/json',
            'PIONEX-KEY': api_key,
            'PIONEX-SIGNATURE': signature
        }
        
        try:
            response = requests.post(f"{base_url}{endpoint}", 
                                  data=body, headers=headers, timeout=10)
            print(f"  Status: {response.status_code}")
            print(f"  Response: {response.text[:200]}...")
        except Exception as e:
            print(f"  Error: {e}")
        
        print()
    
    # Test with different parameter formats
    print("Testing different parameter formats...")
    
    test_params = [
        {
            'name': 'Standard format',
            'params': {
                'symbol': 'BTC_USDT',
                'side': 'BUY',
                'type': 'MARKET',
                'quantity': '0.0001',
                'timestamp': str(server_timestamp)
            }
        },
        {
            'name': 'With price',
            'params': {
                'symbol': 'BTC_USDT',
                'side': 'BUY',
                'type': 'LIMIT',
                'quantity': '0.0001',
                'price': '117500',
                'timestamp': str(server_timestamp)
            }
        },
        {
            'name': 'With clientOrderId',
            'params': {
                'symbol': 'BTC_USDT',
                'side': 'BUY',
                'type': 'MARKET',
                'quantity': '0.0001',
                'clientOrderId': f'test_{int(time.time())}',
                'timestamp': str(server_timestamp)
            }
        }
    ]
    
    for test in test_params:
        print(f"Testing {test['name']}...")
        
        params = test['params']
        sorted_items = sorted(params.items())
        query_string = '&'.join(f'{k}={v}' for k, v in sorted_items)
        path_url = f"/api/v1/trade/order?{query_string}"
        sign_str = f"POST{path_url}"
        body = json.dumps(params, separators=(',', ':'))
        sign_str += body
        signature = hmac.new(secret_key.encode(), sign_str.encode(), hashlib.sha256).hexdigest()
        
        headers = {
            'Content-Type': 'application/json',
            'PIONEX-KEY': api_key,
            'PIONEX-SIGNATURE': signature
        }
        
        try:
            response = requests.post(f"{base_url}/api/v1/trade/order", 
                                  data=body, headers=headers, timeout=10)
            print(f"  Status: {response.status_code}")
            print(f"  Response: {response.text}")
        except Exception as e:
            print(f"  Error: {e}")
        
        print()

if __name__ == "__main__":
    test_trading_endpoint() 