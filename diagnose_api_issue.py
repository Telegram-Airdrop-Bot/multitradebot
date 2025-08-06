#!/usr/bin/env python3
"""
Diagnostic script to identify API credential issues
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def diagnose_api_issue():
    """Diagnose the API credential issue"""
    
    print("🔍 Diagnosing Pionex API Issue...")
    print("=" * 50)
    
    # Check API credentials
    api_key = os.getenv('PIONEX_API_KEY')
    secret_key = os.getenv('PIONEX_SECRET_KEY')
    
    print(f"\n📋 API Credentials Check:")
    print(f"API Key: {'✅ Set' if api_key else '❌ Not set'}")
    print(f"Secret Key: {'✅ Set' if secret_key else '❌ Not set'}")
    
    if api_key and secret_key:
        print(f"API Key length: {len(api_key)} characters")
        print(f"Secret Key length: {len(secret_key)} characters")
        print(f"API Key format: {api_key[:10]}...{api_key[-10:]}")
        print(f"Secret Key format: {secret_key[:10]}...{secret_key[-10:]}")
    
    # Test market data (no auth required)
    print(f"\n📊 Market Data Test (No Auth Required):")
    try:
        response = requests.get("https://api.pionex.com/api/v1/market/tickers", timeout=10)
        if response.status_code == 200:
            print("✅ Market data works - API is accessible")
        else:
            print(f"❌ Market data failed - Status: {response.status_code}")
    except Exception as e:
        print(f"❌ Market data test failed: {e}")
    
    # Test authenticated endpoint
    print(f"\n🔐 Authenticated Endpoint Test:")
    if api_key and secret_key:
        try:
            # Simple test with minimal parameters
            response = requests.get("https://api.pionex.com/api/v1/account/balances", timeout=10)
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
            
            if response.status_code == 200:
                data = response.json()
                if 'result' in data and data['result']:
                    print("✅ Authentication works!")
                else:
                    print(f"❌ Authentication failed: {data.get('message', 'Unknown error')}")
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Authentication test failed: {e}")
    else:
        print("❌ Cannot test authentication - credentials not set")
    
    # Provide solutions
    print(f"\n💡 Possible Solutions:")
    print("1. Check if your API credentials are correct")
    print("2. Verify you're using the right API environment (mainnet vs testnet)")
    print("3. Check if your API key has the necessary permissions")
    print("4. Verify the API key hasn't expired")
    print("5. Check if you need to whitelist your IP address")
    
    print(f"\n🔧 Next Steps:")
    print("1. Log into your Pionex account")
    print("2. Go to API Management")
    print("3. Check if your API key is active and has correct permissions")
    print("4. Try creating a new API key if the current one doesn't work")
    print("5. Make sure your IP is whitelisted if required")
    
    print(f"\n📞 Support:")
    print("If the issue persists, contact Pionex support with:")
    print("- Your API key (first 10 and last 10 characters)")
    print("- The error message: 'INVALID_SIGNATURE'")
    print("- The endpoint being tested: '/api/v1/account/balances'")

if __name__ == "__main__":
    diagnose_api_issue() 