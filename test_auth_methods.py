#!/usr/bin/env python3
"""
Test different authentication methods for Pionex API
"""

import os
import hmac
import hashlib
import time
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_auth_methods():
    """Test different authentication methods"""
    
    api_key = os.getenv('PIONEX_API_KEY')
    secret_key = os.getenv('PIONEX_SECRET_KEY')
    
    if not api_key or not secret_key:
        print("❌ API credentials not found!")
        return
    
    print("🔧 Testing Different Authentication Methods...")
    print("=" * 60)
    
    # Test parameters
    timestamp = str(int(time.time() * 1000))
    method = 'GET'
    endpoint = '/api/v1/account/balances'
    params = {'timestamp': timestamp}
    
    # Method 1: Standard HMAC SHA256
    print("\n1️⃣ Method 1: Standard HMAC SHA256")
    sign_str = f"{method.upper()}{endpoint}?timestamp={timestamp}"
    signature = hmac.new(secret_key.encode('utf-8'), sign_str.encode('utf-8'), hashlib.sha256).hexdigest()
    
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'PionexTradingBot/1.0',
        'PIONEX-KEY': api_key,
        'PIONEX-SIGNATURE': signature,
        'PIONEX-TIMESTAMP': timestamp
    }
    
    test_auth_call("Standard HMAC", headers, params)
    
    # Method 2: Try without Content-Type header
    print("\n2️⃣ Method 2: Without Content-Type header")
    headers_no_content = {
        'User-Agent': 'PionexTradingBot/1.0',
        'PIONEX-KEY': api_key,
        'PIONEX-SIGNATURE': signature,
        'PIONEX-TIMESTAMP': timestamp
    }
    
    test_auth_call("No Content-Type", headers_no_content, params)
    
    # Method 3: Try with different header order
    print("\n3️⃣ Method 3: Different header order")
    headers_ordered = {
        'PIONEX-KEY': api_key,
        'PIONEX-SIGNATURE': signature,
        'PIONEX-TIMESTAMP': timestamp,
        'Content-Type': 'application/json',
        'User-Agent': 'PionexTradingBot/1.0'
    }
    
    test_auth_call("Different header order", headers_ordered, params)
    
    # Method 4: Try with different User-Agent
    print("\n4️⃣ Method 4: Different User-Agent")
    headers_ua = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'PIONEX-KEY': api_key,
        'PIONEX-SIGNATURE': signature,
        'PIONEX-TIMESTAMP': timestamp
    }
    
    test_auth_call("Different User-Agent", headers_ua, params)
    
    # Method 5: Try with Accept header
    print("\n5️⃣ Method 5: With Accept header")
    headers_accept = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': 'PionexTradingBot/1.0',
        'PIONEX-KEY': api_key,
        'PIONEX-SIGNATURE': signature,
        'PIONEX-TIMESTAMP': timestamp
    }
    
    test_auth_call("With Accept header", headers_accept, params)

def test_auth_call(method_name, headers, params):
    """Test a specific authentication method"""
    print(f"Testing {method_name}...")
    
    url = f"https://api.pionex.com/api/v1/account/balances"
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            if 'result' in data and data['result']:
                print(f"✅ {method_name} WORKS!")
                return True
            else:
                print(f"❌ {method_name} failed: {data.get('message', 'Unknown error')}")
        else:
            print(f"❌ {method_name} HTTP error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ {method_name} request failed: {e}")
    
    return False

if __name__ == "__main__":
    test_auth_methods() 