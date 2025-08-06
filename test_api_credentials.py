#!/usr/bin/env python3
"""
Test script to verify Pionex API credentials and signature generation
"""

import os
import hmac
import hashlib
import time
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_api_credentials():
    """Test API credentials and signature generation"""
    
    # Get API credentials
    api_key = os.getenv('PIONEX_API_KEY')
    secret_key = os.getenv('PIONEX_SECRET_KEY')
    
    print("🔧 Testing Pionex API Credentials...")
    print("=" * 50)
    
    print(f"API Key: {api_key[:10]}..." if api_key else "API Key: Not set")
    print(f"Secret Key: {secret_key[:10]}..." if secret_key else "Secret Key: Not set")
    
    if not api_key or not secret_key:
        print("\n❌ API credentials not found!")
        print("Please set the following environment variables:")
        print("export PIONEX_API_KEY='your_api_key'")
        print("export PIONEX_SECRET_KEY='your_secret_key'")
        return
    
    # Test signature generation
    print("\n🔐 Testing Signature Generation...")
    
    # Test parameters
    params = {'timestamp': str(int(time.time() * 1000))}
    
    # Create query string
    sorted_items = sorted(params.items())
    query_string = '&'.join(f'{k}={v}' for k, v in sorted_items)
    
    # Create signature string
    method = 'GET'
    endpoint = '/api/v1/account/balances'
    sign_str = f"{method.upper()}{endpoint}?{query_string}"
    
    # Generate signature
    signature = hmac.new(
        secret_key.encode('utf-8'),
        sign_str.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    print(f"Method: {method}")
    print(f"Endpoint: {endpoint}")
    print(f"Params: {params}")
    print(f"Query String: {query_string}")
    print(f"Signature String: {sign_str}")
    print(f"Generated Signature: {signature}")
    
    # Test API call
    print("\n🌐 Testing API Call...")
    
    url = f"https://api.pionex.com{endpoint}"
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'PionexTradingBot/1.0',
        'PIONEX-KEY': api_key,
        'PIONEX-SIGNATURE': signature,
        'PIONEX-TIMESTAMP': params['timestamp']
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            if 'result' in data and data['result']:
                print("✅ API call successful!")
                print("✅ Credentials are working!")
            else:
                print("❌ API call failed!")
                print(f"Error: {data.get('message', 'Unknown error')}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
    
    # Test alternative signature method
    print("\n🔄 Testing Alternative Signature Method...")
    
    # Try different signature format
    alt_sign_str = f"{method}{endpoint}?{query_string}"
    alt_signature = hmac.new(
        secret_key.encode('utf-8'),
        alt_sign_str.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    print(f"Alternative Signature String: {alt_sign_str}")
    print(f"Alternative Signature: {alt_signature}")
    
    # Test with alternative signature
    headers['PIONEX-SIGNATURE'] = alt_signature
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        print(f"Alternative Status Code: {response.status_code}")
        print(f"Alternative Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            if 'result' in data and data['result']:
                print("✅ Alternative signature method works!")
            else:
                print("❌ Alternative signature method failed!")
        else:
            print(f"❌ Alternative HTTP Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Alternative request failed: {e}")

if __name__ == "__main__":
    test_api_credentials() 