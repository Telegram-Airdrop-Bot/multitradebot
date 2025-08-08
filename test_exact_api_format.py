#!/usr/bin/env python3
"""
Exact API Format Test
Test using the exact format from the official API documentation
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

def test_exact_api_format():
    """Test using the exact format from the API documentation"""
    
    base_url = "https://api.pionex.com"
    api_key = os.getenv('PIONEX_API_KEY')
    secret_key = os.getenv('PIONEX_SECRET_KEY')
    
    print("🔐 Exact API Format Test")
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
    
    # Use exact format from API documentation
    trading_params = {
        'clientOrderId': f'test_{int(time.time())}',
        'symbol': 'BTC_USDT',
        'side': 'BUY',
        'type': 'MARKET',
        'size': '0.0001',
        'timestamp': str(server_timestamp)
    }
    
    print("Testing with exact API documentation format:")
    print(f"   Parameters: {trading_params}")
    
    # Generate signature
    sorted_items = sorted(trading_params.items())
    query_string = '&'.join(f'{k}={v}' for k, v in sorted_items)
    path_url = f"/api/v1/trade/order?{query_string}"
    sign_str = f"POST{path_url}"
    
    # Include all parameters in body for signature
    body_with_timestamp = json.dumps(trading_params, separators=(',', ':'))
    sign_str += body_with_timestamp
    
    trading_signature = hmac.new(secret_key.encode(), sign_str.encode(), hashlib.sha256).hexdigest()
    
    print(f"   Signature string: {sign_str}")
    print(f"   Signature: {trading_signature}")
    
    # Test trading endpoint
    headers = {
        'Content-Type': 'application/json',
        'PIONEX-KEY': api_key,
        'PIONEX-SIGNATURE': trading_signature
    }
    
    try:
        url_with_timestamp = f"{base_url}/api/v1/trade/order?timestamp={server_timestamp}"
        response = requests.post(url_with_timestamp, data=body_with_timestamp, headers=headers, timeout=10)
        print(f"   Trading status: {response.status_code}")
        print(f"   Trading response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('result') == True:
                print("✅ Trade successful!")
                print(f"   Order ID: {data.get('data', {}).get('orderId', 'N/A')}")
                print(f"   Client Order ID: {data.get('data', {}).get('clientOrderId', 'N/A')}")
            else:
                print(f"❌ Trade failed: {data.get('message', 'Unknown error')}")
                print(f"   Error code: {data.get('code', 'N/A')}")
        else:
            print(f"❌ HTTP error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()
    
    # Test with limit order format
    print("Testing with limit order format...")
    
    limit_params = {
        'clientOrderId': f'limit_{int(time.time())}',
        'symbol': 'BTC_USDT',
        'side': 'BUY',
        'type': 'LIMIT',
        'size': '0.0001',
        'price': '117000',
        'timestamp': str(server_timestamp)
    }
    
    print(f"   Limit parameters: {limit_params}")
    
    # Generate signature for limit order
    sorted_items = sorted(limit_params.items())
    query_string = '&'.join(f'{k}={v}' for k, v in sorted_items)
    path_url = f"/api/v1/trade/order?{query_string}"
    sign_str = f"POST{path_url}"
    
    body_with_timestamp = json.dumps(limit_params, separators=(',', ':'))
    sign_str += body_with_timestamp
    
    limit_signature = hmac.new(secret_key.encode(), sign_str.encode(), hashlib.sha256).hexdigest()
    
    print(f"   Limit signature: {limit_signature}")
    
    try:
        url_with_timestamp = f"{base_url}/api/v1/trade/order?timestamp={server_timestamp}"
        response = requests.post(url_with_timestamp, data=body_with_timestamp, headers=headers, timeout=10)
        print(f"   Limit order status: {response.status_code}")
        print(f"   Limit order response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('result') == True:
                print("✅ Limit order successful!")
            else:
                print(f"❌ Limit order failed: {data.get('message', 'Unknown error')}")
        else:
            print(f"❌ HTTP error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_exact_api_format() 