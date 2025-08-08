#!/usr/bin/env python3
"""
Method 3 Trade Test
Test Method 3 signature generation (no query string in signature)
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

def test_method3_trade():
    """Test Method 3 signature generation for trading"""
    
    base_url = "https://api.pionex.com"
    api_key = os.getenv('PIONEX_API_KEY')
    secret_key = os.getenv('PIONEX_SECRET_KEY')
    
    print("🔐 Method 3 Trade Test")
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
    
    # Method 3: No query string in signature
    sign_str = f"POST/api/v1/trade/order"
    
    # Include all parameters in body for signature
    body_with_timestamp = json.dumps(trading_params, separators=(',', ':'))
    sign_str += body_with_timestamp
    
    trading_signature = hmac.new(secret_key.encode(), sign_str.encode(), hashlib.sha256).hexdigest()
    
    print(f"Method 3 signature string: {sign_str}")
    print(f"Method 3 signature: {trading_signature}")
    
    # Test trading endpoint with Method 3
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
    test_method3_trade() 