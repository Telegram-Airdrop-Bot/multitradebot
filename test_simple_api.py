#!/usr/bin/env python3
"""
Simple test to verify API base URL and credentials
"""

import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_simple_api():
    """Test simple API endpoints to verify the API"""
    
    print("🔧 Testing Simple API Endpoints...")
    print("=" * 50)
    
    # Test 1: Market data (no auth required)
    print("\n📊 Testing Market Data (No Auth)...")
    
    try:
        response = requests.get("https://api.pionex.com/api/v1/market/tickers", timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:200]}...")
        
        if response.status_code == 200:
            print("✅ Market data endpoint works!")
        else:
            print("❌ Market data endpoint failed!")
            
    except Exception as e:
        print(f"❌ Market data test failed: {e}")
    
    # Test 2: Check if this is actually Pionex API
    print("\n🔍 Checking API Identity...")
    
    try:
        response = requests.get("https://api.pionex.com/api/v1/common/symbols", timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:200]}...")
        
        if response.status_code == 200:
            print("✅ This appears to be Pionex API!")
        else:
            print("❌ This might not be Pionex API!")
            
    except Exception as e:
        print(f"❌ API identity check failed: {e}")
    
    # Test 3: Check API credentials format
    print("\n🔐 Checking API Credentials...")
    
    api_key = os.getenv('PIONEX_API_KEY')
    secret_key = os.getenv('PIONEX_SECRET_KEY')
    
    if api_key and secret_key:
        print(f"API Key length: {len(api_key)}")
        print(f"Secret Key length: {len(secret_key)}")
        print(f"API Key format: {api_key[:10]}...{api_key[-10:]}")
        print(f"Secret Key format: {secret_key[:10]}...{secret_key[-10:]}")
        
        # Check if they look like valid API credentials
        if len(api_key) > 20 and len(secret_key) > 20:
            print("✅ Credentials look like valid API keys")
        else:
            print("❌ Credentials might be invalid")
    else:
        print("❌ API credentials not found!")
    
    # Test 4: Try different API base URLs
    print("\n🌐 Testing Different API URLs...")
    
    test_urls = [
        "https://api.pionex.com",
        "https://api.pionex.com/api/v1",
        "https://api.pionex.com/api",
        "https://api.pionex.com/v1"
    ]
    
    for url in test_urls:
        try:
            response = requests.get(f"{url}/market/tickers", timeout=5)
            print(f"{url}/market/tickers - Status: {response.status_code}")
        except Exception as e:
            print(f"{url}/market/tickers - Error: {e}")

if __name__ == "__main__":
    test_simple_api() 