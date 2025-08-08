#!/usr/bin/env python3
"""
Method 1 Trade Test
Test Method 1 signature generation (timestamp in body)
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

def test_method1_trade():
    """Test Method 1 signature generation for trading"""
    
    base_url = "https://api.pionex.com"
    api_key = os.getenv('PIONEX_API_KEY')
    secret_key = os.getenv('PIONEX_SECRET_KEY')
    
    print("🔐 Method 1 Trade Test")
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
    
    # Trading endpoint parameters
    trading_params = {
        'symbol': 'BTC_USDT',
        'side': 'BUY',
        'type': 'MARKET',
        'quantity': '0.0001',
        'timestamp': str(server_timestamp)
    }
    
    # Method 1: Include timestamp in body for signature
    sorted_items = sorted(trading_params.items())
    query_string = '&'.join(f'{k}={v}' for k, v in sorted_items)
    path_url = f"/api/v1/trade/order?{query_string}"
    sign_str = f"POST{path_url}"
    
    # Include timestamp in body for signature
    body_with_timestamp = json.dumps(trading_params, separators=(',', ':'))
    sign_str += body_with_timestamp
    
    trading_signature = hmac.new(secret_key.encode(), sign_str.encode(), hashlib.sha256).hexdigest()
    
    print(f"Method 1 signature string: {sign_str}")
    print(f"Method 1 signature: {trading_signature}")
    
    # Test trading endpoint with Method 1
    headers = {
        'Content-Type': 'application/json',
        'PIONEX-KEY': api_key,
        'PIONEX-SIGNATURE': trading_signature
    }
    
    try:
        url_with_timestamp = f"{base_url}/api/v1/trade/order?timestamp={server_timestamp}"
        response = requests.post(url_with_timestamp, data=body_with_timestamp, headers=headers, timeout=10)
        print(f"Trading status: {response.status_code}")
        print(f"Trading response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('result') == True:
                print("✅ Trade successful!")
                print(f"Order ID: {data.get('data', {}).get('orderId', 'N/A')}")
            else:
                print(f"❌ Trade failed: {data.get('message', 'Unknown error')}")
        else:
            print(f"❌ HTTP error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_method1_trade() 