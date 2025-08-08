#!/usr/bin/env python3
"""
Signature Verification Test
Verify the exact signature generation that works
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

def test_signature_verification():
    """Test signature verification with working account endpoint"""
    
    base_url = "https://api.pionex.com"
    api_key = os.getenv('PIONEX_API_KEY')
    secret_key = os.getenv('PIONEX_SECRET_KEY')
    
    print("🔐 Signature Verification Test")
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
    
    # Test 1: Working account endpoint signature
    print("✅ Testing working account endpoint signature...")
    
    # Account endpoint parameters
    account_params = {'timestamp': str(server_timestamp)}
    
    # Generate signature for account endpoint (GET)
    sorted_items = sorted(account_params.items())
    query_string = '&'.join(f'{k}={v}' for k, v in sorted_items)
    path_url = f"/api/v1/account/balances?{query_string}"
    sign_str = f"GET{path_url}"
    account_signature = hmac.new(secret_key.encode(), sign_str.encode(), hashlib.sha256).hexdigest()
    
    print(f"   Account signature string: {sign_str}")
    print(f"   Account signature: {account_signature}")
    
    # Test account endpoint
    headers = {
        'Content-Type': 'application/json',
        'PIONEX-KEY': api_key,
        'PIONEX-SIGNATURE': account_signature
    }
    
    try:
        response = requests.get(f"{base_url}/api/v1/account/balances", 
                             params=account_params, headers=headers, timeout=5)
        print(f"   Account status: {response.status_code}")
        print(f"   Account response: {response.text[:100]}...")
    except Exception as e:
        print(f"   Account error: {e}")
    
    print()
    
    # Test 2: Trading endpoint signature
    print("🔄 Testing trading endpoint signature...")
    
    # Trading endpoint parameters
    trading_params = {
        'symbol': 'BTC_USDT',
        'side': 'BUY',
        'type': 'MARKET',
        'quantity': '0.0001',
        'timestamp': str(server_timestamp)
    }
    
    # Generate signature for trading endpoint (POST)
    sorted_items = sorted(trading_params.items())
    query_string = '&'.join(f'{k}={v}' for k, v in sorted_items)
    path_url = f"/api/v1/trade/order?{query_string}"
    sign_str = f"POST{path_url}"
    
    # Remove timestamp from body for signature
    body_params = {k: v for k, v in trading_params.items() if k != 'timestamp'}
    body = json.dumps(body_params, separators=(',', ':')) if body_params else ''
    sign_str += body
    
    trading_signature = hmac.new(secret_key.encode(), sign_str.encode(), hashlib.sha256).hexdigest()
    
    print(f"   Trading signature string: {sign_str}")
    print(f"   Trading signature: {trading_signature}")
    
    # Test trading endpoint
    headers = {
        'Content-Type': 'application/json',
        'PIONEX-KEY': api_key,
        'PIONEX-SIGNATURE': trading_signature
    }
    
    try:
        url_with_timestamp = f"{base_url}/api/v1/trade/order?timestamp={server_timestamp}"
        response = requests.post(url_with_timestamp, data=body, headers=headers, timeout=10)
        print(f"   Trading status: {response.status_code}")
        print(f"   Trading response: {response.text}")
    except Exception as e:
        print(f"   Trading error: {e}")
    
    print()
    
    # Test 3: Compare signature methods
    print("🔍 Comparing signature methods...")
    
    # Method 1: Include timestamp in body
    body_with_timestamp = json.dumps(trading_params, separators=(',', ':'))
    sign_str_method1 = f"POST/api/v1/trade/order?{query_string}{body_with_timestamp}"
    signature1 = hmac.new(secret_key.encode(), sign_str_method1.encode(), hashlib.sha256).hexdigest()
    print(f"   Method 1 (timestamp in body): {signature1}")
    
    # Method 2: Exclude timestamp from body
    sign_str_method2 = f"POST/api/v1/trade/order?{query_string}{body}"
    signature2 = hmac.new(secret_key.encode(), sign_str_method2.encode(), hashlib.sha256).hexdigest()
    print(f"   Method 2 (timestamp excluded): {signature2}")
    
    # Method 3: No query string in signature
    sign_str_method3 = f"POST/api/v1/trade/order{body}"
    signature3 = hmac.new(secret_key.encode(), sign_str_method3.encode(), hashlib.sha256).hexdigest()
    print(f"   Method 3 (no query): {signature3}")

if __name__ == "__main__":
    test_signature_verification() 