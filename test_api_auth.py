#!/usr/bin/env python3
"""
API Authentication Test
Test the API key and authentication method
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

def test_api_auth():
    """Test API authentication"""
    
    base_url = "https://api.pionex.com"
    api_key = os.getenv('PIONEX_API_KEY')
    secret_key = os.getenv('PIONEX_SECRET_KEY')
    
    print("🔐 API Authentication Test")
    print("=" * 50)
    
    print(f"API Key: {api_key[:20]}..." if api_key else "API Key: Not found")
    print(f"Secret Key: {secret_key[:20]}..." if secret_key else "Secret Key: Not found")
    print()
    
    if not api_key or not secret_key:
        print("❌ Missing API credentials!")
        return
    
    # Step 1: Test authentication headers
    print("📡 Testing authentication headers...")
    
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
    
    print(f"   Server timestamp: {server_timestamp}")
    
    # Test different header formats
    headers_formats = [
        {
            'name': 'PIONEX-KEY',
            'headers': {
                'Content-Type': 'application/json',
                'PIONEX-KEY': api_key,
                'PIONEX-SIGNATURE': 'test_signature'
            }
        },
        {
            'name': 'X-PIONEX-KEY',
            'headers': {
                'Content-Type': 'application/json',
                'X-PIONEX-KEY': api_key,
                'X-PIONEX-SIGNATURE': 'test_signature'
            }
        },
        {
            'name': 'Authorization Bearer',
            'headers': {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {api_key}'
            }
        },
        {
            'name': 'Authorization Basic',
            'headers': {
                'Content-Type': 'application/json',
                'Authorization': f'Basic {api_key}'
            }
        }
    ]
    
    for format_info in headers_formats:
        print(f"   Testing {format_info['name']}...")
        try:
            response = requests.get(f"{base_url}/api/v1/account/balances", 
                                 headers=format_info['headers'], timeout=5)
            print(f"     Status: {response.status_code}")
            print(f"     Response: {response.text[:100]}...")
        except Exception as e:
            print(f"     Error: {e}")
        print()
    
    # Step 2: Test signature generation
    print("🔑 Testing signature generation...")
    
    # Test different signature methods
    params = {'timestamp': str(server_timestamp)}
    
    # Method 1: HMAC SHA256 with query string
    query_string = '&'.join(f'{k}={v}' for k, v in sorted(params.items()))
    signature1 = hmac.new(secret_key.encode(), query_string.encode(), hashlib.sha256).hexdigest()
    print(f"   Method 1 (query string): {signature1}")
    
    # Method 2: HMAC SHA256 with JSON body
    body = json.dumps(params, separators=(',', ':'))
    signature2 = hmac.new(secret_key.encode(), body.encode(), hashlib.sha256).hexdigest()
    print(f"   Method 2 (JSON body): {signature2}")
    
    # Method 3: HMAC SHA256 with path + query
    path = "/api/v1/account/balances"
    sign_str = f"GET{path}?{query_string}"
    signature3 = hmac.new(secret_key.encode(), sign_str.encode(), hashlib.sha256).hexdigest()
    print(f"   Method 3 (path + query): {signature3}")
    
    print()
    
    # Step 3: Test with correct signature
    print("✅ Testing with correct signature...")
    
    headers = {
        'Content-Type': 'application/json',
        'PIONEX-KEY': api_key,
        'PIONEX-SIGNATURE': signature3
    }
    
    try:
        response = requests.get(f"{base_url}/api/v1/account/balances", 
                             params=params, headers=headers, timeout=5)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Step 4: Check if API key is valid
    print("🔍 Checking API key validity...")
    print("   Possible issues:")
    print("   1. API key has expired")
    print("   2. API key doesn't have trading permissions")
    print("   3. API key is for testnet, not mainnet")
    print("   4. API key format is incorrect")
    print("   5. Server is rejecting the key")

if __name__ == "__main__":
    test_api_auth() 