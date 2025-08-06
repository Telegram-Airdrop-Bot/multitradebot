#!/usr/bin/env python3
"""
Test the corrected signature generation method based on official Pionex API documentation
"""

import os
import hmac
import hashlib
import time
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_correct_signature():
    """Test the correct signature generation method"""
    
    api_key = os.getenv('PIONEX_API_KEY')
    secret_key = os.getenv('PIONEX_SECRET_KEY')
    
    if not api_key or not secret_key:
        print("❌ API credentials not found!")
        return
    
    print("🔧 Testing Correct Signature Method...")
    print("=" * 50)
    
    # Test parameters (matching the official example)
    method = 'GET'
    endpoint = '/api/v1/trade/allOrders'
    params = {
        'symbol': 'BTC_USDT',
        'limit': '1'
    }
    
    # Step 1: Get current millisecond timestamp
    timestamp = str(int(time.time() * 1000))
    params['timestamp'] = timestamp
    
    print(f"Step 1 - Timestamp: {timestamp}")
    print(f"Step 2 - Parameters: {params}")
    
    # Step 2 & 3: Sort the key-value pairs in ascending ASCII order by key and concatenate with "&"
    sorted_items = sorted(params.items())
    query_string = '&'.join(f'{k}={v}' for k, v in sorted_items)
    print(f"Step 3 - Query string: {query_string}")
    
    # Step 4: Concatenate above result after PATH with "?" to generate PATH_URL
    path_url = f"{endpoint}?{query_string}"
    print(f"Step 4 - Path URL: {path_url}")
    
    # Step 5: Concatenate METHOD and PATH_URL
    sign_str = f"{method.upper()}{path_url}"
    print(f"Step 5 - Signature string: {sign_str}")
    
    # Step 6: For POST and DELETE, concatenate entity body (if any)
    # Skip for GET request
    
    # Step 7: Use API Secret and the above result to generate HMAC SHA256, then convert to hexadecimal
    signature = hmac.new(
        secret_key.encode('utf-8'),
        sign_str.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    print(f"Step 7 - Generated signature: {signature}")
    
    # Test the API call
    print(f"\n🌐 Testing API Call...")
    
    url = f"https://api.pionex.com{endpoint}"
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'PionexTradingBot/1.0',
        'PIONEX-KEY': api_key,
        'PIONEX-SIGNATURE': signature,
        'PIONEX-TIMESTAMP': timestamp
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            if 'result' in data and data['result']:
                print("✅ API call successful!")
                print("✅ Correct signature method works!")
                return True
            else:
                print(f"❌ API call failed: {data.get('message', 'Unknown error')}")
                return False
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False

def test_balance_endpoint():
    """Test the balance endpoint with correct signature"""
    
    api_key = os.getenv('PIONEX_API_KEY')
    secret_key = os.getenv('PIONEX_SECRET_KEY')
    
    if not api_key or not secret_key:
        print("❌ API credentials not found!")
        return
    
    print(f"\n💰 Testing Balance Endpoint...")
    
    # Test parameters for balance endpoint
    method = 'GET'
    endpoint = '/api/v1/account/balances'
    params = {}
    
    # Step 1: Get current millisecond timestamp
    timestamp = str(int(time.time() * 1000))
    params['timestamp'] = timestamp
    
    # Step 2 & 3: Sort the key-value pairs in ascending ASCII order by key and concatenate with "&"
    sorted_items = sorted(params.items())
    query_string = '&'.join(f'{k}={v}' for k, v in sorted_items)
    
    # Step 4: Concatenate above result after PATH with "?" to generate PATH_URL
    path_url = f"{endpoint}?{query_string}"
    
    # Step 5: Concatenate METHOD and PATH_URL
    sign_str = f"{method.upper()}{path_url}"
    
    # Step 7: Use API Secret and the above result to generate HMAC SHA256, then convert to hexadecimal
    signature = hmac.new(
        secret_key.encode('utf-8'),
        sign_str.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    print(f"Balance endpoint signature: {signature}")
    
    # Test the API call
    url = f"https://api.pionex.com{endpoint}"
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'PionexTradingBot/1.0',
        'PIONEX-KEY': api_key,
        'PIONEX-SIGNATURE': signature,
        'PIONEX-TIMESTAMP': timestamp
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            if 'result' in data and data['result']:
                print("✅ Balance endpoint works!")
                return True
            else:
                print(f"❌ Balance endpoint failed: {data.get('message', 'Unknown error')}")
                return False
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing corrected signature method based on official Pionex API documentation...")
    
    # Test the example from the documentation
    success1 = test_correct_signature()
    
    # Test the balance endpoint
    success2 = test_balance_endpoint()
    
    if success1 and success2:
        print("\n✅ All tests passed! The signature method is working correctly.")
    else:
        print("\n❌ Some tests failed. Please check your API credentials.") 