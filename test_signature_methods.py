#!/usr/bin/env python3
"""
Test different signature generation methods for Pionex API
"""

import os
import hmac
import hashlib
import time
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_signature_methods():
    """Test different signature generation methods"""
    
    api_key = os.getenv('PIONEX_API_KEY')
    secret_key = os.getenv('PIONEX_SECRET_KEY')
    
    if not api_key or not secret_key:
        print("❌ API credentials not found!")
        return
    
    print("🔧 Testing Different Signature Methods...")
    print("=" * 60)
    
    # Test parameters
    timestamp = str(int(time.time() * 1000))
    method = 'GET'
    endpoint = '/api/v1/account/balances'
    params = {'timestamp': timestamp}
    
    # Method 1: Current method (UPPER case method)
    print("\n1️⃣ Method 1: UPPER case method")
    sign_str_1 = f"{method.upper()}{endpoint}?timestamp={timestamp}"
    signature_1 = hmac.new(secret_key.encode('utf-8'), sign_str_1.encode('utf-8'), hashlib.sha256).hexdigest()
    print(f"Signature String: {sign_str_1}")
    print(f"Signature: {signature_1}")
    
    # Method 2: Lower case method
    print("\n2️⃣ Method 2: Lower case method")
    sign_str_2 = f"{method.lower()}{endpoint}?timestamp={timestamp}"
    signature_2 = hmac.new(secret_key.encode('utf-8'), sign_str_2.encode('utf-8'), hashlib.sha256).hexdigest()
    print(f"Signature String: {sign_str_2}")
    print(f"Signature: {signature_2}")
    
    # Method 3: No method in signature
    print("\n3️⃣ Method 3: No method in signature")
    sign_str_3 = f"{endpoint}?timestamp={timestamp}"
    signature_3 = hmac.new(secret_key.encode('utf-8'), sign_str_3.encode('utf-8'), hashlib.sha256).hexdigest()
    print(f"Signature String: {sign_str_3}")
    print(f"Signature: {signature_3}")
    
    # Method 4: Just query string
    print("\n4️⃣ Method 4: Just query string")
    sign_str_4 = f"timestamp={timestamp}"
    signature_4 = hmac.new(secret_key.encode('utf-8'), sign_str_4.encode('utf-8'), hashlib.sha256).hexdigest()
    print(f"Signature String: {sign_str_4}")
    print(f"Signature: {signature_4}")
    
    # Method 5: Sorted query string
    print("\n5️⃣ Method 5: Sorted query string")
    sorted_items = sorted(params.items())
    query_string = '&'.join(f'{k}={v}' for k, v in sorted_items)
    sign_str_5 = f"{method.upper()}{endpoint}?{query_string}"
    signature_5 = hmac.new(secret_key.encode('utf-8'), sign_str_5.encode('utf-8'), hashlib.sha256).hexdigest()
    print(f"Query String: {query_string}")
    print(f"Signature String: {sign_str_5}")
    print(f"Signature: {signature_5}")
    
    # Test all methods
    print("\n🧪 Testing All Methods...")
    
    url = f"https://api.pionex.com{endpoint}"
    base_headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'PionexTradingBot/1.0',
        'PIONEX-KEY': api_key,
        'PIONEX-TIMESTAMP': timestamp
    }
    
    methods = [
        ("Method 1 (UPPER)", signature_1),
        ("Method 2 (lower)", signature_2),
        ("Method 3 (no method)", signature_3),
        ("Method 4 (query only)", signature_4),
        ("Method 5 (sorted)", signature_5)
    ]
    
    for method_name, signature in methods:
        print(f"\nTesting {method_name}...")
        headers = base_headers.copy()
        headers['PIONEX-SIGNATURE'] = signature
        
        try:
            response = requests.get(url, params=params, headers=headers, timeout=10)
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
            
            if response.status_code == 200:
                data = response.json()
                if 'result' in data and data['result']:
                    print(f"✅ {method_name} WORKS!")
                    return method_name, signature
                else:
                    print(f"❌ {method_name} failed: {data.get('message', 'Unknown error')}")
            else:
                print(f"❌ {method_name} HTTP error: {response.status_code}")
                
        except Exception as e:
            print(f"❌ {method_name} request failed: {e}")
    
    print("\n❌ All signature methods failed!")
    return None, None

if __name__ == "__main__":
    test_signature_methods() 